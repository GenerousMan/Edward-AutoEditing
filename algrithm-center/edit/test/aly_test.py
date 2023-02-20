import os
import time
import logging
import unittest
import analyze as aly
from multiprocessing import Process

class AnalyzeTest(unittest.TestCase):
    '''测试视频特征提取：YOLO Alphapose等'''

    @classmethod
    def setUpClass(cls):
        '''清理文件夹下的多余文件'''
        # level = logging.getLevelName(logging.root.level)
        # print(level)
        folder = 'test/videos'
        folders = os.listdir(folder)
        for fd in folders:
            # 删除数据文件
            for i in range(2, 5):
                data_path = os.path.join(folder, fd, 'videos-v{}.pkl'.format(i))
                if os.path.exists(data_path):
                    os.remove(data_path)

    def test1(self):
        folder = 'test/videos/test-1'
        p = Process(target=aly.all_steps, args=(folder, 0.125))
        p.start()
        p.join()
        time.sleep(5)

    def test2(self):
        folder = 'test/videos/test-2'
        p = Process(target=aly.all_steps, args=(folder, 0.125))
        p.start()
        p.join()
        time.sleep(5)

    def test3(self):
        folder = 'test/videos/test-3'
        p = Process(target=aly.all_steps, args=(folder, 0.125))
        p.start()
        p.join()
        time.sleep(5)

    def test4(self):
        folder = 'test/videos/test-4'
        p = Process(target=aly.all_steps, args=(folder, 0.125))
        p.start()
        p.join()
        time.sleep(5)

    def test5(self):
        folder = 'test/videos/test-5'
        p = Process(target=aly.all_steps, args=(folder, 0.125))
        p.start()
        p.join()
        time.sleep(5)

    @classmethod
    def tearDownClass(cls):
        pass