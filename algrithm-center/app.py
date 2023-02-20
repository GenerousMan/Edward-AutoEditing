import os
import logging
import warnings
import sys
sys.path.append('edit')
# import time
# import random
# import pickle
# import sys
# import multiprocessing
from flask import Flask
from edit.api import load_examples
from routes.video_cloth_ads import video_cloth_ads
from routes.exhibit import exhibit

import locks

def run_algrithm_center(host, port, debug):

    logging.basicConfig(level=logging.ERROR)
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    warnings.simplefilter('ignore')

    os.environ['CUDA_VISIBLE_DEVICES'] = '2'
    # os.environ['CUDA_VISIBLE_DEVICES'] = '0'

    locks.init_()

    app = Flask(__name__)
    app.register_blueprint(video_cloth_ads, url_prefix='/video-cloth-ads')
    app.register_blueprint(exhibit, url_prefix='/exhibit')

    app.run(host=host, port=port, threaded=True, debug=debug)

if __name__ == '__main__':
    # load_examples()
    run_algrithm_center('127.0.0.1', 5050, True)