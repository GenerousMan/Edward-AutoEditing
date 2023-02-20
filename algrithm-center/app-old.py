from flask import Flask
from flask import request
import time
import random
import pickle
from werkzeug.contrib.cache import SimpleCache
from multiprocessing import Process, Lock

app = Flask(__name__)
cache = SimpleCache()
uploads_folder = '../uploads/'

# import os
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
# os.environ['CUDA_VISIBLE_DEVICES'] = '0,1,2,3'

# 使用GPU的同步变量，保证只有一个任务在使用GPU
gpu_lock = Lock()

# # 视频剪辑参数预缓存
# from distribution import get_distribute
# @app.route('/distribute', methods=['POST'])
# def distribute():
#     dists = cache.get('dists')
#     if dists is None:
#         dists = get_distribute()
#         cache.set('dists', dists, timeout=60 * 60)
#     return {
#         "distribute": dists
#     }

# # 视频剪辑参数预缓存
# from distribution import get_cat_distribute
# @app.route('/cat-distribute', methods=['POST'])
# def cat_distribute():
#     data = request.json
#     man = cache.get('man')
#     woman = cache.get('woman')
#     child = cache.get('child')
#     if man is None or woman is None or child is None:
#         man, woman, child = get_cat_distribute()
#         cache.set('man', man, timeout=60 * 60)
#         cache.set('woman', woman, timeout=60 * 60)
#         cache.set('child', child, timeout=60 * 60)
#     return {
#         'man': man,
#         'woman': woman,
#         'child': child
#     }

# # 视频剪辑参数预缓存
# from cutVideo import split
# @app.route('/cutvideo', methods=['POST'])
# def cutvideo():
#     data = request.json
#     filename = data.get('filename')
#     split_res = split(uploads_folder + filename)
#     cache.set(filename + 'cutvideo', split_res, timeout=60 * 60)
#     return {
#         "success": 1
#     }

# # 注意力算法接口
# from attention import score as get_attention
# @app.route('/attention', methods=['POST'])
# def attention():
#     data = request.json
#     filename = data.get('filename')
#     # 偏低：一些画面中的显著物体可能较少，可能不易吸引注意力
#     # 偏高：一些画面中的显著物体可能过多，容易造成注意力区域分散
#     score, value, arg_max = get_attention(uploads_folder + filename)
#     if score >= 85:
#         advice = '指标正常，没有改善建议'
#     elif value < arg_max:
#         advice = '一些画面中的显著物体可能较少，可能不易吸引注意力'
#     else:
#         advice = '一些画面中的显著物体可能过多，容易造成注意力区域分散'
#     return {
#         "value": value,
#         "score": score,
#         "advice": advice
#     }

# # 情感效价算法接口
# from valence import score as get_valence
# @app.route('/valence', methods=['POST'])
# def valence():
#     data = request.json
#     filename = data.get('filename')
#     # time.sleep(random.randint(1, 5))
#     # 偏低：一些画面的视觉效果可能过于平淡，可以尝试更加明亮、鲜艳的色彩
#     # 偏高：一些画面的视觉效果可能过于强烈，可以尝试降低饱和度、明暗度，采用更加柔和的色彩
#     score, value, arg_max = get_valence(uploads_folder + filename)
#     if score >= 85:
#         advice = '指标正常，没有改善建议'
#     elif value < arg_max:
#         advice = '一些画面的视觉效果可能过于平淡，可以尝试更加明亮、鲜艳的色彩'
#     else:
#         advice = '一些画面的视觉效果可能过于强烈，可以尝试降低饱和度、明暗度，采用更加柔和的色彩'
#     return {
#         "value": value,
#         "score": score,
#         "advice": advice
#     }

# # 情感激励算法接口
# from arousal import score as get_arousal
# @app.route('/arousal', methods=['POST'])
# def arousal():
#     data = request.json
#     filename = data.get('filename')
#     # time.sleep(random.randint(1, 5))
#     # 偏低：一些画面的视觉效果变化程度可能较小，可以尝试提高镜头切换频率、增加画面饱和度、对比度等
#     # 偏高：一些画面的视觉效果变化程度可能较大，可以尝试降低镜头切换频率、减小画面饱和度、对比度等
#     score, value, arg_max = get_arousal(uploads_folder + filename)
#     if score >= 85:
#         advice = '指标正常，没有改善建议'
#     elif value < arg_max:
#         advice = '一些画面的视觉效果变化程度可能较小，可以尝试提高镜头切换频率、增加画面饱和度、对比度等'
#     else:
#         advice = '一些画面的视觉效果变化程度可能较大，可以尝试降低镜头切换频率、减小画面饱和度、对比度等'
#     return {
#         "value": value,
#         "score": score,
#         "advice": advice
#     }

