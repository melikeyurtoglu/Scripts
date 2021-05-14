#!/bin/python3.6
###Eski sunucusuna ovaları deploy etmek icin.
import readline
import inquirer
import subprocess as sp
import shlex
import sys
import json

def run_realtime_command(command):
    process = sp.Popen(shlex.split(command), stdout=sp.PIPE)
    while True:
        output = process.stdout.read(1).decode('utf-8')
        if output == '' and process.poll() is not None:
            print('')
            break
        if output:
            sys.stdout.write(output)
    rc = process.poll()
    return rc


def input_with_default(prompt, prefill=''):
    readline.set_startup_hook(lambda: readline.insert_text(prefill))
    try:
        return input(prompt)
    finally:
        readline.set_startup_hook()

# Get credentials from database
json_file = open('database.json')
json_str = json_file.read()
json_data = json.loads(json_str)
SERVERS=json_data["servers"]
PATHS=json_data["ova-paths"]

# Ask which server
servers = SERVERS.keys()
questions = [
    inquirer.List('servers', message="Select an ESXI server to deploy OVA:", choices=servers)
]
selected_server = inquirer.prompt(questions).get('servers')
print('ESXI server \'' + selected_server + '\' selected.')

# Ask which OVA
ovas = []
for path in PATHS:
    command = f'ls -1 {path}/*.ova'
    result = sp.run(command, stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True, shell=True)
    ovas.extend([ova.strip() for ova in result.stdout.split('\n') if "Error" not in ova and ova != ""])
questions = [
    inquirer.List('ovas', message="Select an OVA file to deploy:", choices=ovas)
]
selected_ova = inquirer.prompt(questions).get('ovas')
print('Ova file \'' + selected_ova + '\' selected.')
print('Deploying OVA file now...')

# Ask VM name
vm_name = input_with_default('[?] Please enter VM name: ', selected_ova.split('/')[-1].split('.ova')[0])

# Ask datastore
command = f'ssh {selected_server} \'esxcli storage vmfs extent list\' | awk \'{{print $1}}\' | tail -n +3'
result = sp.run(command, stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True, shell=True)
datastores = [datastore.strip() for datastore in result.stdout.split('\n') if
              "Error" not in datastore and datastore != ""]
questions = [
    inquirer.List('datastores', message="Select a datastore to deploy OVA:", choices=datastores)
]
selected_datastore = inquirer.prompt(questions).get('datastores')

# Deploy OVA
command = f'ovftool --noSSLVerify --name="{vm_name}" --diskMode="thin" --datastore="{selected_datastore}" --network="VM Network" --sourceType="OVA" {selected_ova} "vi://{SERVERS[selected_server]["username"]}:{SERVERS[selected_server]["password"]}@{selected_server}"'
run_realtime_command(command)
print('Ova deployed.')