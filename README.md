# CryptoServer

#Running 
This service is built on on Python 3.6.

### Virtual Env
This project uses a virtual env to manage dependancies. In order to use it, navagate to the root of the project and run : 

```
source my_venv_dir/bin/activate
```

If you are doing a fresh run of the project, you will need to install dependancies. To do so run:
To run Server use cmd
```
PYTHONPATH=. python3 sockets/server.py
```
for demo use client
```
PYTHONPATH=. python3 sockets/client.py 
```


For REST api version use following cmds
```
pip install -r requirements.txt 
```
To run the API locally clone the repo and run 
```
python3 crypto_server.py -p 8000
```
or
```
uwsgi --socket 0.0.0.0:8000 --protocol=http -w wsgi
```

### Api Details
to fetch currency symbol details hit on below url
```
GET http://127.0.0.1:8000/currency/{symbol}
```

to fetch all currency details hit on below url
```
GET http://127.0.0.1:8000/currency/all
```
