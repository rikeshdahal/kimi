import sys
import urllib.request
import json
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton
from PyQt5.QtGui import QPixmap
from urllib.parse import quote


class ImageSearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Search App")
        self.layout = QVBoxLayout()
        self.search_box = QLineEdit()
        self.search_button = QPushButton("Search")
        self.result_label = QLabel()
        self.layout.addWidget(self.search_box)
        self.layout.addWidget(self.search_button)
        self.layout.addWidget(self.result_label)
        self.setLayout(self.layout)

        self.search_button.clicked.connect(self.search_image)

    def search_image(self):
        query = self.search_box.text()
        if query:
            try:
                encoded_query = quote(query)
                search_url = f"https://www.googleapis.com/customsearch/v1?key=AIzaSyAuVDszlW7809n8JXeRQ_rgMy2wLvgb5rI&cx=158a408d737fc46f5&q={encoded_query}&searchType=image"
                response = urllib.request.urlopen(search_url)
                data = json.loads(response.read())
                # Get the URL of the first image result
                image_url = data["items"][0]["link"]
                image_data = urllib.request.urlopen(image_url).read()
                pixmap = QPixmap()
                pixmap.loadFromData(image_data)
                self.result_label.setPixmap(pixmap)
            except Exception as e:
                self.result_label.setText(f"Error: {str(e)}")
        else:
            self.result_label.setText("Please enter a search query.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageSearchApp()
    window.show()
    sys.exit(app.exec_())
