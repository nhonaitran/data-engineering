import configparser
import boto3
import click
import json
import pandas as pd
import psycopg2
from sql_queries import create_table_queries, drop_table_queries

# Load data warehouse configuration settings
config = configparser.ConfigParser()
config.read('dwh.cfg')

KEY                     = config.get('AWS','KEY')
SECRET                  = config.get('AWS','SECRET')

DWH_CLUSTER_TYPE        = config.get("CLUSTER","DWH_CLUSTER_TYPE")
DWH_NUM_NODES           = config.get("CLUSTER","DWH_NUM_NODES")
DWH_NODE_TYPE           = config.get("CLUSTER","DWH_NODE_TYPE")
DWH_REGION              = config.get("CLUSTER","DWH_REGION")

DWH_CLUSTER_IDENTIFIER  = config.get("CLUSTER","DWH_CLUSTER_IDENTIFIER")
DWH_DB                  = config.get("CLUSTER","DWH_DB")
DWH_DB_USER             = config.get("CLUSTER","DWH_DB_USER")
DWH_DB_PASSWORD         = config.get("CLUSTER","DWH_DB_PASSWORD")
DWH_PORT                = config.get("CLUSTER","DWH_PORT")

DWH_IAM_ROLE_NAME       = config.get("IAM_ROLE", "ARN")


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

def prettyRedshiftProps(props):
    """
    Show current propertiers about the cluster
    """
    pd.set_option('display.max_colwidth', None)
    keysToShow = ["ClusterIdentifier", "NodeType", "ClusterStatus", "MasterUsername", "DBName", "Endpoint", "NumberOfNodes", 'VpcId']
    x = [(k, v) for k,v in props.items() if k in keysToShow]
    return pd.DataFrame(data=x, columns=["Key", "Value"])

def create_aws_resources():
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

def setup_role(iam):
    try:
        # creating a new IAM Role
        dwhRole = iam.create_role(
            Path='/',
            RoleName=DWH_IAM_ROLE_NAME,
            Description="Allow Redshift clusters to call AWS services on your behalf",
            AssumeRolePolicyDocument=json.dumps(
                {'Statement': [{'Action': 'sts:AssumeRole',
                            'Effect': 'Allow',
                            'Principal': {'Service': 'redshift.amazonaws.com'}}],
                'Version': '2012-10-17'}
            )
        )

        # Attach Policy
        iam.attach_role_policy(RoleName=DWH_IAM_ROLE_NAME, PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess")['ResponseMetadata']['HTTPStatusCode']
    except Exception as e:
        print(e)

def create_cluster(iam, redshift):
    try:
         # check the IAM role ARN
        roleArn = iam.get_role(RoleName=DWH_IAM_ROLE_NAME)['Role']['Arn']

        response = redshift.create_cluster(
            # TODO: add parameters for hardware
            ClusterType=DWH_CLUSTER_TYPE,
            NodeType=DWH_NODE_TYPE,
            NumberOfNodes=int(DWH_NUM_NODES),

            # TODO: add parameters for identifiers & credentials
            DBName=DWH_DB,
            ClusterIdentifier=DWH_CLUSTER_IDENTIFIER,
            MasterUsername=DWH_DB_USER,
            MasterUserPassword=DWH_DB_PASSWORD,

            # TODO: add parameter for role (to allow s3 access)
            IamRoles=[roleArn]
        )
    except Exception as e:
        print(e)

def open_tcp_port_for_external_access(ec2, clusterProps):
    try:
        vpc = ec2.Vpc(id=clusterProps['VpcId'])
        defaultSg = list(vpc.security_groups.all())[0]
        print(defaultSg)

        defaultSg.authorize_ingress(
            GroupName=defaultSg.group_name,
            CidrIp='0.0.0.0/0',
            IpProtocol='TCP',
            FromPort=int(DWH_PORT),
            ToPort=int(DWH_PORT)
        )
    except Exception as e:
        print(e)

@click.command()
@click.option('--command', default="create", help='Operation to execute.')
def main(command):

    conn_str = f"host={DWH_CLUSTER_IDENTIFIER} dbname={DWH_DB} user={DWH_DB_USER} password={DWH_DB_PASSWORD} port={DWH_PORT}"
    print(conn_str)

    ec2, s3, iam, redshift = create_aws_resources()

    print(command)
    if command == "create":
        setup_role(iam)
        create_cluster(iam, redshift)

        clusterProps = redshift.describe_clusters(ClusterIdentifier=DWH_CLUSTER_IDENTIFIER)['Clusters'][0]
        print(prettyRedshiftProps(clusterProps))

    elif command == "delete":

        redshift.delete_cluster(ClusterIdentifier=DWH_CLUSTER_IDENTIFIER, SkipFinalClusterSnapshot=True)

        clusterProps = redshift.describe_clusters(ClusterIdentifier=DWH_CLUSTER_IDENTIFIER)['Clusters'][0]
        print(prettyRedshiftProps(clusterProps))

    else:
        try:
            clusterProps = redshift.describe_clusters(ClusterIdentifier=DWH_CLUSTER_IDENTIFIER)['Clusters'][0]
            print(prettyRedshiftProps(clusterProps))

            DWH_ENDPOINT = clusterProps['Endpoint']['Address']
            DWH_ROLE_ARN = clusterProps['IamRoles'][0]['IamRoleArn']
            print("DWH_ENDPOINT :: ", DWH_ENDPOINT)
            print("DWH_ROLE_ARN :: ", DWH_ROLE_ARN)

            if clusterProps['ClusterStatus'] == "available":
                open_tcp_port_for_external_access(ec2)

                sampleDbBucket = s3.Bucket("udacity-labs")
                for obj in sampleDbBucket.objects.filter(Prefix="tickets"):
                    print(obj)
        except Exception as e:
            print(e)
    # connect to the database and get cursor to it
    #conn = psycopg2.connect(conn_str)
    #cur = conn.cursor()

    # drop all tables
    #drop_tables(cur, conn)

    # create all tables
    #create_tables(cur, conn)

    # close connection to database
    #conn.close()


if __name__ == "__main__":
    main()
