import sys, os, json, pprint
import xml.etree.ElementTree as xml
from cStringIO import StringIO
from Qt import QtGui, QtWidgets, QtCore, QtCompat
import sgtk

import pyside2uic as pysideuic
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
import maya.cmds as cmds
import pymel.core as pm
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import jj_reviewer_fn


UI_FILE = os.path.normpath( "/Volumes/public/StoryBots/production/series/ask_the_storybots/03_shared_assets/01_cg/05_maya_tools/pipeline/tool/__menu/__pipeline/jj_reviewer2/jj_reviewer.ui")

def loadUiType(uiFile):
    parsed = xml.parse(uiFile)
    widget_class = parsed.find('widget').get('class')
    form_class = parsed.find('class').text

    with open(uiFile, 'r') as f:
        o = StringIO()
        frame = {}
        pysideuic.compileUi(f, o, indent=0)
        pyc = compile(o.getvalue(), '<string>', 'exec')
        exec pyc in frame

        # Fetch the base_class and form class based on their type in the xml from designer
        form_class = frame['Ui_%s' % form_class]
        base_class = getattr(QtWidgets, widget_class)
    return form_class, base_class

form_class, base_class = loadUiType( UI_FILE)


### class for QtWindow ###
class MyDockingWindow(form_class, base_class):

    def __init__(self, parent=None):

        # set variables
        # initializint GUI
        QtWidgets.QDialog.__init__( self, parent)
        self.setupUi(self)

        _all_camera_shape = pm.ls(type="camera")
        _show_camera = []

        for i in _all_camera_shape:
            if i.getTransform().name() == "shot_cam" or i.getTransform().name() == "persp":
                _show_camera.append( str(i.getTransform()))

        _show_camera.reverse()
        self.comboBox_4.addItems( _show_camera)

        self.pushButton.clicked.connect( self._button_do)

        self.setProperty("saveWindowPref", False)

    def _button_do( self):


        ### file name define ###
        try:
            
            _sceneName = pm.sceneName()
            _tk = sgtk.sgtk_from_path(_sceneName)
            _ctx = _tk.context_from_path( _sceneName)
            _type_workspace = _ctx.entity


            if _type_workspace["type"] == "Asset":
                _template_target = _tk.templates["maya_asset_review"]
                _template_publish = _tk.templates["maya_asset_work"]

            elif _type_workspace["type"] == "Shot":
                _template_target = _tk.templates["maya_shot_review"]
                _template_publish = _tk.templates["maya_shot_work"]

            _fields = _template_publish.get_fields( _sceneName)
            _path = _template_target.apply_fields(_fields)

        except:
            raise ValueError( "please let TD know, you have something problem.")

        _size = self.comboBox_2.currentText()
        _width, _height = _size.split("*")
        _cam = self.comboBox_4.currentText() 
        _comm = self.textEdit.toPlainText()
        _update_review = str(self.checkBox.checkState ()).split(".")[-1]
        _slate = str(self.checkBox_2.checkState ()).split(".")[-1]


        _do_playblast = jj_reviewer_fn._playblast_fn(
                             _shot_cam =_cam,
                             _file = _path,
                             _resolution_size = [int(_width), int(_height)],
                             _comment = _comm,
                             _upload_status = _update_review,
                             _slate_states = _slate
                             )
