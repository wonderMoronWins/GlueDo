import os
import zipfile
from core.filetype_detector import guess_extension

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

def create_zip(files, zip_path):
    with zipfile.ZipFile(zip_path, "w") as z:
        for file in files:
            z.write(file, arcname=os.path.basename(file))
