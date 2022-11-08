"""
Simple ansible host inventory script.
It takes two arguments:
 - TAG_NAME - Name of the resource tag
 - TAG_VALUE - Value of the given tag
Then creates the hosts file with values
Example:
    [awsservershosts]
    xxx.xxx.xxx.xxx ansible_user=ubuntu
"""
import sys
import re
import pathlib
import boto3

TAG_NAME = sys.argv[1]
TAG_VALUE = sys.argv[2]

EC2 = boto3.client('ec2')
AWSAMI = boto3.resource("ec2")

responce = EC2.describe_instances(Filters=[
                {
                   "Name": f"tag:{TAG_NAME}",
                    "Values": [f"{TAG_VALUE}"]
            }
        ])

instance_number = len(responce["Reservations"]) # All instances number

def get_ssh_name_by_aws_image_name():
    """
    Return ssh username based on what AMI is used for EC2 instance
    """
    for ec2_instance_number in range(0,instance_number):
        if re.search("(ubuntu)", AWSAMI.Image(responce["Reservations"][ec2_instance_number]["Instances"][0]["ImageId"]).name) or re.search("Terraria-1447-srv",AWSAMI.Image(responce["Reservations"][ec2_instance_number]["Instances"][0]["ImageId"]).name):
            return "ubuntu"
        if re.search("(amazon)", AWSAMI.Image(responce["Reservations"][ec2_instance_number]["Instances"][0]["ImageId"]).name):
            return "ec2-user"
    return None

print("Number of EC2: ", instance_number)

def get_ip_addr(instance_list: dict):
    """
    Return public IPv4 address of EC2 instance
    """
    return instance_list["NetworkInterfaces"][0]["Association"]["PublicIp"]

def get_hosts():
    """
    Return list of IPv4 for found EC2 instances
    """
    addresses = []
    for instance_count in range(0, instance_number):
        for key in responce["Reservations"][instance_count]["Instances"]:
            addresses.append(get_ip_addr(key))
    return addresses

def get_result():
    """
    Creates template for ansible hosts file
    Example:
    [awsservershosts]
    xxx.xxx.xxx.xxx ansible_user=ubuntu

    """
    pattern = "[awsservershosts]\n"
    for instance_count in range(0, instance_number):
        pattern += get_hosts()[instance_count] + f" ansible_user={get_ssh_name_by_aws_image_name()}" + "\n"
    return pattern

with open(f"{pathlib.Path().resolve()}/hosts", "w", encoding="utf-8") as f:
    f.write(get_result())