# # 画面清晰度算法接口
# from clarity import score as get_clarity
# @app.route('/clarity', methods=['POST'])
# def clarity():
#     data = request.json
#     filename = data.get('filename')
#     # time.sleep(random.randint(1, 5))
#     # 偏低：一些画面的清晰度可能较低，可能不利于画面信息传达
#     # 偏高：一些画面的清晰度可能过高，可以尝试降低画面锐度、对比度
#     score, value, arg_max = get_clarity(uploads_folder + filename)
#     if score >= 85:
#         advice = '指标正常，没有改善建议'
#     elif value < arg_max:
#         advice = '一些画面的清晰度可能较低，可能不利于画面信息传达'
#     else:
#         advice = '一些画面的清晰度可能过高，可以尝试降低画面锐度、对比度'
#     return {
#         "value": value,
#         "score": score,
#         "advice": advice
#     }

# # 画面平稳度算法接口
# from steady_and_cam import score as get_steady_and_cam
# @app.route('/steady', methods=['POST'])
# def steady():
#     data = request.json
#     filename = data.get('filename')
#     # time.sleep(random.randint(1, 5))
#     # 偏低：一些画面的运动幅度可能过于抖动，节奏过快，可能不利于镜头信息传达，可以尝试降低帧率、降低镜头切换频率
#     # 偏高：一些画面的运动幅度可能缺少变化，可能会容易造成缓慢、无聊的观感，可以尝试提高帧率、提高镜头切换频率
#     split_res = cache.get(filename + 'cutvideo')
#     if split_res is None:
#         print('Cuts cache not found, re-calculating')
#         split_res = split(uploads_folder + filename)
#         cache.set(filename + 'cutvideo', split_res, timeout=60 * 60)
#     else:
#         print('Cuts cache found.')
#     steady_score, video_steady, arg_max_steady, cam_score, video_cam, arg_max_cam = get_steady_and_cam(split_res, uploads_folder + filename)
#     cache.set(filename + 'cam_score', cam_score, timeout=60 * 60)
#     cache.set(filename + 'video_cam', video_cam, timeout=60 * 60)
#     cache.set(filename + 'arg_max_cam', arg_max_cam, timeout=60 * 60)
#     if steady_score >= 85:
#         advice = '指标正常，没有改善建议'
#     elif video_steady < arg_max_steady:
#         advice = '一些画面的运动幅度可能过于抖动，节奏过快，可能不利于镜头信息传达，可以尝试降低帧率、降低镜头切换频率'
#     else:
#         advice = '一些画面的运动幅度可能缺少变化，可能会容易造成缓慢、无聊的观感，可以尝试提高帧率、提高镜头切换频率'
#     return {
#         "value": video_steady,
#         "score": steady_score,
#         "advice": advice
#     }


# # 画面丰富度算法接口
# from complexity import score as get_complexity
# @app.route('/complexity', methods=['POST'])
# def complexity():
#     data = request.json
#     filename = data.get('filename')
#     # time.sleep(random.randint(1, 5))
#     # 偏低：一些画面的内容可能过于单调，可以尝试补充画面信息（如文字、图案等）
#     # 偏高：一些画面的内容可能过于繁杂，可能会造成画面信息负载过大，可以尝试虚化背景或采用较为纯净背景拍摄的素材
#     score, value, arg_max = get_complexity(uploads_folder + filename)
#     if score >= 85:
#         advice = '指标正常，没有改善建议'
#     elif value < arg_max:
#         advice = '一些画面的内容可能过于单调，可以尝试补充画面信息（如文字、图案等）'
#     else:
#         advice = '一些画面的内容可能过于繁杂，可能会造成画面信息负载过大，可以尝试虚化背景或采用较为纯净背景拍摄的素材'
#     return {
#         "value": value,
#         "score": score,
#         "advice": advice
#     }

