import sys

import numpy as np
import sympy
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from matplotlib import pyplot as plt

from extra_file import Ui_MainWindow
from agent import agent


class mywindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.StartBtn.clicked.connect(self.start)
        self.Slider.valueChanged.connect(self.slide)
        self.StopBtn.setVisible(False)
        self.count = 0

    def start(self):
        A = int(self.AEdit.toPlainText())
        B = int(self.BEdit.toPlainText())
        D = int(self.DEdit.toPlainText())
        tp = self.TypeBox.currentText()
        countpop = self.CountPopSB.value()
        strengMut = float(self.MutStrange.toPlainText())
        chastMut = float(self.MutChast.toPlainText())
        countos = self.CountOsSB.value()
        self.Slider.setMaximum(countpop - 1)
        self.agents = []
        x = sympy.Symbol('x')
        fun = sympy.lambdify(x, self.FunEdit.toPlainText())
        ar = np.array(self.gen_x(A, B))
        xx, y = self.get_y(fun, ar)

        for i in range(countos):
            par = (B - A) * np.random.rand() + A
            self.agents.append(agent(par))
            self.agents[-1].calculate(fun)
        for i in range(countpop):
            self.drawplot(xx, y)
            for k in range(int(countos / 2)):
                minim = 1000
                maxim = -1000
                index = 0
                ind = 0
                if tp == 'max':
                    for d in self.agents:
                        if d.rY() < minim:
                            minim = d.rY()
                            index = ind
                        ind += 1
                elif tp == 'min':
                    for d in self.agents:
                        if d.rY() > maxim:
                            maxim = d.rY()
                            index = ind
                        ind += 1
                self.drawpoint(self.agents[index].rX(), self.agents[index].rY(), 'r')
                del self.agents[index]
            for f in self.agents:
                self.drawpoint(f.rX(), f.rY(), 'g')
            self.saveplt("name")

            secund = 0
            for dl in range(int(countos / 2)):
                self.agents.append(agent(self.agents[secund].rX()))
                secund += 1
            for ag in range(len(self.agents)):
                self.agents[ag].mutate(strengMut, chastMut)
                self.agents[ag].calculate(fun)
        self.show_graph(0)

    def slide(self):
        self.show_graph(self.Slider.value())

    def show_graph(self, name):
        # self.mypix = QPixmap("./tmp/" + str(name) + ".jpg").scaled(640, 480)
        self.mypix = QPixmap("./tmp/" + "name" + ".jpg")
        self.Graph.setPixmap(self.mypix)

    def gen_x(self, A, B):
        shag = 0.01
        ret = []
        while A < B:
            ret.append(A)
            A += shag
        return ret

    def get_y(self, fun, ar):
        ret = np.zeros(len(ar))
        for ind, i in enumerate(ar):
            ret[ind] = fun(i)
        return ar, ret

    def drawplot(self, xx, y):
        fig = plt.figure()
        self.xx = fig.add_subplot(1, 1, 1)
        self.xx.plot(xx, y)

    def drawpoint(self, x, y, color):
        self.xx.scatter(x, y, c=color)

    def saveplt(self, name):
        plt.savefig('./tmp/' + name + '.jpg', dpi=50)
        plt.close()


app = QtWidgets.QApplication([])
application = mywindow()
application.show()
sys.exit(app.exec())
