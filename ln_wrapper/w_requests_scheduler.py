#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
w_requests_scheduler.py,
routines for wrapping http-request and 
http-requests-scheduler according to 
asyncio && aiohttp libraries.

the request wrapped is one kind of 
coroutine, it is also asynchronous.

aiohttp is the third party library.
lxr, 2020.02
"""

import json
import asyncio
try:
    from aiohttp import ClientSession as as_client
except:
    exit('try to run following command to install the third parties\n\t'
         + 'pip3 install -r requirements.txt')

def _method_mapping(client, method):
    ''' mapping method 'get', 'post', 
        'delete', 'put' to client.get, 
        client.post, client.delete, 
        client.put respectively. '''
    if   method == 'get':
        return client.get
    elif method == 'post':
        return client.post
    elif method == 'delete':
        return client.delete
    elif method == 'put':
        return client.put
    else:
        return None

async def _w_method(aiohttp_m, url, 
    hdrs=None, params=None, data=None, timeout=None):
    ''' wrapper for the aiohttp_m, e.g. 
        aiohttp.as_client.get '''
    async with aiohttp_m(url = url,
                     headers = hdrs,
                     params  = params,
                     data    = data,
                     timeout = timeout) as resp:
        try: return await resp.text(encoding='utf-8')
        except Exception as e: print(e)
    
    return None

async def w_request(url, method,
    hdrs=None, params=None, data=None, timeout=None):
    ''' wrapper for aiohttp.as_client.method,
        make it be asynchronous coroutine. '''
    async with as_client() as client:
        method = _method_mapping(client, method)
        try: return await _w_method(method, url, 
                        hdrs=hdrs, params=params,
                        data=data, timeout=timeout)
        except Exception as e: print(e)
    return None

class w_rScheduler():
    ''' wrapper for asyncio '''
    def __init__(self):
        try:
            self.loop = asyncio.get_event_loop()
        except Exception as e: exit(e)

    def w_loop(self, requests):
        ''' run requests asynchronously 
            in asyncio.loop() '''
        try:
            w_r = asyncio.wait(requests)
            self.loop.run_until_complete(w_r)
        except Exception as e: print(e)
        else: print('')
        
    def w_close(self):
        self.loop.close()

if __name__ == '__main__':
    ''' for testing w_aiohttp.py '''
    url = 'https://mijisou.com/'
    async def w_r_first(index):
        resp = await w_request(url, 'get')
        print(f'{index} {resp[0:9] if resp != None else None}')
    async def w_r_then(index):
        resp = await w_request(url, 'get')
        print(f'{index} {resp[0:9] if resp != None else None}')
        
    r_first = []
    r_then  = []
    for i in range(3):
        r_first.append(w_r_first(i + 1))
    for i in range(3, 6):
        r_then.append(w_r_then(i + 1))
    
    r_sched = w_rScheduler()
    r_sched.w_loop(r_first)
    r_sched.w_loop(r_then)
    r_sched.w_close()
