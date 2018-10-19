# crowbar-guacamole
Guacamole implementation which allows for communication with a virtual machine using RDP

## To install:
Python2 must be used in this case. This will be updated later to Python3</br>

pip install -r requirements.txt

## Config.ini
To run the server, some values must be set in the config. These are the following:
FERNET_KEY= key value   
GUACD_HOST= ip address of container

The Fernet key is the key used to encrypt and decrypt the user tokens. The key must be the same across all
Calipso components    
Guacd Host is the ip address of the container which is running guacd.  

All config values must not be put in quotes etc.