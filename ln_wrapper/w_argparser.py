#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
w_argparser.py,
routines for wrapping argparse library 
to parse configurations from command or 
config file.

lxr, 2020.02
"""

import argparse
import os, sys, json

class wConfigParse():
    ''' to parse configurations by argparse module.
        instance variables PARSER, ARGS, HAS_CFG, 
        HAS_ARGS, can be used directlly by outside. '''
    def __init__(self):
        self.HAS_CFG  = False
        self.HAS_ARGS = False
        self.PARSER   = self.ARGS = None
        
        parser = self.__create_cmdarg_parser()
        self.__add_optargs(parser)
        
        args = self.__parse_cmdargs(parser)
        self.__default_configurations(args)
        self.__update_cfg_depend_on_user(args)
        self.__tips_for_logs_output_file(args)
        
        self.ARGS   = args
        self.PARSER = parser
        
    def __create_cmdarg_parser(self):
        ARGS = argparse.ArgumentParser(
            description = self._desc   + '-' * len(self._desc),
            epilog      = self._epilog + '-' * len(self._epilog),
            formatter_class = argparse.RawTextHelpFormatter)
        return ARGS
    
    def __add_optargs(self, parser):
        self.__add_version_optarg(parser)
        self.__add_server_optargs(parser)
        self.__add_cfg_optargs(parser)
        self.__add_log_optargs(parser)
        self.__add_default_optargs(parser)
        
    def __add_version_optarg(self, parser):
        parser.add_argument('-v', '--version',
                action  = 'version',
                version = f'{sys.argv[0]} 0.1.1' )
    
    def __add_server_optargs(self, parser):
        group = parser.add_argument_group(self._optarg_desc['server'])
        group.add_argument('-s',
                metavar = '  IP',
                dest    = 'ip', 
                type    = str,
                default = self._default_cfg['ip'],
                help    = self._help['ip'] )
        group.add_argument('-p',
                metavar = '  PORT',
                dest    = 'port',
                type    = int,
                default = self._default_cfg['port'],
                help    = self._help['port'] )
        group.add_argument('-hdr',
                metavar = 'HEADER',
                dest    = 'header',
                type    = str,
                default = self._default_cfg['header'],
                help    = self._help['header'])

    def __add_log_optargs(self, parser):
        def str2bool(_str):
            return True if _str.lower() not in ['flase', '0'] else False
        group = parser.add_argument_group(self._optarg_desc['log'])
        group.add_argument('-req', 
                metavar = '0/1',
                dest    = 'req',
                type    = str2bool,
                default = self._default_cfg['req'],
                help    = self._help['req'] )
        group.add_argument('-rep', 
                metavar = '0/1',
                dest    = 'rep',
                type    = str2bool,
                default = self._default_cfg['rep'],
                help    = self._help['rep'] )
        group.add_argument('-jsi', 
                metavar = 'NR',
                dest    = 'jsi',
                type    = int,
                default = self._default_cfg['jsi'],
                choices = range(1, 8),
                help    = self._help['jsi'] )
        group.add_argument('--log',
                metavar = 'LOGFILE',
                type    = argparse.FileType('w', encoding='UTF-8'),
                default = self._default_cfg['log'],
                help    = self._help['log'] )
    
    def __add_cfg_optargs(self, parser):
        group = parser.add_argument_group(self._optarg_desc['cfg'])
        group.add_argument('--cfg',
                metavar = 'CONFIGFILE',
                type    = str,
                default = self._default_cfg['cfg'],
                help    = self._help['cfg'])
    
    def __add_default_optargs(self, parser):
        group = parser.add_argument_group(self._optarg_desc['dft'])
        group.add_argument('-dft', '--default',
                action = 'store_true',
                help   = self._help['dft'])
        
    def __parse_cmdargs(self, parser):
        try: return parser.parse_args()
        except IOError as e: exit(e)
    
    def __tips_for_logs_output_file(self, args):
        nlogf = args.__dict__['log'].name
        dlogf = self._default_cfg['log'].name
        if nlogf != dlogf:
            tips = f"\nplease check the * {nlogf} * to see logs"
            print(tips, '-' * len(tips), sep='\n')
    
    def __default_configurations(self, args):
        if args.default:
            cfg_dict = self._default_cfg.copy()
            cfg_dict['log'] = self._default_cfg['log'].name
            print(json.dumps(cfg_dict, indent=4))
            tips = 'the default configurations here you are\n'
            exit(tips + '-' * len(tips)) if 2 == len(sys.argv) else None
            
    def __update_cfg_depend_on_user(self, args):
        if 1 < len(sys.argv): 
            self.HAS_ARGS = True
            yon = input(f'update the command arguments'
                + f' to the * {args.cfg} * (y/n)?')
            if yon.lower() in ('y', 'yes'): 
                self.__update_cfg(args.cfg, args.__dict__)
        
        if os.path.exists(args.cfg):
            self.HAS_CFG = True
        
    def __update_cfg(self, cfg, cfg_v):
        v = cfg_v.copy();v['log'] = cfg_v['log'].name
        with open(cfg, mode='w', encoding='utf-8') as f:
            try: f.write(json.dumps(v, indent=4))
            except Exception as e: exit(e)
        print(f"the command arguments have been"
            f" updated to the * {cfg_v['cfg']} *")
    
    ''' the default configurations of server '''
    _default_cfg = {
        'ip': 'api.heclouds.com',
        'port': 80,
        'header': None,
        
        'req': True,
        'rep': False,
        'jsi': 1,
        'log': sys.stdout,
        'cfg': 'httpApiTest_config.json'
    }
    
    _help = {
        'ip':     "set API-server's     ip to be IP",
        'port':   "set API-server's   port to be PORT",
        'header': "set API-server's header to be HEADER",
        
        'req': 'set flag decides whether to show requests',
        'rep': 'set flag decides whether to show responses',
        'jsi': 'set NR-indent for json format responses',
        
        'log': 'set logs output to LOGFILE',
        'cfg': 'set config file to be CONFIGFILE',
        'dft': 'show the default configurations',
    }
    
    _optarg_desc = {
        'server': 'optional arguments on HTTP-API server',
        'log':    'optional arguments on log',
        'cfg':    'optional arguments on config file',
        'dft':    'optional arguments on default',
    }
    
    _desc = f'{sys.argv[0]}  arguments manual\n'
    _epilog = 'those arguments can be configured in CONFIGFILE statically too\n'


if __name__ == '__main__':
    ''' for testing w_argparser.py '''
    args = wConfigParse()
    args.ARGS.log.write(f'{args.ARGS.__dict__}')
    args.ARGS.log.close()