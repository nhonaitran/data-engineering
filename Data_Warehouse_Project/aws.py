import boto3
import configparser
import json
import logging
import pandas as pd
import psycopg2

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
                    datefmt='%m.%d.%Y %H:%M:%S %p',
                    level=logging.INFO)

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
DWH_ROLE_ARN = ""

LOG_DATA = config.get('S3', 'LOG_DATA')
SONG_DATA = config.get('S3', 'SONG_DATA')


def create_aws_resources():
    """
    Create AWS resources and clients
    :return:
    aws_ec2, aws_s3, aws_iam, aws_redshift
    """
    logging.info("Init AWS Client and Resource instances")
    aws_ec2 = boto3.resource('ec2',
                             region_name=DWH_REGION,
                             aws_access_key_id=KEY,
                             aws_secret_access_key=SECRET)

    aws_s3 = boto3.resource('s3',
                            region_name=DWH_REGION,
                            aws_access_key_id=KEY,
                            aws_secret_access_key=SECRET)

    aws_iam = boto3.client('iam',
                           region_name=DWH_REGION,
                           aws_access_key_id=KEY,
                           aws_secret_access_key=SECRET)

    aws_redshift = boto3.client('redshift',
                                region_name=DWH_REGION,
                                aws_access_key_id=KEY,
                                aws_secret_access_key=SECRET)

    return aws_ec2, aws_s3, aws_iam, aws_redshift


def create_cluster():
    """
    Given the AWS IAM and redshift clients, create and launch a new cluster
    :return: None
    """
    try:
        logging.info(f"Creating Redshift cluster {DWH_NAME}")

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
    except Exception as e:
        logging.error(e)


def delete_cluster() -> None:
    """
    Delete the cluster with given cluster identifier
    :return: None
    """
    try:
        logging.info(f"Deleting cluster {DWH_NAME}")
        redshift.delete_cluster(ClusterIdentifier=DWH_NAME, SkipFinalClusterSnapshot=True)
    except Exception as e:
        logging.error(e)


def setup_role() -> None:
    """
    Given the AWS IAM object, setup a programmatic role for for interacting
    with the AWS data warehouse.
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
        logging.info(f"Role {DWH_IAM_ROLE} already exists")
        return 1
    except Exception as e:
        logging.error(e)
        return 0


def show_cluster_property() -> None:
    """
    Show current status of a cluster
    :return: None
    """
    if cluster_props is None:
        return

    try:
        logging.info(prettify_redshift_props())

        if cluster_props['ClusterStatus'] == "available":
            logging.info(f"DWH_ENDPOINT :: {cluster_props['Endpoint']['Address']}")
            logging.info(f"DWH_ROLE_ARN :: {cluster_props['IamRoles'][0]['IamRoleArn']}")
    except redshift.exceptions.ClusterNotFoundFault:
        logging.warning(f"Cluster {DWH_NAME} has been deleted")
    except Exception as e:
        logging.error(e)


def connect_to_data_warehouse():
    """
    Connect to data warehouse cluster
    :return:
    (conn, cur): tuple with database connection object and cursor object for interacting with the data warehouse
    """
    open_tcp_port_for_external_access()

    end_point = cluster_props['Endpoint']['Address']

    logging.info(f"Connecting to {DWH_DB} at {end_point}, and get cursor to it")
    conn = psycopg2.connect(
        host=end_point,
        user=DWH_DB_USER,
        port=DWH_PORT,
        password=DWH_DB_PASSWORD,
        dbname=DWH_DB
    )
    cur = conn.cursor()
    return conn, cur


def prettify_redshift_props():
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
    x = [(k, v) for k, v in cluster_props.items() if k in keys_to_show]
    return pd.DataFrame(data=x, columns=["Key", "Value"])


def open_tcp_port_for_external_access():
    """
    Open TCP port for access database
    :return: None
    """
    try:
        vpc = ec2.Vpc(id=cluster_props['VpcId'])
        default_sg = list(vpc.security_groups.all())[2]
        logging.info(default_sg)

        default_sg.authorize_ingress(
            GroupName=default_sg.group_name,
            CidrIp='0.0.0.0/0',
            IpProtocol='TCP',
            FromPort=int(DWH_PORT),
            ToPort=int(DWH_PORT)
        )
    except Exception as e:
        logging.error(e)


# show db info
conn_str = f"host={DWH_NAME} dbname={DWH_DB} user={DWH_DB_USER} password={DWH_DB_PASSWORD} port={DWH_PORT}"
logging.info(f"Data warehouse cluster info: {conn_str}")

ec2, s3, iam, redshift = create_aws_resources()

try:
    logging.info("Fetching AWS IAM role for loading data to data warehouse")
    cluster_props = redshift.describe_clusters(ClusterIdentifier=DWH_NAME)['Clusters'][0]
    if cluster_props['ClusterStatus'] == "available":
        DWH_ROLE_ARN = cluster_props['IamRoles'][0]['IamRoleArn']
        logging.info(f"IAM Role: {DWH_ROLE_ARN}")
except redshift.exceptions.ClusterNotFoundFault:
    cluster_props = None
    logging.warning(f"Cluster {DWH_NAME} is not found")
except Exception as e:
    logging.error(e)
