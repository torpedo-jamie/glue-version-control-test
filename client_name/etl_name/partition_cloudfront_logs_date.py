import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)
job.commit()

import sys
import os
from datetime import date, timedelta
import boto3

SOURCE_BUCKET = 'cloudfront-logs-996091670049-eu-west-1'
TARGET_BUCKET = 'cloudfront-logs-partitioned-996091670049'


client = boto3.client('s3')
s3 = boto3.resource('s3')
 
bucket = s3.Bucket(SOURCE_BUCKET)

for obj in bucket.objects.all():
    key = obj.key
    
    key_date = key.split('.')[1].split('-')
    year = key_date[0]
    month = key_date[1]
    day = key_date[2]
    
    key_date_str = year + '-' + month + '-' + day
    
    copy_source = {
            'Bucket': SOURCE_BUCKET,
            'Key': key
            }
    
    s3.meta.client.copy(copy_source, TARGET_BUCKET, 'partition_cloudfront_logs_date/dt='+ key_date_str + '/' + key.split('/')[-1])
    
 print("Hello world")
