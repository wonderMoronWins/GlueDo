def guess_extension(data: bytes) -> str:
    if data.startswith(b'\xFF\xD8\xFF'):
        return ".jpg"
    elif data.startswith(b'\x89PNG'):
        return ".png"
    elif data.startswith(b'%PDF'):
        return ".pdf"
    elif data.startswith(b'PK\x03\x04'):
        return ".zip"  # или docx/xlsx/pptx — уточняется позже
    elif data.startswith(b'GIF87a') or data.startswith(b'GIF89a'):
        return ".gif"
    elif data.startswith(b'BM'):
        return ".bmp"
    elif data.startswith(b'RIFF') and b'WAVE' in data[8:16]:
        return ".wav"
    elif data.startswith(b'fLaC'):
        return ".flac"
    elif data.startswith(b'OggS'):
        return ".ogg"
    elif data[4:8] == b'ftyp':
        return ".mp4"
    elif data.startswith(b'\x1A\x45\xDF\xA3'):
        return ".webm"
    elif data.startswith(b'7z\xBC\xAF\x27\x1C'):
        return ".7z"
    elif data.startswith(b'Rar!\x1A\x07\x00'):
        return ".rar"
    elif data.startswith(b'\x1F\x8B'):
        return ".gz"
    elif data.startswith(b'ID3') or data[0:2] in (b'\xFF\xFB', b'\xFF\xF3', b'\xFF\xF2'):
        return ".mp3"
    elif data.startswith(b'<?xml'):
        return ".xml"
    elif b'<svg' in data[:300]:
        return ".svg"
    elif data.startswith(b'{') and b'"' in data[:100]:
        return ".json"
    elif b'{\\rtf' in data[:100]:
        return ".rtf"
    elif data[:4] == b'\x7FELF':
        return ".elf"
    elif data[:2] == b'MZ':
        return ".exe"
    elif is_probably_text(data):
        return ".txt"
    else:
        return ".bin"

def is_probably_text(data: bytes, threshold: float = 0.9) -> bool:
    if b'\x00' in data:
        return False  # null bytes → бинарник
    try:
        text = data.decode('utf-8', errors='ignore')
        readable = sum(1 for c in text if c.isprintable())
        return (readable / len(text)) >= threshold if text else False
    except:
        return False
