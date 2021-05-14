###requirements.txt
#pycrypto 
#pyopenssl
import os
## Creds
AWS_EC2_ACCESS_ID='xxxx'
AWS_EC2_SECRET_KEY = 'xxxx'
PEM_FILE = os.path.expanduser('***.pem')

### Get Windows Admin password of the newly created AWS instance
import boto.ec2
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

access_key = AWS_EC2_ACCESS_ID
secret_key = AWS_EC2_SECRET_KEY
pem_file_loc = PEM_FILE

def decrypt(ciphertext, keyfile = pem_file_loc ):
    input = open(keyfile)
    key = RSA.importKey(input.read())
    input.close()
    cipher = PKCS1_v1_5.new(key)
    plaintext = cipher.decrypt(ciphertext, None)
    return plaintext

def get_ec2_instance_secur_info(region='us-west-1',instance_name=''):
    ec2_conn = boto.ec2.connect_to_region(region,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key)
    
    # Get all instance
    reservations = ec2_conn.get_all_reservations()
    
    # Get all the instances and search for the instance based on the provided Tag - Name
    for reservation in reservations:    
        for instance in reservation.instances:
            if instance_name == instance.tags['Name']:
                # Get the encrypted password and decrypt
                print ec2_conn.get_password_data(instance.id).decode('base64')
                print ec2_conn.get_password_data(instance.id)
                password = decrypt(ec2_conn.get_password_data(instance.id).decode('base64'))
                return {'instance':instance,'ec2_conn':ec2_conn,'private_ip':instance.private_ip_address,'pwd':password}
    
    # Looks like there are no instance with the provided Tag - Name
    print instance_name + ' is not found'

instance_name = 'Demo'
node = get_ec2_instance_secur_info(instance_name = instance_name)
print node
