import os
import datetime
from flask import Blueprint
from flask import request
# from flask import g
from multiprocessing import Process
from edit import api
import locks

vca = video_cloth_ads = Blueprint('video_cloth_ads', __name__)

# gpu_lock = locks.get_gpu_lock()

@vca.route('/preprocess', methods=['POST'])
def preprocess():
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

@vca.route('/generate-video', methods=['POST'])
def generate_video():
    data = request.json
    taskId = data.get('taskId')
    template = data.get('template')
    resultId = api.get_random_id(8)
    api.generate_shot_line_video(taskId, resultId, template)
    return {
        "taskId": taskId,
        "resultId": resultId
    }

@vca.route('/create-project', methods=['POST'])
def create_project():
    data = request.json
    taskId = data.get('taskId')
    template = data.get('template')
    projectId = api.get_random_id(8)
    api.create_project(taskId, template, projectId)
    return {
        "taskId": taskId,
        "projectId": projectId
    }

@vca.route('/get-project-info', methods=['POST'])
def get_project_info():
    data = request.json
    taskId = data.get('taskId')
    projectId = data.get('projectId')
    projectInfo = api.get_project_info(taskId, projectId)
    return projectInfo

@vca.route('/save-project-info', methods=['POST'])
def save_project_info():
    data = request.json
    taskId = data.get('taskId')
    projectId = data.get('projectId')
    projectInfo = data.get('projectInfo')
    api.save_project_info(taskId, projectId, projectInfo)
    return {
        "taskId": taskId,
        "projectId": projectId
    }

@vca.route('/get-project-preview', methods=['POST'])
def get_project_preview():
    data = request.json
    taskId = data.get('taskId')
    projectId = data.get('projectId')
    projectInfo = data.get('projectInfo')
    api.save_project_info(taskId, projectId, projectInfo)
    video = api.get_project_preview(taskId, projectId)
    return {
        "taskId": taskId,
        "projectId": projectId,
        "video": video
    }

@vca.route('/save-and-generate', methods=['POST'])
def save_and_generate():
    data = request.json
    taskId = data.get('taskId')
    projectId = data.get('projectId')
    projectInfo = data.get('projectInfo')
    api.save_project_info(taskId, projectId, projectInfo)
    resultId = api.get_project_result(taskId, projectId)
    return {
        "taskId": taskId,
        "projectId": projectId,
        "resultId": resultId
    }
