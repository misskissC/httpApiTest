#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ln_comm.py,
the common routines according to wrapper/ 
for experiences/ using.

lxr, 2020.02
"""

import json
from ln_wrapper import w_argparser as _lnap

class Common():
    ''' instance variables
        CMD - commad argument-parsing
        LOG - config file for log output
        CFGN - the dict format of command arguments
    '''
    def __init__(self):
        self.CMD  = _lnap.wConfigParse()
        self.LOG  = self.CMD.ARGS.log
        self.CFGN = self.__get_cfgn()
        
    def __get_cfgn(self):
        cmd = self.CMD
        if (not cmd.HAS_ARGS) and cmd.HAS_CFG:
            cfgn   = self.__get_cfgn_from_cfg(cmd.ARGS.cfg)
        else: cfgn = self.__get_cfgn_from_cmd(cmd.ARGS)
        
        self.__check_cfgn_if_valid(cfgn)
        return cfgn
        
    def __get_cfgn_from_cfg(self, cfg):
        with open(cfg, mode='r', encoding='utf-8') as f:
            try: return json.loads(f.read())
            except Exception as e: exit(f'{cfg}: {e}')
        
    def __get_cfgn_from_cmd(self, args):
        return args.__dict__
    
    @staticmethod
    def __check_cfgn_if_valid(cfgn):
        n_keys = {'ip'}
        if not n_keys < set(cfgn.keys()):
            exit(f"necessary fields {n_keys} not in {cfgn['cfg']}")
        # the other checks
    
    def get_url_comm_part(self):
        addr, port = self.CFGN['ip'], self.CFGN['port']
        if not any(prtcl in addr for prtcl in ['http://', 'https://']):
            addr = 'http://' + addr
        return '%s:%d' % (addr, port)
    
    def get_header(self):
        return self.CFGN['header']
    
    def get_request_showing_flag(self):
        return self.CFGN['req']
    
    def get_response_showing_flag(self):
        return self.CFGN['rep']
    
    def get_response_json_indent(self):
        return self.CFGN['jsi']

if __name__ == '__main__':
    ''' for testing ln_comm.py '''
    comm = Common()
    comm.LOG.write(f'{comm.CFGN}')
    comm.LOG.close()