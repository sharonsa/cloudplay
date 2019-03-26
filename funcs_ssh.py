import sys
import boto3
import botocore
import paramiko
import cloudplay_conf as vars

def ssh_vm(ip):
   key = paramiko.RSAKey.from_private_key_file(vars.SSHKeyFile)
   client = paramiko.SSHClient()
   client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   #cmd=run
   
   try:
      client.connect(hostname=ip, username="ec2-user", pkey=key)
   except Exception, e:
      print e
      sys.exit(2) 
   return client

def run(client,cmd):
    try:
        stdin, stdout, stderr = client.exec_command(cmd)
        return stdout.read()
    
    except Exception, e:
        print e

def ssh_close(client):
    try:
        client.close()
    except Exception, e:
        print e

