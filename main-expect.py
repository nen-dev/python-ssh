import yaml
from pexpect import pxssh

from app import sshclass

with open('config.yml','r') as configfile:
    config = yaml.safe_load(configfile)
    devices = {}
    for host in config['hosts']:      
        devices[host['name']] = sshclass.device(name=host['name'],
                                username=host['username'],
                                password=host['password'],
                                getpassword=host['getpassword'],
                                su=host['su'],
                                sugetpassword=host['sugetpassword'],
                                use_sudo=host['use_sudo'],
                                interact=host['interact'],
                                logfile=host['logfile'],
                                cmd=host['cmd'])
        