# # 信息类型丰富度算法接口
# from info import score as get_info
# @app.route('/info', methods=['POST'])
# def info():
#     data = request.json
#     filename = data.get('filename')
#     # time.sleep(random.randint(1, 5))
#     # 偏低：视频中展示的产品信息类型可能过少，可以尝试补充多种信息类型镜头
#     # 偏高：视频中展示的产品信息类型可能过多，可能会造成短视频内信息负载过大
#     split_res = cache.get(filename + 'cutvideo')
#     if split_res is None:
#         print('Cuts cache not found, re-calculating')
#         split_res = split(uploads_folder + filename)
#         cache.set(filename + 'cutvideo', split_res, timeout=60 * 60)
#     else:
#         print('Cuts cache found.')
#     info_score, video_info, info_results, arg_max = get_info(split_res, uploads_folder + filename)
#     cache.set(filename + 'info_results', info_results, timeout=60 * 60)
#     if info_score >= 85:
#         advice = '指标正常，没有改善建议'
#     elif video_info < arg_max:
#         advice = '视频中展示的产品信息类型可能过少，可以尝试补充多种信息类型镜头'
#     else:
#         advice = '视频中展示的产品信息类型可能过多，可能会造成短视频内信息负载过大'
#     return {
#         "value": video_info,
#         "score": info_score,
#         "advice": advice
#     }

# # 视角丰富度算法接口
# from view import score as get_view
# @app.route('/view', methods=['POST'])
# def view():
#     data = request.json
#     filename = data.get('filename')
#     # time.sleep(random.randint(1, 5))
#     # 偏低：视频中的相同信息类型的镜头间视角重复度较高，可以尝试补充同一信息类型的多角度镜头。
#     # 偏高：视频中的相同信息类型的镜头间视角重复度较低，可能会造成短视频内信息负载过大
#     split_res = cache.get(filename + 'cutvideo')
#     if split_res is None:
#         print('Cuts cache not found, re-calculating')
#         split_res = split(uploads_folder + filename)
#         cache.set(filename + 'cutvideo', split_res, timeout=60 * 60)
#     else:
#         print('Cuts cache found.')
#     info_results = cache.get(filename + 'info_results')
#     if info_results is None:
#         print('Info cache not found, re-calculating')
#         info_score, video_info, info_results, arg_max = get_info(split_res, uploads_folder + filename)
#     else:
#         print('Info cache found.')
#     view_score, video_view, arg_max = get_view(split_res, info_results[0], uploads_folder + filename)
#     if view_score >= 85:
#         advice = '指标正常，没有改善建议'
#     elif video_view < arg_max:
#         advice = '视频中的相同信息类型的镜头间视角重复度较高，可以尝试补充同一信息类型的多角度镜头。'
#     else:
#         advice = '视频中的相同信息类型的镜头间视角重复度较低，可能会造成短视频内信息负载过大'
#     return {
#         "value": video_view,
#         "score": view_score,
#         "advice": advice
#     }

# # 运动连贯算法接口
# from move import score as get_move
# @app.route('/move', methods=['POST'])
# def move():
#     data = request.json
#     filename = data.get('filename')
#     # time.sleep(random.randint(1, 5))
#     # 偏低：视频中相邻镜头的运动节奏差异过大、不够连贯，可以尝试采用快慢相对一致的镜头相接
#     # 偏高：视频中相邻镜头的运动节奏差异过小，可能缺少变化
#     split_res = cache.get(filename + 'cutvideo')
#     if split_res is None:
#         print('Cuts cache not found, re-calculating')
#         split_res = split(uploads_folder + filename)
#         cache.set(filename + 'cutvideo', split_res, timeout=60 * 60)
#     else:
#         print('Cuts cache found.')
#     move_score, video_move, arg_max = get_move(split_res, uploads_folder + filename)
#     if move_score >= 85:
#         advice = '指标正常，没有改善建议'
#     elif video_move < arg_max:
#         advice = '视频中相邻镜头的运动节奏差异过大、不够连贯，可以尝试采用快慢相对一致的镜头相接'
#     else:
#         advice = '视频中相邻镜头的运动节奏差异过小，可能缺少变化'
#     return {
#         "value": video_move,
#         "score": move_score,
#         "advice": advice
#     }

# # 主体位置连贯算法接口
# from location import score as get_location
# @app.route('/location', methods=['POST'])
# def location():
#     data = request.json
#     filename = data.get('filename')
#     # time.sleep(random.randint(1, 5))
#     # 偏低：视频中相邻镜头间的主体位置可能变化过大、不够连贯，容易造成跳跃、不适的观感
#     # 偏高：视频中镜头间的主体位置可能缺少变化
#     split_res = cache.get(filename + 'cutvideo')
#     if split_res is None:
#         print('Cuts cache not found, re-calculating')
#         split_res = split(uploads_folder + filename)
#         cache.set(filename + 'cutvideo', split_res, timeout=60 * 60)
#     else:
#         print('Cuts cache found.')
#     location_score, video_location, arg_max = get_location(split_res, uploads_folder + filename)
#     if location_score >= 85:
#         advice = '指标正常，没有改善建议'
#     elif video_location < arg_max:
#         advice = '视频中相邻镜头间的主体位置可能变化过大、不够连贯，容易造成跳跃、不适的观感'
#     else:
#         advice = '视频中镜头间的主体位置可能缺少变化'
#     return {
#         "value": video_location,
#         "score": location_score,
#         "advice": advice
#     }

