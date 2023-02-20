import os
import re
import time
import logging
import unittest
import preprocess as pp

class PreProcessTest(unittest.TestCase):
    '''测试视频预处理：转码、压缩等'''

    @classmethod
    def setUpClass(cls):
        '''清理文件夹下的多余文件'''
        # level = logging.getLevelName(logging.root.level)
        # print(level)
        folder = 'test/videos'
        folders = os.listdir(folder)
        for fd in folders:
            # 删除数据文件
            data_path = os.path.join(folder, fd, 'videos-v1.pkl')
            if os.path.exists(data_path):
                os.remove(data_path)
            # 删除预处理过的视频文件
            files = os.listdir(os.path.join(folder, fd))
            pattern = r'video-[A-Z0-9]{10}.mp4'
            regex = re.compile(pattern, flags=re.IGNORECASE)
            for file in files:
                if regex.match(file):
                    file_path = os.path.join(folder, fd, file)
                    os.remove(file_path)

    def test1(self):
        folder = 'test/videos/test-1'
        pp.all_steps(folder, pp.pp_videos)

    def test2(self):
        folder = 'test/videos/test-2'
        pp.all_steps(folder, pp.pp_videos)

    def test3(self):
        folder = 'test/videos/test-3'
        pp.all_steps(folder, pp.pp_videos)

    def test4(self):
        folder = 'test/videos/test-4'
        pp.all_steps(folder, pp.pp_videos)

    def test5(self):
        folder = 'test/videos/test-5'
        pp.all_steps(folder, pp.pp_videos)

    @classmethod
    def tearDownClass(cls):
        pass