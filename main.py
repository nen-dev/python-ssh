import yaml
import logging

from pexpect import pxssh
from app import sshclass
from time import gmtime, strftime


with open('config.yml','r') as configfile:
    config = yaml.safe_load(configfile)
    devices = {}        
    today = strftime("%y%m%d-%H%M%S", gmtime())
    logfiledir = config['logfiledir']
    # TODO file exist check try
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(message)s',
                        datefmt='%C%y-%m-%dT%H:%M:%S',#'%m-%d %H:%M',
                        filename=logfiledir+'/'+today+'.log',
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s %(message)s')
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)   
    # TODO add key file host
    # TODO add adding key file 
    for host in config['hosts']:      
        devices[host['name']] = sshclass.device(name=host['name'],
                                username=host['username'],
                                password=host['password'],
                                getpassword=host['getpassword'],
                                su=host['su'],
                                sugetpassword=host['sugetpassword'],
                                use_sudo=host['use_sudo'],
                                interact=host['interact'],
                                cmd=host['cmd'])
        


