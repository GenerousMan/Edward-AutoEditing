import os
import time
import random
import progressbar
import multiprocessing
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import analyze as aly
from datetime import datetime
from classes.tshot_bag import TShotBag
from choose import approx_simi, accuri_simi

def save_tshot_bags(templates_folder):
    print('Save TSB:')
    tempaltes = os.listdir(templates_folder)
    lent = len(tempaltes)
    p = progressbar.ProgressBar()
    p.start(lent)
    tempaltes = sorted(tempaltes, key=lambda t: int(t.split('-')[-1]))
    for index, tempalte in enumerate(tempaltes):
        p.update(index + 1)
        shots_path = os.path.join(templates_folder, tempalte)
        # data_path = os.path.join(templates_folder, tempalte, 'data.pkl')
        tshot_bag = TShotBag(shots_path)
        TShotBag.save(tshot_bag)
    p.finish()

def load_tshot_bags(templates_folder):
    print('Load TSB:')
    tempaltes = os.listdir(templates_folder)
    tempaltes = sorted(tempaltes, key=lambda t: int(t.split('-')[-1]))
    tshot_bags = []
    lent = len(tempaltes)
    p = progressbar.ProgressBar()
    p.start(lent)
    for index, tempalte in enumerate(tempaltes):
        p.update(index + 1)
        shots_path = os.path.join(templates_folder, tempalte)
        tshot_bag = TShotBag.load(shots_path)
        tshot_bags.append(tshot_bag)
    p.finish()
    return tshot_bags

def calc_matrix(templates_folder):
    tshot_bags = load_tshot_bags(templates_folder)
    print('Matrix:')
    view_matrix = pd.DataFrame(index=tempaltes, columns=tempaltes).fillna(0.0)
    direct_matrix = pd.DataFrame(index=tempaltes, columns=tempaltes).fillna(0.0)
    pose_matrix = pd.DataFrame(index=tempaltes, columns=tempaltes).fillna(0.0)
    motion_matrix = pd.DataFrame(index=tempaltes, columns=tempaltes).fillna(0.0)
    lent = len(tempaltes)
    p = progressbar.ProgressBar()
    p.start(lent * lent / 2 - lent / 2)
    count = 0
    for i, ti in enumerate(tshot_bags):
        ti_name = tempaltes[i]
        for j, tj in enumerate(tshot_bags):
            if i >= j:
                continue
            tj_name = tempaltes[j]

            hd = TShotBag.hist_distance(ti.view_hist, tj.view_hist)
            view_matrix.loc[ti_name, tj_name] = hd
            view_matrix.loc[tj_name, ti_name] = hd
            hd = TShotBag.hist_distance(ti.direct_hist, tj.direct_hist)
            direct_matrix.loc[ti_name, tj_name] = hd
            direct_matrix.loc[tj_name, ti_name] = hd
            hd = TShotBag.hist_distance(ti.pose_hist, tj.pose_hist)
            pose_matrix.loc[ti_name, tj_name] = hd
            pose_matrix.loc[tj_name, ti_name] = hd
            hd = TShotBag.hist_distance(ti.motion_hist, tj.motion_hist)
            motion_matrix.loc[ti_name, tj_name] = hd
            motion_matrix.loc[tj_name, ti_name] = hd

            count += 1
            p.update(count)

    p.finish()
    # print(view_matrix)
    view_matrix.to_csv('edit/data/view.csv')
    direct_matrix.to_csv('edit/data/direct.csv')
    pose_matrix.to_csv('edit/data/pose.csv')
    motion_matrix.to_csv('edit/data/motion.csv')

def load_matrix():
    view_matrix = pd.read_csv('edit/data/view.csv', header=0, index_col=0)
    direct_matrix = pd.read_csv('edit/data/direct.csv', header=0, index_col=0)
    pose_matrix = pd.read_csv('edit/data/pose.csv', header=0, index_col=0)
    motion_matrix = pd.read_csv('edit/data/motion.csv', header=0, index_col=0)
    return (view_matrix, direct_matrix, pose_matrix, motion_matrix)

def template_filter(templates_folder, tempalte, poss, matrix):
    (vm, dm, pm, mm) = matrix
    result = (poss[0] * vm + poss[1] * dm + poss[2] * pm + poss[3] * mm) / 4
    if any(poss):
        result = result[tempalte].sort_values()
    else:
        result = result.sample(frac=1)[tempalte]
    if tempalte in result.index:
        rank = result.drop([tempalte])
    return rank

