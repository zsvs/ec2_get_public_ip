import boto3
import sys

TagName = sys.argv[1]#"Env"
TagValue = sys.argv[2]#"Test"
SSHUserName = sys.argv[3]

ec2 = boto3.client('ec2')
responce = ec2.describe_instances(Filters=[
                {
                   "Name": "tag:{0}".format(TagName),
                    "Values": ["{0}".format(TagValue)]
            }
        ])

InstanceNumber = len(responce["Reservations"]) # All instances number
#!Debug info print("Number of EC2: ", InstanceNumber)

def GetIPv4Add(InstanceList):
    return InstanceList["NetworkInterfaces"][0]["Association"]["PublicIp"]

def GetResult():
    Pattern = "[aws_hosts]\n"
    for InstanceCount in range(0, InstanceNumber+1):
        Pattern += GetHosts()[InstanceCount] + "\n"
    return Pattern + "[aws_hosts:vars]\nansible_user={0}".format(SSHUserName)

def GetHosts():
    Addresses = list()
    for InstanceCount in range(0, InstanceNumber):
        for Key in responce["Reservations"][InstanceCount]["Instances"]:
           Addresses.append(GetIPv4Add(Key))
    #!Debug info print("Instance counter:", InstanceCount)
    return Addresses

GetResult()

