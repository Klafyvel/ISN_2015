#! /usr/bin/python3
# Nomenclature
# Copyright (C) 2015 BOUVIN Valentin, HONNORATY Vincent, LEVY-FALK Hugo

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys

from versBrute import *

from BruteVersClass import *

from nomenclature import nomenclature

from molecule import *

from math import *

DOUBLE = 1
SIMPLE = 0

DRAW_LANGUAGE = {
    "avance_simple": 1,
    "avance_double": 2,
    "branche4": 3,
    "C": 4,
    "branche": 5,
    "finbranche": 6,
}


def printPrgm(prgm):
    for i in prgm:
        if i is 1:
            print("Avance Simple")
        elif i is 2:
            print("Avance Double")
        elif i is 3:
            print("branche4")
        elif i is 4:
            print("C")
        elif i is 5:
            print("branche")
        elif i is 6:
            print("fin branche")
        else:
            print(i)


class Drawer(QWidget):
    ready = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)

        self.draw_zone = DrawZone(self)

        self.editor = MoleculeEdit(self)

        self.btn_export = QPushButton("Exporter")
        self.btn_reset = QPushButton("Effacer")
        self.btn_ready = QPushButton("Convertir")
        self.btn_add_hydro = QPushButton("Ajouter les hydrogènes")
        self.btn_remove_hydro = QPushButton("Enlever les hydrogènes")

        self.layout_btn = QVBoxLayout(self)
        self.layout_btn.addWidget(self.btn_add_hydro)
        self.layout_btn.addWidget(self.btn_remove_hydro)
        self.layout_btn.addWidget(self.btn_reset)
        self.layout_btn.addWidget(self.btn_export)
        self.layout_btn.addWidget(self.btn_ready)

        self.layout.addWidget(self.draw_zone)
        self.layout.addWidget(self.editor)

        self.layout.addLayout(self.layout_btn)

        self.setLayout(self.layout)

        QObject.connect(self.btn_ready, SIGNAL('clicked()'), self.ready)
        QObject.connect(self.btn_reset, SIGNAL('clicked()'), self.reset)
        QObject.connect(self.btn_export, SIGNAL('clicked()'), self.export)
        QObject.connect(
            self.btn_add_hydro, SIGNAL('clicked()'), self.editor.addHydro)
        QObject.connect(
            self.btn_remove_hydro, SIGNAL('clicked()'), self.editor.removeHydro)

    def getMolecule(self):
        self.draw_zone.reset()
        self.draw_zone.draw(self.editor.getDrawCode())
        return self.editor.buildMolecule()

    @pyqtSlot()
    def reset(self):
        self.editor.reset()
        self.draw_zone.reset()

    @pyqtSlot()
    def export(self):
        fichier = QFileDialog.getSaveFileName(
            self, "Enregistrer la formule topologique", "", "*.png")
        if fichier is not "":
            self.draw_zone.save(fichier)
            QMessageBox.information(
                self, "Information", "Formule sauvegardée dans {}".format(fichier))
    @pyqtSlot()
    def fromMolecule(self, molecule):
        # print(molecule)
        self.editor.fromMolecule(molecule)
        self.draw_zone.reset()
        self.draw_zone.draw(self.editor.getDrawCode())

class Stack:

    def __init__(self):
        self.data = []

    def add(self, pos):
        self.data.append(pos)

    def look(self):
        return self.data[-1]

    def pop(self):
        r = self.data[-1]
        self.data = self.data[:-1]
        return r

    def reset(self):
        self.data = []


