import soundfile as sf
import librosa
import glob
import os

def stretch_audio_at_zero_crossings(input_file, output_file, stretch_factor=2):
    # 音声データ読み込み
    audio, sr = librosa.load(input_file, sr=None)

    # タイムストレッチ適用
    output_audio = librosa.effects.time_stretch(audio, rate=1.0/stretch_factor)

    # wavファイルを保存
    sf.write(output_file, output_audio, sr)

output_file = "output_stretched.wav"
stretch_factor = 5
dir_path = "./"

file_list = glob.glob(os.path.join(dir_path, ".wav"))

for input_file in file_list:
    stretch_audio_at_zero_crossings(input_file, output_file, stretch_factor)
