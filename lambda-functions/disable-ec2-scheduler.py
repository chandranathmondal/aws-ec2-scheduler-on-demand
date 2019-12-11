import json
import os
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

events = boto3.client('events')

def disable_rule(name):
    events.disable_rule(
        Name = name
    )
    
    logger.info("Rule '" + name + "' is disabled successfully.")
    
def lambda_handler(event, context):
    name = event['Name']
    
    disable_rule(name=name + "-start")
    disable_rule(name=name + "-stop")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Scheduler disabled successfully.')
    }