class DrawZone(QGraphicsView):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.pos_stor = Stack()
        self.angle_stor = Stack()
        self.fact_stor = Stack()
        self.current_angle_step_stor = Stack()
        self.current_pos = (0, 0)
        self.current_angle = pi / 3
        self.current_angle_step = 2 * pi / 3

        self.fact = 1

    def draw(self, bytecode):
        self.pos_stor.add(self.current_pos)
        self.angle_stor.add(0)
        self.fact_stor.add(1)
        for x, i in enumerate(bytecode):
            if i is DRAW_LANGUAGE["C"]:
                self.scene.addEllipse(
                    self.current_pos[0], self.current_pos[1], 1, 1)
            elif i in [DRAW_LANGUAGE["avance_simple"], DRAW_LANGUAGE["avance_double"]]:
                self.draw_line(i)
            elif i is DRAW_LANGUAGE["branche"]:
                self.current_angle = (
                    self.current_angle + self.current_angle_step * self.fact)
                self.current_angle_step_stor.add(self.current_angle_step)
                self.pos_stor.add(self.current_pos)
                self.angle_stor.add(self.current_angle)
                self.fact_stor.add(self.fact)
                self.current_angle_step = 2 * pi / 3
                self.fact *= -1
                self.current_angle = self.fact * \
                    3 * pi / 3 + self.current_angle
            elif i is DRAW_LANGUAGE["branche4"]:
                self.current_angle = (
                    self.current_angle + self.current_angle_step * self.fact)
                self.current_angle_step_stor.add(self.current_angle_step)
                self.pos_stor.add(self.current_pos)
                self.angle_stor.add(self.current_angle)
                self.fact_stor.add(self.fact)
                self.current_angle_step = pi / 2
                self.current_angle = self.fact * \
                    pi + self.current_angle
            elif i is DRAW_LANGUAGE["finbranche"]:
                self.current_pos = self.pos_stor.pop()
                self.current_angle = self.angle_stor.pop()
                self.fact = self.fact_stor.pop()
                self.current_angle_step = self.current_angle_step_stor.pop()
            else:
                self.draw_atome(i)
        self.setScene(self.scene)

    def draw_atome(self, atome):
        pos = self.current_pos
        t = self.scene.addText(atome)
        t.setPos(pos[0], pos[1])
        t.setHtml(
            "<div style='background-color:#FFFFFF;'>" + atome + "</div>")
        t.setFlags(QGraphicsItem.ItemIsFocusable | QGraphicsItem.ItemIsMovable |
                   QGraphicsItem.ItemIsSelectable | t.flags())

    def draw_line(self, line):
        pos = self.pos_stor.look()
        deplacement = (
            cos(self.current_angle) * 30, sin(self.current_angle) * 30)
        new_pos = (pos[0] + deplacement[0], pos[1] + deplacement[1])

        self.scene.addLine(pos[0], pos[1], new_pos[0], new_pos[1])

        if line is DRAW_LANGUAGE["avance_double"]:
            rect = (sqrt(25 - 25 / (1 + (deplacement[1] / deplacement[0]) ** 2)), sqrt(
                25 / (1 + (deplacement[1] / deplacement[0]) ** 2)))
            self.scene.addLine(
                pos[0] + rect[0], pos[1] + rect[1], new_pos[0] + rect[0], new_pos[1] + rect[1])
        self.current_pos = new_pos
        self.setScene(self.scene)

    def reset(self):
        self.pos_stor.reset()
        self.angle_stor.reset()
        self.scene.clear()
        self.setScene(self.scene)
        self.current_angle = 0
        self.current_pos = (0, 0)
        self.fact = 1

    def save(self, fichier):
        self.scene.clearSelection()
        self.scene.setSceneRect(self.scene.itemsBoundingRect())
        image = QImage(self.scene.sceneRect().size().toSize(), QImage.Format_ARGB32)
        image.fill(Qt.transparent)
        painter = QPainter(image)
        self.scene.render(painter)
        image.save(fichier)
        del painter


