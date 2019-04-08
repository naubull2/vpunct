# -*- coding: utf-8 -*-
from sanic import Sanic
from sanic import response
from sanic.exceptions import ServerError
import os
import argparse
import asyncio
import requests
import sys
import time
import json
import random
import logging
from urllib.parse import urlencode
from logging.handlers import RotatingFileHandler

from concurrent.futures import ThreadPoolExecutor

from configs import Config as cfg
from punctuate import qmark_restore

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

random.seed(time.time())

## Sanic app setting
app = Sanic('punctuate')
app.config.update(cfg.sanic_config)

if not os.path.exists(BASE_DIR + '/logs'):
    os.mkdir(BASE_DIR + '/logs')

## Log setting
logger = logging.getLogger('punctuation')
_FMT_STRING = '%(asctime)s - %(name)s(%(process)d) [%(levelname)s] %(module)s - %(message)s'
_FORMATTER = logging.Formatter(_FMT_STRING)
_HANDLER = RotatingFileHandler(BASE_DIR + '/logs/app.log',
                               maxBytes=26214400,
                               backupCount=5,
                               encoding='utf-8')
_HANDLER.setFormatter(_FORMATTER)
logger.setLevel(logging.DEBUG)
logger.addHandler(_HANDLER)


@app.route("/en/punctuation", methods=['GET', 'POST'])
async def punctuation(request):
    rst = dict()
    verbose = False
    if request.method == 'POST':
        raw_data = request.json
        msg = raw_data.get('userRequest', dict()).get('utterance', '')
        uid = raw_data.get('userRequest', dict()).get('user', dict()).get('id', 'test')
    else:
        msg = request.args.get('q', '')
        uid = request.args.get('uid', 'test')
        verbose = bool(request.args.get('verbose', ''))
    code = 200
    
    try:
        ret = qmark_restore(msg)
    except:
        code = 400
        ret = msg
    
    rst.update({'code': code, 'input': msg, 'output': ret}) 

    return response.json(rst)

# Health check
@app.route( '_hcheck.hdn' )
def dohealthcheck( request ):
    content = ""
    with open( BASE_DIR + "/data/_hcheck.hdn", "r" ) as content_file:
        content = content_file.read()
    return response.html( content )

# run server
@app.listener('before_server_start')
def before_start(app, loop):
    logger.warning( "STARTING SERVER" )

@app.listener('after_server_start')
def after_start(app, loop):
    logger.warning( "SERVER STARTED" )

@app.listener('before_server_stop')
def before_stop(app, loop):
    logger.warning( "STOPPING SERVER" )

@app.listener('after_server_stop')
def after_stop(app, loop):
    logger.warning( "SERVER STOPPED" )

# app crash exceptions
@app.exception(ServerError)
async def test_exception(request, exception):
    return response.json({"exception": "{}".format(exception), "status": exception.status_code}, status=exception.status_code)


if __name__ == '__main__':
    _PARSER = argparse.ArgumentParser(description='demo-punctuation')
    _PARSER.add_argument('--host', type=str, default="0.0.0.0", help="host")
    _PARSER.add_argument('--port', type=int, default=9965, help="port")
    _PARSER.add_argument('--worker', type=int, default=1, help="number of worker")
    _PARSER.add_argument('--mode', type=str, default="beta", help="deploy mode", choices=[ "sandbox", "beta", "stage", "real" ] )
    _PARSER.add_argument('--log', type=str, default=".", help="log location" )
    _ARGS = _PARSER.parse_args()

    app.run(host=_ARGS.host, port=_ARGS.port, workers=_ARGS.worker, debug=True)
