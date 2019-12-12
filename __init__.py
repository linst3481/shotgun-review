import sys, os, json
import xml.etree.ElementTree as xml
from cStringIO import StringIO
from Qt import QtGui, QtWidgets, QtCore, QtCompat

import pyside2uic as pysideuic
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
import maya.cmds as cmds
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

SCRIPT_PATH = "/Volumes/public/StoryBots/production/series/ask_the_storybots/03_shared_assets/01_cg/05_maya_tools/pipeline/tool/__menu/__pipeline"
QT_PATH = "/Volumes/public/StoryBots/production/series/ask_the_storybots/03_shared_assets/01_cg/05_maya_tools/pipeline/module"

# add environment
for _path in [SCRIPT_PATH, QT_PATH]:
    sys.path.append( _path)

# import Qt module
import Qt

def name_remove():
    try:
        objs = [x for x in cmds.ls(shortNames=True) if '|shot_cam' in x]
        objs.sort(key=lambda x : x.count('|'))
        objs.reverse()

        for i in range(len(objs)):
            cmds.rename(objs[i], objs[i].replace('|', ''))
    except:
        pass



def delMods(modName):
    
    modules = sys.modules.copy()
    #print( modules)
    
    #print "<< Deleting Modules >> \n"
    #This deletes the module out of the system list.
    
    for n in modName:
        for module in modules:
            if module.find(n)!= -1:
                del(sys.modules[module])
                #print 'Deleted...', module,'\n'
    
    #This line deletes the module name, Bad things happen if it's deleted before
    #it can finish looping through it.
    del(modName)
    
    #print "<< Done >>\n\n"

##Delete modules

toDelete = ["jj_reviewer_GUI"]
delMods( toDelete)
toDelete = ["jj_reviewer_fn"]
delMods( toDelete)


##Import modules
from jj_reviewer_GUI import *


def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

def show():
    '''
    this is the funciton that start things up
    '''
    name_remove()
    global MyDockingWindow
    MyDockingWindow = MyDockingWindow( maya_main_window())
    MyDockingWindow.show()
    return MyDockingWindow
