import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from constants import *
import os

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

        self.setCentralWidget(self.scroll)

    def refresh(self):
        self.updateTracks()

    def chooseTrack(self, over):

        selector = TrackSelector()

        if selector.ct:
            tracks [over] = selector.ct
        else:
            tracks.pop(over)

        self.refresh()



class TrackSelector(QDialog):
    def __init__(self):
        super().__init__()

        self.ct = None

        self.initUI(True)

    def getTracks(self):
        path = os.getcwd()

        cts = []

        for file in os.listdir(f"{path}/Courses"):
            cts.append(file)

        return cts

    def refresh(self):
        l = self.layout()
        widget = l.takeAt(0)
        while widget:
            l.removeWidget(widget.widget())
            widget = l.takeAt(0)

        self.initUI()

    def callback(self, track):
        self.ct = track
        self.refresh()


    def accept(self):
        if self.ct == None:
            return

        super().accept()

    def reject(self):
        self.ct = None
        super().reject()

    def initUI(self, first=False):

        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(50, 50, 50))
        self.setPalette(p)

        self.widget = QWidget()

        layout = QVBoxLayout()

        for track in self.getTracks():
            name = QLabel(self)
            if self.ct == track:
                name.setStyleSheet("background-color: #aaaaaa")
            name.mouseReleaseEvent = (lambda x: lambda y: self.callback(x))(track)
            name.setText(track)
            name.show()

            layout.addWidget(name)

        self.widget.setLayout(layout)

        self.scroll = QScrollArea()
        self.scroll.setWidget(self.widget)

        if first:
            self.mainLayout = QVBoxLayout()
            self.setLayout(self.mainLayout)

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

main()