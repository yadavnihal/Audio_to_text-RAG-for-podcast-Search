import os
import librosa
import noisereduce as nr
import soundfile as sf
from faster_whisper import WhisperModel

def denoise(path):
    y, sr = librosa.load(path, sr=16000, mono=True)
    y = nr.reduce_noise(y=y, sr=sr)
    tmp = path + ".clean.wav"
    sf.write(tmp, y, sr)
    return tmp

def transcribe_episode(audio_path, model_size="small", beam_size=5):
    clean = denoise(audio_path)
    model = WhisperModel(model_size, compute_type="int8")
    segments, info = model.transcribe(clean, beam_size=beam_size, vad_filter=True)
    out = []
    for s in segments:
        out.append({"text": s.text.strip(), "start": float(s.start), "end": float(s.end)})
    try:
        os.remove(clean)
    except Exception:
        pass
    return out