# Create s3 bucket, to be used, 
# for automation that require pre-created buckets
import boto3, botocore
import logging
import json
import sys
import argparse


# boto3.setup_default_session(profile_name='always')
session = boto3.Session(profile_name='always')
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument('--delete-if-exists', help='Delete specified s3 bucket if it exist', action='store_true')
parser.add_argument('--delete-bucket', help='Delete specified s3 bucket', action='store_true')
args = parser.parse_args()


def create_s3_bucket(bucket_name):
    try:
        s3_client = session.client('s3')
        client_response = s3_client.create_bucket(Bucket=bucket_name)
        return True, client_response
    except botocore.exceptions.ClientError as e:
        print(e.response)
        create_err_message = e.response
        if e.response['Error']['Code'] == "InvalidBucketName":
            create_http_response_code = e.response['ResponseMetadata']['HTTPStatusCode']
            create_bucket_name = e.response['Error']['BucketName']
            message = e.response['Error']['Message']
            logging.error(f"code: {create_http_response_code} ")
            logging.error(f"invalid bucket name \"{create_bucket_name}\". AWS s3 doesn't permit special characters prefix in bucket names. please check bucket name and try again")
        return False, create_err_message


def check_s3_bucket_exists(bucket_name):
    s3_client = session.client('s3')
    check_response = s3_client.list_buckets(Bucket=bucket_name)['Buckets']
    bucket_names = []
    for bucket in check_response:
        bucket_names.append(bucket['Name'])
        
    for name in bucket_names:
        if(name in bucket_names):
            return False, bucket_names
        else:
            return True, bucket_names


def delete_s3_bucket(bucket_name):
        try:
            s3_client = session.client('s3')
            delete_response = s3_client.delete_bucket(Bucket=bucket_name)
            return delete_response
        except botocore.exceptions.ClientError as err:
            if err.response['Error']['Code'] == "NoSuchBucket":
                delete_http_response_code = err.response['ResponseMetadata']['HTTPStatusCode']
                delete_err_bucket_name = err.response['Error']['BucketName']
                logging.error(f"code: {delete_http_response_code} ")
                delete_error_message = logging.error(f"s3 bucket \"{delete_err_bucket_name}\" doesn't exist , and cannot be deleted. please double check the bucket name")
                return False, delete_error_message



if __name__ == '__main__':
    bucket_name = "dev-boto-bucket"
    check_s3_bucket_exists(bucket_name)
    bucket_names = check_s3_bucket_exists(bucket_name)[1]
    if bucket_name not in bucket_names:
        logging.warning(f"creating bucket: \"{bucket_name}\"")
        create_s3_bucket(bucket_name)


    if args.delete_if_exists:
        check_s3_bucket_exists(bucket_name)
        if (check_s3_bucket_exists(bucket_name)) and (bucket_name in bucket_names):
            logging.warning(f"bucket: \"{bucket_name}\" exists")
            logging.warning(f"deleting bucket: \"{bucket_name}\".")
            delete_s3_bucket(bucket_name)
            logging.info(f"bucket: \"{bucket_name}\" successfully deleted.")
            logging.info(f"creating bucket: \"{bucket_name}\".")
            create_s3_bucket(bucket_name)
            logging.info(f"bucket: \"{bucket_name}\" created successfully.")
    elif args.delete_bucket:
        check_s3_bucket_exists(bucket_name)
        delete_error_message = delete_s3_bucket(bucket_name)
        if bucket_name in bucket_names:
            logging.warning(f"bucket: \"{bucket_name}\" exists")
            delete_s3_bucket(bucket_name)
            logging.warning(f"deleting bucket: \"{bucket_name}\" successfully deleted")
            sys.exit(0)
        else:
            logging.error(delete_error_message)
            sys.exit(1)


    







