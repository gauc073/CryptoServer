# CryptoServer

#Running 
This service is built on on Python 3.6.

### Virtual Env
This project uses a virtual env to manage dependancies. In order to use it, navagate to the root of the project and run : 

```
source my_venv_dir/bin/activate
```

If you are doing a fresh run of the project, you will need to install dependancies. To do so run:

```
pip install -r requirements.txt 
```
To run the API locally clone the repo and run 
```
python3 crypto_server.py
```
or
```
uwsgi --socket 0.0.0.0:8000 --protocol=http -w wsgi
```