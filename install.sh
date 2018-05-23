#!/usr/bin/bash
python3 -m pip install -r requirements.txt
openssl req  -nodes -new -x509 -subj '/CN=local/O=local/C=US'  -keyout local.key -out local.crt 
