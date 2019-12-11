import json
import os
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    instance_ids = event['InstanceIds']
    ec2.start_instances(InstanceIds=instance_ids)
    logger.info('Started instance(s): ' + str(instance_ids))
    return {
        'statusCode': 200,
        'body': json.dumps('Started instance(s): ' + str(instance_ids))
    }
