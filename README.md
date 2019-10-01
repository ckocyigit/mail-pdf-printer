# mail-pdf-printer
This script is used to print all new mails with PDF appending from an email account. Files will be printed two sided by default.

### Config
The main script uses a `config.py`. This file need to be in the same directory as main script. In this file these 5 variables needs to be declared:

`email_user = '<Username of mailaccount>'`

`email_pass = '<Password of mailaccount>'`

`email_server='<Adress of the imap server>'`

`printer_name='<The name of the printer wich will be used in lpr>'`

`custom_temp='<A directory where the downloaded files can be cached>'`

### Docker
Mount the `config.py` in the container directory: `/skript/data` and start with command:

`sudo docker run -i -t -v <Path to config.py>:/skript/data <Container name>`
