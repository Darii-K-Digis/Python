import json
import logging
import os
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import boto3

logger = logging.getLogger(__name__)

s3 = boto3.client('s3')
ses = boto3.client('ses', region_name='aws-region')


def handler(event, _):
    logger.info(f'Received event: {json.dumps(event, indent=2)}')

    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']

    file_name = os.path.basename(object_key)
    tmp_file_name = '/tmp/' + file_name

    s3.download_file(bucket_name, object_key, tmp_file_name)

    # Set the email parameters
    sender = 'user@example.com'
    recipient = 'user2@example.com'

    msg = MIMEMultipart()
    msg['Subject'] = 'Example Message'
    msg['From'] = sender
    msg['To'] = recipient

    text_part = MIMEText(
        'Hello, please find attached file really interesting. \nBest regards, Digis',
        'plain'
    )
    msg.attach(text_part)

    attachment = MIMEApplication(open(tmp_file_name, 'rb').read())
    attachment.add_header(
        'Content-Disposition',
        'attachment',
        filename='digis-attachment.pdf'
    )
    msg.attach(attachment)

    try:
        response = ses.send_raw_email(
            Source=sender,
            Destinations=[
                sender,
            ],
            RawMessage={
                'Data': msg.as_string(),
            },
        )
        logger.info(f'Message id : {response["MessageId"]}')
        logger.info('Message send successfully!')
    except Exception as e:
        logger.error(f'Got error while sending email: {e}')

    return {
        'statusCode': 200,
        'body': json.dumps('Email sent successfully'),
    }
