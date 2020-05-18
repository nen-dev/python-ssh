import yaml
import getpass
import logging
import sys


from pexpect import pxssh,spawn, EOF

class device():
    def __init__(self,name,username,password,getpassword,su,sugetpassword,use_sudo,interact,cmd, add_pub_auth, control_host, manager_username, manager_password, manager_sudo_nopass, manager_password_control_host, public_key_auth, ssh_key):
        ''' Should specify all params '''
        self.name=name
        self.username=username
        self.ssh_key = ssh_key
        self.password=str(password)
        self.getpassword=getpassword
        self.su=str(su)
        self.sugetpassword=sugetpassword
        self.use_sudo=use_sudo
        self.interact=interact
        self.cmd=cmd
        self.logger = logging.getLogger(name)
        self.add_pub_auth = add_pub_auth
        self.control_host = control_host
        self.manager_username = manager_username
        self.manager_password_control_host = manager_password_control_host
        self.manager_password = manager_password
        self.manager_sudo_nopass = manager_sudo_nopass
        self.public_key_auth = public_key_auth
        
        
        self.cmd_local = ['sudo useradd -m -s /bin/bash ' + self.manager_username,
                          'sudo echo "' + self.manager_username + ':' + self.manager_password_control_host + '" | sudo /usr/sbin/chpasswd']

        self.cmd_genkey = ['sudo echo "' + self.manager_username + '    ' + 'ALL=(ALL)    NOPASSWD:    ALL" > /etc/sudoers.d/' + self.manager_username,
                           'sudo apt-get install sshpass -y',
                           'sudo su - ' + self.manager_username + ' -c "rm ~/.ssh/' + self.name +  '*"',
                           'sudo su - ' + self.manager_username + ' -c "ssh-keygen -b 4096 -t rsa -f ~/.ssh/' + self.name + ' -q -P \'\' "',
                           'sudo su - ' + self.manager_username + ' -c "sshpass -p "' + self.manager_password + '" ssh-copy-id -f -o StrictHostKeyChecking=no -i ~/.ssh/' + self.name + ' ' + self.manager_username + '@' + self.name + '"']    
        
        self.cmd_managed_conf = ['apt-get install -y sudo',
                                 'useradd -m -s /bin/bash ' + self.manager_username,
                                 'echo "' + self.manager_username + ':' + self.manager_password + '" | /usr/sbin/chpasswd',
                                 'echo "' + self.manager_username + ' ' +  ' ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/' + self.manager_username]
       
       # TODO: improve adding users
        if bool(self.add_pub_auth):
            self.spawn_local(cmd=self.cmd_local) # 1.. Create ansible user for a control host and change password
            
            self.spawn()
            print('DEBUG: ', self.cmd_managed_conf)
            self.spawn_su(cmd = self.cmd_managed_conf) # 2. Create ansible user for a managed host and change password
            self.logout()

            self.spawn_local(cmd = self.cmd_genkey) # 3. Generate rsa key on control host and copy key to a managed host 
            
        # TODO check format of params 
        # TODO lock input/output
        # TODO key auth
        # TODO add public auth

        if not self.cmd:
            print('INFO: command list is empty')
        else:
            if bool(self.public_key_auth):
                try:
                    self.spawn_pubauth() 
                except Exception as e:
                    print("login error: ",e)               
            else:
                if bool(getpassword):
                    try:
                        self.spawn_input() 
                    except Exception as e:
                        print("login error: ",e)         
                else:
                    try:
                        self.spawn() 
                    except Exception as e:
                        print("login error: ",e)
                    
                    
            if bool(self.use_sudo):
                self.send_sudo(cmd = self.cmd)
            else:
                self.send(finteract=bool(self.interact), cmd = self.cmd)
            self.logout()                  
            
    def send_sudo(self,  finteract = bool(False), cmd = []):
        try:        
            # TODO ADD CHECK SUDO
            for command in cmd:
                self.child.sendline('sudo ' + command)
                self.child.prompt()
                self.logger.info(self.child.before.decode('UTF-8')) 
            if finteract:
                self.child.interact()        
        except Exception as e:
            print("Enter command error: ",e)         
    def spawn_su(self, cmd = []):
        try:        
            for command in cmd:
                print('DEBUG: ','su - root -c \'' + command + '\'' )
                self.child.sendline('su - root -c \'' + command + '\'' )
                self.child.waitnoecho()
                self.child.sendline(self.su)
                self.child.prompt()
                self.logger.info(self.child.before.decode('UTF-8'))
        except Exception as e:
            print("Enter command error: ",e)    
    def spawn_local(self,cmd = []):
        try:        
            # TODO ADD CHECK SUDO
            for command in cmd:
                self.local_child = spawn(command)
                self.local_child.expect(EOF)
                self.logger.info(self.local_child.before)  
        except Exception as e:
            print("Enter local command error: ",e)           
    def spawn_pubauth(self):
        try:
            ssh_options = 
            self.child = pxssh.pxssh(options=ssh_options)
            self.child.login(hostname=self.name, username=self.username, ssh_key=self.ssh_key)
        except pxssh.ExceptionPxssh as e:
            print("pxssh failed on login.")
            print(e)            
    def spawn(self):
        try:
            self.child = pxssh.pxssh()
            self.child.login(self.name, self.username, self.password)
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
            
    def send(self, finteract = bool(False), cmd = []):
        try:        
            # TODO ADD CHECK SUDO
            for command in cmd:
                self.child.sendline(command)
                self.child.prompt()
                self.logger.info(self.child.before.decode('UTF-8')) 
            if finteract:
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
