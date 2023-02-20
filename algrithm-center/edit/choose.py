import time
import copy
import numpy as np
import cut
import analyze as aly
from classes.path import Path
from classes.shot_line import ShotLine

def calc_best_path(prev_sg, next_sg):
    for i, _pvs in enumerate(prev_sg.vshots):
        path = prev_sg.paths[i]
        if path is None:
            continue
        for j, nvs in enumerate(next_sg.vshots):
            test_score = path.get_test_score(nvs)
            if test_score == 0:
                continue
            elif next_sg.paths[j] is None:
                next_path = copy.deepcopy(path)
                next_path.add_vshot(nvs, j)
                next_sg.paths[j] = next_path
            elif test_score > next_sg.paths[j].get_score():
                next_path = copy.deepcopy(path)
                next_path.add_vshot(nvs, j)
                next_sg.paths[j] = next_path

def get_best_shot_lines(shot_groups):
    cut_shot_lines = []
    start_sg = shot_groups[0]
    for i, vshot in enumerate(start_sg.vshots):
        start_sg.paths[i] = Path(vshot, i)
    prev_sg = start_sg
    for i in range(1, len(shot_groups)):
        next_sg = shot_groups[i]
        calc_best_path(prev_sg, next_sg)
        prev_sg = next_sg
    
    paths = [path for path in prev_sg.paths if path]
    paths = sorted(paths, key=lambda path: path.get_score(), reverse=True)

    shot_lines = []
    for path in paths:
        vshots = []
        for sg_index in range(path.size):
            vshot_index = path.vshot_index[sg_index]
            vshot = shot_groups[sg_index].vshots[vshot_index]
            vshots.append(vshot)
        shot_lines.append(ShotLine(vshots))

    return shot_lines

def approx_simi(template_path, videos_path, videos=None):
    if videos is None:
        videos = aly.load_videos(videos_path, 4)
    tshots = aly.load_shots(template_path)
    shot_groups = cut.get_shot_groups(tshots, videos)
    for sg in shot_groups:
        if len(sg.vshots) == 0:
            return 0
    simis = []
    for sg in shot_groups:
        top_vshots = sg.vshots[:3]
        simis.append(np.mean([vshot.simi for vshot in top_vshots]))
    simi = np.mean(simis)
    return simi

def accuri_simi(template_path, videos_path, videos=None):
    if videos is None:
        videos = aly.load_videos(videos_path, 4)
    tshots = aly.load_shots(template_path)
    shot_groups = cut.get_shot_groups(tshots, videos)
    for sg in shot_groups:
        if len(sg.vshots) == 0:
            return 0, 0, 0, 0, 0
    shot_lines = get_best_shot_lines(shot_groups)
    if len(shot_lines) == 0:
        return 0, 0, 0, 0, 0
    else:
        simi = shot_lines[0].simi
        vs = shot_lines[0].view_simi
        ds = shot_lines[0].direction_simi
        ps = shot_lines[0].pose_simi
        ms = shot_lines[0].motion_simi
        return simi, vs, ds, ps, ms

if __name__ == "__main__":
    videos = aly.load_videos('uploads/videos/compare-1', 4)
    tshots = aly.load_shots('new_templates/taobao-0')
    shot_groups = cut.get_shot_groups(tshots, videos)
    shot_lines = get_best_shot_lines(shot_groups)
    start = time.time()
    print(approx_simi('new_templates/taobao-0', 'uploads/videos/compare-1', videos))
    end = time.time()
    print(accuri_simi('new_templates/taobao-0', 'uploads/videos/compare-1', videos))
    print('Choose cost:', end - start)