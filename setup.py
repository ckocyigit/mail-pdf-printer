import os
import getpass
try:
    os.system('mkdir data')
except:
    pass

email_user = input("email_user:")
email_pass = getpass.getpass(prompt='email_pass: ', stream=None) 
email_server=input("email_server:")
printer_name=input("printer_name:")
custom_temp=input("custom_temp:")

output='email_user = "{email_user}"\n'.format(email_user=email_user)
output+='email_pass = "{email_pass}"\n'.format(email_pass=email_pass)
output+='email_server = "{email_server}"\n'.format(email_server=email_server)
output+='printer_name = "{printer_name}"\n'.format(printer_name=printer_name)
output+='custom_temp = "{custom_temp}"'.format(custom_temp=custom_temp)

fp = open("data/config.py", 'w')
fp.write(output)
fp.close()