class MoleculeEdit(QTreeWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.first = AtomeItem(CARBONE, self)
        self.first.createEditor()
        self.setMinimumWidth(500)

        self.setHeaderLabels(
            ["Atome", "", "Liaison à créer", "Atome à créer", ""])
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        QObject.connect(
            self, SIGNAL('customContextMenuRequested(QPoint)'), self.contextMenu)

    def buildMolecule(self):
        return Molecule(*self.first.getAndLinkAtome())

    def reset(self):
        self.first.deleteAllChilds()

    @pyqtSlot(QPoint)
    def contextMenu(self, point):
        selected = self.itemAt(point)
        if selected is None:
            return
        menu = QMenu("Renommer en ...")
        menu.addAction("C")
        menu.addAction("H")
        menu.addAction("O")
        menu.addAction("N")
        menu.addSeparator()
        menu.addAction("Simple")
        menu.addAction("Double")

        action = menu.exec(self.mapToGlobal(point))
        if action is not None:
            if action.text() in "CHON":
                selected.changeName(action.text())
            else:
                selected.changeLiaison(action.text())

    def getDrawCode(self):
        self.addHydro()
        return self.first.getDrawCode()

    @pyqtSlot()
    def addHydro(self):
        self.first.addHydro()

    @pyqtSlot()
    def removeHydro(self):
        self.first.removeHydro()

    def fromMolecule(self, molecule):
        self.clear()
        self.first = AtomeItem(self.first.ATOME_TYPE[molecule[0].nom], self, atome_object=molecule[0])
        self.first.createEditor()
        self.first.fromMolecule()


class AtomeItem(QTreeWidgetItem):
    ATOME_TYPE = {
        "C": CARBONE,
        "H": HYDROGENE,
        "O": OXYGENE,
        "N": AZOTE,
    }
    LIAISON_TYPE = {
        "Simple": 1,
        "Double": 2,
    }

    def __init__(self, atome, molecule, liaison=None, num=None, base=None, atome_object=None):
        super().__init__()
        if atome_object:
            self.atome = atome_object
            self.atome.gui_visited = True
        else:
            self.atome = atome()
        self.childs = []
        self.setText(0, self.atome.nom)
        self.molecule = molecule

        self.nb_hydro = 0

        if liaison == self.LIAISON_TYPE["Simple"]:
            self.setIcon(0, QIcon(QPixmap("simple.png")))
            self.liaison_type = self.LIAISON_TYPE["Simple"]
        elif liaison == self.LIAISON_TYPE["Double"]:
            self.setIcon(0, QIcon(QPixmap("double.png")))
            self.liaison_type = self.LIAISON_TYPE["Double"]
        else:
            molecule.addTopLevelItem(self)
            self.liaison_type = -1

        if num is not None:
            self.num = num
        else:
            self.num = None
        if base is not None:
            self.base = base
        else:
            self.base = None

        self.delete = QPushButton(QIcon(QPixmap("list-remove.png")), "")
        self.btn = QPushButton(QIcon(QPixmap("list-add.png")), "")
        self.liaison = QComboBox()
        self.liaison.addItem("Simple")
        self.liaison.addItem("Double")

        self.nature = QComboBox()
        self.nature.addItem("C")
        self.nature.addItem("H")
        self.nature.addItem("O")
        self.nature.addItem("N")

        QObject.connect(self.btn, SIGNAL('clicked()'), self.createChild)
        QObject.connect(self.delete, SIGNAL('clicked()'), self.deleteAtome)
    def __str__(self):
        r = self.atome.nom + "\n"
        for i in self.childs:
            f = True 
            for j in str(i).split("\n"):
                if j is '':
                    pass
                elif f:
                    r += " ∟ " + j + "\n"
                    f = False
                else :
                    r += "   " + j + "\n"

        return r


    @pyqtSlot()
    def createChild(self):
        nature = self.nature.currentText()
        # if nature is "H":
        #     self.nb_hydro += 1
        nouveau = AtomeItem(self.ATOME_TYPE[nature], self.molecule, self.LIAISON_TYPE[
                            self.liaison.currentText()], len(self.childs), self)
        self.addChild(nouveau)
        nouveau.createEditor()
        self.molecule.setCurrentItem(nouveau)

    @pyqtSlot()
    def deleteAtome(self):
        for i in self.childs:
            i.deleteAtome()
        if not self.base is None:
            self.base.deleteChild(self.num)

    def deleteChild(self, num):
        self.removeChild(self.childs[num])
        if self.childs[num].atome.nom is "H":
            self.nb_hydro -= 1
        self.childs.pop(num)
        for i in range(num, len(self.childs)):
            self.childs[i].num = i

    @pyqtSlot()
    def deleteAllChilds(self):
        while len(self.childs) > 0:
            self.childs[0].deleteAllChilds()
            self.childs[0].deleteAtome()

    def createEditor(self):
        self.molecule.setItemWidget(self, 4, self.btn)
        self.molecule.setItemWidget(self, 2, self.liaison)
        self.molecule.setItemWidget(self, 3, self.nature)
        self.molecule.setItemWidget(self, 1, self.delete)

    def addChild(self, c):
        if c.atome.nom is "H":
            self.nb_hydro += 1
        self.childs.append(c)
        super().addChild(c)

    def getAndLinkAtome(self):
        self.atome.delink()
        if len(self.childs) == 0:
            return [self.atome]
        else:
            voisins = []
            for i in self.childs:
                a = i.getAndLinkAtome()
                voisins = a + voisins
                n = 1
                if i.liaison_type is self.LIAISON_TYPE["Double"]:
                    n=2
                try:
                    self.atome.link(voisins[0], n=n)
                except OverLinked as e:
                    self.atome.delink()
                    QMessageBox.critical(self.molecule, "Erreur", str(e))
                    self.molecule.setCurrentItem(i)
            return [self.atome] + voisins

    def changeName(self, name):
        self.atome = self.ATOME_TYPE[name]()
        if self.atome.nom is "H" and not self.base is None:
            self.base.nb_hydro += 1
        self.setText(0, self.atome.nom)

    def changeLiaison(self, liaison):
        if self.liaison_type == -1:
            return
        self.liaison_type = self.LIAISON_TYPE[liaison]
        if self.liaison_type == self.LIAISON_TYPE["Simple"]:
            self.setIcon(0, QIcon(QPixmap("simple.png")))
        elif self.liaison_type == self.LIAISON_TYPE["Double"]:
            self.setIcon(0, QIcon(QPixmap("double.png")))

    def getDrawCode(self):
        r = []
        if self.atome.nom is "H":
            return r

        liaison4 = 3
        if self.liaison_type is -1:
            liaison4 = 4
        if (len(self.childs) - self.nb_hydro) < liaison4:
            r.append(DRAW_LANGUAGE["branche"])
        elif (len(self.childs) - self.nb_hydro) >= liaison4:
            r.append(DRAW_LANGUAGE["branche4"])
        if self.liaison_type is self.LIAISON_TYPE["Simple"]:
            r.append(DRAW_LANGUAGE["avance_simple"])
        if self.liaison_type is self.LIAISON_TYPE["Double"]:
            r.append(DRAW_LANGUAGE["avance_double"])
        if self.atome.nom is "C":
            r.append(DRAW_LANGUAGE[self.atome.nom])
        elif self.atome.nom in ["O", "N"]:
            nb_h = self.nb_hydro
            if nb_h > 1:
                r.append(self.atome.nom + "H" + str(nb_h))
            elif nb_h == 1:
                r.append(self.atome.nom + "H")
            else:
                r.append(self.atome.nom)
        for i in self.childs:
            r += i.getDrawCode()
        r.append(DRAW_LANGUAGE["finbranche"])
        return r

    def addHydro(self):
        for i in self.childs:
            i.addHydro()

        borne = 0
        nb_childs = 0
        for i in self.childs:
            if i.liaison_type is self.LIAISON_TYPE["Double"]:
                nb_childs += 2
            else:
                nb_childs += 1
        if self.base is None and nb_childs < self.atome.nb_liaison:
            borne = self.atome.nb_liaison - nb_childs
        elif self.liaison_type is self.LIAISON_TYPE["Simple"] and (nb_childs + 1) < self.atome.nb_liaison:
            borne = self.atome.nb_liaison - (nb_childs + 1)
        elif self.liaison_type is self.LIAISON_TYPE["Double"] and (nb_childs + 2) < self.atome.nb_liaison:
            borne = self.atome.nb_liaison - (nb_childs + 2)
            
        for i in range(borne):
            nouveau = AtomeItem(self.ATOME_TYPE["H"], self.molecule, self.LIAISON_TYPE[
                "Simple"], len(self.childs), self)
            self.addChild(nouveau)
            nouveau.createEditor()

    def removeHydro(self):
        for i in self.childs:
            i.removeHydro()
        i = 0
        while self.nb_hydro > 0 and i < len(self.childs):
            if self.childs[i].atome.nom is "H":
                self.childs[i].deleteAtome()
            else:
                i += 1

    def fromMolecule(self):
        for i in self.atome.get_link():
            if not i[0].gui_visited:
                nouveau = AtomeItem(self.ATOME_TYPE[i[0].nom], self.molecule, i[1], len(self.childs), self, atome_object=i[0])
                self.addChild(nouveau)
                nouveau.createEditor()
                nouveau.fromMolecule()



class TextInput(QWidget):
    ready = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)

        self.button = QPushButton('Valider', self)
        self.input = QLineEdit(self)

        self.layout.addWidget(self.input)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)
        QObject.connect(self.button, SIGNAL('clicked()'), self.ready)

    def setText(self, s):
        self.input.setText(s)

    def getText(self):
        return self.input.text()

