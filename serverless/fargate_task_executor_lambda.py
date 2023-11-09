import json
import logging
import os
import urllib.parse

import boto3

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ecs = boto3.client('ecs')
ec2 = boto3.client('ec2')


def _resolve_security_group_id(vpc_id: str, group_name: str = 'default') -> str:
    """
    Resolve security group id by vpc id and group name.

    :param vpc_id: vpc id
    :param group_name: security group name
    :return: resolved security group id
    """
    response = ec2.describe_security_groups(
        Filters=[
            dict(
                Name='vpc-id',
                Values=[
                    vpc_id,
                ]
            ),
            dict(
                Name='group-name',
                Values=[
                    group_name,
                ]
            )
        ]
    )
    return response['SecurityGroups'][0]['GroupId']


def lambda_handler(event, _):
    logger.info(f'Received event: {json.dumps(event, indent=2)}')

    # resolve event data
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key'],
        encoding='utf-8'
    )

    response = ecs.run_task(
        cluster='Cluster',
        taskDefinition='ClusterFamily:1',
        launchType='FARGATE',
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': [value for key, value in os.environ.items() if key.startswith('SUBNET_ID')],
                'securityGroups': [
                    _resolve_security_group_id(os.getenv('VPC_ID'))
                ],
                'assignPublicIp': 'ENABLED'
            }
        },
        overrides={
            'containerOverrides': [
                {
                    'name': 'etl-lambda',
                    'environment': [
                        {
                            'name': 'S3_BUCKET',
                            'value': bucket
                        },
                        {
                            'name': 'S3_KEY',
                            'value': key
                        }
                    ]
                }
            ]
        }
    )

    logger.info(
        f'Response: {json.dumps(response, indent=2, sort_keys=True, default=str)}'
    )

    return {
        'statusCode': 200,
        'body': json.dumps('ECS task started successfully')
    }
