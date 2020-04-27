import yaml
import getpass
import logging

from pexpect import pxssh

class device():
    def __init__(self,name,username,password,getpassword,su,sugetpassword,use_sudo,interact,cmd):
        ''' Should specify all params '''
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
        # TODO check format of params 
        # TODO lock input/output
        # TODO key auth
        # TODO add public auth
        
        if not self.cmd:
            print('INFO: command list is empty')
        else:
            if bool(getpassword):
                self.spawn_input() 
                self.send()
                self.logout()            
            else:
                self.spawn() 
                self.send()
                self.logout()

    def spawn(self):
        try:
            self.child = pxssh.pxssh()
            self.child.login(self.name, self.username, self.password)
            self.child.sendline('uptime')
            self.child.prompt()
        except pxssh.ExceptionPxssh as e:
            print("pxssh failed on login.")
            print(e)
    def spawn_input(self):        
        try:
            self.child = pxssh.pxssh()
            self.password = getpass.getpass('password: ')
            self.child.login(self.name, self.username, self.password)
            self.child.sendline('uptime')
            self.child.prompt()
        except pxssh.ExceptionPxssh as e:
            print("pxssh failed on login.")
            print(e)
    
    def logout(self):
        try:
            self.child.logout()
            print(self.name, ' - completed')
        except Exception as e:
            print("Connection error: ",e)   
            
    def send(self):
        try:        
            # TODO ADD CHECK SUDO
            for command in self.cmd:
                self.child.sendline(command)
                self.child.prompt()
                self.logger.info(self.child.before.decode('UTF-8')) 
            if bool(self.interact):
                self.child.interact()        
        except Exception as e:
            print("Enter command error: ",e)          
            
    def __print__(self):
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
