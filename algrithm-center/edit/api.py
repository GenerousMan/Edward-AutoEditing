'''平台需要的二次开发API'''

import os
import uuid
import shutil
import random
import preprocess as pp
import analyze as aly
import search
import cut
import choose
import render
from tools import progress
from tools import match_results
from tools import example as exple
from classes.editor_project import EditorProject

def get_random_id(length):
    alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return ''.join(random.sample(alphabet, length))

def move_upload_videos(upload_path, save_path, filenames):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    for filename in filenames:
        source = upload_path + filename
        target = save_path + filename
        shutil.move(source, target)

def init_progress(taskId):
    progress.init_(taskId)

def calc_videos_data(save_path, taskId):
    '''完成上传视频的所有预处理过程，转码，特征计算等'''
    videos = pp.pp_videos(save_path, taskId)
    pp.save_videos(save_path, videos)
    sample_time_interval = 0.125
    aly.all_steps(save_path, sample_time_interval, taskId)

def get_match_results(save_path, template_root, templates, taskId):
    save_shot_lines = []
    videos = aly.load_videos(save_path, 4)
    data_len = len(templates)
    for i, template_name in enumerate(templates):
        template_path = os.path.join(template_root, template_name)
        print('template_path:', template_path)
        tshots = aly.load_shots(template_path)
        shot_groups = cut.get_shot_groups(tshots, videos)
        shot_lines = choose.get_best_shot_lines(shot_groups)
        if len(shot_lines) > 0:
            shot_lines[0].template_path = template_name
            result_name = str(uuid.uuid4()) + '.mp4'
            shot_lines[0].result_name = result_name
            shot_lines[0].saveThumbnails()
            save_shot_lines.append((shot_lines[0], shot_groups))
        if taskId: progress.set_(taskId, 'match', i + 1, data_len)
    save_shot_lines = sorted(
        save_shot_lines, key=lambda x: x[0].simi, reverse=True)
    if len(save_shot_lines) > 10:
        save_shot_lines = save_shot_lines[:10]
    if taskId: match_results.save(taskId, save_shot_lines)
    print('save_shot_lines:', len(save_shot_lines))
    return save_shot_lines

def generate_shot_line_videos(shot_lines, taskId, compress=False):
    data_len = len(shot_lines)
    for i, shot_line in enumerate(shot_lines):
        template_name = shot_line[0].template_path
        result_name = shot_line[0].result_name
        file_path = '../api-center/public/tempoFiles/videos/' + result_name
        music_path = '../templates/' + template_name + '/music.mp3'
        # get_cut_shot_line_video(file_path, music_path, cut_shot_line[0])
        render.gen_shot_line_video(file_path, music_path, shot_line[0], compress)
        if taskId: progress.set_(taskId, 'render', i + 1, data_len)

def begin_preprocess(save_path, filter, lock, taskId):
    '''完成大部分需要预计算的内容：预处理、匹配、生成等'''
    print('Begin process:', save_path)

    # 转码、特征计算
    lock.acquire()
    try:
        print('Get lock.')
        calc_videos_data(save_path, taskId)
    finally:
        print('Release lock.')
        lock.release()

    # 案例库匹配
    template_root = '../templates/'
    templates = os.listdir(template_root)
    if filter:
        # 使用限定的案例集
        filter = [t.strip() for t in filter.split(',') if t.strip() != '']
        templates = [folder for folder in templates if os.path.isdir(os.path.join(template_root, folder)) and folder in filter]
    else:
        # 进行案例集搜索
        templates = random.sample(templates, 4)
        _, _, _, templates = search.template_search(templates, save_path, box=4, step=6, pb=True)

    shot_lines = get_match_results(save_path, template_root, templates, taskId)

    # 生成预览视频
    generate_shot_line_videos(shot_lines, taskId, compress=False)

    results = []

    # 保存结果数据到数据库里
    for sl, sgs in shot_lines:
        data = sl.get_match_data()
        results.append(data)

    exple.save_results(taskId, results)

def generate_shot_line_video(taskId, resultId, template):
    shot_lines = match_results.load(taskId)
    file_path = '../api-center/public/tempoFiles/videos/' + resultId + '.mp4'
    music_path = '../templates/' + template + '/music.mp3'
    for sl, sgs in shot_lines:
        if sl.template_path == template:
            render.gen_shot_line_video(file_path, music_path, sl)
            break

