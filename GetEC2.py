import boto3
import sys
import re
import pathlib

TagName = sys.argv[1]
TagValue = sys.argv[2]

ec2 = boto3.client('ec2')
AWSAMI = boto3.resource("ec2")

responce = ec2.describe_instances(Filters=[
                {
                   "Name": "tag:{0}".format(TagName),
                    "Values": ["{0}".format(TagValue)]
            }
        ])

InstanceNumber = len(responce["Reservations"]) # All instances number

def GetSSHNameByAWSImageName():
    for EC2InstanceNumber in range(0,InstanceNumber):
        if re.search("(ubuntu)", AWSAMI.Image(responce["Reservations"][EC2InstanceNumber]["Instances"][0]["ImageId"]).name):
            return "ubuntu"
        elif re.search("(amazon)", AWSAMI.Image(responce["Reservations"][EC2InstanceNumber]["Instances"][0]["ImageId"]).name):
            return "ec2-user"

print("Number of EC2: ", InstanceNumber)

def GetIPv4Add(InstanceList):
    return InstanceList["NetworkInterfaces"][0]["Association"]["PublicIp"]

def GetHosts():
    Addresses = list()
    for InstanceCount in range(0, InstanceNumber):
        for Key in responce["Reservations"][InstanceCount]["Instances"]:
           Addresses.append(GetIPv4Add(Key))
    return Addresses

def GetResult():
    Pattern = "[awsservershosts]\n"
    for InstanceCount in range(0, InstanceNumber):
        Pattern += GetHosts()[InstanceCount] + f" ansible_user={GetSSHNameByAWSImageName()}" + "\n"
    return Pattern

with open(f"{pathlib.Path().resolve()}/hosts", "w") as f:
    f.write(GetResult())
