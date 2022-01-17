import boto3
import sys



TagName = sys.argv[1]#"Env"
TagValue = sys.argv[2]#"Test"

ec2 = boto3.client('ec2')

def GetIPv4Add(InstanceList):
    return InstanceList["NetworkInterfaces"][0]["Association"]["PublicIp"]

def GetHosts():
    Addresses = list()
    responce = ec2.describe_instances(Filters=[
                {
                   "Name": "tag:{0}".format(TagName),
                    "Values": ["{0}".format(TagValue)]
            }
        ])

    for InstanceCount in range(0, len(responce["Reservations"]), 1):
       for Key in responce["Reservations"][InstanceCount]["Instances"]:
          Addresses.append(GetIPv4Add(Key))
    return Addresses

print(GetHosts())
