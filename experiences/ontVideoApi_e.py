#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ontVideoApi.py,
routines for one HTTP-API to 
experiencing asyncio && coroutines.

lxr, 2019.02
"""
from sys import path
path.append('../')
path.append('../ln_wrapper')

import json, time, random, ln_comm
from platform   import python_version       as py_ver
from ln_wrapper import w_requests_scheduler as ln_rsch

'''
some wrappers, none special ticks.
for checking, for logs decorator etc.
'''
def _check_python_version():
    if '3.7' > py_ver():
        exit(f"python version can't be less than 3.7\n")

def _done_tips(sync_time, async_time, comm):
    tips = 'time saved about %8.2fms from sync to async' % \
           (sync_time - async_time)
    comm.LOG.write(  'sync  request total time: %8.2fms' % sync_time
        + f'\nasync request total time: %8.2fms' % async_time
        + f'\n{tips}'
        + f'\n{"-" * (round(len(tips)/2)-2)}done{"-" * round((len(tips)/2)-2)}')

def _show_log(index, url, resp, dtm, comm):
    ''' show corresponding information 
        according to configurations '''
    if comm.get_request_showing_flag():
        comm.LOG.write(f'{index} {url} {"%8.2f" % (dtm)}ms\n')

    indent = comm.get_response_json_indent()
    indent = None if indent == 1 else indent
    json_flag = 1
    _LOG = comm.LOG
    try:
        resp_dict = json.loads(resp, encoding='utf-8')
        if resp_dict['errno'] != 0 and resp_dict['errno'] != 200:
            _LOG.write(json.dumps(resp_dict, indent=indent) + '\n\n')
            return None
    except Exception as e: 
        json_flag = 0
        resp = resp if resp != None else 'None'
        _LOG.write('response: '+ resp + '\n\n')
    
    if comm.get_response_showing_flag() and json_flag:
        _LOG.write(json.dumps(json.loads(resp), indent=indent) + '\n\n')
    
_time_sync = 0
def _log_decorator(api_fn):
    ''' one decorator for HTTP API showing logs '''
    async def _w(index, comm):
        global _time_sync
        
        ltm = time.time_ns()
        url, resp = await api_fn(index, comm)
        dtm = (time.time_ns() - ltm) / 1.0e+6
        _time_sync += dtm
        
        _show_log(index, url, resp, dtm, comm)
        
    return _w

'''
    HTTP API experiences
    
    because the website 
    http://api.heclouds.com:80/ipc/video/boot_address
    wouldn't refuse requests, use it for experiences 
    here by following steps:
    [1] get configurations(url etc.) of HTTP-API 
        by ln_comm;
    [2] request the url with corresponding 
        configurations by w_requests_scheduler.w_request,
        w_request is an async-coroutine, so use await 
        to wait response.
     [3] use '_log_decorator' to decorate HTTP-API,
        this is optional, you can use another better.
'''
@_log_decorator
async def get_boot_addr(index, comm):
    path = '/ipc/video/boot_address'
    url  = comm.get_url_comm_part() + path
    resp = await ln_rsch.w_request(url, 'get')
    return url, resp


if __name__ == '__main__':
    ''' for all HTTP-APIs testing '''
    _check_python_version()
    comm  = ln_comm.Common()
    
    group = 15;max = 33
    apis_first = []
    for i in range(group):
        apis_first.append(get_boot_addr(i, comm))
    
    apis_then = []
    for i in range(group, max):
        apis_then.append(get_boot_addr(i, comm))
    
    time_async_s = time.time_ns()
    rsch = ln_rsch.w_rScheduler()
    rsch.w_loop(apis_first)
    rsch.w_loop(apis_then)
    rsch.w_close()
    time_async_e = time.time_ns()
    
    _done_tips(_time_sync, (time_async_e - time_async_s) / 1.0e+6, comm)