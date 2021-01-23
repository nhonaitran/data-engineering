import configparser
import boto3
import click
import json
import pandas as pd
import psycopg2
import logging
from sql_queries import create_table_queries, drop_table_queries

# Load data warehouse configuration settings
config = configparser.ConfigParser()
config.read('dwh.cfg')

KEY = config.get('AWS', 'KEY')
SECRET = config.get('AWS', 'SECRET')

DWH_NAME = config.get("CLUSTER", "NAME")
DWH_REGION = config.get("CLUSTER", "REGION")
DWH_CLUSTER_TYPE = config.get("CLUSTER", "TYPE")
DWH_NUM_NODES = config.get("CLUSTER", "NUM_NODES")
DWH_NODE_TYPE = config.get("CLUSTER", "NODE_TYPE")

DWH_DB = config.get("CLUSTER", "DB")
DWH_DB_USER = config.get("CLUSTER", "DB_USER")
DWH_DB_PASSWORD = config.get("CLUSTER", "DB_PASSWORD")
DWH_PORT = config.get("CLUSTER", "DB_PORT")

DWH_IAM_ROLE = config.get("IAM_ROLE", "ARN")


def drop_tables(cur, conn):
    """
    Drop each table using the queries in 'drop_table_queries' list.
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Create each table using the queries in `create_table_queries` list.
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def prettify_redshift_props(props):
    """
    Map a dict containing Redshift properties to a pandas dataframe
    """
    pd.set_option('display.max_colwidth', None)
    keys_to_show = ["ClusterIdentifier",
                    "NodeType",
                    "ClusterStatus",
                    "MasterUsername",
                    "DBName",
                    "Endpoint",
                    "NumberOfNodes",
                    'VpcId']
    x = [(k, v) for k, v in props.items() if k in keys_to_show]
    return pd.DataFrame(data=x, columns=["Key", "Value"])


def create_aws_resources():
    """
    Create AWS resources and clients
    :return:
    ec2, s3, iam, redshift
    """
    logging.info("Init AWS clients and resources")
    ec2 = boto3.resource('ec2',
                         region_name=DWH_REGION,
                         aws_access_key_id=KEY,
                         aws_secret_access_key=SECRET)

    s3 = boto3.resource('s3',
                        region_name=DWH_REGION,
                        aws_access_key_id=KEY,
                        aws_secret_access_key=SECRET)

    iam = boto3.client('iam',
                       region_name=DWH_REGION,
                       aws_access_key_id=KEY,
                       aws_secret_access_key=SECRET)

    redshift = boto3.client('redshift',
                            region_name=DWH_REGION,
                            aws_access_key_id=KEY,
                            aws_secret_access_key=SECRET)

    return ec2, s3, iam, redshift


def setup_role(iam) -> None:
    """
    Given the AWS IAM object, setup a programmatic role for for interacting
    with the AWS data warehouse.
    :param iam: AWS IAM client
    :return: None
    """
    logging.info("Setting up IAM role")
    try:
        # creating a new IAM Role
        iam.create_role(
            Path='/',
            RoleName=DWH_IAM_ROLE,
            Description="Allow Redshift clusters to call AWS services on your behalf",
            AssumeRolePolicyDocument=json.dumps(
                {'Statement': [{'Action': 'sts:AssumeRole',
                                'Effect': 'Allow',
                                'Principal': {'Service': 'redshift.amazonaws.com'}}],
                 'Version': '2012-10-17'}
            )
        )

        # attach policy to role
        iam.attach_role_policy(RoleName=DWH_IAM_ROLE,
                               PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess")['ResponseMetadata'][
            'HTTPStatusCode']
        return 1
    except iam.exceptions.EntityAlreadyExistsException:
        logging.info("Role already exists")
        return 1
    except Exception as e:
        logging.error(e)
        return 0


def create_cluster(iam, redshift):
    """
    Given the AWS IAM and redshift clients, create and launch a new
    cluster
    :param iam:
    :param redshift:
    :return:
    """
    msg = "creating cluster"
    try:
        # check the IAM role ARN
        role_arn = iam.get_role(RoleName=DWH_IAM_ROLE)['Role']['Arn']

        redshift.create_cluster(
            ClusterType=DWH_CLUSTER_TYPE,
            NodeType=DWH_NODE_TYPE,
            NumberOfNodes=int(DWH_NUM_NODES),
            DBName=DWH_DB,
            ClusterIdentifier=DWH_NAME,
            MasterUsername=DWH_DB_USER,
            MasterUserPassword=DWH_DB_PASSWORD,
            IamRoles=[role_arn]
        )
        msg = msg + "done."
    except Exception as e:
        msg = msg + str(e)

    logging.info(msg)


def open_tcp_port_for_external_access(ec2, cluster_props):
    """
    Open TCP port for access database
    :param ec2:
    :param cluster_props:
    :return:
    """
    try:
        vpc = ec2.Vpc(id=cluster_props['VpcId'])
        default_sg = list(vpc.security_groups.all())[0]
        logging.info(default_sg)

        default_sg.authorize_ingress(
            GroupName=default_sg.group_name,
            CidrIp='0.0.0.0/0',
            IpProtocol='TCP',
            FromPort=int(DWH_PORT),
            ToPort=int(DWH_PORT)
        )
    except Exception as e:
        print(e)


@click.command()
@click.option('--command', default="create", help='Operation to execute.')
@click.option('--log_level', default="INFO", help='Level of logging.')
def main(command, log_level):
    logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=log_level)

    conn_str = f"host={DWH_NAME} dbname={DWH_DB} user={DWH_DB_USER} password={DWH_DB_PASSWORD} port={DWH_PORT}"
    logging.info(f"data warehouse cluster info: {conn_str}")

    ec2, s3, iam, redshift = create_aws_resources()

    if command == "create":
        if setup_role(iam):
            create_cluster(iam, redshift)

            cluster_props = redshift.describe_clusters(ClusterIdentifier=DWH_NAME)['Clusters'][0]
            logging.info(prettify_redshift_props(cluster_props))

            open_tcp_port_for_external_access(ec2, cluster_props)

    elif command == "delete":

        redshift.delete_cluster(ClusterIdentifier=DWH_NAME, SkipFinalClusterSnapshot=True)

        cluster_props = redshift.describe_clusters(ClusterIdentifier=DWH_NAME)['Clusters'][0]
        logging.info(prettify_redshift_props(cluster_props))

    else:
        try:
            cluster_props = redshift.describe_clusters(ClusterIdentifier=DWH_NAME)['Clusters'][0]
            logging.info(prettify_redshift_props(cluster_props))

            end_point = cluster_props['Endpoint']['Address']
            role_arn = cluster_props['IamRoles'][0]['IamRoleArn']
            logging.info("DWH_ENDPOINT :: ", end_point)
            logging.info("DWH_ROLE_ARN :: ", role_arn)

            if cluster_props['ClusterStatus'] == "available":
                sample_db_bucket = s3.Bucket("udacity-labs")
                for obj in sample_db_bucket.objects.filter(Prefix="tickets"):
                    logging.info(obj)

        except redshift.exceptions.ClusterNotFoundFault:
            logging.warning(f"Cluster {DWH_NAME} has been deleted")
        except Exception as e:
            logging.error(e)
    # connect to the database and get cursor to it
    # conn = psycopg2.connect(conn_str)
    # cur = conn.cursor()

    # drop all tables
    # drop_tables(cur, conn)

    # create all tables
    # create_tables(cur, conn)

    # close connection to database
    # conn.close()


if __name__ == "__main__":
    main()
