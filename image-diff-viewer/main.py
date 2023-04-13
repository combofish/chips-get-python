import os
import sys

from PyQt5.QtWidgets import QWidget, QApplication, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap

from form import Ui_Form


class QMyWidget(QWidget):
    def __init__(self):
        super(QMyWidget, self).__init__()
        self.__ui = Ui_Form()
        self.__ui.setupUi(self)

        self.__ui.prev_btn_1.setText('prev')
        self.__ui.prev_btn_2.setText('prev')
        self.__ui.next_btn_1.setText('next')
        self.__ui.next_btn_3.setText('next')
        self.__ui.enter_btn_1.setText('enter')
        self.__ui.enter_btn_2.setText('enter')
        self.__ui.exit_btn.setText('exit')
        self.__ui.exit_btn.setShortcut('Ctrl-Q')
        self.__ui.exit_btn.clicked.connect(self.close)

        self.load_path_1 = ""
        self.load_path_2 = ""

        # for test
        self.load_path_1 = '/home/larry/文档/论文显著性图/MoLF/LFSD/'
        self.load_path_2 = '/home/larry/文档/论文显著性图/MoLF/HFUT/'

        self.__ui.enter_btn_1.clicked.connect(self.enter_press)
        self.__ui.enter_btn_2.clicked.connect(self.enter_press)

        self.__ui.prev_btn_1.clicked.connect(self.show_prev)
        self.__ui.prev_btn_2.clicked.connect(self.show_prev)
        self.__ui.next_btn_1.clicked.connect(self.show_next)
        self.__ui.next_btn_3.clicked.connect(self.show_next)

        self.img_path_list_1 = []
        self.img_path_list_2 = []

        self.show_number_per_line = 6

        self.name_lab_up = generate_q_labels(
            self.show_number_per_line,
            self.__ui.gridLayout_lab_1
        )
        self.name_lab_down = generate_q_labels(
            self.show_number_per_line,
            self.__ui.gridLayout_lab_2
        )
        self.name_img_up = generate_q_labels(
            self.show_number_per_line,
            self.__ui.gridLayout_img_1
        )
        self.name_img_down = generate_q_labels(
            self.show_number_per_line,
            self.__ui.gridLayout_img_2
        )

        # for test
        self.img_path_list_1 = load_img_path(self.load_path_1)
        self.img_path_list_2 = load_img_path(self.load_path_2)

        self.show_id_1 = 0
        self.show_id_2 = 0

        self.show_img_and_lab()

    def show_img_and_lab(self):
        len1 = len(self.img_path_list_1)
        if len1 != 0:
            print('proc 1', self.img_path_list_1)

            show_img_and_lab_with_id(
                self.name_lab_up,
                self.name_img_up,
                self.show_id_1,
                self.show_number_per_line,
                self.img_path_list_1
            )

        len2 = len(self.img_path_list_2)
        if len2 != 0:
            print("proc 2", self.img_path_list_2)

            show_img_and_lab_with_id(
                self.name_lab_down,
                self.name_img_down,
                self.show_id_2,
                self.show_number_per_line,
                self.img_path_list_2
            )

    def show_next(self):
        sender = self.sender()
        if sender == self.__ui.next_btn_1:
            if self.show_id_1 + 1 < len(self.img_path_list_1):
                self.show_id_1 = self.show_id_1 + 1
            else:
                self.show_id_1 = 0
        elif sender == self.__ui.next_btn_3:
            if self.show_id_2 + 1 < len(self.img_path_list_2):
                self.show_id_2 = self.show_id_2 + 1
            else:
                self.show_id_2 = 0

        self.show_img_and_lab()

    def show_prev(self):
        sender = self.sender()
        if sender == self.__ui.prev_btn_1:
            if self.show_id_1 - 1 >= 0:
                self.show_id_1 = self.show_id_1 - 1
            else:
                self.show_id_1 = len(self.img_path_list_1) - 1

        elif sender == self.__ui.prev_btn_2:
            if self.show_id_2 - 1 > 0:
                self.show_id_2 = self.show_id_2 - 1
            else:
                self.show_id_2 = len(self.img_path_list_2) - 1

        self.show_img_and_lab()

    def enter_press(self):
        """ enter btn pressed """
        sender = self.sender()
        if sender == self.__ui.enter_btn_1:
            self.load_path_1 = self.__ui.lineEdit.text()
            print("enter_btn_1 pressed: ", self.load_path_1)
            self.img_path_list_1 = load_img_path(self.load_path_1)
            self.show_id_1 = 0
            self.show_img_and_lab()

        elif sender == self.__ui.enter_btn_2:
            self.load_path_2 = self.__ui.lineEdit_2.text()
            print("enter_btn_2 pressed: ", self.load_path_2)
            self.img_path_list_2 = load_img_path(self.load_path_2)
            self.show_id_2 = 0
            self.show_img_and_lab()


def show_img_and_lab_with_id(name_labs, img_labs, idx, numbers, src):
    len1 = len(src)
    for i in range(numbers):
        if idx + i < len1:
            name_labs[i].setAlignment(Qt.AlignCenter)
            name_labs[i].setText(src[i + idx][0])

            img_labs[i].clear()
            img_labs[i].setPixmap(
                QPixmap.fromImage(
                    QImage(
                        src[i + idx][1]
                    )
                )
            )
            img_labs[i].setScaledContents(True)
        else:
            name_labs[i].setText('---')
            img_labs[i].clear()
            img_labs[i].setText('---')


def generate_q_labels(numbers, widget):
    """ generate labels for show """
    positions = [(0, j) for j in range(numbers)]

    q_labels = []
    for position in positions:
        lab = QLabel('--')
        q_labels.append(lab)
        widget.addWidget(lab, *position)

    return q_labels


def load_img_path(img_path):
    img_paths = []
    for file in os.listdir(img_path):
        if file.endswith('png') or file.endswith('jpg'):
            img_paths.append([file, os.path.join(img_path, file)])

    return img_paths


def main():
    app = QApplication(sys.argv)
    my_widget = QMyWidget()
    my_widget.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
