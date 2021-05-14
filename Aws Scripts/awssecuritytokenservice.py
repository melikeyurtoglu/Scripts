# Author: Melike
# Desc: Analy of AWS Security Token Service cases as draft script.
#AWS Security Token Service (AWS STS) is a web service that enables you to request temporary, limited-privilege credentials for AWS Identity and Access Management (IAM) users or for users that you authenticate (federated users).

import boto3
import os
import sys
import re
import inquirer

#STS-User

userclient = boto3.client(
    'sts',
    aws_access_key_id=${ACCESS_KEY},
    aws_secret_access_key=${SECRET_KEY},
)

response = userclient.assume_role(
    RoleArn='arn:aws:iam::${id}:role/example-role',
    RoleSessionName='AWSCLI-Session',
)


accesskey=response['Credentials']['AccessKeyId']
secrekey=response['Credentials']["SecretAccessKey"]
sessiontoken=response['Credentials']['SessionToken']

question = [inquirer.List('service', message='Please choose the service',
                              choices=["s3","ec2","iam"], ), ]
answers = inquirer.prompt(question)
answers=answers['service']

if answers=='ec2':
    userclient = boto3.client(
        'ec2',
        aws_access_key_id=${ACCESS_KEY},
        aws_secret_access_key=${SECRET_KEY},
    )
    regions = userclient.describe_regions()
    question = [inquirer.List('region', message='Please choose the region to list instance information',
                              choices=[name['RegionName'] for name in regions['Regions']], ), ]
    region = inquirer.prompt(question)
    region = region['region']
    client = boto3.client(
        answers,
        aws_access_key_id=accesskey,
        aws_secret_access_key=secrekey,
        aws_session_token=sessiontoken,
        region_name=region,
    )
else:
    client = boto3.client(
        answers,
        aws_access_key_id=accesskey,
        aws_secret_access_key=secrekey,
        aws_session_token=sessiontoken,
    )

if answers=="iam":
    userinformation = client.list_users()['Users']
    mfa = client.list_virtual_mfa_devices()['VirtualMFADevices']
    mfauser = {}
    for mfainf in mfa:
        try:
            mfauser.update({'{}'.format(mfainf['User']['UserName']): '{}'.format(mfainf['EnableDate'])})
        except KeyError:
            continue
    rows = [['UserName', 'UserId', 'CreateDate', 'PasswordLastUsed','MFAEnableDate']]
    for userinf in userinformation:
        try:
            for name,date in mfauser.items():
                if name==userinf['UserName']:
                    rows.append([userinf['UserName'], userinf['UserId'], str(userinf['CreateDate']),str(userinf['PasswordLastUsed']),str(date)])
                else:
                    rows.append([userinf['UserName'],userinf['UserId'],str(userinf['CreateDate']),str(userinf['PasswordLastUsed']),''])
        except Exception:
            continue

    username_max_len = max([len(row[0]) for row in rows]) + 5
    userid_max_len = max([len(row[1]) for row in rows]) + 5
    createdate_max_len = max([len(row[2]) for row in rows]) + 5
    passwordlastused_max_len = max([len(row[3]) for row in rows]) + 2
    mfaenabledate_max_len = max([len(row[4]) for row in rows]) + 5

    str = '\n\t\t\tUser Detail\n'
    for row in rows:
        str += '\n{}\t{}{}{}{}'.format(row[0].ljust(username_max_len), row[1].ljust(userid_max_len), row[2].ljust(createdate_max_len), row[3].ljust(passwordlastused_max_len), row[4].ljust(mfaenabledate_max_len))
    print(str)
elif answers=="ec2":
    list = []
    rows = ['InstanceId', 'InstanceType', 'LaunchTime', 'PrivateIpAddress', 'PublicIpAddress', 'State', 'SubnetId','VpcId', 'SecurityGroupId', 'SecurityGroupName', 'instancename']
    title_max_len = max([len(row) for row in rows]) + 5
    response = client.describe_instances()
    for instance in response['Reservations']:
        dict = {}
        for ins in instance['Instances']:
            for key, value in ins.items():
                if key == 'SecurityGroups':
                    for i in value:
                        sid = i['GroupId']
                        sname = i['GroupName']
                        print('{}:{}'.format(rows[8].ljust(title_max_len), sid))
                        print('{}:{}'.format(rows[9].ljust(title_max_len), sname))
                    dict.update({'{}'.format('SecurityGroupId'): '{}'.format(sid)})
                    dict.update({'{}'.format('SecurityGroupName'): '{}'.format(sname)})
                elif key == 'Tags':
                    for i in value:
                        instancename = i['Value']
                    print('{}:{}'.format(rows[10].ljust(title_max_len), instancename))
                    dict.update({'{}'.format('InstanceName'): '{}'.format(instancename)})
                elif key == 'State':
                        # instancename=value['value']
                    state = value['Name']
                    print('{}:{}'.format(rows[5].ljust(title_max_len), state))
                    dict.update({'{}'.format('State'): '{}'.format(state)})
                elif key == 'InstanceId':
                    print('{}:{}'.format(rows[0].ljust(title_max_len), value))
                    dict.update({'{}'.format('InstanceId'): '{}'.format(value)})
                elif key == 'InstanceType':
                    print('{}:{}'.format(rows[1].ljust(title_max_len), value))
                    dict.update({'{}'.format('InstanceType'): '{}'.format(value)})
                elif key == 'LaunchTime':
                    print('{}:{}'.format(rows[2].ljust(title_max_len), value))
                    dict.update({'{}'.format('LaunchTime'): '{}'.format(value)})
                elif key == 'PrivateIpAddress':
                    print('{}:{}'.format(rows[3].ljust(title_max_len), value))
                    dict.update({'{}'.format('PrivateIpAddress'): '{}'.format(value)})
                elif key == 'PublicIpAddress':
                     print('{}:{}'.format(rows[4].ljust(title_max_len), value))
                     dict.update({'{}'.format('PublicIpAddress'): '{}'.format(value)})
                elif key == 'SubnetId':
                     print('{}:{}'.format(rows[6].ljust(title_max_len), value))
                     dict.update({'{}'.format('SubnetId'): '{}'.format(value)})
                elif key == 'VpcId':
                     print('{}:{}'.format(rows[7].ljust(title_max_len), value))
                     dict.update({'{}'.format('VpcId'): '{}'.format(value)})
            print('\n\n\n')
            list.append(dict)
else:
    response = client.list_buckets()
    # Output the bucket names
    rows = [['Name', 'CreationDate', 'LocationConstraint']]
    rows.append(['', '', ''])
    for bucket in response['Buckets']:
        region = client.get_bucket_location(Bucket=bucket["Name"])
        if type(region["LocationConstraint"])==type(None):
            rows.append([bucket["Name"], str(bucket["CreationDate"]),'No region'])
        else:
            rows.append([bucket["Name"], str(bucket["CreationDate"]), region["LocationConstraint"]])
    name_max_len = max([len(row[0]) for row in rows]) + 5
    date_max_len = max([len(row[1]) for row in rows]) + 5
    location_max_len = max([len(row[2]) for row in rows]) + 5

    str = '\n\t\t\tBucket Detail\n'
    for row in rows:
        str += '\n{}\t{}{}'.format(row[0].ljust(name_max_len), row[1].ljust(date_max_len), row[2].ljust(location_max_len))
    print(str)