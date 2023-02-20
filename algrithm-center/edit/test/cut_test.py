import os
import time
import logging
import unittest
import analyze as aly
import cut
from multiprocessing import Process

class CutTest(unittest.TestCase):
    '''测试镜头生成'''

    @classmethod
    def setUpClass(cls):
        pass

    def test1(self):
        tshots = aly.load_shots('test/templates/taobao-0')
        folder = 'test/videos/test-1'
        videos = aly.load_videos(folder, 4)
        sgs = cut.get_shot_groups(tshots, videos)

    def test2(self):
        tshots = aly.load_shots('test/templates/taobao-0')
        folder = 'test/videos/test-2'
        videos = aly.load_videos(folder, 4)
        sgs = cut.get_shot_groups(tshots, videos)

    def test3(self):
        tshots = aly.load_shots('test/templates/taobao-0')
        folder = 'test/videos/test-3'
        videos = aly.load_videos(folder, 4)
        sgs = cut.get_shot_groups(tshots, videos)

    def test4(self):
        tshots = aly.load_shots('test/templates/taobao-0')
        folder = 'test/videos/test-4'
        videos = aly.load_videos(folder, 4)
        sgs = cut.get_shot_groups(tshots, videos)

    def test5(self):
        tshots = aly.load_shots('test/templates/taobao-0')
        folder = 'test/videos/test-5'
        videos = aly.load_videos(folder, 4)
        sgs = cut.get_shot_groups(tshots, videos)

    @classmethod
    def tearDownClass(cls):
        pass