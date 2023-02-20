import os
import cv2
import cut
import choose
import uuid
import analyze as aly
import moviepy.editor as mpe

def get_video_writer_by_vshot(file_path, video, compress=False):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # fourcc = 0x00000020 # Unknown Fourcc, just know opencv would fallback to this
    fps = video.fps
    width = video.width
    height = video.height
    if compress:
        width = int((width + 1) / 2)
        height = int((height + 1) / 2)
    writer = cv2.VideoWriter(file_path, fourcc, fps, (width, height))
    return writer

def gen_shot_line_video(file_path, music_path, shot_line, compress=False):
    vshots = shot_line.vshots
    temp_video_name = 'temp-{}.mp4'.format(uuid.uuid4())
    writer = get_video_writer_by_vshot(temp_video_name, vshots[0].video, compress)
    for vshot in vshots:
        start_frame = vshot.video.frames[vshot.start]
        end_frame = vshot.video.frames[vshot.end - 1]
        tshot = vshot.tshot

        total_frame_count = int(round(tshot.video.frame_count * vshot.video.fps / tshot.video.fps))

        over_count = total_frame_count - (end_frame.frame_number - start_frame.frame_number)
        start_frame_number = 0 if round(start_frame.frame_number - over_count / 2) < 0 else round(start_frame.frame_number - over_count / 2)
        end_frame_number = round(start_frame_number + total_frame_count)
        cap = cv2.VideoCapture(vshot.video.path)
        print('[ REND ]', vshot.video.name, start_frame_number, end_frame_number)
        frame_count = start_frame_number
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame_number)
        while cap.isOpened():
            ret, frame = cap.read()
            if ret is True:
                if frame_count >= end_frame_number:
                    break
                if start_frame_number <= frame_count < end_frame_number:
                    if compress:
                        frame = cv2.pyrDown(frame)
                    writer.write(frame)
                frame_count += 1
            else:
                break
        cap.release()
    writer.release()
    my_clip = mpe.VideoFileClip(temp_video_name)
    audio_background = mpe.AudioFileClip(music_path)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(file_path)
    if os.path.exists(temp_video_name):
        os.remove(temp_video_name)

if __name__ == "__main__":
    template_path = 'new_templates/taobao-0'
    tshots = aly.load_shots(template_path)
    videos_path = 'uploads/videos/compare-1'
    videos = aly.load_videos(videos_path, 4)
    shot_groups = cut.get_shot_groups(tshots, videos)
    shot_lines = choose.get_best_shot_lines(shot_groups)
    best_shot_line = shot_lines[0]
    file_path = 'render-ouput.mp4'
    music_path = os.path.join(template_path, 'music.mp3')
    gen_shot_line_video(file_path, music_path, best_shot_line)