def template_search(templates, videos_path, box=4, step=4, pb=True):
    videos = aly.load_videos(videos_path, 4)
    pick = pd.Series([]) # 精算案例
    pool = pd.Series([]) # 粗算后的备选案例
    all_pool = pd.Series([]) # 所有的粗算案例
    matrix = load_matrix() # 预加载数据
    for i in range(step):
        # 计算templates的粗精准度
        p = progressbar.ProgressBar() if pb else None
        p.start(box) if pb else None
        count = 0
        for t in templates:
            template_path = os.path.join('../templates', t)
            simi = approx_simi(template_path, videos_path, videos)
            pool[t] = simi
            all_pool[t] = simi
            count += 1
            p.update(count) if pb else None
        p.finish() if pb else None
        max_template = pool.idxmax()
        max_simi = pool[max_template]
        print('Choose', max_template, max_simi) if pb else None
        # 计算template的细精准度
        template_folder = os.path.join('../templates', max_template)
        template_path = os.path.join(template_folder)
        simi, vs, ds, ps, ms = accuri_simi(template_path, videos_path, videos)
        simi, vs, ds, ps, ms = np.array([simi, vs, ds, ps, ms]) / 100
        # 精算的案例加入到pick_list中
        pick[max_template] = simi
        # 在pool中删除精算的案例
        pool = pool.drop([max_template])
        # 根据匹配度权重获得新的案例集
        rank = template_filter(template_folder, max_template, (vs, ds, ps, ms), matrix)
        # 把pick排除出去
        for t in pick.index:
            if t in rank.index:
                rank = rank.drop([t])
        # 把pool排除出去
        for t in pool.index:
            if t in rank.index:
                rank = rank.drop([t])
        # 新的案例集
        templates = rank[:box].index
        print('Step:', step, template_path, simi, vs, ds, ps, ms) if pb else None
    mx = pick.max()
    mean = pick.mean()
    all_mean = all_pool.mean()
    # ts = [t.split('-')[-1] for t in all_pool.sort_values(ascending=False).index]
    ts = [t for t in all_pool.sort_values(ascending=False).index]
    return mx, mean, all_mean, ts

def algrithm_test(videos_path, box=4, step=6, pb=True):
    random.seed(datetime.now())
    # 一次算法流程测试
    tempaltes = os.listdir('templates')
    templates = random.sample(tempaltes, box)
    return template_search(templates, videos_path, box, step, pb), templates

def random_test(videos_path, box=4, step=6, pb=True):
    random.seed(datetime.now())
    # 随机挑选案例
    tempaltes = os.listdir('templates')
    samples = random.sample(tempaltes, box * step)
    videos = aly.load_videos(videos_path, 4)
    p = progressbar.ProgressBar() if pb else None
    p.start(box * step) if pb else None
    count = 0
    pool = pd.Series([])
    temp = []
    simis1 = []
    for i, template in enumerate(samples):
        template_path = os.path.join('templates', template)
        simi = approx_simi(template_path, videos_path, videos)
        if i > 0:
            pool[template] = simi
            simis1.append(simi)
        temp.append((template, simi))
        count += 1
        p.update(count) if pb else None
    p.finish() if pb else None
    temp = sorted(temp, key=lambda item: item[1], reverse=True)
    temp = temp[:step]
    max_simi = 0
    max_template = 'null'
    p = progressbar.ProgressBar() if pb else None
    p.start(step) if pb else None
    count = 0
    simis2 = []
    for template, _ in temp:
        template_path = os.path.join('templates', template)
        simi, vs, ds, ps, ms = accuri_simi(template_path, videos_path, videos)
        simi = simi / 100
        simis2.append(simi)
        if simi > max_simi:
            max_simi = simi
            max_template = template
        count += 1
        p.update(count) if pb else None
    p.finish() if pb else None
    ts = [t.split('-')[-1] for t in pool.sort_values(ascending=False).index]
    if max_template == 'null':
        return 0, np.mean(simis2), np.mean(simis1), ts
    else:
        return max_simi, np.mean(simis2), np.mean(simis1), ts

def one_test_round(folder, write=False):
    videos_path = 'uploads/videos/{}'.format(folder)
    start = time.time()
    max_simi, accuri_mean_simi, approx_mean_simi, ts = random_test(videos_path, pb=not write)
    print('Rand:', max_simi, '\t', round(accuri_mean_simi, 2), '\t', round(approx_mean_simi, 3))
    if write and lock:
        try:
            lock.acquire()
            f = open('data/random.csv', 'a+')
            output = [max_simi, accuri_mean_simi, approx_mean_simi]
            output = [str(round(item, 4)) for item in output]
            f.write(','.join(output) + '\n')
        except:
            print('Error')
        finally:
            f.close()
            lock.release()
    (max_simi, accuri_mean_simi, approx_mean_simi, ts), rt = algrithm_test(videos_path, pb=not write)
    print('Algr:', max_simi, '\t', round(accuri_mean_simi, 2), '\t', round(approx_mean_simi, 3))
    if write and lock:
        try:
            lock.acquire()
            f = open('data/algrithm.csv', 'a+')
            output = [max_simi, accuri_mean_simi, approx_mean_simi]
            output = [str(round(item, 4)) for item in output]
            f.write(','.join(output) + '\n')
        except:
            print('Error')
        finally:
            f.close()
            lock.release()
    end = time.time()

