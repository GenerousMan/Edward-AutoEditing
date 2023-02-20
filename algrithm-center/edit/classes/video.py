import os
import sys
sys.path.append('../')
import cv2
import shutil
import unittest
import skvideo.io
from tools.rid import get_random_id
from classes.frame import Frame

MAX_LENGTH = 1280

class Video:
    '''视频素材类
    '''

    def __init__(self, path, compress=False, template=False):
        self.path = path
        self.frames = []
        if os.path.exists(path):
            if template:
                self.name = os.path.split(self.path)[-1]
                self.check(compress)
            elif not self.check(compress):
                self.convert(compress)
            elif not template:
                self.rename()
            self.set_frame_count()
        else:
            raise IOError('Video path not exist: {}'.format(path))

    def check(self, compress=False):
        '''检查视频的格式和编码并保存信息'''
        postfix = self.path.split('.')[-1]
        name = os.path.split(self.path)[-1]
        metadata = skvideo.io.ffprobe(self.path)
        if 'video' in metadata:
            metadata = metadata['video']
            self.width = int((metadata['@width']))
            self.height = int((metadata['@height']))
            self.fps = int(round(eval(metadata['@avg_frame_rate'])))
            self.codec = metadata['@codec_name']
            print('[META] Scikit-Video {} {}x{} {}fps {}'.format(name, self.width, self.height, self.fps, self.codec))
        else:
            cap = cv2.VideoCapture(self.path)
            self.width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.fps = int(round(cap.get(cv2.CAP_PROP_FPS)))
            codec = int(cap.get(cv2.CAP_PROP_FOURCC))
            self.codec = 'h264' if codec == 828601953 else 'other'
            print('[META] OpenCV {} {}x{} {}fps {}'.format(name, self.width, self.height, self.fps, self.codec))
        if postfix != 'mp4' or self.codec != 'h264':
            return False
        elif compress and max(self.width, self.height) > MAX_LENGTH:
            return False
        else:
            return True

    def convert(self, compress=False):
        '''将视频转为mp4-h264编码格式，并删除原文件'''
        src = self.path
        folder = os.path.split(self.path)[0]
        self.name = get_random_id(10, prefix='video') + '.mp4'
        dst = os.path.join(folder, self.name)
        video_max_len = max(self.width, self.height)
        if compress and video_max_len > MAX_LENGTH:
            # 进行尺寸压缩
            if self.width == video_max_len:
                self.height = int(round(self.height * (MAX_LENGTH / self.width)))
                self.height = self.height if self.height % 2 == 0 else self.height + 1
                self.width = MAX_LENGTH
            elif self.height == video_max_len:
                self.width = int(round(self.width * (MAX_LENGTH / self.height)))
                self.width = self.width if self.width % 2 == 0 else self.width + 1
                self.height = MAX_LENGTH
        cmd = "ffmpeg -i {} -s {}x{} -r {} -vcodec libx264 -preset veryfast {}".format(src, self.width, self.height, self.fps, dst)
        print(cmd)
        ret = os.system(cmd)
        self.path = dst
        if ret == 0:
            # os.remove(src)
            pass
        else:
            raise IOError('FFmpeg convert failed', src)

    def rename(self):
        src = self.path
        folder = os.path.split(self.path)[0]
        self.name = get_random_id(10, prefix='video') + '.mp4'
        dst = os.path.join(folder, self.name)
        # os.rename(src, dst)
        shutil.copy(src, dst)
        self.path = dst

    def set_frame_count(self):
        if os.path.exists(self.path):
            metadata = skvideo.io.ffprobe(self.path)
            if 'video' in metadata:
                self.frame_count = int(metadata['video']['@nb_frames'])
            else:
                # 视频内容/格式错误
                print('[Error] C:Video Content/Format', os.path.split(self.path)[-1])
                raise IOError('Wrong Content/Format', 'C:Video', os.path.split(self.path)[-1])
        else:
            # 文件不存在
            print('[Error] C:Video File not exist', os.path.split(self.path)[-1])
            raise IOError('File not exist', 'C:Video', os.path.split(self.path)[-1])

    def init_frames(self, sample_time_interval):
        self.sample_time_interval = sample_time_interval
        frame_interval = self.fps * sample_time_interval
        frame_interval = frame_interval if frame_interval >= 1 else 1
        frame_number = 0
        while int(round(frame_number)) < self.frame_count:
            frame = Frame(int(round(frame_number)))
            self.frames.append(frame)
            frame_number += frame_interval

    def __eq__(self, other):
        return self.path == other.path

    def __str__(self):
        return '[Video] {} {}x{} {}fps {}fs'.format(self.name, self.width, self.height, self.fps, self.frame_count)

class TestFunc(unittest.TestCase):

    def test1(self):
        video_path = '../del_aft_test/0.mp4'
        video = Video(video_path)

    def test2(self):
        video_path = '../del_aft_test/test1.mp4'
        video = Video(video_path)

    def test3(self):
        video_path = '../del_aft_test/zaimnotgrv.mp4'
        video = Video(video_path)

    def test4(self):
        video_path = '../del_aft_test/lxhzj.flv'
        video = Video(video_path)

if __name__ == "__main__":
    unittest.main()