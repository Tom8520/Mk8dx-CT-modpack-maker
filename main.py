import random
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from constants import *
import os
import json
import datetime
import compile

global tracks
tracks = {}

class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(50, 50, 50))
        self.setPalette(p)

        QToolTip.setFont(QFont('SansSerif', 10))

        self.updateTracks()

        self.setGeometry(300, 300, 1600, 1000)
        self.setWindowTitle('Mk8dx Modpack Maker')
        self.show()

    def updateTracks(self):
        self.mainWidget = QWidget(self)
        self.mainLayout = QVBoxLayout()

        self.layout = QGridLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(10)

        for i in range(len(TRACK_NAMES) + 12):
            if i % 5 == 0:
                pic = QLabel(self)
                pic.setContentsMargins(40, 0, 40, 0)
                pic.setPixmap(QPixmap(f"assets/cups/cup_{i//5}.png"))
                pic.show()
            else:
                name = QLabel(self)
                pic = QLabel(self)
                name.setFont(QFont('SansSerif', 20))
                name.setStyleSheet("color: #bbbbbb")

                if not CUP_TRACKS [CUPS [i//5]][i%5-1] in tracks:
                    name.setText(CUP_TRACKS [CUPS [i//5]][i%5-1])
                    pic.setPixmap(QPixmap("assets/NoTrackSelected.png"))
                else:
                    name.setText(tracks [CUP_TRACKS [CUPS [i//5]][i%5-1]])
                    pic.setPixmap(QPixmap(f"Courses/{tracks [CUP_TRACKS[CUPS[i // 5]][i % 5 - 1]]}/icon.jpg").scaled(300, 200))

                pic.mouseReleaseEvent = (lambda x: lambda y: self.chooseTrack(x))(CUP_TRACKS [CUPS [i//5]][i%5-1])
                pic.show()
                name.show()

                self.layout.addWidget(name, 2 * (i // 5) + 1, i % 5)

            self.layout.addWidget(pic, 2 * (i//5), i%5)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.scroll = QScrollArea()

        self.scroll.setWidget(self.widget)

        self.bottomMenu = QWidget(self)
        self.bottomMenuLayout = QHBoxLayout()

        self.compileButton = QPushButton("Compile", self)
        self.compileButton.clicked.connect(self.compileModpack)
        self.bottomMenuLayout.addWidget(self.compileButton)

        self.randomiseButton = QPushButton("Randomise", self)
        self.randomiseButton.clicked.connect(self.randomise)
        self.bottomMenuLayout.addWidget(self.randomiseButton)

        self.resetButton = QPushButton("Reset", self)
        self.resetButton.clicked.connect(self.reset)
        self.bottomMenuLayout.addWidget(self.resetButton)

        self.bottomMenu.setLayout(self.bottomMenuLayout)

        self.mainLayout.addWidget(self.scroll)
        self.mainLayout.addWidget(self.bottomMenu)

        self.mainWidget.setLayout(self.mainLayout)

        self.setCentralWidget(self.mainWidget)

    def getTrackIndex(self, track):
        i = 0
        for key, val in CUP_TRACKS.items():
            for t in range(len(val)):
                if val [t] == track:
                    return i + 2*t + 1
            i += 9
        return -1

    def refresh(self, over, ct):
        index = self.getTrackIndex(over)

        name = self.layout.itemAt(index).widget()
        img = self.layout.itemAt(index+1).widget()

        if ct is None:
            name.setText(over)
            img.setPixmap(QPixmap("assets/NoTrackSelected.png"))
        else:
            name.setText(ct)
            img.setPixmap(QPixmap(f"Courses/{ct}/icon.jpg").scaled(300, 200))

    def chooseTrack(self, over):

        selector = TrackSelector()

        if selector.ct:
            tracks [over] = selector.ct
        else:
            if over in tracks:
                tracks.pop(over)

        self.refresh(over, selector.ct)

    def randomise(self):
        path = os.getcwd()

        cts = os.listdir(f"{path}/Courses")

        random.shuffle(cts)

        for cup, trks in CUP_TRACKS.items():
            for trk in trks:
                tracks [trk] = cts [0]
                self.refresh(trk, cts [0])
                cts.pop(0)

    def reset(self):
        for cup, trks in CUP_TRACKS.items():
            for trk in trks:
                self.refresh(trk, None)

    def compileModpack(self):

        text, ok = QInputDialog.getText(self, 'Compile modpack',
                                        'Enter the modpack name:')

        if not ok:
            return

        trks = []
        for key, val in tracks.items():
            trks.append([val, NAME_TO_TRACK [key]])

        compile.compile(os.getcwd(), trks, text)



class TrackSelector(QDialog):
    def __init__(self):
        super().__init__()

        self.ct = None

        self.cts = self.getTracks()

        self.initUI(True)

    def getTracks(self):
        path = os.getcwd()

        cts = []

        for file in os.listdir(f"{path}/Courses"):
            data = json.loads(open(f"{path}/Courses/{file}/data.json", "r").read())
            cts.append([file, data ["Creator"], data ["Audio"], data ["UI"], data ["Released"]])

        return cts

    def refresh(self, ct):
        index = 5 * self.cts.index(ct)

        for x in range(self.layout.count()):
            w = self.layout.itemAt(x).widget()
            w.setStyleSheet("background-color: #aaaaaa" if x >= index and x < index+5 else "color: #dddddd")

    def callback(self, track):
        self.ct = track [0]
        self.refresh(track)


    def accept(self):
        if self.ct == None:
            return

        super().accept()

    def reject(self):
        self.ct = None
        super().reject()

    def sort(self, field):
        if field == 4:
            key = lambda i: datetime.datetime.strptime(i [4], "%d/%m/%Y")
        else:
            key = lambda i: i [field]

        self.cts = sorted(self.cts, key=key)

        for x in range(self.headerLayout.count()):
            w = self.headerLayout.itemAt(x).widget()
            w.setStyleSheet("background-color: #aaaaaa" if x == field else "color: #dddddd")

        for x in range(self.layout.count()):
            self.layout.removeWidget(self.layout.itemAt(0).widget())

        i = 0
        for track in self.cts:
            for j in range(5):
                name = QLabel(self)
                name.setStyleSheet("color: #dddddd")
                name.mouseReleaseEvent = (lambda x: lambda y: self.callback(x))(track)

                text = track[j]
                while len(text) < 35:
                    text += " "

                if len(text) > 35:
                    text = text[:35]

                name.setText(text)
                name.show()

                self.layout.addWidget(name, i, j)

            i += 1

    def initUI(self, first=False):

        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(50, 50, 50))
        self.setPalette(p)

        self.widget = QWidget()

        self.layout = QGridLayout()

        i = 0
        for track in self.cts:
            for j in range(5):
                name = QLabel(self)
                name.setStyleSheet("color: #dddddd")
                name.mouseReleaseEvent = (lambda x: lambda y: self.callback(x))(track)

                text = track [j]
                while len(text) < 35:
                    text += " "

                if len(text) > 35:
                    text = text [:35]

                name.setText(text)
                name.show()

                self.layout.addWidget(name, i, j)

            i += 1

        self.widget.setLayout(self.layout)

        self.scroll = QScrollArea()
        self.scroll.setWidget(self.widget)

        if first:
            self.mainLayout = QVBoxLayout()
            self.setLayout(self.mainLayout)

        self.headerRow = QWidget()
        self.headerLayout = QHBoxLayout()

        for text in ["Name", "Creator", "Custom music", "UI", "Release date"]:
            name = QLabel(self)
            name.setText(text)
            name.setStyleSheet("color: #dddddd")
            name.mouseReleaseEvent = (lambda x: lambda y: self.sort(x))(["Name", "Creator", "Custom music", "UI", "Release date"].index(text))
            name.show()

            self.headerLayout.addWidget(name)

        self.headerRow.setLayout(self.headerLayout)

        self.mainLayout.addWidget(self.headerRow)
        self.mainLayout.addWidget(self.scroll)
        self.mainLayout.addWidget(self.buttonBox)

        if first:
            self.setFixedWidth(800)
            self.setFixedHeight(500)

            self.exec()






def main():

    app = QApplication(sys.argv)

    main = Main()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()