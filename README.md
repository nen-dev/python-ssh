# python-ssh
This application connect to different server throuh ssh using settings from config.yml.

```yml
hosts:
 - name: 10.1.1.1 # Specify name or IP of control host
   username: true_old_admin # Specify username 
   password: strong-password # Specify password
   getpassword: False # Set true if you want enter password
   su: very-strong-password # Specify su password
   sugetpassword: False # Set true if you want enter password
   use_sudo: False # Set true if you want run command with sudo
   interact: False # Set true if you want interact cli 
   logfile: /home/true_old_admin/python-ssh-today.log # Specify log file path
   cmd: ['ls -la','echo $PATH $HOME','uptime']
 - name: 10.1.1.2 # Specify name or IP of control host
   username: true_old_admin # Specify username 
   password: strong-password # Specify password
   getpassword: False # Set true if you want enter password
   su: very-strong-password # Specify su password
   sugetpassword: False # Set true if you want enter password
   use_sudo: False # Set true if you want run command with sudo
   interact: False # Set true if you want interact cli 
   logfile: /home/true_old_admin/python-ssh-today.log # Specify log file path
   cmd: ['echo "Hello world!"']
```
# How to use it?
*** Requirements: apt-get -y install python3 python3-venv
git clone git@github.com:nen-dev/python-ssh.git'
cd python-ssh
sourse bin/activate
python3 main.py