def calc_all_templates_simi(template_folder, videos_name, pb=False):
    videos_path = os.path.join('uploads/videos', videos_name)
    templates = os.listdir(template_folder)
    templates = sorted(templates, key=lambda t:int(t.split('-')[-1]))
    lines = [['template', 'simi', 'vs', 'ds', 'ps', 'ms']]
    p = progressbar.ProgressBar() if pb else None
    p.start(len(templates)) if pb else None
    for i, t in enumerate(templates):
        videos = aly.load_videos(videos_path, 4)
        template_path = os.path.join('templates', t, 'shots')
        simi, vs, ds, ps, ms = accuri_simi(template_path, videos_path, videos)
        lines.append([t, simi, vs, ds, ps, ms])
        p.update(i+1) if pb else None
    p.finish() if pb else None
    with open('data/{}.csv'.format(videos_name), 'w') as f:
        lines = [','.join(list(map(str, line))) + '\n' for line in lines]
        f.writelines(lines)
    print('All templates done.')

def init(l):
    global lock
    lock = l

def multi_process(folder, round):
    lock = multiprocessing.Lock()
    pool = multiprocessing.Pool(processes=6, initializer=init, initargs=(lock,))
    for i in range(round):
        pool.apply_async(one_test_round, args=(folder, True, ))
    pool.close()
    pool.join()

def compare_item(v1, v2):
    rmm, rms = v1.mean(), v1.std()
    amm, ams = v2.mean(), v2.std()
    print(rmm, rms)
    print(amm, ams)
    x = np.arange(v1.shape[0])
    ry = v1.values
    ay = v2.values
    plt.plot(x, ry, color='#00b2ff', label='Random', lw=3)
    plt.plot(x, ay, color='#ff683d', label='Algrithm', lw=3)
    plt.legend()
    plt.grid()
    plt.show()

def compare(postfix=''):
    plt.style.use("classic")
    random_results = pd.read_csv('data/random{}.csv'.format(postfix), names=['max', 'top-4', 'all'])
    random_results = random_results.fillna(0.5)
    algrithm_results = pd.read_csv('data/algrithm{}.csv'.format(postfix), names=['max', 'top-4', 'all'])
    algrithm_results = algrithm_results.fillna(0.5)
    min_len = min(random_results.shape[0], algrithm_results.shape[0])
    random_results = random_results[:min_len]
    algrithm_results = algrithm_results[:min_len]
    # Max 指标
    random_max = random_results['max'].sort_values()
    algrithm_max = algrithm_results['max'].sort_values()
    compare_item(random_max, algrithm_max)
    # Top-4 指标
    random_top_4 = random_results['top-4'].sort_values()
    algrithm_top_4 = algrithm_results['top-4'].sort_values()
    compare_item(random_top_4, algrithm_top_4)
    # All 指标
    random_all = random_results['all'].sort_values()
    algrithm_all = algrithm_results['all'].sort_values()
    compare_item(random_all, algrithm_all)

def real_time_compare():
    plt.ion()
    plt.figure(1)
    while True:
        random_results = pd.read_csv('data/random.csv', names=['max', 'top-4', 'all'])
        random_results = random_results.fillna(0.5)
        algrithm_results = pd.read_csv('data/algrithm.csv', names=['max', 'top-4', 'all'])
        algrithm_results = algrithm_results.fillna(0.5)
        # 统一长度
        min_len = min(random_results.shape[0], algrithm_results.shape[0])
        # All 指标
        random_all = random_results['all'][:min_len].sort_values()
        algrithm_all = algrithm_results['all'][:min_len].sort_values()
        rmm, rms = random_all.mean(), random_all.std()
        amm, ams = algrithm_all.mean(), algrithm_all.std()
        # print('Rand:', rmm, rms, 'Algr:', amm, ams, end='\r')
        os.system('cls')
        print('Rand:', rmm, rms)
        print('Algr:', amm, ams)
        # sys.stdout.flush()
        plt.clf()
        x = np.arange(min_len)
        ry = random_all.values
        ay = algrithm_all.values
        plt.plot(x, ry, color='#00b2ff', label='Random', lw=3)
        plt.plot(x, ay, color='#ff683d', label='Algrithm', lw=3)
        plt.draw()
        # time.sleep(2)
        plt.pause(10)

if __name__ == "__main__":
    one_test_round('compare-1')
    # multi_process('compare-1', 502)
    # compare()
    # real_time_compare()
    # calc_all_templates_simi('templates', 'compare-4', True)