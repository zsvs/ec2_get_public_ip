import boto3
import sys
import re
import pathlib

tag_name = sys.argv[1]
tag_value = sys.argv[2]

ec2 = boto3.client('ec2')
AWSAMI = boto3.resource("ec2")

responce = ec2.describe_instances(Filters=[
                {
                   "Name": f"tag:{tag_name}",
                    "Values": [f"{tag_value}"]
            }
        ])

instance_number = len(responce["Reservations"]) # All instances number

def get_ssh_name_by_AWS_image_name():
    for EC2instance_number in range(0,instance_number):
        if re.search("(ubuntu)", AWSAMI.Image(responce["Reservations"][EC2instance_number]["Instances"][0]["ImageId"]).name):
            return "ubuntu"
        elif re.search("(amazon)", AWSAMI.Image(responce["Reservations"][EC2instance_number]["Instances"][0]["ImageId"]).name):
            return "ec2-user"

print("Number of EC2: ", instance_number)

def get_IPv4Addr(instance_list):
    return instance_list["NetworkInterfaces"][0]["Association"]["PublicIp"]

def get_hosts():
    Addresses = list()
    for instance_count in range(0, instance_number):
        for Key in responce["Reservations"][instance_count]["Instances"]:
           Addresses.append(get_IPv4Addr(Key))
    return Addresses

def get_result():
    Pattern = "[awsservershosts]\n"
    for instance_count in range(0, instance_number):
        Pattern += get_hosts()[instance_count] + f" ansible_user={get_ssh_name_by_AWS_image_name()}" + "\n"
    return Pattern

with open(f"{pathlib.Path().resolve()}/hosts", "w") as f:
    f.write(get_result())
