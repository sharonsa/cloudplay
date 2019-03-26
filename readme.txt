# CloudPlay by - Sharon Saadon
# More info at -
# http://www.sharontools.com/blog/scripts/amazon-aws-automation-using-python/

# 1.pre-requirements:
pip install boto3
pip install paramiko

# 2.Please create 'cloudplay_conf.py' file with this parameters
#   and Cahnge default region to AWS datacenter you want

KeyName = 'XXXX'
SSHKeyFile='keys/xxxx'
ACCESS_ID='XXXX'
ACCESS_KEY='XXXX'

default_region='paris'
region_name={'paris':'eu-west-3'}
region_SubnetId={'paris':'XXXX'}
image_id='ami-0451ae4fd8dd178f7'


# 3.add ssh pem keys file to keys folder

$ 4.Allow SSH from your IP address at AWS default security group
