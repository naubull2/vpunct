# -*- coding: utf-8 -*-
import os

class Config:
    home_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    sanic_config = {
        'KEEP_ALIVE_TIMEOUT': 10 
    }

