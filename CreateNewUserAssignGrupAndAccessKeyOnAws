import boto3
import pyotp
import os
import sys
import re
sys.path.append(os.path.realpath('.'))
from pprint import pprint
import inquirer

client = boto3.client('iam')
response = client.list_users(MaxItems=128)

newuser=input("Please enter new user name that you want to create:")

####Choose Policy to add user into it. #######
policyname=[]
pol=client.list_policies()['Policies']
question = [inquirer.List('policy', message='Please enter policy name that seen in the screen:',
                              choices=[poli['PolicyName'] for poli in pol], ), ]
policies = inquirer.prompt(question)
polarn=''
for poli in pol:
    if poli['PolicyName']==policies['policy']:
        polarn=poli['Arn']

createuser=client.create_user( UserName='{}'.format(newuser),PermissionsBoundary='{}'.format(polarn))

##################ASk Group############
groupname=[]
question = [inquirer.List('check', message=f'Do you want to add the {newuser} into group?(y/n):',
                              choices=['Y','N'], ), ]
checking = inquirer.prompt(question)
if (checking['check']=='Y'):
    groups=client.list_groups()
    #print(groups['Groups'])
    for group in groups['Groups']:
        groupname.append(group['GroupName'])

    gro=print('Please choose the group to add the user into group')
    question = [inquirer.List('group', message='Please choose the group to add user into group:',
                              choices=[name for name in groupname], ), ]
    answers = inquirer.prompt(question)
    addusertogroup = client.add_user_to_group(GroupName='{}'.format(answers['group']),UserName='{}'.format(newuser))



userinformation=client.list_users()['Users']
####Chose user and create accesskey####
print("Creating accesskey for the user")
username=[]
for user in userinformation:
    for key,value in user.items():
        if key=='UserName':
            username.append(value)
            #print(f'{value}')
question = [inquirer.List('user',message='access key will be created for which user Please choose:',choices=[name for name in username],),]
answers= inquirer.prompt(question)


createaccesskey = client.create_access_key(UserName='{}'.format(answers['user']))
for key,value in createaccesskey['AccessKey'].items():
    if key == 'AccessKeyId':
        acceskey=value
        print(f"Accesskey of the {newuser}:{acceskey}")
    elif key=='SecretAccessKey':
        seckey =value
        print(f"SecretKey of the {newuser}:{seckey}")


#print(client.delete_user(UserName='{}'.format(newuser)))

