vmidcommand="ssh root@${ESXI_ADDRESS} \"vim-cmd vmsvc/getallvms\" | grep '${vmname}' | awk '{printf $1}' "
vmid=subprocess.getoutput(vmidcommand)

command=f'ssh root@${ESXI_ADDRESS} "vim-cmd vmsvc/get.snapshotinfo {vmid}" | grep -e name -e id | sed -e \'s/^[[:space:]]*//\' |  cut -d "," -f1'
output=subprocess.getoutput(command)
lines=output.split("\n")


name_id_list = [line.split("=")[1].strip(' "') for line in lines]
key_list = name_id_list[::2]
values_list = name_id_list[1::2]
my_dict=dict(zip(key_list,values_list))
write_string = ',\n'.join(key_list)
with open("$HOME/vmid", "w") as snapshotfile:
    json.dump(my_dict,snapshotfile)
print(write_string)