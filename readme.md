introduce for httpApiTest
---

### usage
```python
$ python ln_comm.py -h
usage: ontVideoApi_e.py [-h] [-v] [-s   IP] [-p   PORT] [-hdr HEADER]
                        [--cfg CONFIGFILE] [-req 0/1] [-rep 0/1] [-jsi NR]
                        [--log LOGFILE] [-dft]

ln_comm.py  arguments manual
----------------------------

optional arguments:
  -h, --help        show this help message and exit
  -v, --version     show program's version number and exit

optional arguments on HTTP-API server:
  -s   IP           set API-server's     ip to be IP
  -p   PORT         set API-server's   port to be PORT
  -hdr HEADER       set API-server's header to be HEADER

optional arguments on config file:
  --cfg CONFIGFILE  set config file to be CONFIGFILE

optional arguments on log:
  -req 0/1          set flag decides whether to show requests
  -rep 0/1          set flag decides whether to show responses
  -jsi NR           set NR-indent for json format responses
  --log LOGFILE     set logs output to LOGFILE

optional arguments on default:
  -dft, --default   show the default configurations

those arguments can be configured in CONFIGFILE statically too
---------------------------------------------------------------
```

### catlog
```python
├─ln_comm.py
├─readme.md
├─requirements.txt
│
└─ln_wrapper
│  readme.md
│  w_argparser.py
│  w_requests_scheduler.py
│
├─experiences
│  ontVideoApi_e.py
│
├─doc
   一种在 python 中用异步协程实现的HTTP-API测试工具.md
```

### coding for yourself
see python code, or a little reference by `doc`.

### sidelights
this my first time to use `python` write something, so the routines not mature enough, maybe. goddess would hope more knowledgeable guys just like you can continue to improve it.