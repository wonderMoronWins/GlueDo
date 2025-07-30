from PyQt5.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QMessageBox, QFileDialog
)
from PyQt5.QtGui import QFont, QFontDatabase
from gui.widgets import DropArea
from core.binder import embed_file, extract_embedded, create_zip
import sys, os

def load_emoji_font():
    preferred_fonts = ["Segoe UI Emoji", "Apple Color Emoji", "Noto Color Emoji"]

    # Пробуем использовать системный emoji-шрифт
    for name in preferred_fonts:
        font = QFont(name, 16)
        if not font.family().startswith("."):
            return font

    # fallback — подгружаем из assets/fonts
    font_path = os.path.join(os.path.dirname(__file__), "..", "assets", "fonts", "NotoColorEmoji.ttf")
    if os.path.exists(font_path):
        font_id = QFontDatabase.addApplicationFont(font_path)
        families = QFontDatabase.applicationFontFamilies(font_id)
        if families:
            return QFont(families[0], 16)

    return QFont()  # если ничего не нашли — стандартный шрифт

def launch_gui():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("GlueDo")
    os.makedirs("output", exist_ok=True)
    os.makedirs("temp", exist_ok=True)

    left = DropArea("Left")
    right = DropArea("Right")

    emoji_font = load_emoji_font()

    green = QPushButton("➡️")
    green.setFont(emoji_font)

    red = QPushButton("⬅️")
    red.setFont(emoji_font)

    def save_dialog(path, suggested):
        target, _ = QFileDialog.getSaveFileName(window, "Save File", suggested)
        if target:
            with open(path, "rb") as fsrc, open(target, "wb") as fdst:
                fdst.write(fsrc.read())

    def handle_arrow(source: DropArea, target: DropArea, direction: str):
        src_files = source.file_paths
        tgt_files = target.file_paths

        if len(src_files) > 0 and len(tgt_files) > 0:
            hidden_path = src_files[0]
            if len(src_files) > 1:
                hidden_path = "temp/archive.zip"
                create_zip(src_files, hidden_path)
            for host_path in tgt_files:
                ext = os.path.splitext(host_path)[1]
                out_path = f"output/embedded_{os.path.basename(host_path)}"
                embed_file(host_path, hidden_path, out_path)
                save_dialog(out_path, os.path.basename(out_path))
            QMessageBox.information(window, "OK", f"Embedded into {len(tgt_files)} file(s).")
        elif len(src_files) > 0 and len(tgt_files) == 0:
            extracted = extract_embedded(src_files[0], "output/extracted")
            if extracted:
                target.file_paths = [extracted]
                target.list_widget.clear()
                target.list_widget.addItem(os.path.basename(extracted))
                target.button_save.setEnabled(True)
                target.button_save.clicked.connect(lambda: save_dialog(extracted, os.path.basename(extracted)))
            else:
                QMessageBox.warning(window, "Error", "FILE DOES NOT CONTAIN INFORMATION")
        else:
            QMessageBox.warning(window, "Error", "FILE IS EMPTY")

    green.clicked.connect(lambda: handle_arrow(left, right, "RIGHT"))
    red.clicked.connect(lambda: handle_arrow(right, left, "LEFT"))

    arrows = QVBoxLayout()
    arrows.addStretch()
    arrows.addWidget(green)
    arrows.addWidget(red)
    arrows.addStretch()

    layout = QHBoxLayout()
    layout.addWidget(left)
    layout.addLayout(arrows)
    layout.addWidget(right)

    window.setLayout(layout)
    window.resize(1000, 500)
    window.show()
    sys.exit(app.exec_())