# # 画面连贯算法接口
# @app.route('/cam', methods=['POST'])
# def cam():
#     data = request.json
#     filename = data.get('filename')
#     # time.sleep(random.randint(1, 5))
#     # 偏低：视频中镜头切换的前后画面变化过大、不够连贯，容易造成跳跃、不适的观感
#     # 偏高：视频中镜头切换的前后画面过于相似，可能缺少变化，容易造成跳剪的观感
#     split_res = cache.get(filename + 'cutvideo')
#     if split_res is None:
#         print('Cuts cache not found, re-calculating')
#         split_res = split(uploads_folder + filename)
#         cache.set(filename + 'cutvideo', split_res, timeout=60 * 60)
#     else:
#         print('Cuts cache found.')
#     cam_score = cache.get(filename + 'cam_score')
#     video_cam = cache.get(filename + 'video_cam')
#     arg_max_cam = cache.get(filename + 'arg_max_cam')
#     if cam_score is None or video_cam is None or arg_max_cam is None:
#         print('Cam cache not found, re-calculating')
#         steady_score, video_steady, arg_max_steady, cam_score, video_cam, arg_max_cam = get_steady_and_cam(split_res, uploads_folder + filename)
#     else:
#         print('Cam cache found.')
#     if cam_score >= 85:
#         advice = '指标正常，没有改善建议'
#     elif video_cam < arg_max_cam:
#         advice = '视频中镜头切换的前后画面变化过大、不够连贯，容易造成跳跃、不适的观感'
#     else:
#         advice = '视频中镜头切换的前后画面过于相似，可能缺少变化，容易造成跳剪的观感'
#     return {
#         "value": video_cam,
#         "score": cam_score,
#         "advice": advice
#     }

# # 剪辑素材预处理
# import shutil
# import datetime
# from edit.preprocess import calcShotsData

# def begin_preprocess(save_path, lock):
#     print('Begin process:', save_path)
#     lock.acquire()
#     try:
#         print('Get lock.')
#         sample_time_interval = 0.125
#         calcShotsData(save_path, sample_time_interval)
#     finally:
#         print('Release lock.')
#         lock.release()

# @app.route('/preprocess', methods=['POST'])
# def preprocess():
#     '''
#         将用户上传的素材从upload_path中复制到save_pth=upload_path/match_id中
#         在save_pth遍历处理所有素材，将同名的data文件也储存在save_pth
#         返回该次匹配请求的match_id
#     '''
#     data = request.json
#     filenames = data.get('filenames')
#     # 生成一个match_id
#     now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     match_id = now + str(random.random())
#     upload_path = '../uploads/'
#     save_path = '../express-back-end/public/uploads/' + match_id + '/'
#     folder = os.path.exists(save_path)
#     if not folder:
#         os.makedirs(save_path)
#     for filename in filenames:
#         source = upload_path + filename
#         target = save_path + filename
#         # print('copy %s %s' % (source, target))
#         shutil.copy(source, target)
#         # os.system('copy "%s" "%s"' % (upload_path + filename, save_path + filename)) # windows
#         # # os.system('cp %s %s' % (upload_path + filename, save_path + filename)) # linux
#     # split_res = cache.get(filename + 'cutvideo')
#     p = Process(target=begin_preprocess, args=(save_path, gpu_lock,))
#     p.start()
#     p.join()

#     cache.set('match:' + match_id, save_path, timeout=(60 * 60))

#     return {
#         "match_id": match_id
#     }

# # 和案例库进行匹配，找出匹配度最高的几个案例，这个需要遍历匹配，然后保存匹配度
# #TODO 从data中get的风格标签命名统一一下
# from edit.match import match_best_cut_shot_line
# @app.route('/match', methods=['POST'])
# def match():
#     '''
#         从cache中得到处理后素材的文件地址save_path
#         templateType ：用户选择的风格标签，不选择则为所有的标签
#         templateName ：用户选择的具体模板名称，不指定则为空
#         save_shots_line 用pickle存在save_path
#     '''
#     data = request.json
#     match_id = data.get('matchId')
#     template_type = data.get('templateType')
#     template_name = data.get('templateName')

#     save_path = cache.get('match:' + match_id)

