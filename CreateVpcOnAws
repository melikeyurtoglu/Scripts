#!/bin/bash
#
#
# Desc: Create an IPv4 VPC and Subnets Using the AWS CLI.
#

#bash ./changeawsregion.bash #(if you want use this line(script), you should put same folder.)
OFFICE_IP="xxxx"
TEMP="temp"
control=0


VPC_CIDR=$(aws ec2 describe-vpcs --query 'Vpcs[*].{id:CidrBlock}' --output=text)
echo "There are these cidrs:"
for i in ${VPC_CIDR[@]}; do
	if [[ ! -z "${i}" ]];then
		echo "${i}"
	fi
done

#####add vpc cidr
get_cidr_block(){
	echo "Please Enter Cidr block for vpc. For example; 10.10.10.0/24"
	#For example CDIR_BLOCK="10.10.10.0/24"
	read CDIR_BLOCK
	if [[ ! -z "$CDIR_BLOCK" ]];then
		if ! [[ ${CDIR_BLOCK%/*}  =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ && ${CDIR_BLOCK#*/}  =~ ^[0-9]{1,2}$ ]];then 
			echo "Please check variable that entered. You should not use letter"
			get_cidr_block
		fi
	else
		get_cidr_block
	fi
	#control vpc cidr block
	
	for i in ${VPC_CIDR[@]}; do
		if [[ "${i}" == "${CDIR_BLOCK}" ]];then
			echo "There is cidr block.Please Enter different cidr block"
			get_cidr_block
		fi
	done
}

SUBNET_CIDRS=($(aws ec2 describe-subnets --query 'Subnets[*].{id:CidrBlock}' --output=text))

get_cidr_block_for_subnet(){ 
	completed=true
	for i in ${SUBNET_CIDRS[@]}; do
		if [[ "${i}" == "${variable}" ]];then
			echo "There is cidr block.Please Enter different cidr block"
			read variable
			get_cidr_block_for_subnet
			completed=false
			break
		else
			if ! [[ -z "$variable" ]];then
				if ! [[ ${variable%/*}  =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ && ${variable#*/}  =~ ^[0-9]{1,2}$ ]];then
					echo "Please check variable that entered. You should not use letter"
					read variable
					get_cidr_block_for_subnet
					completed=false
					break
				fi
			fi
		fi
	done
	if [[ $completed == true ]]; then
		TEMP=${variable}
	fi
	
}

ask_subnet(){
	echo "Please Enter cidr block for subnet. For example; 10.10.10.0/25"
	read variable
	if [[ ! -z "$variable" ]];then
		if ! [[ ${variable%/*}  =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ && ${variable#*/}  =~ ^[0-9]{1,2}$ ]];then 
			echo "Please check variable that entered. You should not use letter"
			ask_subnet
		fi
	else
		ask_subnet
	fi
	get_cidr_block_for_subnet
	SUBNET_CIDR=$TEMP
}

recursive(){
	if [[ "${preferred}" == "y" ]]; then
		echo "Please Enter cidr block 2 for subnet"
		read variable
		if [[ ! -z "$variable" ]];then
			if [[ ${variable%/*}  =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ && ${variable#*/}  =~ ^[0-9]{1,2}$ ]];then
				get_cidr_block_for_subnet
				SUBNET_CIDR2=$TEMP
			else
				echo "Please check variable that entered. You should not use letter"
				recursive
			fi
		else
			recursive
		fi
	elif [[ "${preferred}" == "n" ]]; then
		control=1
	else
		echo "Please Enter y or n"
		read preferred
		recursive

	fi
}
#get vpc variable
get_cidr_block
#get subnet variable
ask_subnet
SUBNET_CIDRS+=("${SUBNET_CIDR}")
#get secondary subnet variable
echo "Do you want to define second cidr block for subnet?(y/n)"
read preferred
recursive
echo "Please wait for a while"
#create vpc
VPC_ID=$(aws ec2 create-vpc --cidr-block ${CDIR_BLOCK} --query 'Vpc.{id:VpcId}' --output=text)

#create subnet
SUBNET_ID=$(aws ec2 create-subnet --vpc-id ${VPC_ID} --cidr-block ${SUBNET_CIDR} --query 'Subnet.{id:SubnetId}' --output=text)

#create second subnet
if [ ${control} != 1 ];then
	SUBNET_ID2=$(aws ec2 create-subnet --vpc-id ${VPC_ID} --cidr-block ${SUBNET_CIDR2} --query 'Subnet.{id:SubnetId}' --output=text)
	#echo ${SubnetId2}
fi

#create internet gateway
INTERNET_GATEWAY=$(aws ec2 create-internet-gateway --query 'InternetGateway.{id:InternetGatewayId}' --output=text)
#echo $INTERNET_GATEWAY

#attach vpc to internet gateway 
Booblean=$(aws ec2 attach-internet-gateway --vpc-id ${VPC_ID} --internet-gateway-id ${INTERNET_GATEWAY})

#create route table
ROUTE_ID=$(aws ec2 create-route-table --vpc-id ${VPC_ID} --query 'RouteTable.{id:RouteTableId}' --output=text)

#create route
Routebooblean=$(aws ec2 create-route --route-table-id ${ROUTE_ID} --destination-cidr-block ${OFFICE_IP} --gateway-id ${INTERNET_GATEWAY})


#find subnet_id
#SUBNET_ID=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=${VPC_ID}" --query 'Subnets[*].{ID:SubnetId}' --output=text)

#echo $SUBNET_ID

#choose which subnet to associate with the custom route table
AssociationId=$(aws ec2 associate-route-table  --subnet-id ${SUBNET_ID} --route-table-id ${ROUTE_ID})

#instance launched into the subnet automatically receives a public IP address.
aws ec2 modify-subnet-attribute --subnet-id ${SUBNET_ID} --map-public-ip-on-launch