def create_project(taskId, template, projectId):
    save_shot_lines = match_results.load(taskId)
    for ssl in save_shot_lines:
        sl = ssl[0]
        sgs = ssl[1]
        if sl.template_path == template:
            print(template)
            project = EditorProject(taskId, projectId, template, sl, sgs)
            project.generate_temp_files()
            EditorProject.save_project(project, taskId, projectId)
            break

def get_project_info(taskId, projectId):
    project = EditorProject.load_project(taskId, projectId)
    projectInfo = project.get_project_info()
    return projectInfo

def save_project_info(taskId, projectId, projectInfo):
    project = EditorProject.load_project(taskId, projectId)
    project.update_project_info(projectInfo)
    EditorProject.save_project(project, taskId, projectId)

def get_project_preview(taskId, projectId):
    project = EditorProject.load_project(taskId, projectId)
    video = project.get_project_preview()
    return video

def get_project_result(taskId, projectId):
    project = EditorProject.load_project(taskId, projectId)
    resultId = project.get_project_result()
    return resultId

def pp_example(folder):
    pp.all_steps(folder, pp.pp_videos)
    aly.all_steps(folder, sample_time_interval=0.125)

def load_examples():
    examples_folder = '../examples'
    public_folder = '../api-center/public/examples'
    folders = os.listdir(examples_folder)
    for folder in folders:
        folder_path = os.path.join(examples_folder, folder)
        if os.path.isdir(folder_path):
            # check status of folder
            data_path = os.path.join(folder_path, 'videos-v4.pkl')
            if not os.path.exists(data_path):
                print('Error!!!!')
            # load videos
            videos = aly.load_videos(folder_path, 4)
            example = {'name':folder, 'videos':[]}
            for video in videos:
                name = video.name
                duration = int(video.frame_count / video.fps)
                url = '/examples/{}/{}'.format(folder, video.name)
                example['videos'].append({'name':name, 'dura':duration, 'url':url})
            exple.init_(example)
            # clear the folder
            public_example_path = os.path.join(public_folder, folder)
            if os.path.exists(public_example_path) and os.path.isdir(public_example_path):
                shutil.rmtree(public_example_path)
            if not os.path.exists(public_example_path):
                os.mkdir(public_example_path)
            # copy video file to public folder
            for video in videos:
                source = os.path.join(folder_path, video.name)
                target = os.path.join(public_example_path, video.name)
                shutil.copy(source, target)

def copy_example_videos(name, videos, selected, save_path):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    folder_path = os.path.join('../examples', name)
    videos = aly.load_videos(folder_path, 4)
    selected_names = [video['name'] for video in selected]
    selected_videos = []
    for video in videos:
        if video.name in selected_names:
            source = os.path.join(folder_path, video.name)
            target = os.path.join(save_path, video.name)
            shutil.copy(source, target)
            video.path = target
            selected_videos.append(video)
    aly.save_videos(save_path, selected_videos, 4)

def init_example_progress(taskId):
    progress.init_(taskId)
    dones = ['trans', 'yolo', 'alphapose', 'features']
    for item in dones:
        progress.set_(taskId, item, 1, 1)

def begin_example_process(save_path, filter, taskId):
    '''完成大部分需要预计算的内容：预处理、匹配、生成等'''
    print('Begin process:', save_path)

    # 案例库匹配
    template_root = '../templates/'
    templates = os.listdir(template_root)

    if filter:
        # 使用限定的案例集
        filter = [t.strip() for t in filter.split(',') if t.strip() != '']
        templates = [folder for folder in templates if os.path.isdir(os.path.join(template_root, folder)) and folder in filter]
    else:
        # 进行案例集搜索
        templates = random.sample(templates, 4)
        _, _, _, templates = search.template_search(templates, save_path, box=4, step=6, pb=True)

    shot_lines = get_match_results(save_path, template_root, templates, taskId)

    # 生成预览视频
    generate_shot_line_videos(shot_lines, taskId, False)

    results = []

    # 保存结果数据到数据库里
    for sl, sgs in shot_lines:
        data = sl.get_match_data()
        results.append(data)

    exple.save_results(taskId, results)