#     if save_path is None:
#         pass
#     else:
#         template_root = '../express-back-end/public/templates/'
#         save_shots_lines = []
#         # if template_name:  # 如果指定了某个具体模板
#         #     template_path = os.path.join(
#         #         template_root, template_type[0], template_name)
#         #     template_shots_path = os.path.join(template_path, 'shots')
#         #     save_shots_line = match_best_cut_shot_line(
#         #         template_shots_path, save_path)
#         #     save_shots_line[0].template_path = template_path[7:]
#         #     save_shots_line[0].saveThumbnails()
#         #     save_shots_lines.append(save_shots_line[0])
#         # else:  # 没有指定具体模板，指定了风格，得到所有的匹配序列
#         for template_floder in template_type:
#             print('save_shots_lines:', template_floder)
#             template_paths = []
#             for template_name in os.listdir(os.path.join(template_root, template_floder)):
#                 if template_name != '.gitignore':
#                     template_paths.append(os.path.join(template_root, template_floder, template_name))
#             # template_paths = [os.path.join(template_root, template_floder, template_name)
#             #                     for template_name in os.listdir(os.path.join(template_root, template_floder))]

#             for template_path in template_paths:
#                 print('template_path:', template_path)
#                 template_shots_path = os.path.join(template_path, 'shots')
#                 print('template_shots_path:', template_shots_path)
#                 print('save_path:', save_path)
#                 save_shots_line = match_best_cut_shot_line(
#                     template_shots_path, save_path)
#                 if len(save_shots_line) > 0:
#                     save_shots_line[0].template_path = template_path[27:]
#                     save_shots_line[0].saveThumbnails()
#                     save_shots_lines.append(save_shots_line[0])

#         save_shots_lines = sorted(
#             save_shots_lines, key=lambda x: x.simi, reverse=True)
#         print('save_shots_lines:', len(save_shots_lines))
#         print('save_path:', save_path)
#         save_match_res(match_id, save_shots_lines, save_path)

#     return {
#         "match_id": match_id
#     }

# @app.route('/get_match', methods=['POST'])
# def get_match():
#     data = request.json
#     match_id = data.get('match_id')
#     save_path = cache.get('match:' + match_id)

#     if save_path is None:
#         return {
#             'match_id': match_id,
#             "shots_lines": []
#         }
#     else:
#         save_shots_lines = load_match_res(match_id, save_path)
#         shots_lines = []
#         for shots_line in save_shots_lines:
#             video_path = shots_line.template_path + '/video.mp4'

#             shots = shots_line.getThumbnails()
#             print(shots)
#             shots_lines.append({
#                 'template': shots_line.template_path,
#                 'template_video': video_path,
#                 'shots': shots
#             })
#         return {
#             'match_id': match_id,
#             "shots_lines": shots_lines
#         }


# # 保存匹配结果
# def save_match_res(match_id, save_shots_lines, save_path):
#     match_res_name = 'match_res.data'
#     match_res_path = os.path.join(save_path, match_res_name)
#     with open(match_res_path, "wb") as f:
#         pickle.dump(save_shots_lines, f)

# # 读取匹配结果
# def load_match_res(match_id, save_path):
#     match_res_name = 'match_res.data'
#     match_res_path = os.path.join(save_path, match_res_name)
#     with open(match_res_path, "rb") as f:
#         save_shots_lines = pickle.load(f)
#         return save_shots_lines
#     return None

# # 进行视频生成
# from edit.render import get_cut_shot_line_video
# @app.route('/render', methods=['POST'])
# def render():
#     data = request.json
#     match_id = data.get('match_id')
#     template = data.get('template')
#     save_path = cache.get('match:' + match_id)
#     save_shots_lines = load_match_res(match_id, save_path)
#     video_folder = '../express-back-end/public/tempoFiles/videos/'
#     template_list = template.split('/')
#     template_name = '-'.join(template_list[1:])
#     file_path = video_folder + match_id + '-' + template_name + '.mp4'
#     now = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
#     result_id = now + str(random.random())
#     if not os.path.exists(file_path):
#         for shots_line in save_shots_lines:
#             if shots_line.template_path == template:
#                 get_cut_shot_line_video(file_path, '../express-back-end/public/' + template + '/music.mp3', shots_line)
#                 break
#     cache.set('result:' + result_id, file_path[27:], timeout=(60 * 60))
#     return {
#         "result_id": result_id
#     }

# @app.route('/get_video_path', methods=['POST'])
# def get_video_path():
#     data = request.json
#     result_id = data.get('result_id')
#     video_path = cache.get('result:' + result_id)
#     if video_path is None:
#         return {
#             "video_path": ''
#         }
#     else:
#         return {
#             "video_path": video_path
#         }


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000, threaded=True)
