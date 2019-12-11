import json
import os
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

events = boto3.client('events')

def enable_rule(name):
    events.enable_rule(
        Name = name
    )
    
    logger.info("Rule '" + name + "' is enabled successfully.")
    
def lambda_handler(event, context):
    name = event['Name']
    
    enable_rule(name=name + "-start")
    enable_rule(name=name + "-stop")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Scheduler enabled successfully.')
    }
