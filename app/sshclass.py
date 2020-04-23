import yaml
from pexpect import pxssh
import getpass
import logging

# TO DO file exist check try

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(message)s',
                    datefmt='%C%y-%m-%dT%H:%M:%S',#'%m-%d %H:%M',
                    filename='/home/nen/expect-log.log',
                    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s %(message)s')
console.setFormatter(formatter)
 # add the handler to the root logger
logging.getLogger('').addHandler(console)   


class device():
    def __init__(self,name,username,password,getpassword,su,sugetpassword,use_sudo,interact,logfile,cmd):
        self.name=name
        self.username=username
        self.password=str(password)
        self.getpassword=getpassword
        self.su=su
        self.sugetpassword=sugetpassword
        self.use_sudo=use_sudo
        self.interact=interact
        self.logfile=logfile
        self.cmd=cmd
        self.logger = logging.getLogger(name)
        self.print_device()
        self.spawn() 

    def spawn(self):
        # TO DO add check params
        try:
            child = pxssh.pxssh()
            child.login(self.name, self.username, self.password)
            child.sendline('uptime')
            child.prompt()
            # TO DO ADD CHECK SUDO
            # TO DO ADD CHECK ERROR CMD
            for command in self.cmd:
                child.sendline(command)
                child.prompt()
                self.logger.info(child.before.decode('UTF-8')) 
            if bool(self.interact):
                child.interact()
            child.logout()
        except pxssh.ExceptionPxssh as e:
            print("pxssh failed on login.")
            print(e)
    
    def print_device(self):
        try: 
            print("name: {name}\nusername: {username}\npassword: {password}\ngetpassword: {getpassword}\nsu: {su}\nsugetpassword: {sugetpassword}\nuse_sudo: {use_sudo}\ninteract: {interact}\nlogfile: {logfile}\nCommands: {cmd}".format(name=self.name,
                                               username=self.username,
                                               password=self.password,
                                               getpassword=self.getpassword,
                                               su=self.su,sugetpassword=self.sugetpassword,
                                               use_sudo=self.use_sudo,
                                               interact=self.interact,
                                               logfile=self.logfile,cmd=self.cmd))
        except Exception as e:
            print("Something went wrong with config.yaml: ",e) 
        #finally:

def main():          
    print('DEBUG: Class initialisation')
if __name__ == "__main__":
    main()
