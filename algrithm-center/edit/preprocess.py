'''素材预处理模块

素材预处理模块主要负责对输入素材进行规范化，
通常会进行格式转码，大小压缩等操作，提取出素材对象。
'''

import os
import time
import pickle
import unittest
from classes.video import Video
from tools import progress

def pp_videos(folder, taskId=None):
    '''预处理文件夹下的所有视频，返回所有视频对象'''
    files = os.listdir(folder)
    video_files = [file for file in files if file.lower().endswith(('.mp4', '.flv', '.avi', '.mkv', '.wmv', '.rmvb'))]
    videos = []
    for i, file in enumerate(video_files):
        path = os.path.join(folder, file)
        videos.append(Video(path, compress=True))
        if taskId: progress.set_(taskId, 'trans', i + 1, len(video_files))
    return videos

def pp_template_videos(folder):
    folder = os.path.join(folder, 'shots')
    files = os.listdir(folder)
    video_files = [file for file in files if file.lower().endswith(('.mp4', '.flv', '.avi', '.mkv', '.wmv', '.rmvb'))]
    video_files = sorted(video_files, key=lambda file: int(file[:-4]))
    videos = []
    for file in video_files:
        path = os.path.join(folder, file)
        videos.append(Video(path, template=True))
    return videos

def save_videos(folder, videos):
    path = os.path.join(folder, 'videos-v1.pkl')
    # with open(path, 'wb') as f:
    #     pickle.dump(videos, f)
    f = open(path, 'wb')
    pickle.dump(videos, f)
    f.close()

def load_videos(folder):
    path = os.path.join(folder, 'videos-v1.pkl')
    with open(path, 'rb') as f:
        videos = pickle.load(f)
        return videos

def all_steps(folder, pp_func):
    start = time.time()
    videos = pp_func(folder)
    for video in videos:
        print('[PreP]', video)
    end = time.time()
    save_videos(folder, videos)
    print('[PreP] Cost:', end - start)

if __name__ == "__main__":
    # folder = 'del_aft_test'
    # all_steps(folder, pp_videos)
    # all_steps('new_templates/taobao-0', pp_template_videos)
    # all_steps('new_templates/taobao-2', pp_template_videos)
    # all_steps('new_templates/taobao-3', pp_template_videos)
    # all_steps('new_templates/taobao-4', pp_template_videos)
    all_steps('uploads/videos/compare-1', pp_videos)