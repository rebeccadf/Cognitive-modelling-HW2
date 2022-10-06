from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QShortcut
from PyQt5 import uic, QtGui
import os
import sys
import random
import pandas as pd
from PIL import Image

class RatingGUI(QMainWindow):

    def __init__(self, rating_table):
        super(RatingGUI, self).__init__()
        uic.loadUi("ratingGUI0_8.ui", self)
        self.show()
        self.setWindowTitle("Cognitive Modelling HW2 - Rating experiment")
        self.setMinimumSize(600, 800)
        self.ratings = rating_table["rating"]
        self.file_list = rating_table["file"]
        self.file_counter = 0
        self.progressBar.setValue(0)
        self.current_file = self.file_list[self.file_counter]
        with Image.open("generated/" + self.current_file)as img:
            self.proportion = img.size[1] / img.size[0]
        self.update_image()
        self.label.setMinimumSize(1, 1)

        self.pushButton.clicked.connect(lambda: self.register_rating(1))
        self.pushButton_2.clicked.connect(lambda: self.register_rating(2))
        self.pushButton_3.clicked.connect(lambda: self.register_rating(3))
        self.pushButton_4.clicked.connect(lambda: self.register_rating(4))
        self.pushButton_5.clicked.connect(lambda: self.register_rating(5))
        self.pushButton_6.clicked.connect(lambda: self.register_rating(6))
        self.pushButton_7.clicked.connect(lambda: self.register_rating(7))
        self.pushButton_8.clicked.connect(lambda: self.register_rating(0))
        self.pushButton_9.clicked.connect(lambda: self.register_rating(8))

        self.actionPrevious_Image.triggered.connect(self.previous_image)
        self.actionSave.triggered.connect(self.save)
        self.actionContinue_from_save.triggered.connect(self.load_save)
        self.actionQuit.triggered.connect(self.quit_session)

        self.shortcut_1 = QShortcut("1", self)
        self.shortcut_1.activated.connect(lambda: self.register_rating(1))
        self.shortcut_2 = QShortcut("2", self)
        self.shortcut_2.activated.connect(lambda: self.register_rating(2))
        self.shortcut_3 = QShortcut("3", self)
        self.shortcut_3.activated.connect(lambda: self.register_rating(3))
        self.shortcut_4 = QShortcut("4", self)
        self.shortcut_4.activated.connect(lambda: self.register_rating(4))
        self.shortcut_5 = QShortcut("5", self)
        self.shortcut_5.activated.connect(lambda: self.register_rating(5))
        self.shortcut_6 = QShortcut("6", self)
        self.shortcut_6.activated.connect(lambda: self.register_rating(6))
        self.shortcut_7 = QShortcut("7", self)
        self.shortcut_7.activated.connect(lambda: self.register_rating(7))
        self.shortcut_8 = QShortcut("0", self)
        self.shortcut_8.activated.connect(lambda: self.register_rating(0))
        self.shortcut_9 = QShortcut("8", self)
        self.shortcut_9.activated.connect(lambda: self.register_rating(8))
    
    def get_dimensions(self):
        if self.width() * self.proportion < self.height() - 150:
            w = self.width()
            h = int(w * self.proportion)
        else:
            h = self.height() - 150
            w = int(h / self.proportion)
        return w, h
        
    def update_image(self):
        pixmap = QtGui.QPixmap("generated/" + self.current_file)
        w, h = self.get_dimensions()
        pixmap = pixmap.scaled(w, h)
        self.label.setPixmap(pixmap)

    def resizeEvent(self, event):
        try:
            pixmap = QtGui.QPixmap("generated/" + self.current_file)
            w, h = self.get_dimensions()
        except:
            pixmap = QtGui.QPixmap("generated/0.JPG")
            w, h = self.width(), self.height()
        pixmap = pixmap.scaled(w, h)
        self.label.setPixmap(pixmap)
        self.label.resize(w, h)
    
    def next_image(self):
        self.file_counter += 1
        self.progressBar.setValue(int(self.file_counter / len(self.file_list) * 100))
        if self.file_counter == len(self.file_list):
            self.save()
            self.file_counter -= 1
        self.current_file = self.file_list[self.file_counter]
        self.update_image()

    def previous_image(self):
        self.ratings.at[self.file_counter] = 0
        self.file_counter -= 1
        self.progressBar.setValue(int(self.file_counter / len(self.file_list) * 100))
        self.current_file = self.file_list[self.file_counter]
        self.update_image()
    
    def register_rating(self, rating):
        self.ratings.at[self.file_counter] = rating
        self.next_image()

    def save(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save file", "", "csv (*.csv)")
        if filename != "":
            rating_table = pd.concat([self.file_list, self.ratings], axis=1)
            rating_table.to_csv(filename)
    
    def load_save(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", "", "csv (*.csv)")
        if filename != "":
            try:
                rating_table = pd.read_csv(filename, index_col=0)
                self.ratings = rating_table["rating"]
                self.file_list = rating_table["file"]
                self.file_counter = self.ratings.idxmin() - 1
                self.next_image()
            except:
                print("Error: the selected file is not in the correct format")
    
    def quit_session(self):
        sys.exit()

def main():

    list_im = [f for f in os.listdir("generated") if not f.startswith('.')]
    list_im *= 10
    random.shuffle(list_im)
    rating_table = pd.DataFrame({"file": list_im,
                                 "rating": [0 for i in range(len(list_im))]
                                 })

    app = QApplication([])
    app.setStyle('Fusion')
    window = RatingGUI(rating_table)
    window.resize(600, 800)
    app.exec_()

if __name__ == "__main__":
    main()