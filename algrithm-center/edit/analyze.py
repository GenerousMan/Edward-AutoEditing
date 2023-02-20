'''特征提取模块

特征提取模块主要负责提取输入素材的特征，
YOLO、AlphaPose、镜头语义识别等等。
'''
import os
import time
import pickle
import preprocess as pp
from tools import progress
from multiprocessing import Process, Manager
from classes.tshot import TShot
from numba import cuda

def save_videos(folder, videos, version):
    # 整体存储
    path = os.path.join(folder, 'videos-v{}.pkl'.format(version))
    f = open(path, 'wb')
    pickle.dump(videos, f)
    f.close()

def load_videos(folder, version):
    path = os.path.join(folder, 'videos-v{}.pkl'.format(version))
    with open(path, 'rb') as f:
        return pickle.load(f)
    raise IOError('No Video Data File', folder)

def init_video_frames(videos, sample_time_interval):
    for video in videos:
        video.init_frames(sample_time_interval)

def calc_roi(videos, folder, taskId=None):
    from tools.yolo import calc_roi_of_videos
    calc_roi_of_videos(videos, taskId)
    save_videos(folder, videos, 2)
    # cuda.select_device(0) # 选择GPU设备
    # cuda.close() # 释放GPU资源

def calc_alphapose(videos, folder, taskId=None):
    from tools.alphapose import calc_pose_of_videos_v2
    calc_pose_of_videos_v2(videos, taskId)
    save_videos(folder, videos, 3)
    # cuda.select_device(0) # 选择GPU设备
    # cuda.close() # 释放GPU资源

def combine_roi_pose(videos):
    from tools.alphapose import get_pose_roi_data
    for video in videos:
        for frame in video.frames:
            pose = frame.alphapose
            roi = frame.roi
            frame.comb_data = get_pose_roi_data(pose, roi)

def calc_features(videos, taskId=None):
    from tools.feature import calc_view_of_videos
    calc_view_of_videos(videos)
    if taskId: progress.set_(taskId, 'features', 25, 100)
    from tools.feature import calc_direction_of_videos
    calc_direction_of_videos(videos)
    if taskId: progress.set_(taskId, 'features', 50, 100)
    from tools.feature import calc_pose_of_videos
    calc_pose_of_videos(videos, 6)
    if taskId: progress.set_(taskId, 'features', 75, 100)
    from tools.feature import calc_motion_of_videos
    calc_motion_of_videos(videos, 4)
    if taskId: progress.set_(taskId, 'features', 100, 100)

def all_steps(folder, sample_time_interval, taskId=None):
    start = time.time()
    videos = pp.load_videos(folder)
    init_video_frames(videos, sample_time_interval)
    for video in videos:
        print('[Anal]', video.name, len(video.frames))
    p = Process(target=calc_roi, args=(videos, folder, taskId))
    p.start()
    p.join()
    videos = load_videos(folder, 2)
    p = Process(target=calc_alphapose, args=(videos, folder, taskId))
    p.start()
    p.join()
    videos = load_videos(folder, 3)
    combine_roi_pose(videos)
    calc_features(videos, taskId)

    for video in videos:
        print(video.name)
        view = [frame.view for frame in video.frames]
        direction = [frame.direction for frame in video.frames]
        pose = [frame.pose for frame in video.frames]
        motion = [frame.motion for frame in video.frames]
        print('view', view)
        # view_label_index = {"full-shot":0, "whole-body":1, "above-knee":2, "upper-body":3, "lower-body":4, "upper-cloth":5, "portrait":6, "waist":7, "detail":8, "scene":9}
        # 可以增加对view的众数滤波
        print('direction', direction)
        # direction_label_index = {"left":0, "half-left":1, "center":2, "half-right":3, "right":4, "back":5, "none":6}
        # 可以增加对direction的众数滤波
        print('pose', pose)
        # 可以增加对pose的众数滤波
        # pose_dict = {'stand': 0,'sit': 1,'walk': 2,'spin': 3,'none': 4 }
        print('motion', motion)

    save_videos(folder, videos, 4)
    end = time.time()
    print('[Anal] Cost:', end - start)

def save_shots(folder, shots):
    # 整体存储
    path = os.path.join(folder, 'shots.pkl')
    # with open(path, 'wb') as f:
    #     pickle.dump(shots, f)
    f = open(path, 'wb')
    pickle.dump(shots, f)
    f.close()

def load_shots(folder):
    path = os.path.join(folder, 'shots.pkl')
    with open(path, 'rb') as f:
        return pickle.load(f)
    raise IOError('No Shot Data File', folder)

def tempalte_all_steps(folder, sample_time_interval):
    # p = Process(target=all_steps, args=(folder, sample_time_interval))
    # p.start()
    # p.join()
    pp.all_steps(folder, pp.pp_template_videos)
    all_steps(folder, sample_time_interval)
    videos = load_videos(folder, 4)
    tshots = []
    for video in videos:
        tshot = TShot(video)
        tshots.append(tshot)
    save_shots(folder, tshots)

if __name__ == "__main__":
    # folder = 'del_aft_test'
    sample_time_interval = 0.125
    # all_steps(folder, sample_time_interval)
    # all_steps('uploads/videos/compare-1', sample_time_interval)
    # p = Process(target=tempalte_all_steps, args=('new_templates/taobao-0', sample_time_interval))
    # p.start()
    # p.join()
    # p = Process(target=tempalte_all_steps, args=('new_templates/taobao-2', sample_time_interval))
    # p.start()
    # p.join()
    # p = Process(target=tempalte_all_steps, args=('new_templates/taobao-3', sample_time_interval))
    # p.start()
    # p.join()
    # p = Process(target=tempalte_all_steps, args=('new_templates/taobao-4', sample_time_interval))
    # p.start()
    # p.join()
    templates_folder = 'templates'
    tempaltes = os.listdir(templates_folder)
    tempaltes = sorted(tempaltes, key=lambda f: int(f.split('-')[-1]))
    start = 327
    end = 787
    for template in tempaltes:
        index = int(template.split('-')[-1])
        if start <= index < end:
            folder_path = os.path.join(templates_folder, template)
            p = Process(target=tempalte_all_steps, args=(folder_path, sample_time_interval))
            p.start()
            p.join()