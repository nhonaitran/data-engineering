import configparser
import os
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, DoubleType, IntegerType, StringType, LongType
from pyspark.sql.functions import udf, col
from pyspark.sql.functions import to_timestamp, year, month, dayofmonth, hour, weekofyear, dayofweek

config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID'] = config.get('default', 'AWS_ACCESS_KEY_ID')
os.environ['AWS_SECRET_ACCESS_KEY'] = config.get('default', 'AWS_SECRET_ACCESS_KEY')


def create_spark_session():
    """
    Create Spark session:q
    """
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    """
    Process song dataset to extract songs and artists data
    """

    # get filepath to song data file
    song_data = os.path.join(input_data, 'song_data/A/*/*/*.json')

    # define schema for song data
    song_data_schema = StructType([
        StructField("num_songs", IntegerType()),
        StructField("artist_id", StringType()),
        StructField("artist_latitude", DoubleType()),
        StructField("artist_longitude", DoubleType()),
        StructField("artist_location", StringType()),
        StructField("artist_name", StringType()),
        StructField("song_id", StringType()),
        StructField("title", StringType()),
        StructField("duration", DoubleType()),
        StructField("year", IntegerType())
    ])

    # read song data file
    df = spark.read.json(song_data, song_data_schema)
    df.printSchema()

    # extract columns to create songs table
    songs_table = df \
        .select("song_id",
                "title",
                "artist_id",
                "year",
                "duration")
    songs_table.printSchema()
    songs_table.show(50, False)

    # write songs table to parquet files partitioned by year and artist
    songs_parquet_path = os.path.join(output_data, 'songs')
    songs_table \
        .write \
        .partitionBy("year", "artist_id") \
        .mode("overwrite") \
        .parquet(songs_parquet_path)

    # extract columns to create artists table
    artists_table = df \
        .select("artist_id",
                col("artist_name").alias("name"),
                col("artist_location").alias("location"),
                col("artist_latitude").alias("latitude"),
                col("artist_longitude").alias("longitude")) \
        .dropDuplicates(['artist_id'])
    artists_table.printSchema()
    artists_table.show(50, False)

    # write artists table to parquet files
    artists_parquet_path = os.path.join(output_data, 'artists')
    artists_table \
        .write \
        .mode("overwrite") \
        .parquet(artists_parquet_path)

    print(f"songs_table:   {songs_table.count()}")
    print(f"artists_table: {artists_table.count()}")


def process_log_data(spark, input_data, output_data):
    """
    Process log data to extract songs played and user activity.
    :param spark: SparkSession instance
    :param input_data: the S3 bucket where song and log data reside
    :param output_data: the S3 bucket where the ELT process populates data for the fact and dimension tables
    :return: None
    """
    # get filepath to log data file
    log_data = os.path.join(input_data, 'log_data/2018/11/*.json')

    # define schema
    songplays_schema = StructType([
        StructField("artist", StringType()),
        StructField("auth", StringType()),
        StructField("firstName", StringType()),
        StructField("gender", StringType()),
        StructField("itemInSession", IntegerType()),
        StructField("lastName", StringType()),
        StructField("length", DoubleType()),
        StructField("level", StringType()),
        StructField("location", StringType()),
        StructField("method", StringType()),
        StructField("page", StringType()),
        StructField("registration", DoubleType()),
        StructField("sessionId", IntegerType()),
        StructField("song", StringType()),
        StructField("status", IntegerType()),
        StructField("ts", LongType()),
        StructField("userAgent", StringType()),
        StructField("userId", StringType())
    ])

    # read log data file
    df = spark.read.json(log_data, songplays_schema)

    # filter by actions for song plays
    log_df = df.filter(df.page == "NextSong")

    log_df.show(50, truncate=False)

    # extract columns for users table
    users_table = log_df \
        .select(col("userId").alias("user_id"),
                col("firstName").alias("first_name"),
                col("lastName").alias("last_name"),
                "gender",
                "level") \
        .dropDuplicates(['user_id', 'level'])
    users_table.show(50, truncate=False)

    # write users table to parquet files
    users_path = os.path.join(output_data, 'users')
    users_table \
        .write \
        .mode("overwrite") \
        .parquet(users_path)

    # create timestamp column from original timestamp column
    time_table = log_df \
        .select(col("ts").alias("start_time")) \
        .withColumn("ts_timestamp", to_timestamp(col("start_time") / 1000))

    # extract columns to create time table
    time_table = time_table \
        .withColumn("hour", month("ts_timestamp")) \
        .withColumn("day", dayofmonth("ts_timestamp")) \
        .withColumn("week", weekofyear("ts_timestamp")) \
        .withColumn("month", month("ts_timestamp")) \
        .withColumn("year", year("ts_timestamp")) \
        .withColumn("weekday", dayofweek("ts_timestamp")) \
        .drop("ts_timestamp")

    # write time table to parquet files partitioned by year and month
    time_data_path = os.path.join(output_data, 'time')
    time_table \
        .write \
        .partitionBy("year", "month") \
        .mode("overwrite") \
        .parquet(time_data_path)
    time_table.show(50, truncate=False)

    # read in song and artist data to use for songplays table
    songs_df = spark.read.parquet(os.path.join(output_data, 'songs'))
    artists_df = spark.read.parquet(os.path.join(output_data, 'artists'))

    # setup aliases in preparation for joining the tables
    lt = log_df.alias("lt")
    st = songs_df.alias("st")
    at = artists_df.alias("at")
    tt = time_table.alias("tt")

    # extract columns from joined song and log datasets to create songplays table
    songplays_table = lt\
        .join(st, lt.song == st.title, how='left') \
        .join(at, lt.artist == at.name, how='left') \
        .join(tt, lt.ts == tt.start_time, how='left') \
        .select(col("lt.ts").alias("start_time"),
                col("lt.userId").alias("user_id"),
                "lt.level",
                "st.song_id",
                "at.artist_id",
                col("lt.sessionId").alias("session_id"),
                "lt.location",
                col("lt.userAgent").alias("user_agent"),
                "tt.year",
                "tt.month")
    songplays_table.show(50, truncate=False)

    # write songplays table to parquet files partitioned by year and month
    songplays_path = os.path.join(output_data, 'songplays')
    songplays_table\
        .write\
        .partitionBy("year", "month")\
        .mode("overwrite")\
        .parquet(songplays_path)


def main():
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    output_data = "s3a://aws-sparkify-data-lake/"

    process_song_data(spark, input_data, output_data)
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
