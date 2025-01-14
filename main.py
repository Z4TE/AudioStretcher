import soundfile as sf
import numpy as np

def stretch_audio_at_zero_crossings(input_file, output_file, stretch_factor=2):
    # 音声データを読み込む
    data, samplerate = sf.read(input_file)
    
    # モノラルかステレオかを判定
    is_stereo = len(data.shape) == 2
    if is_stereo:
        # ステレオの場合、各チャンネルを別々に処理する
        audio = data[:, 0]
    else:
        audio = data

    # ゼロクロスを検出
    zero_crossings = np.where(np.diff(np.sign(audio)) != 0)[0]

    # ゼロクロス地点で音声を区間ごとに分けて複製
    new_audio = []
    prev_crossing = 0
    for crossing in zero_crossings:
        # 区間を取得
        segment = audio[prev_crossing:crossing]
        # 複製
        new_audio.extend([segment] * stretch_factor)
        prev_crossing = crossing

    # 最後の区間を追加
    new_audio.append(audio[prev_crossing:])
    
    # 音声データを結合
    new_audio = np.concatenate(new_audio)
    
    # ステレオに戻す
    if is_stereo:
        new_audio = np.column_stack([new_audio, new_audio])
    
    # 新しい音声データを保存
    sf.write(output_file, new_audio, samplerate)

input_file = "test.wav"
output_file = "output_stretched.wav"
stretch_factor = 3
stretch_audio_at_zero_crossings(input_file, output_file, stretch_factor)
