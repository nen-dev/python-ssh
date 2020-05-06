# python-ssh

This application connect to different servers throuh ssh using settings from config.yml.
Run different commands on each.
Provide log to screen and files.

Simple multithreading support ^^

```yaml
hosts:
 - name: 10.1.1.1 # Specify name or IP of control host
   username: true_old_admin # Specify username
   public_key_auth : False  # conect using key auth   
   password: strong-password # Specify password
   getpassword: False # Set true if you want enter password
   su: very-strong-password # Specify su password
   sugetpassword: False # Set true if you want enter password
   use_sudo: False # Set true if you want run command with sudo
   interact: False # Set true if you want interact cli 
   cmd: ['ls -la','echo $PATH $HOME','uptime']
   add_pub_auth: True # Configure public authentication.
   # 1. Add %manager_username% to control and managed host.
   # 2. Create private key and copy it to managed host
   # 3*. Add to sudo NOPASSWD
   control_host: 192.168.1.111
   manager_username: ansible
   manager_password: very-very-strong-passw0rd
   manager_sudo_nopass: False      
 - name: 10.1.1.2 
   username: true_old_admin
   password: strong-password 
   getpassword: False 
   su: very-strong-password 
   sugetpassword: False 
   use_sudo: False 
   interact: False 
   cmd: ['echo "Hello world!"]
logfiledir:  /home/true_old_admin/ssh-log # Specify log directory path. Full file path will be logfiledir/%y%m%d-%H%M%S.log 
```
# How to use it?

**Requirements: apt-get -y install python3 python3-venv**
1) Run:
```bash
git clone git@github.com:nen-dev/python-ssh.git
```
2) Customize config.yml
3) Run:
```bash
cd python-ssh
source bin/activate
python3 main.py
```
