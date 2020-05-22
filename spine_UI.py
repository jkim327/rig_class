#import UI modules
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from shiboken2 import wrapInstance

#import logger
import logging
logger = logging.getLogger(__name__)

#import maya modules
import os.path
import maya.OpenMayaUI as OpenMayaUI
import maya.cmds as cmds

#import modules
import rig_class.spine_rig as st
import rig_class.spine_data as sd

#get file directory
base_dir = os.path.dirname(os.path.abspath(st.__file__))
fk_path = '{}\\fk_img.png'.format(base_dir)
ik_path = '{}\\ik_img.png'.format(base_dir)

def _getMayaWindow():

    ptr = OpenMayaUI.MQtUtil.mainWindow ()
    if ptr is not None:
        return wrapInstance (long (ptr), QMainWindow)


class spine_window(QDialog, object):
    def __init__(self, spine_data = None):
        super(spine_window, self).__init__(parent=_getMayaWindow())

        winName = 'spine_tool_window'

        self.spine_data = sd.SpineData()
        self.spine_object = st.SpineRig(self.spine_data)


        # If the UI already exists, delete the old one.
        if cmds.window (winName, exists=True):
            cmds.deleteUI (winName, window=True)

        # Set the dialog object name, window title and size
        self.setObjectName(winName)
        self.setWindowTitle('spine_test')
        self.setMinimumSize(313, 406)
        self.setFixedSize(QSize(313, 406))

        self.customUI()

        self.show()


    def customUI(self):


        self.spine_widget = QtWidgets.QWidget(self)
        self.spine_widget.setGeometry(QtCore.QRect(10, 10, 291, 411))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spine_widget.sizePolicy().hasHeightForWidth())
        self.spine_widget.setSizePolicy(sizePolicy)
        self.spine_widget.setMinimumSize(QtCore.QSize(291, 411))
        self.spine_widget.setMaximumSize(QtCore.QSize(291, 411))
        self.spine_widget.setObjectName("spine_widget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.spine_widget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 271, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.spine_num_layout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.spine_num_layout.setContentsMargins(0, 0, 0, 0)
        self.spine_num_layout.setObjectName("spine_num_layout")
        self.spine_label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.spine_label.setObjectName("spine_label")
        self.spine_num_layout.addWidget(self.spine_label)
        self.spine_int = QtWidgets.QSpinBox(self.horizontalLayoutWidget)
        self.spine_int.setMinimum(3)
        self.spine_int.setMaximum(10)
        self.spine_int.setObjectName("spine_int")
        self.spine_num_layout.addWidget(self.spine_int)
        spacerItem = QtWidgets.QSpacerItem(15, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.spine_num_layout.addItem(spacerItem)
        self.spine_int_slider = QtWidgets.QSlider(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spine_int_slider.sizePolicy().hasHeightForWidth())
        self.spine_int_slider.setSizePolicy(sizePolicy)
        self.spine_int_slider.setMinimum(3)
        self.spine_int_slider.setMaximum(10)
        self.spine_int_slider.setOrientation(QtCore.Qt.Horizontal)
        self.spine_int_slider.setObjectName("spine_int_slider")
        self.spine_num_layout.addWidget(self.spine_int_slider)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.spine_widget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 90, 271, 191))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.spine_opt_ho_layout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.spine_opt_ho_layout.setContentsMargins(0, 0, 0, 0)
        self.spine_opt_ho_layout.setObjectName("spine_opt_ho_layout")
        self.img_field = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.img_field.sizePolicy().hasHeightForWidth())
        self.img_field.setSizePolicy(sizePolicy)
        self.img_field.setMaximumSize(QtCore.QSize(132, 189))
        self.img_field.setText("")
        self.img_field.setPixmap(QtGui.QPixmap(fk_path))
        self.img_field.setScaledContents(True)
        self.img_field.setObjectName("img_field")
        self.spine_opt_ho_layout.addWidget(self.img_field)
        self.spine_opt_ver_layout = QtWidgets.QVBoxLayout()
        self.spine_opt_ver_layout.setObjectName("spine_opt_ver_layout")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.spine_opt_ver_layout.addItem(spacerItem1)
        self.FK_spine_opt = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.FK_spine_opt.setObjectName("FK_spine_opt")
        self.FK_spine_opt.setChecked(True)
        #self.spine_data.fk_rig
        self.spine_opt_ver_layout.addWidget(self.FK_spine_opt)
        self.IK_spine_opt = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        self.IK_spine_opt.setObjectName("IK_spine_opt")
        #self.spine_data.ik_rig
        self.spine_opt_ver_layout.addWidget(self.IK_spine_opt)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.spine_opt_ver_layout.addItem(spacerItem2)
        self.spine_opt_ho_layout.addLayout(self.spine_opt_ver_layout)
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.spine_widget)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(10, 290, 271, 31))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.name_layout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.name_layout.setContentsMargins(0, 0, 0, 0)
        self.name_layout.setObjectName("name_layout")
        self.name_label = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.name_label.sizePolicy().hasHeightForWidth())
        self.name_label.setSizePolicy(sizePolicy)
        self.name_label.setMaximumSize(QtCore.QSize(34, 29))
        self.name_label.setObjectName("name_label")
        self.name_layout.addWidget(self.name_label)
        self.name_field = QtWidgets.QTextEdit(self.horizontalLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.name_field.sizePolicy().hasHeightForWidth())
        self.name_field.setSizePolicy(sizePolicy)
        self.name_field.setMaximumSize(QtCore.QSize(229, 29))
        self.name_field.setObjectName("name_field")
        self.name_layout.addWidget(self.name_field)
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(self.spine_widget)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(10, 330, 271, 51))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.button_layout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.button_layout.setContentsMargins(0, 0, 0, 0)
        self.button_layout.setObjectName("button_layout")
        self.run_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget_4)
        self.run_btn.setObjectName("run_btn")
        self.button_layout.addWidget(self.run_btn)
        self.close_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget_4)
        self.close_btn.setObjectName("close_btn")
        self.button_layout.addWidget(self.close_btn)
        self.sample_btn = QtWidgets.QPushButton(self.spine_widget)
        self.sample_btn.setGeometry(QtCore.QRect(210, 60, 75, 23))
        self.sample_btn.setObjectName("sample_btn")

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

        #----------------signals-------------------
        #change img thumbnails when radio button is clicked.
        self.FK_spine_opt.clicked.connect(self.show_fk)
        self.IK_spine_opt.clicked.connect(self.show_ik)

        #spin box and slider are connected
        self.spine_int.valueChanged.connect(self.slider_change)
        self.spine_int_slider.valueChanged.connect(self.spine_change)

        #the int value affects function
        self.sample_btn.clicked.connect(self.call_sample)

        #create spine rig
        self.run_btn.clicked.connect(self.create_spine)

        #close the window
        self.close_btn.clicked.connect(self.close_window)


    def retranslateUi(self, spine_dialog):
        spine_dialog.setWindowTitle(QtWidgets.QApplication.translate("spine_dialog", "Spine", None, -1))
        self.spine_label.setText(QtWidgets.QApplication.translate("spine_dialog", "spine", None, -1))
        self.FK_spine_opt.setText(QtWidgets.QApplication.translate("spine_dialog", "FK Spine", None, -1))
        self.IK_spine_opt.setText(QtWidgets.QApplication.translate("spine_dialog", "IK Spine", None, -1))
        self.name_label.setText(QtWidgets.QApplication.translate("spine_dialog", "Name", None, -1))
        self.run_btn.setText(QtWidgets.QApplication.translate("spine_dialog", "Run", None, -1))
        self.close_btn.setText(QtWidgets.QApplication.translate("spine_dialog", "Close", None, -1))
        self.sample_btn.setText(QtWidgets.QApplication.translate("spine_dialog", "call sample", None, -1))

    #----------------slots-------------------
    def show_fk(self):
        self.img_field.setPixmap(QtGui.QPixmap(fk_path))

    def show_ik(self):
        self.img_field.setPixmap(QtGui.QPixmap(ik_path))

    def slider_change(self):
        size = self.spine_int.value()
        self.spine_int_slider.setValue(size)

    def spine_change(self):
        size = self.spine_int_slider.value()
        self.spine_int.setValue(size)

    def call_sample(self):
        self.spine_object.spine_data.num_jnt = self.spine_int.value()#update data object
        self.spine_object.create_sample()

    def close_window(self):
        self.close

    def create_spine(self):

        self.spine_object.spine_data.cha_naming = self.name_field.toPlainText()
        self.spine_object.spine_data.fk_rig = self.FK_spine_opt.isChecked()
        self.spine_object.spine_data.ik_rig = self.IK_spine_opt.isChecked()

        if not self.spine_object.spine_data.temp_jnt_list:
            return logging.error('Nothing exists. Please set temporary joints first.')

        if not self.spine_object.spine_data.cha_naming:
            return logging.error('Name is not specified.')


        if self.FK_spine_opt.isChecked():
            spineJnt = st.FK_rig(self.spine_object.spine_data)
            spineJnt.create_FK()
            logging.info('FK Creation {}'.format(self.spine_object.spine_data))

        elif self.IK_spine_opt.isChecked():
            spineJnt = st.IK_rig(self.spine_object.spine_data)
            spineJnt.create_IK()
            logging.info('IK Creation {}'.format(self.spine_object.spine_data))


def initUI():
    spine_window()





initUI()