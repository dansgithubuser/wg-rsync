#!/usr/bin/env python3

import atexit
import json
import os
import subprocess

DIR = os.path.dirname(os.path.realpath(__file__))

os.chdir(DIR)

def invoke(invocation, check=True, **kwargs):
    p = subprocess.run(invocation.split(), **kwargs)
    print(invocation, '✅' if p.returncode == 0 else '❌', p.returncode)
    if check and p.returncode:
        raise Exception(f'`{invocation}` failed, exit code {p.returncode}')
    return p

with open('config.json') as f:
    config = json.load(f)
invoke(config['wg_up_cmd'])
atexit.register(lambda: invoke(config['wg_down_cmd']))
for rsync in config['rsyncs']:
    src_path = rsync['src_path']
    user = rsync['user']
    hostname = rsync['hostname']
    dst_path = rsync['dst_path']
    invoke(f'rsync -r {src_path} {user}@{hostname}:{dst_path}', check=False)
