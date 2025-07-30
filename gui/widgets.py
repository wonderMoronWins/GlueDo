from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import os

class DropArea(QWidget):
    def __init__(self, label_text="Drop File"):
        super().__init__()
        self.setAcceptDrops(True)
        self.file_paths = []
        self.label = QLabel("Drop file(s) here")
        self.label.setAlignment(Qt.AlignCenter)

        self.button_add = QPushButton("Add Files")
        self.button_add.clicked.connect(self.browse_files)

        self.button_clear = QPushButton("Clean")
        self.button_clear.clicked.connect(self.clear_files)

        self.button_save = QPushButton("Save")
        self.button_save.setEnabled(False)

        self.list_widget = QListWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button_add)
        layout.addWidget(self.button_clear)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.button_save)
        self.setLayout(layout)

    def update_list(self):
        self.list_widget.clear()
        for path in self.file_paths:
            item = QListWidgetItem(os.path.basename(path))
            icon = QIcon(path)
            item.setIcon(icon)
            self.list_widget.addItem(item)
        if not self.file_paths:
            self.label.setText("Drop file(s) here")
        else:
            self.label.setText("")

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                path = url.toLocalFile()
                if path and path not in self.file_paths:
                    self.file_paths.append(path)
        self.update_list()

    def browse_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files")
        for file in files:
            if file and file not in self.file_paths:
                self.file_paths.append(file)
        self.update_list()

    def clear_files(self):
        self.file_paths = []
        self.list_widget.clear()
        self.label.setText("Drop file(s) here")
        self.button_save.setEnabled(False)
