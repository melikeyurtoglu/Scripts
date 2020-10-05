sys.path.append(os.path.realpath('.'))
from pprint import pprint
import inquirer


client = boto3.client('iam')
response = client.list_users(MaxItems=128)

userinformation=client.list_users()['Users']
mfa=client.list_virtual_mfa_devices()['VirtualMFADevices']

count=10
mfauser={}
allusername=[]
for mfainf in mfa:
  for key,value in mfainf['User'].items():
    if key=='UserName':
      mfauser.update({'{}'.format(value):'{}'.format(mfainf['EnableDate'])})
      count=len(value)


row=['Path','MFAEnableDate','UserName','UserId','Arn','CreateDate','PasswordLastUsed']

for tittle in row:
    print(f'{tittle}\t\t', end="")
print('\n')
values=[]
for userinf in userinformation:
  for key,value in userinf.items():
    if key=='UserName':
        allusername.append(value)
        if value in mfauser:
            print(f'{mfauser[value]}\t', end="")
        else:
            print(' '.ljust(count*2), end="")
    #values.append(value)
    print("{}\t".format(value).ljust(8), end="")
  print('\n')


question = [inquirer.List('user', message='Please choose a user to do active to mfa:',
                              choices=[name for name in allusername], ), ]
username = inquirer.prompt(question)

mfaqr=client.create_virtual_mfa_device(VirtualMFADeviceName='{}'.format(username['user']))


for key,value in mfaqr['VirtualMFADevice'].items():
   if key=='Base32StringSeed':
     base32=value
   elif key=='SerialNumber':
     serial=value
   elif key=='QRCodePNG':
       with open("qr.png", "wb") as f:
          f.write(value)
   else:
     continue

sra = str(base32,'utf-8')

totp=pyotp.TOTP(sra)
token1=totp.now()
token2=totp.now()

while(token1==token2):
    token2=totp.now()

response=client.enable_mfa_device(UserName='{}'.format(username['user']),SerialNumber='{}'.format(serial),AuthenticationCode1='{}'.format(token1),AuthenticationCode2='{}'.format(token2))
print(response)
