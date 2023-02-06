import os
from os.path import join
from pathlib import Path

import subprocess as sp
from tempfile import mktemp
import speech_recognition as sr
from os import path
from pydub import AudioSegment

SCRIPT_PARENT_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
TEMP_WORKING_AUDIO_CLIPS_DIR_PATH = join(SCRIPT_PARENT_DIR_PATH, "TMP_WRK_AUDIO_CLIPS")


def get_audio_from_video(in_vid_path, out_audio_path):
    ''' Returns .wav file, no spaces in path, will overwrite '''

    cmd = 'ffmpeg -i ' + in_vid_path + ' -acodec pcm_s16le -ac 2 ' + out_audio_path + ' -y'
    sp.call(cmd, shell = False)


def get_audio_duration(in_audio_path):
    ''' Takes .wav file, no spaces in path '''

    cmd = 'ffprobe -i ' + in_audio_path + ' -show_entries format=duration -v quiet -of csv="p=0"'
    d = sp.check_output(cmd, shell = False)
    return float(d)


def clip_audio(in_audio_path, clipped_audio_path, start_time, end_time):
    ''' Takes .wav file, no spaces in path, will overwrite '''

    cmd = 'ffmpeg -i ' + in_audio_path + ' -ss ' + str(start_time) + ' -to ' + str(end_time) + ' -c copy ' + clipped_audio_path + ' -y'
    sp.call(cmd, shell = False)


def transcribe_audio(in_audio_path, with_confidence = False):
    ''' Returns False if there is no speech in audio '''
    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(in_audio_path) as source:
            audio = r.record(source)  # read the entire audio file
    try:
        return r.recognize_google(audio, with_confidence = with_confidence)
    except sr.UnknownValueError:
        return False
    

def get_transcript_from_vid(in_vid_path, start_time = 0, end_time = None, with_confidence = False):
    Path(TEMP_WORKING_AUDIO_CLIPS_DIR_PATH).mkdir(parents=True, exist_ok=True)
    tmp_whole_vid_audio_wav_path = mktemp(prefix = TEMP_WORKING_AUDIO_CLIPS_DIR_PATH + os.path.sep, suffix=f"_whole_tmp.wav")
    print(f"{tmp_whole_vid_audio_wav_path=}")
    get_audio_from_video(in_vid_path, tmp_whole_vid_audio_wav_path)

    transcript_str = None
    if end_time == None:
        transcript_str = transcribe_audio(tmp_whole_vid_audio_wav_path, with_confidence)
    else:
        tmp_clip_vid_audio_wav_path = mktemp(prefix = TEMP_WORKING_AUDIO_CLIPS_DIR_PATH + os.path.sep, suffix=f"_clip_tmp.wav")
        clip_audio(tmp_whole_vid_audio_wav_path, tmp_clip_vid_audio_wav_path, start_time, end_time)
        transcript_str = transcribe_audio(tmp_clip_vid_audio_wav_path, with_confidence)
        os.remove(tmp_clip_vid_audio_wav_path)

    os.remove(tmp_whole_vid_audio_wav_path)

    return transcript_str


if __name__ == '__main__':
    import os.path as path
    print("Running ",  path.abspath(__file__),  '...')
    # t = get_transcript_from_vid("C:/p/tik_tb_vid_big_data/ignore/BIG_BOY_fg_TBS/Family_Guy___TBS/Family_Guy__National_Dog_Day__Clip____TBS/Family_Guy__National_Dog_Day__Clip____TBS.mp4",
    #                          start_time = 0, end_time = None)
    # print(t)


    # get_audio_from_video("C:/p/tik_tb_vid_big_data/ignore/BIG_BOY_fg_TBS/Family_Guy___TBS/Family_Guy__National_Dog_Day__Clip____TBS/Family_Guy__National_Dog_Day__Clip____TBS.mp4",
    # "C:/p/tik_tb_vid_big_data/ignore/BIG_BOY_fg_TBS/Family_Guy___TBS/Family_Guy__National_Dog_Day__Clip____TBS/whole.wav")

    # clip_audio(in_audio_path = "C:/p/tik_tb_vid_big_data/ignore/BIG_BOY_fg_TBS/Family_Guy___TBS/Family_Guy__National_Dog_Day__Clip____TBS/whole.wav",
    #             clipped_audio_path = "C:/p/tik_tb_vid_big_data/ignore/BIG_BOY_fg_TBS/Family_Guy___TBS/Family_Guy__National_Dog_Day__Clip____TBS/clip.wav",
    #              start_time=0, end_time=1.369)

    # t = transcribe_audio("C:/p/tik_tb_vid_big_data/ignore/BIG_BOY_fg_TBS/Family_Guy___TBS/Family_Guy__National_Dog_Day__Clip____TBS/clip.wav")
    # print(f"{t=}")

    t,c = get_transcript_from_vid("C:/p/tik_tb_vid_big_data/ignore/BIG_BOY_fg_TBS/Family_Guy___TBS/Family_Guy__National_Dog_Day__Clip____TBS/Family_Guy__National_Dog_Day__Clip____TBS.mp4",
                            0, 1.369, with_confidence = True)
    print(t)
    print(c)

    print("End of Main")
