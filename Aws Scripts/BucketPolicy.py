import boto3
import pyotp
import os
import sys
import re
sys.path.append(os.path.realpath('.'))
import pprint
import inquirer
import json

# Retrieve the list of existing buckets
s3 = boto3.client('s3')
response = s3.list_buckets()

# Output the bucket names
print('Existing buckets:')
for bucket in response['Buckets']:
    region=s3.get_bucket_location(Bucket=bucket["Name"])
    print(f'Name:  {bucket["Name"].ljust(30)}\tCreationDate:  {bucket["CreationDate"]}\tLocationConstraint{region["LocationConstraint"]}')



question = [inquirer.List('name',message='Please choose the bucket to see policy that belongs the bucket',choices=[bucket['Name'] for bucket in response['Buckets']],),]
answers= inquirer.prompt(question)
bucketname=answers['name']

result = s3.get_bucket_policy(Bucket=bucketname)

djson=json.loads(result['Policy'])

for key, value in djson.items():
    if key == "Statement":
        for values in value:
            for k, v in values.items():
                print(f'{k}\t{v}')
    else:
        print(f'{key}\t{value}')
