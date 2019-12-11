import json
import os
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

events = boto3.client('events')

def delete_rule(name):
    events.remove_targets(
        Rule = name,
        Ids = [
            name
        ],
        Force = True
    )
    
    logger.info("Target removed from rule '" + name + "'.")
        
    events.delete_rule(
        Name = name,
        Force = True
    )
    
    logger.info("Rule '" + name + "' deleted successfully.")
    
def lambda_handler(event, context):
    name = event['Name']
    
    delete_rule(name=name + "-start")
    delete_rule(name=name + "-stop")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Scheduler deleted successfully.')
    }
