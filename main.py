import soundfile as sf
import librosa

def stretch_audio_at_zero_crossings(input_file, output_file, stretch_factor=2):
    # 音声データ読み込み
    audio, sr = librosa.load(input_file, sr=None)

    # タイムストレッチ適用
    output_audio = librosa.effects.time_stretch(audio, rate=1.0/stretch_factor)

    # wavファイルを保存
    sf.write(output_file, output_audio, sr)

input_file = "test.wav"
output_file = "output_stretched.wav"
stretch_factor = 5
stretch_audio_at_zero_crossings(input_file, output_file, stretch_factor)
