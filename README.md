# mail-pdf-printer
This script is used to print all new mails with PDF appending from an email account. Files will be printed two sided by default.

[![Docker](http://dockeri.co/image/fius/mail-pdf-printer)](https://hub.docker.com/r/fius/mail-pdf-printer)


### Config
The main script uses a `config.py`. This file needs to be in a subdirectory from the main script called `data/`. In this file these 5 variables needs to be declared:

`email_user = '<Username of mailaccount>'`

`email_pass = '<Password of mailaccount>'`

`email_server='<Adress of the imap server>'`

`printer_name='<The name of the printer wich will be used in lpr>'`

`custom_temp='<A directory where the downloaded files can be cached>'`

The file can be created by the `setup.py` script.

### Docker
Mount the `config.py` in the container directory: `/skript/data` and start with command:

`sudo docker run -i -t -v <Path to config.py>:/skript/data <Container name>`
