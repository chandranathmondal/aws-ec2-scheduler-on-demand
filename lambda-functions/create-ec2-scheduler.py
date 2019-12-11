import json
import os
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

events = boto3.client('events')

def put_rule(name, description, time):
    time_components = time.split(':')
    hour = time_components[0]
    minute = time_components[1]
    
    events.put_rule(
        Name = name,
        ScheduleExpression = 'cron(' + minute + ' ' + hour + ' * * ? *)',
        State = 'ENABLED',
        Description = description
    )
    
    logger.info("Rule '" + name + "' created successfully.")
    
def put_target(rule, arn, instance_ids):
    events.put_targets(
        Rule = rule,
        Targets = [
            {
                'Id': rule,
                'Arn': arn,
                'Input' : "{ \"InstanceIds\" : " + str(instance_ids).replace('\'', '\"') + " }"
            }
        ]
    )
    
    logger.info("Target added successfully to the rule '" + rule + "'")
    
def create_start_scheduler(name, description, time, instance_ids):
    rule = name + '-start'
    put_rule(name=rule, description=description, time=time)
    put_target(rule=rule, arn='arn:aws:lambda:<AWS_REGION>:<AWS_ACCOUNT_ID>:function:start-ec2-instances', instance_ids=instance_ids)
    
def create_stop_scheduler(name, description, time, instance_ids):
    rule = name + "-stop"
    put_rule(name=rule, description=description, time=time)
    put_target(rule=rule, arn='arn:aws:lambda:<AWS_REGION>:<AWS_ACCOUNT_ID>:function:stop-ec2-instances', instance_ids=instance_ids)

def lambda_handler(event, context):
    name = event['Name']
    description = event['Description']
    start_time = event['StartTime']
    stop_time = event['StopTime']
    instance_ids = event['InstanceIds']
    
    create_start_scheduler(name=name, description=description, time=start_time, instance_ids=instance_ids)
    create_stop_scheduler(name=name, description=description, time=stop_time, instance_ids=instance_ids)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Scheduler created successfully.')
    }
