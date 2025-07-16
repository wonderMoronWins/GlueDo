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
    elif data.startswith(b'ID3') or data[0:2] == b'\xFF\xFB':
        return ".mp3"
    else:
        return ".bin"

def create_zip(files, zip_path):
    with zipfile.ZipFile(zip_path, "w") as z:
        for file in files:
            z.write(file, arcname=os.path.basename(file))
