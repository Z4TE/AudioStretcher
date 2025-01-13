import soundfile as sf
import numpy as np

def stretch_audio(input_file, output_file, stretch_factor=2):
    # 音声データを読み込む
    data, samplerate = sf.read(input_file)
    
    # モノラルかステレオかを判定
    is_stereo = len(data.shape) == 2
    if is_stereo:
        # ステレオの場合、各チャンネルを別々に処理する
        audio = data[:, 0]
    else:
        audio = data

    # 音量が0の箇所を検出
    silence_threshold = 1e-4  # 音量0と見なす閾値
    silence_positions = np.where(np.abs(audio) < silence_threshold)[0]
    
    # 無音区間の開始位置と終了位置を特定
    silence_intervals = []
    if len(silence_positions) > 0:
        start = silence_positions[0]
        for i in range(1, len(silence_positions)):
            if silence_positions[i] != silence_positions[i - 1] + 1:
                end = silence_positions[i - 1]
                silence_intervals.append((start, end))
                start = silence_positions[i]
        silence_intervals.append((start, silence_positions[-1]))

    # 各無音区間間のセグメントを複製して引き伸ばし
    new_audio = []
    prev_end = 0
    for start, end in silence_intervals:
        # 無音区間までの音声を追加
        new_audio.append(audio[prev_end:start])
        
        # 無音区間を含むセグメントを複製
        segment = audio[prev_end:end + 1]
        new_audio.extend([segment] * stretch_factor)
        
        prev_end = end + 1

    # 最後のセグメントを追加
    new_audio.append(audio[prev_end:])
    
    # 音声データを結合
    new_audio = np.concatenate(new_audio)
    
    # ステレオに戻す
    if is_stereo:
        new_audio = np.column_stack([new_audio, new_audio])
    
    # 新しい音声データを保存
    sf.write(output_file, new_audio, samplerate)

# 使用例
input_file = "input.wav"
output_file = "output_stretched.wav"
stretch_factor = 3  # 複製回数
stretch_audio(input_file, output_file, stretch_factor)
