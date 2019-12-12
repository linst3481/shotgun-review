from tank.platform.engine import current_engine
import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel
import sgtk, os, sys
import shotgun_api3
import tank
import subprocess
import getpass, string, datetime

sys.path.append( "/Volumes/public/StoryBots/production/series/ask_the_storybots/03_shared_assets/01_cg/05_maya_tools/pipeline/module")

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

class _playblast_fn:

    def __init__( self, _shot_cam, _file, _resolution_size, _comment, _upload_status, _slate_states):




        # input values
        self._RV_path = "/Applications/RV64.app/Contents/MacOS/rv "
        self._shot_cam = pm.PyNode( _shot_cam)
        self._file = str( _file)


        self.resolution_size = _resolution_size
        self._comment = _comment
        self._upload = _upload_status

        # camera attribute
        self._filmgate = []
        self._resolution = []
        self._gatemast = []
        self._overscan = []        
        self._slate_states = _slate_states

        # camera setup
        self._cam_setup()

        # playblaster
        self._do_playblast()

        # camera restore
        self._cam_restore()

        # update it for shotgun review
        if str(self._upload) == "Checked":
            self._upload_review()
            self._copy_mov_to_shots()
        else:
            pass

    def _cam_setup ( self):

        self._filmgate = self._shot_cam.displayFilmGate.get()
        self._resolution = self._shot_cam.displayResolution.get()
        self._gatemast = self._shot_cam.displayGateMask.get()
        self._overscan = self._shot_cam.overscan.get()

        # in case of the attribute locked
        self._shot_cam.displayFilmGate.unlock()
        self._shot_cam.displayFilmGate.set(0)
        self._shot_cam.displayResolution.unlock()
        self._shot_cam.displayResolution.set(0)
        self._shot_cam.displayGateMask.unlock(0)
        self._shot_cam.displayGateMask.set(0)
        self._shot_cam.overscan.unlock(0)
        self._shot_cam.overscan.set(1)
  
    def _cam_restore ( self):
        self._shot_cam.displayFilmGate.set( self._filmgate)
        self._shot_cam.displayResolution.set( self._resolution)
        self._shot_cam.displayGateMask.set( self._gatemast)
        self._shot_cam.overscan.set( self._overscan)

    def _do_playblast(self):
            
        MODEL_EDITOR_PARAMS = {
            "activeView": True,
            "cameras": False,
            "controlVertices": False,
            "deformers": False,
            "dimensions": False,
            "displayAppearance": "smoothShaded",
            "displayLights": "default",
            "displayTextures": True,
            "dynamicConstraints": False,
            "fogging": False,
            "follicles": False,
            "grid": False,
            "handles": False,
            "headsUpDisplay": True,
            "hulls": False,
            "ignorePanZoom": False,
            "ikHandles": False,
            "imagePlane": True,
            "joints": False,
            "lights": False,
            "locators": False,
            "manipulators": False,
            "nurbsCurves": False,
            "nurbsSurfaces": True,
            "pivots": False,
            "planes": False,
            "selectionHiliteDisplay": False,
            "shadows": False,
            "sortTransparent": True,
            "strokes": True,
            "textures": True,
            "useDefaultMaterial": False,
            "wireframeOnShaded": False,
            }
       
        windowName = "review_blast"


        try:
            _current_panel = pm.getPanel(wf=True)
            if pm.modelEditor(_current_panel, q=True,fogging=True) == True:
                MODEL_EDITOR_PARAMS["fogging"] = True
        except:
            pass
       
        try:
            if pm.windowPref(windowName, exists=True):
                pm.windowPref( windowName, remove=True )
                pm.deleteUI(windowName)  
        except:
            pass
            
        _window = pm.window( windowName, titleBar=True, iconify=True,
                              leftEdge = 100, topEdge = 100,
                              width = 800, height = 600,
                              sizeable = False)
       
        _layout = pm.formLayout()
        _editor = pm.modelEditor( **MODEL_EDITOR_PARAMS)
       
        pm.formLayout( _layout, edit=True,
                       attachForm = ( ( _editor, "left", 0 ), 
                                      ( _editor, "top", 0 ),
                                      ( _editor, "right", 0 ),
                                      ( _editor, "bottom", 0 ) ) )

        # Legacy viewport used
        try:
            mel.eval( "setRendererInModelPanel ogsRenderer {};".format( _editor))
        except:
            cmds.confirmDialog(  message='You need to change your viewport as the legacy version', dismissString='No' )

        # viewport 2.0 used
        # mel.eval( "setRendererInModelPanel \"vp2Renderer\" {};".format( _editor))

                                     
        pm.setFocus( _editor )
        pm.lookThru( _editor, self._shot_cam) 
    
        cmds.refresh()

        _labelColor = cmds.displayColor('headsUpDisplayLabels', q=True, dormant=True)
        _labelValue = cmds.displayColor('headsUpDisplayValues', q=True, dormant=True)

        visibleHUDs = [f for f in pm.headsUpDisplay(listHeadsUpDisplays=True)
                                           if pm.headsUpDisplay(f, query=True, visible=True)]
        map(lambda f: pm.headsUpDisplay(f, edit=True, visible=False), visibleHUDs)


        for h in pm.headsUpDisplay(listHeadsUpDisplays=True):
            if pm.headsUpDisplay( h, q=1, s=1) == 7 :
                if pm.headsUpDisplay( h, q=1, b=1) == 5:
                    try:
                        pm.headsUpDisplay( h, rem=True)
                    except:
                        pass
                
        for h in pm.headsUpDisplay(listHeadsUpDisplays=True):
            if pm.headsUpDisplay( h, q=1, s=1) == 7 :
                if pm.headsUpDisplay( h, q=1, b=1) == 6:
                    try:
                        pm.headsUpDisplay( h, rem=True)
                    except:
                        pass


        cmds.displayColor('headsUpDisplayValues',17, dormant=True)
        cmds.displayColor('headsUpDisplayLabels', 16, dormant=True)

        def hudShot():
            _nameTemp = cmds.file(q=1, ns=1).split(".")[0]
            return _nameTemp.rsplit("_", 1)[0]

        def hudName():
            return getpass.getuser()

        pm.headsUpDisplay( 'HUDCurrentFrame', edit=True, visible=True, labelFontSize="large", dataFontSize="large", section=5, block=1)
        #cmds.headsUpDisplay('HUDA',s=7,b=6, blockAlignment='center', dataFontSize='large', command=hudShot)
        #cmds.headsUpDisplay('HUDB',s=7,b=5, blockAlignment='center', dataFontSize='large', label="Artist:", labelFontSize="large", command=hudName)

        pm.setFocus( _editor )

        #if pm.headsUpDisplay('HUDCurrentFrame', query=True, visible=False):
        #    print "works 111"            
        #    pass
        #else:
        _mov_file = os.path.splitext( self._file)[0]
        # print _mov_file
        # __audios = pm.ls(type="audio")
        __audios = pm.ls( type="audio")

        if len(__audios) > 0:
            __audio = str( __audios[0])
        else:
            __audio = False

        # frame catching min, max, current
        _min_frame = pm.playbackOptions(q=1, min=1)
        _max_frame = pm.playbackOptions(q=1, max=1)
        _current_frame = pm.currentTime(q=1)
        pm.currentTime( _min_frame)

        ### playblast option ###
        # play_args = "playblast -format avfoundation -filename \"{}\" -sound \"{}\" -sequenceTime 0 -clearCache 1 -viewer 1 -forceOverwrite -showOrnaments 1 -offScreen -fp 4 -percent 100 -compression \"H.264\" -quality 70 -widthHeight {} {};".format( self._file, __audio, self.resolution_size[0], self.resolution_size[1])

        try:

            _temp_path, _temp_file = os.path.split( self._file)
            _temp_mov_path = _temp_path + "/.temp"

            _temp_file_01 = os.path.splitext( _temp_file)
            _temp_mov_file = _temp_file_01[0] + "_uncomp" + _temp_file_01[1]


            _full_temp_mov_file = os.path.join( _temp_mov_path, _temp_mov_file)

            print _full_temp_mov_file

            try:
                if not os.path.exists(_temp_mov_path):
                    os.makedirs(_temp_mov_path)

                if os.path.exists( _full_temp_mov_file):
                    os.remove( _full_temp_mov_file)
            except:
                raise

            ### making playblast 
            play_args = "playblast -format qt -filename \"{}\" -sound \"{}\" -sequenceTime 0 -clearCache 1 -viewer 0 -showOrnaments 1 -compression \"H.264\" -offScreen -fp 4 -percent 100 -quality 100 -widthHeight {} {};".format( _full_temp_mov_file, __audio, self.resolution_size[0], self.resolution_size[1])
            mel.eval( play_args)
            pm.currentTime( _current_frame)


            sceneName = pm.sceneName()
            tk = sgtk.sgtk_from_path( sceneName)

            # get entity information
            _context = tk.context_from_path(sceneName)

            _date = datetime.date.today()
            _task = _context.step["name"]
            _shot_name = _context.entity["name"]
            _png_file = os.path.normpath( _temp_mov_path + "/" + _context.user["name"].translate(None, string.whitespace) + ".png")

            try:
                if not os.path.exists(_temp_mov_path):
                    os.makedirs(_temp_mov_path)

                if os.path.exists( _png_file):
                    os.remove( _png_file)
            except:
                raise
                
                        
            ### write information on png file ###
            _copylight = "Copyright (C) {} JibJab Studios - All Rights Reserved".format(_date.year)
            _img = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0))
            _slate_image = ImageDraw.Draw(_img)
            _type_shot_asset = ImageFont.truetype('/Library/Fonts/arial.ttf', 30)
            _type_copyright = ImageFont.truetype('/Library/Fonts/arial.ttf', 15)
            _type_task = ImageFont.truetype('/Library/Fonts/arial.ttf', 18)

            _slate_image.text((820, 1000), _shot_name, font=_type_shot_asset, fill=(255,255, 255,128))
            _slate_image.text((780, 1060), _copylight, font=_type_copyright, fill=(255, 255, 255,128))
            _slate_image.text((910, 1035), "Task : {}".format( _task), font=_type_task, fill=(255, 255, 255,128))
            # _slate_image.text((1610, 1060), _review_file, font=_type_copyright, fill=(255,255,255,80))

            _img.save( _png_file, 'PNG')


            ### convert uncomppresed file to h.264
            #t = os.system("/Volumes/public/StoryBots/production/series/ask_the_storybots/03_shared_assets/01_cg/05_maya_tools/pipeline/module/ffmpeg/ffmpeg -y -i " + _full_temp_mov_file + " -vcodec libx264 -pix_fmt yuv420p -preset slower -crf 0 -vf eq=brightness=0.04 -g 1 -acodec copy " + self._file)
            t = os.system("/Volumes/public/StoryBots/production/series/ask_the_storybots/03_shared_assets/01_cg/05_maya_tools/pipeline/module/ffmpeg/ffmpeg -y -i " + _full_temp_mov_file + " -i " + _png_file + " -vcodec libx264 -pix_fmt yuv420p -preset slow -crf 22 -filter_complex \"overlay=x=(main_w-overlay_w)/2:y=(main_h-overlay_h)/2\" -g 0 -acodec copy " + self._file)
            ###################################### 
            #### This is RV open with mov file ###
            ######################################

            _mov_path_RV, _mov_file_RV = os.path.split( self._file)
            os.chdir( _mov_path_RV)
            subprocess.Popen( self._RV_path + _mov_file_RV, shell=True)

            if os.path.exists( _full_temp_mov_file):
                os.remove( _full_temp_mov_file)
            
            if os.path.exists( _png_file):
                os.remove( _png_file)


        except:
            pm.confirmDialog( title="Playblast Error", message="Close your RV or deselect the file.\nYour file is being used from other application", defaultButton="Yes")
            raise


        # playblast  -format avfoundation -sound "ATS_301_sq020_020" -sequenceTime 0 -clearCache 1 -viewer 1 -showOrnaments 0 -offScreen  -fp 4 -percent 80 -compression "H.264" -quality 70 -widthHeight 1920 1080;
        #pm.showWindow( _window )
        pm.headsUpDisplay( 'HUDCurrentFrame', edit=True, visible=False, section=5, block=1)
        # cmds.headsUpDisplay( 'HUDA', rem=True )
        # cmds.headsUpDisplay( 'HUDB', rem=True )
        # delete playblast window
        pm.deleteUI(_window)
        # revive HOD modes

        cmds.displayColor('headsUpDisplayValues',_labelColor, dormant=True)
        cmds.displayColor('headsUpDisplayLabels', _labelValue, dormant=True)
        map(lambda f: pm.headsUpDisplay(f, edit=True, visible=True), visibleHUDs)

    def _upload_review( self):
        ### permission to upload review
        sg = shotgun_api3.Shotgun('https://jibjab.shotgunstudio.com', 'versionUpdate', '738afb3552cce7dc5bf998996dd98d2b5e8f7cc0a4ea5db58f39415d3a98970b')
        
        ### define workspace and the project and all information to upload
        
        # maya scene name 
        
        sceneName = pm.sceneName()
        tk = sgtk.sgtk_from_path( sceneName)
        
        # get entity information
        _context = tk.context_from_path(sceneName)
        
        # task
        filters = [
                        [ 'project', 'is', {'type':_context.project['type'], 'id': _context.project['id'] } ],
                        [ 'entity', 'is', {'type': _context.entity['type'], 'id': _context.entity['id'] } ],
                        [ 'step.Step.code', 'is', _context.step['name']]
                    ]
        
        _task = sg.find_one('Task', filters)
        
       
        # version code name
        _work_filename = os.path.split( sceneName)[1]
        _version_name = os.path.splitext( _work_filename)[0] + ".mov"

        # user
        _user = sgtk.util.get_current_user(tk)
        
        # comment
        comment = self._comment
        
        # path to frame
        _path_to_frames = None
        
        # playblast path
        _movie_file = str( os.path.normpath( self._file))
        
        ##### project #####
        args = {
            "project": _context.project,
            "user": _user,
            "description": comment,
            "sg_path_to_frames": _path_to_frames,
            "sg_path_to_movie": _movie_file,
            "code" : _version_name,
            "sg_status_list": "rev",
            "entity": _context.entity,
            "sg_task" : _task,
            "sg_first_frame" : 0,
            "sg_work_file_location" : sceneName            
            }

        version = sg.find_one("Version", [["code", "is", args["code"]]])

        if version:
            result = sg.update('Version', version["id"], args)
        else:
            result = sg.create('Version', args)
        
        _upload = sg.upload("Version", result["id"], _movie_file, field_name="sg_uploaded_movie")

    def _copy_mov_to_shots(self):

        _movie_file = str( os.path.normpath( self._file))

        src = _movie_file
        path_pieces = _movie_file.split('/')
        seq_path = '/'.join(path_pieces[:10])
        mov_name_version = path_pieces[-1:][0]
        mov_name_shots = mov_name_version.split('_anim_')[0]+'.mov'
        dst = os.path.join(seq_path, '_shots', mov_name_shots)
        cmd_cp = 'cp -f {} {}'.format(src, dst)
        os.system(cmd_cp)