class Help(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.txt = QTextEdit()
        with open("help_text.txt", "r", encoding='utf-8') as txt:
            self.txt.setText(txt.read())
        self.txt.setReadOnly(True)
        self.layout.addWidget(self.txt)
        self.setLayout(self.layout)
        self.setWindowTitle("Aide")
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)

class Fenetre(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.in_layout = QVBoxLayout()
        self.layout = QHBoxLayout(self)
        self.help_btn = QPushButton("Aide")
        self.help_window = Help(self)
        self.layout_text = QFormLayout(self)
        #self.molecule_choice = QListWidget(self)

        self.input_brute = TextInput(self)
        self.input_nomenc = TextInput(self)

        self.draw = Drawer(self)

        self.in_layout.addWidget(self.help_btn)
        self.in_layout.addWidget(self.draw)

        self.layout_text.addRow('Formule brute :', self.input_brute)
        self.layout_text.addRow('Formule nomenclature :', self.input_nomenc)

        self.in_layout.addLayout(self.layout_text)

        # self.layout.addWidget(self.molecule_choice)
        self.layout.addLayout(self.in_layout)

        self.setLayout(self.layout)

        self.setWindowTitle("Nomenclature")
        self.setMinimumWidth(900)
        self.setMinimumHeight(600)

        QObject.connect(self.draw, SIGNAL('ready()'), self.fromGraph)
        QObject.connect(self.help_btn, SIGNAL('clicked()'), self.help_window.show)
        QObject.connect(self.input_nomenc, SIGNAL('ready()'), self.fromName)
        QObject.connect(self.input_brute, SIGNAL('ready()'), self.fromBrute)
        #QObject.connect(self.molecule_choice, SIGNAL('currentItemChanged(QListWidgetItem * current, QListWidgetItem * previous)'), self.changeMolecule)

    @pyqtSlot()
    def fromGraph(self):
        try:
            m = self.draw.getMolecule()
            self.input_brute.setText(versFormuleBrute(m))
        except OverLinked as e:
            QMessageBox.critical(self, "Erreur", str(e))
    @pyqtSlot()
    def fromName(self):
        m = nomenclature(self.input_nomenc.getText())
        self.draw.fromMolecule(m)
        self.input_brute.setText(versFormuleBrute(m))
    @pyqtSlot()
    def changeMolecule(self, current, previous):
        self.input_nomenc.setText(current.text())
        self.draw.fromMolecule(m)
    @pyqtSlot()
    def fromBrute(self):
        try:
            m = bruteVersClass(self.input_brute.getText())
            self.input_nomenc.setText("")
            self.draw.fromMolecule(m)
        except ImpossibleCombinaison:
            QMessageBox.critical(self, "Erreur", "Combinaison impossible : {}".format(self.input_brute.getText()))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    t = Fenetre()
    t.show()
    sys.exit(app.exec_())
