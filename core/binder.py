import os
import zipfile

MARKER = b"GLUEDO_SPLIT"

def embed_file(host_path, hidden_path, output_path):
    with open(host_path, "rb") as f1, open(hidden_path, "rb") as f2:
        data = f1.read() + MARKER + f2.read()
    with open(output_path, "wb") as out:
        out.write(data)

def extract_embedded(file_path, output_path_guess):
    with open(file_path, "rb") as f:
        data = f.read()
    if MARKER in data:
        idx = data.index(MARKER)
        hidden = data[idx + len(MARKER):]
        ext = guess_extension(hidden)
        final = output_path_guess + ext
        with open(final, "wb") as out:
            out.write(hidden)
        return final
    return None

def guess_extension(data):
    if data.startswith(b'\xFF\xD8\xFF'):
        return ".jpg"
    elif data.startswith(b'\x89PNG'):
        return ".png"
    elif data.startswith(b'%PDF'):
        return ".pdf"
    elif data.startswith(b'PK\x03\x04'):
        return ".zip"
    elif data.startswith(b'GIF87a') or data.startswith(b'GIF89a'):
        return ".gif"
    elif data.startswith(b'BM'):
        return ".bmp"
    elif data.startswith(b'RIFF') and b'WAVE' in data[8:16]:
        return ".wav"
    elif data.startswith(b'ID3') or data[0:2] in (b'\xFF\xFB', b'\xFF\xF3', b'\xFF\xF2'):
        return ".mp3"
    elif data[4:8] == b'ftyp':
        return ".mp4"
    elif data.startswith(b'<?xml'):
        return ".xml"
    elif data.startswith(b'{') and b'"' in data[:100]:
        return ".json"
    elif data[:4] == b'\x7fELF':
        return ".elf"
    elif data[:2] == b'MZ':
        return ".exe"
    elif is_probably_text(data):
        return ".txt"
    else:
        return ".bin"

def is_probably_text(data: bytes, threshold: float = 0.9) -> bool:
    if b'\x00' in data:
        return False  # null bytes mean it's binary
    try:
        text = data.decode('utf-8', errors='ignore')
        readable = sum(1 for c in text if c.isprintable())
        return (readable / len(text)) >= threshold if text else False
    except:
        return False

def create_zip(files, zip_path):
    with zipfile.ZipFile(zip_path, "w") as z:
        for file in files:
            z.write(file, arcname=os.path.basename(file))
