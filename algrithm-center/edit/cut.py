import os
import time
import analyze as aly
from classes.shot_group import ShotGroup

# def generate_t_shots(folder):
#     videos = aly.load_videos(folder)
    
def get_shot_groups(tshots, videos):
    return [ShotGroup(tshot, videos) for tshot in tshots]


if __name__ == "__main__":
    # folder = 'uploads/videos/compare-1'
    start = time.time()
    videos = aly.load_videos('uploads/videos/compare-1', 4)
    end = time.time()
    start = time.time()
    end = time.time()
    start = time.time()
    tshots = aly.load_shots('new_templates/taobao-0')
    sgs = get_shot_groups(tshots, videos)
    
    # for tshot in tshots:
    #     print(ShotGroup(tshot, videos))
    # end = time.time()
    # print('Match Cost:', end - start)