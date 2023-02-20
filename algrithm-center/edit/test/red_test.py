import os
import time
import logging
import unittest
import analyze as aly
import cut
import choose
import render
from multiprocessing import Process

class RenderTest(unittest.TestCase):
    '''测试序列生成'''

    @classmethod
    def setUpClass(cls):
        pass

    def test1(self):
        template_path = 'test/templates/taobao-4'
        tshots = aly.load_shots(template_path)
        folder = 'test/videos/test-1'
        videos = aly.load_videos(folder, 4)
        shot_groups = cut.get_shot_groups(tshots, videos)
        shot_lines = choose.get_best_shot_lines(shot_groups)
        if shot_lines:
            best_shot_line = shot_lines[0]
            file_path = 'test/results/1.mp4'
            music_path = os.path.join(template_path, 'music.mp3')
            temp_folder = 'test/results'
            render.gen_shot_line_video(file_path, music_path, best_shot_line, temp_folder)

    def test2(self):
        template_path = 'test/templates/taobao-4'
        tshots = aly.load_shots(template_path)
        folder = 'test/videos/test-2'
        videos = aly.load_videos(folder, 4)
        shot_groups = cut.get_shot_groups(tshots, videos)
        shot_lines = choose.get_best_shot_lines(shot_groups)
        if shot_lines:
            best_shot_line = shot_lines[0]
            file_path = 'test/results/2.mp4'
            music_path = os.path.join(template_path, 'music.mp3')
            temp_folder = 'test/results'
            render.gen_shot_line_video(file_path, music_path, best_shot_line, temp_folder)

    def test3(self):
        template_path = 'test/templates/taobao-4'
        tshots = aly.load_shots(template_path)
        folder = 'test/videos/test-3'
        videos = aly.load_videos(folder, 4)
        shot_groups = cut.get_shot_groups(tshots, videos)
        shot_lines = choose.get_best_shot_lines(shot_groups)
        if shot_lines:
            best_shot_line = shot_lines[0]
            file_path = 'test/results/3.mp4'
            music_path = os.path.join(template_path, 'music.mp3')
            temp_folder = 'test/results'
            render.gen_shot_line_video(file_path, music_path, best_shot_line, temp_folder)

    def test4(self):
        template_path = 'test/templates/taobao-4'
        tshots = aly.load_shots(template_path)
        folder = 'test/videos/test-4'
        videos = aly.load_videos(folder, 4)
        shot_groups = cut.get_shot_groups(tshots, videos)
        shot_lines = choose.get_best_shot_lines(shot_groups)
        if shot_lines:
            best_shot_line = shot_lines[0]
            file_path = 'test/results/4.mp4'
            music_path = os.path.join(template_path, 'music.mp3')
            temp_folder = 'test/results'
            render.gen_shot_line_video(file_path, music_path, best_shot_line, temp_folder)

    @classmethod
    def tearDownClass(cls):
        pass