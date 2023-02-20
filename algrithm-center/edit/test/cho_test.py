import os
import time
import logging
import unittest
import analyze as aly
import cut
import choose
from multiprocessing import Process

class ChooseTest(unittest.TestCase):
    '''测试序列生成'''

    @classmethod
    def setUpClass(cls):
        pass

    def test1(self):
        tshots = aly.load_shots('test/templates/taobao-0')
        folder = 'test/videos/test-1'
        videos = aly.load_videos(folder, 4)
        shot_groups = cut.get_shot_groups(tshots, videos)
        shot_lines = choose.get_best_shot_lines(shot_groups)

    def test2(self):
        tshots = aly.load_shots('test/templates/taobao-0')
        folder = 'test/videos/test-2'
        videos = aly.load_videos(folder, 4)
        shot_groups = cut.get_shot_groups(tshots, videos)
        shot_lines = choose.get_best_shot_lines(shot_groups)

    def test3(self):
        tshots = aly.load_shots('test/templates/taobao-0')
        folder = 'test/videos/test-3'
        videos = aly.load_videos(folder, 4)
        shot_groups = cut.get_shot_groups(tshots, videos)
        shot_lines = choose.get_best_shot_lines(shot_groups)

    def test4(self):
        tshots = aly.load_shots('test/templates/taobao-0')
        folder = 'test/videos/test-4'
        videos = aly.load_videos(folder, 4)
        shot_groups = cut.get_shot_groups(tshots, videos)
        shot_lines = choose.get_best_shot_lines(shot_groups)

    def test5(self):
        tshots = aly.load_shots('test/templates/taobao-0')
        folder = 'test/videos/test-5'
        videos = aly.load_videos(folder, 4)
        shot_groups = cut.get_shot_groups(tshots, videos)
        shot_lines = choose.get_best_shot_lines(shot_groups)

    def test6(self):
        template_path = 'test/templates/taobao-0'
        videos_path = 'test/videos/test-1'
        videos = aly.load_videos(videos_path, 4)
        choose.approx_simi(template_path, videos_path, videos)
        choose.accuri_simi(template_path, videos_path, videos)

    @classmethod
    def tearDownClass(cls):
        pass