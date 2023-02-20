import os
from flask import Blueprint
from flask import request
from multiprocessing import Process, Lock
from edit import api
import locks

exh = exhibit = Blueprint('exhibit', __name__)

@exh.route('/select-begin', methods=['POST'])
def select_begin():
    ''' 将用户上传的素材从upload_path中复制到save_pth=upload_path/match_id中
        在save_pth遍历处理所有素材，将同名的data文件也储存在save_pth
        返回该次匹配请求的match_id
    '''
    data = request.json
    name = data.get('name')
    videos = data.get('videos')
    selected = data.get('selected')

    # 生成随机任务Id
    taskId = api.get_random_id(8)

    # 拷贝视频到任务文件夹下
    save_path = '../uploads/' + taskId + '/'
    api.copy_example_videos(name, videos, selected, save_path)

    # 初始化进度
    api.init_example_progress(taskId)

    # 开始计算
    p = Process(target=api.begin_example_process, args=(save_path, None, taskId))
    p.start()

    return {
        "taskId": taskId
    }

@exh.route('/upload-begin', methods=['POST'])
def upload_begin():
    ''' 将用户上传的素材从upload_path中复制到save_pth=upload_path/match_id中
        在save_pth遍历处理所有素材，将同名的data文件也储存在save_pth
        返回该次匹配请求的match_id
    '''
    data = request.json
    filenames = data.get('filenames')
    filter = data.get('filter')

    # 生成随机任务Id
    taskId = api.get_random_id(8)

    # 拷贝视频到任务文件夹下
    upload_path = '../uploads/'
    save_path = '../uploads/' + taskId + '/'
    api.move_upload_videos(upload_path, save_path, filenames)

    # 初始化进度
    api.init_progress(taskId)

    p = Process(target=api.begin_preprocess, args=(save_path, filter, locks.get_gpu_lock(), taskId,))
    p.start()

    return {
        "taskId": taskId
    }