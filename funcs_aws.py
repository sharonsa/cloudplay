# Scripts for AWS 
# By Sharon Saadon - sharonsaa@gmail.com

import sys
import boto3
import cloudplay_conf as vars

def create_ec2(name, region):
    if region=='':
        region=vars.default_region
    ec2 = boto3.resource('ec2',
            region_name = vars.region_name[region],
            aws_access_key_id=vars.ACCESS_ID,
            aws_secret_access_key=vars.ACCESS_KEY)
    result = ec2.create_instances(
        ImageId = vars.image_id,
        MinCount = 1,
        MaxCount = 1,
        InstanceType = 't2.micro',
        KeyName =vars.KeyName ,
        SubnetId = vars.region_SubnetId[region])
    instance = result[0]
    ec2.create_tags(Resources = [instance.id], Tags = [{'Key': 'Name', 'Value': name}])
    return instance

def get_vms(region):
    if region=='':
        region=vars.default_region
    try:
        vms = []
        ec2 = boto3.resource("ec2",
                region_name = vars.region_name[region],
                aws_access_key_id=vars.ACCESS_ID,
                aws_secret_access_key=vars.ACCESS_KEY)
        for i in ec2.instances.filter():
            name = ""
            if i.tags:
                for tag in i.tags:
                    if tag['Key'] == "Name":
                        name = tag['Value']
            vols = []
            snaps = []
            for vol in i.volumes.all():
                for attach in vol.attachments:
                    vols.append({'id': vol.id, 'size': vol.size, 'device': attach['Device']})
                for snap in vol.snapshots.all():
                    snaps.append({'id': snap.id, 'volume': snap.volume_id})
            sgs = []
            for sg in i.security_groups:
                sgs.append(sg['GroupId'])
            vms.append({'id': i.instance_id, 'type': i.instance_type, 'arch': i.architecture, 'ami': i.image_id, 'created': str(i.launch_time), 'public ip': i.public_ip_address, 'private ip': i.private_ip_address, 'key': i.key_name, 'subnet': i.subnet_id, 'state': i.state['Name'], 'vpc': i.vpc_id, 'name': name, 'volumes': vols, 'security groups': sgs, 'snapshots': snaps, 'zone': i.placement['AvailabilityZone']})
        return vms
    except:
        a, b, c = sys.exc_info()
        print ("Error: Could not list VMs: " + str(b))
        return []

def get_ec2_ip(name,region):
    if region=='':
        region=vars.default_region
    try:
        ip=''
        ec2 = boto3.resource("ec2",
                region_name = vars.region_name[region],
                aws_access_key_id=vars.ACCESS_ID,
                aws_secret_access_key=vars.ACCESS_KEY)
        for i in ec2.instances.filter():
            i_name = ""
            if i.tags:
                for tag in i.tags:
                    if tag['Key'] == "Name":
                        i_name = tag['Value']
            #print 'name='+name,'id='+i.instance_id,'name='+i_name
            if (name !='' and name==i.instance_id):
                ip=i.public_ip_address
                break
            elif (name !='' and name==i_name):
                ip=i.public_ip_address
                break
        return ip
                
    except:
        a, b, c = sys.exc_info()
        print ("Error: Could not find Instance "+name+" "+id+" IP: " + str(b))
        return []
