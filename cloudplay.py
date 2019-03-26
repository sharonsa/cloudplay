#!/usr/bin/python
# CloudPlay Scripts for Cloud automation 
# By Sharon Saadon - sharonsaa@gmail.com
# www.sharontools.com

import sys, getopt
import time
import functions
import funcs_aws
import funcs_ssh

def main(argv):
    print "AWS automation script"
    print "By: Sharon Saadon"

    ins_action = ''
    ins_name = ''
    ins_region= ''
    ins_run=''
    ins_install=''
    debug_mode=False

    try:
        opts, args = getopt.getopt(argv,"hds:c:C:I:r:R:",["help","debug","create=","install=","connect=","region=","show=","run="])
    except getopt.GetoptError:
        print_help()
	sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_help()
            sys.exit()
        elif opt in ("-s", "--show"):
            ins_action="show"
            ins_name = arg
        elif opt in ("-C", "--create"):
            ins_action="create"
            ins_name = arg
        elif opt in ("-c", "--connect"):
            ins_action="connect"
            ins_name = arg
        elif opt in ("-R", "--region"):
            ins_region= arg
        elif opt in ("-r", "--run"):
            ins_run= arg
        elif opt in ("-I", "--install"):
            ins_install= arg
        elif opt in ("-d", "--debug"):
            debug_mode=True
    if ins_action=='':
        print_help()
        sys.exit()
    elif ins_action=='create':
        print 'Creating EC2:', ins_name, 'Region:', ins_region
        create(ins_name,ins_install,ins_region,debug_mode)
    elif ins_action=='connect':
        connect(ins_name,ins_install,ins_run,ins_region,debug_mode)
    elif ins_action=='show':
	print "show",ins_name
        print_instances(ins_name, ins_region)

def create(ins_name,ins_install,ins_region,debug_mode):
    instance=funcs_aws.create_ec2(ins_name,ins_region)
    print instance.id , 'Created'
    if (ins_install !=''):
        print 'Waiting for instance to be ready..'
        instance.wait_until_running()
        print 'Checking EC2 IP..'
        ins_ip=funcs_aws.get_ec2_ip(ins_name,ins_region)
        if (ins_ip==''):
             print "Error: can't find IP address of",ins_name
             sys.exit()  
        if (ins_install != ''):
            time.sleep(5)
            install(ins_ip,ins_install,debug_mode)
        elif (ins_run != ''):
            run_command(ins_ip,ins_run)

def connect(ins_name,ins_install,ins_run,ins_region,debug_mode):
    if (functions.is_ip(ins_name)):
        ins_ip=ins_name
    else:
        print 'Checking EC2 IP..', ins_name, 'Region:', ins_region   
        ins_ip=funcs_aws.get_ec2_ip(ins_name,ins_region)
        if (ins_ip==''):
             print "Error: can't find IP address of",ins_name
             sys.exit()
    #print "Connecting ",ins_name,"("+ins_ip+")"
    if (ins_install != ''):
	install(ins_ip,ins_install,debug_mode)
    elif (ins_run != ''):
        run_command(ins_ip,ins_run)

def run_command(ins_ip,ins_run):
    client=funcs_ssh.ssh_vm(ins_ip)
    result=funcs_ssh.run(client,ins_run)
    funcs_ssh.ssh_close(client)
    print  result

def install(ins_ip,app,debug_mode):
    try:
        filename='apps/'+app+'.conf'
        file = open(filename , 'r')
    except:
        a, b, c = sys.exc_info()
        print "\nCould not open file '"+filename+"'\n", str(b),"\n"
        sys.exit()
    print "Connecting ",ins_ip,".."
    client=funcs_ssh.ssh_vm(ins_ip)
    for line in file: 
        if line.startswith('#print'):
            line=line.replace('#print ','')
            print line.strip()
        elif (not line.startswith('#') and line.strip() != ''):
            result=funcs_ssh.run(client,line)
            if (debug_mode):
                print result
    print "Instance IP-",ins_ip
    funcs_ssh.ssh_close(client)
    print ""

def print_help():
    print ''
    print 'Help'
    print '----'
    print 'aws.py [-h|-d] [-C|-c|-s] <instance-name>  [-I <application>] [-R <region>]'
    print ''
    print ' -h --help     show this help'
    print ' -d --debug    debug mode - show more info'
    print ' -s --show     show all VMs or specific VM'
    print ' -C --create   create  VM'
    print " -I --install  Install app at remote VM (for now only 'proxy' is supported)"
    print ' -c --connect  Instance Name,ID or IP address'
    print ' -r --run      run command at remote instance'
    print ' -R --region   select region, if not set default region is selected,'
    print '               You can set default region at cloudplay_conf.py'
    print ''
    print 'Examples:'
    print 'Create new VM:'
    print '  ./cloudplay.py -C VM1 -I proxy [-R paris]'
    print 'Show all VMS:'
    print '  ./cloudplay.py -s all [-R paris>]'
    print 'Show specific VM:'
    print '  ./cloudplay.py -s VM1 [-R paris]'

#def print_created_instance(instance):
    #print instance.id , 'Created'
    #print("Private IP: " + instance.private_ip_address)
    #print("Public IP: " + instance.public_ip_address)

def print_instances(ins_name, ins_region):
    print "Name \tID \t\t\tType \t\tPrivate IP\tPublic IP \tState";
    for i in funcs_aws.get_vms(ins_region):
        if (ins_name=='all' or ins_name==i['name']):
            i_name=i['name']
            i_id=i['id']
            i_type=i['type']
            i_state=i['state']

            if (i['state']=='terminated'):
                i_private_ip="xxx.xxx.xxx"
                i_public_ip="xxx.xxx.xxx"
            else:
                i_private_ip=i['private ip']
                i_public_ip=i['public ip']

            print (i_name+"\t"+i_id+"\t"+i_type+"\t"+i_private_ip+"\t"+i_public_ip+"\t"+i_state)

if __name__ == "__main__":
    main(sys.argv[1:])
