from typing import List, Dict

def chunk_segments(segments: List[Dict], max_chars=500, overlap_chars=80):
    chunks = []
    buf = ""
    start = None
    end = None
    for seg in segments:
        t = seg["text"]
        s = seg["start"]
        e = seg["end"]
        if start is None:
            start = s
        if len(buf) + len(t) + 1 <= max_chars:
            buf = (buf + " " + t).strip()
            end = e
        else:
            chunks.append({"text": buf, "start": start, "end": end})
            cut = buf[-overlap_chars:] if len(buf) > overlap_chars else buf
            buf = (cut + " " + t).strip()
            start = end
            end = e
    if buf:
        chunks.append({"text": buf, "start": start, "end": end})
    return chunks