import os
import pickle
import pandas as pd
from pandas.core.frame import DataFrame
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
import joblib

motion_dict = {
    'still': 0,
    'low': 1,
    'high': 2,
    'none': 3
}

def get_mirro_data(data):
    width, height = data[:2]
    frame_x_center = width / 2
    y1, x1, y2, x2 = data[53:]
    x_center = (x2 - x1) / 2
    pose = []
    for i in range(17):
        x, y, prob = data[2+i*3:5+i*3]
        x = 2 * x_center - x
        pose += [x, y, prob]
    x1 = int(2 * frame_x_center - x1)
    x2 = int(2 * frame_x_center - x2)
    return [width, height] + pose + [y1, x1, y2, x2]

def get_train_data(mark_data, frame_data, data_length):
    if os.path.exists('motion_train_data_{}.pkl'.format(data_length)):
        with open('motion_train_data_{}.pkl'.format(data_length), 'rb') as f:
            (x, y) = pickle.load(f)
    else:
        mark_data = pd.read_csv(mark_data)
        frame_data = pd.read_csv(frame_data)
        size, _ = mark_data.shape
        x = []
        y = []
        for i in range(size):
            file_name = mark_data.iloc[i]['file_name']
            motion = motion_dict[mark_data.iloc[i]['motion']]
            fps = int(mark_data.iloc[i]['frame_rate'])
            video_frames = frame_data[frame_data['file_name']==file_name]
            # 采样间隔是1/8s，每一组数据采样1/2s，一共5帧
            sample_time_interval = 0.125
            frame_interval = fps * sample_time_interval
            frame_interval = frame_interval if frame_interval >= 1 else 1
            for i in range(len(video_frames)):
                if int(round(i + frame_interval * (data_length - 1))) >= len(video_frames):
                    break
                frames = []
                mirror_frames = []
                for j in range(data_length):
                    frame_number = int(round(i + j * frame_interval))
                    frame = video_frames[video_frames['frame_number']==frame_number]
                    x_data = np.array(frame)[0][2:].tolist()
                    frames += x_data
                    mirror_frames += get_mirro_data(x_data)
                    # print(x_data)
                    # print(get_mirro_data(x_data))
                    # break
                # break
                x.append(frames)
                y.append(motion)
                x.append(mirror_frames)
                y.append(motion)
            # break
        with open('motion_train_data_{}.pkl'.format(data_length), 'wb') as f:
            pickle.dump((x, y), f)
    # print(len(x), len(y))
    return x, y

def get_test_data(test_data, mark_data, data_length):
    mark_data = pd.read_csv(mark_data)
    test_data = pd.read_csv(test_data)
    size, _ = mark_data.shape
    test_group = []
    for i in range(size):
        file_name = mark_data.iloc[i]['file_name']
        fps = int(mark_data.iloc[i]['frame_rate'])
        video_frames = test_data[test_data['file_name']==file_name]
        # 采样间隔是1/8s，每一组数据采样1/2s，一共5帧
        sample_time_interval = 0.125
        frame_interval = fps * sample_time_interval
        frame_interval = frame_interval if frame_interval >= 1 else 1
        test_unit = []
        i = 0
        while i < len(video_frames):
            if int(round(i + frame_interval * (data_length - 1))) >= len(video_frames):
                break
            frames = []
            for j in range(data_length):
                frame_number = int(round(i + j * frame_interval))
                frame = video_frames[video_frames['frame_number']==frame_number]
                x_data = np.array(frame)[0][2:].tolist()
                frames += x_data
            test_unit.append(frames)
            i = int(round(i + frame_interval))
        test_group.append({
            'file_name': file_name,
            'test_unit': test_unit
        })
    return test_group

def tuning_model(data_length):
    frame_data = 'frame_data_fix.csv'
    mark_data = 'final v5.csv'
    x, y = get_train_data(mark_data, frame_data, data_length)
    print(len(x), len(y))
    # x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33)
            
    # param_test = { 'n_estimators': range(10, 71, 10) }
    param_test = {'max_depth':range(3,14,2), 'min_samples_split':range(50,201,20)}
    # # param_test = {'min_samples_split':range(2,45,3), 'min_samples_leaf':range(2,45,3)}
    rfc = RandomForestClassifier(n_estimators=40, min_samples_split=100, min_samples_leaf=20, max_depth=8, max_features='auto', random_state=10, n_jobs=8)
    gsearch = GridSearchCV(estimator=rfc, param_grid=param_test, scoring='f1_macro', cv=3, n_jobs=8)
    gsearch.fit(x, y)
    print(gsearch)
    # summarize the results of the grid search
    print(gsearch.best_score_)
    print(gsearch.best_params_)

def train_model(data_length):
    frame_data = 'frame_data_fix.csv'
    mark_data = 'final v5.csv'
    x, y = get_train_data(mark_data, frame_data, data_length)
    print(len(x), len(y))
    # x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33)
    rfc = RandomForestClassifier(oob_score=True, n_jobs=4)
    rfc.fit(x, y)
    # y_predict = rfc.predict(x_test)
    # target_names = ['stand', 'sit', 'walk', 'spin', 'none']
    # print(classification_report(y_test, y_predict, target_names=target_names))
    # rfr = RandomForestRegressor(n_estimators=110, min_samples_split=17,
    #                         min_samples_leaf=8, max_depth=17, max_features='auto', random_state=10)
    # # rfr = RandomForestRegressor(n_estimators=220, min_samples_split=32,
    # #                         min_samples_leaf=8, max_depth=13, max_features='auto', random_state=10)
    # # rfr = RandomForestRegressor()
    # rfr.fit(x, y)
    # y_predict = rfr.predict(x_test)
    # print(mean_squared_error(y_test, y_predict))
    # print(y_test - y_predict)
    # y_predict = rfr.predict(x)
    # print(mean_squared_error(y, y_predict))
    # print(y - y_predict)
    # print(y[4])
    # print(y_predict[4])
    joblib.dump(rfc, 'motion_rf.m')

def predict(test_data, test_meta, data_length):
    target_names = ['still', 'low', 'high', 'none']
    rfc = joblib.load('motion_rf.m')
    test_group = get_test_data(test_data, test_meta, data_length)
    for unit in test_group:
        file_name = unit['file_name']
        test_unit = unit['test_unit']
        test_result = pd.Series(rfc.predict(test_unit))
        # print(file_name, pd.value_counts(test_result))
        print(file_name, target_names[test_result.mode()[0]])
        print(pd.value_counts(test_result))
        print(np.array(test_result).tolist())

import tools.path_tool as pt

def load_model():
    import warnings
    # from sklearn.exceptions import UserWarning
    warnings.filterwarnings(action='ignore', category=UserWarning)
    modelPath = pt.get_path("motion_rf.m")
    rfc = joblib.load(modelPath)
    return rfc

if __name__ == "__main__":
    # data_roi_fix(frame_data)
    # tuning_model(4)
    train_model(4)
    # predict('daily_t.csv', 'daily_t_meta.csv', 2)
    # predict('dynamic.csv', 'dynamic_meta.csv', 2)
    # predict('daily.csv', 'daily_meta.csv', 2)




