import yaml
import logging

from pexpect import pxssh
from app import sshclass
from time import gmtime, strftime
from threading import Thread

MAXIMUM_THREADS=8
def run_device(host):
    item = q.get()
    deviceone = sshclass.device(**host)
    q.task_done()
    

with open('config.yml','r') as configfile:
    fcontinue = True
    config = yaml.safe_load(configfile)
    threads = []
    q = Queue()
    today = strftime("%y%m%d-%H%M%S", gmtime())
    logfiledir = config['logfiledir']
    # TODO file exist check try
    # TODO config file parser
    if logfiledir:
        try: 
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
        except Exception as e:
            print("Error setting up logging: ", e) 
    else:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(message)s',datefmt='%C%y-%m-%dT%H:%M:%S','%m-%d %H:%M')
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(name)-12s %(message)s')
        console.setFormatter(formatter)
        # add the handler to the root logger
        logging.getLogger('').addHandler(console)          
    
    # TODO add key file host
    # TODO add adding key file 
    for host in config['hosts']:     
        t = Thread(target=run_device, args=(host,))
        t.setName(host['name'])
        t.daemon = True
        t.start()
        threads.append(t) 
    for t in threads:
        t.join() 
        # while(fcontinue):
        # fcontinue = False
        # for t in threads:
        # fcontinue =+ t.isAlive() to join, blocked request 
    
    for item in source():
        q.put(item)

    q.join()       # block until all tasks are done
    print("All is done")
