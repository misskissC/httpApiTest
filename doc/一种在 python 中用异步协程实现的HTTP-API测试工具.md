一种在 python 中用异步协程实现的HTTP-API测试工具
---

##### 1 实现内容
通过包装 python 的内部模块`argparse`，`asyncio`和第三方库`aiohttp`，结合 python 3.5 之后的 `async`, `await`, `装饰器`等语法糖编写了一个 HTTP-API 测试工具，各 HTTP-API 以协程为单位异步并发请求。

对于主要心思花在 诸如`HTTP`结合`RESTful`接口设计开发或架构相关得广泛 的角色可以考虑用这个工具测试所编写的HTTP-API接口。如和是30个相同HTTP-API的请求的运行打个照面（异步并发将节约2s时间）：
```python
...
15 http://api.heclouds.com:80/ipc/video/boot_address    31.41ms
17 http://api.heclouds.com:80/ipc/video/boot_address    46.86ms
20 http://api.heclouds.com:80/ipc/video/boot_address    46.86ms

sync  request total time:  1939.13ms
async request total time:   203.08ms
time saved about  1736.05ms from sync to async
---------------------done---------------------
```

`httpApiTest`默认
1. 默认显示各个请求及请求耗时（可关闭）；
2. 默认显示出错HTTP-API请求及响应；
3. 同步请求和异步协程请求的耗时差；

可配置
1. 显示 HTTP-API 响应；
2. 指定缩进显示 json 格式的响应；
3. 指定日志文件（默认为标准输出）；
4. 可同步命令行配置参数到指定配置文件中（默认无配置文件）；
5. 配置参数优先级：命令行参数 > 配置文件参数 > 程序内置参数。

以上涉及具体功能可根据个人喜好配置。
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

##### 2 依赖库及包装或修改
`httpApiTest`目前只依赖`aiohttp`这一个第三方库。缺乏第三方库时，`httpApiTest`会提示运行`pip3 install -r requirements.txt`进行安装。另外，python 版本较低时`httpApiTest`也会提示。

`httpApiTest`在 ln_wrapper 目录下对`asyncio`&&`aiohttp`,`argparse`进行了包装供上层使用，里面的代码都比较简单和粗糙。

如果需要添加某功能时可修改这些代码，如
1. 有的 HTTP-API 对客户端有一些参数要求，可通过稍加改写 w_argparser.py 将这些参数变成可配置。直接参照已有代码依瓢画葫芦，可能会省去查库时间（有的功能还真的不好查，比如 --help 中分组显示各个模块的可配置参数）;
2. 需要先检查 HTTP-API 返回码时（=200？）去 w_requests_scheduler.py 中加一个if语句即可；
3. 响应返回的处理，httpApiTest 使用装饰器 _log_decorator 统一处理，可改写或换其他相应方式处理。

##### 3 源码备份地址
github 备份：[https://github.com/misskissC/httpApiTest](https://github.com/misskissC/httpApiTest)
gitee  备份：[https://gitee.com/misskissC/httpApiTest](https://gitee.com/misskissC/httpApiTest)

##### 4 源码提升
这是此文的第一份 python 程序且之前无python课经历，以至代码可能偏青涩。若python代码风格&&内涵成熟稳重的角色可出手隔空指点一二，那将引发极大开心和收获——达风格&&内涵成熟稳重往往不是太容易。
