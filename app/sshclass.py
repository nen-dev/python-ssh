import yaml
import getpass
import logging

from pexpect import pxssh

class device():
    def __init__(self,name,username,password,getpassword,su,sugetpassword,use_sudo,interact,cmd):
        self.name=name
        self.username=username
        self.password=str(password)
        self.getpassword=getpassword
        self.su=su
        self.sugetpassword=sugetpassword
        self.use_sudo=use_sudo
        self.interact=interact
        self.cmd=cmd
        self.logger = logging.getLogger(name)
        self.print_device()
        self.spawn() 

    def spawn(self):
        # TODO add check params
        try:
            child = pxssh.pxssh()
            child.login(self.name, self.username, self.password)
            child.sendline('uptime')
            child.prompt()
            # TODO ADD CHECK SUDO
            # TODO ADD CHECK ERROR CMD
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
            print("name: {name}\nusername: {username}\npassword: {password}\ngetpassword: {getpassword}\nsu: {su}\nsugetpassword: {sugetpassword}\nuse_sudo: {use_sudo}\ninteract: {interact}\nCommands: {cmd}".format(name=self.name,
                                               username=self.username,
                                               password=self.password,
                                               getpassword=self.getpassword,
                                               su=self.su,sugetpassword=self.sugetpassword,
                                               use_sudo=self.use_sudo,
                                               interact=self.interact,
                                               cmd=self.cmd))
        except Exception as e:
            print("Something went wrong with config.yaml: ",e) 
        #finally:

def main():          
    print('DEBUG: Class initialisation')
if __name__ == "__main__":
    main()
