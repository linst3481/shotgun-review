import sys
sys.path.append("/Volumes/public/StoryBots/production/series/ask_the_storybots/03_shared_assets/01_cg/05_maya_tools/pipeline/module")
import datetime

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 



def _make_slate( project, shot, task, artist):
	'''
	variables
	'''

	_project = project
	_task =  task
	_artist = artist
	_date = datetime.date.today()
	_shot = shot


	_copylight = "Copyright (C) {} JibJab Studios - All Rights Reserved".format(_date.year)

	img = Image.open("/Volumes/public/StoryBots/production/series/ask_the_storybots/03_shared_assets/01_cg/05_maya_tools/pipeline/tool/__menu/__pipeline/jj_reviewer/slate.png")
	d = ImageDraw.Draw(img)
	font = ImageFont.truetype('/Library/Fonts/arial.ttf', 30)
	font_02 = ImageFont.truetype('/Library/Fonts/arial.ttf', 15)
	font_03 = ImageFont.truetype('/Library/Fonts/arial.ttf', 18)

	d.text((820, 1000), shot, font=font, fill=(255,255,255,128))
	d.text((780, 1060), _copylight, font=font_02, fill=(255,255,255,128))
	d.text((910, 1035), "Task : {}".format( _task), font=font_03, fill=(255,255,255,128))


	# d.text((800, 300), "Date : {}".format(_date), font=font, fill=(255,255,255,128))
	img.save('/Users/jinchuljung/Desktop/eee/slate02.png')

_make_slate("Ask The Storybots", "ATS_301_sq101_020", "Anim", "Jeff.J")

import os
### ffmpeg Convert option ###
'''
aaa = "/Volumes/public/StoryBots/production/series/ask_the_storybots/03_shared_assets/01_cg/05_maya_tools/pipeline/module/ffmpeg/ffmpeg -y \
		-i /Users/jinchuljung/Desktop/eee/ATS_301_sq020_020_anim_scene.v009_01.mov \
		-i /Users/jinchuljung/Desktop/eee/slate02.png \
		-filter_complex \"[0:v][1:v] overlay=0:0\" \
		-vf \"drawtext=fontfile=Arial.ttf: text=%{n}: x=(w-tw)/2: y=h-(2*lh): fontcolor=white: box=1: boxcolor=0x00000099\" \
		-acodec copy /Users/jinchuljung/Desktop/eee/test.mov"
'''

aaa = "/Volumes/public/StoryBots/production/series/ask_the_storybots/03_shared_assets/01_cg/05_maya_tools/pipeline/module/ffmpeg/ffmpeg -y \
		-i /Users/jinchuljung/Desktop/eee/ATS_301_sq020_020_anim_scene.v009_01.mov \
		-i /Users/jinchuljung/Desktop/eee/slate02.png \
		-filter_complex \"overlay=x=(main_w-overlay_w)/2:y=(main_h-overlay_h)/2\" \
		-acodec copy /Users/jinchuljung/Desktop/eee/test.mov"

'''
aaa = "/Volumes/public/StoryBots/production/series/ask_the_storybots/03_shared_assets/01_cg/05_maya_tools/pipeline/module/ffmpeg/ffmpeg -y \
		-i /Users/jinchuljung/Desktop/eee/ATS_301_sq020_020_anim_scene.v009_01.mov \
		-vf \"drawtext=fontfile=/Library/Fonts/arial.ttf: text=%{n}: x=(w-tw)/2: y=h-(2*lh): fontcolor=white: box=1: boxcolor=0x00000099\"  \
		-acodec copy /Users/jinchuljung/Desktop/eee/test.mov"

bbb = "/Volumes/public/StoryBots/production/series/ask_the_storybots/03_shared_assets/01_cg/05_maya_tools/pipeline/module/ffmpeg/ffmpeg -y \
		-i /Users/jinchuljung/Desktop/eee/test.mov \
		-i /Users/jinchuljung/Desktop/eee/slate1.png \
		-filter_complex \"overlay=x=(main_w-overlay_w)/2:y=(main_h-overlay_h)/2\" \
		-vf \"drawtext=fontfile=/Library/Fonts/arial.ttf: text=%{n}: x=(w-tw)/2: y=h-(2*lh): fontcolor=white: box=1: boxcolor=0x00000099\"  \
		-acodec copy /Users/jinchuljung/Desktop/eee/test.mov"
'''
# ffmpeg -i video.mov -vcodec r210 -vf "drawtext=fontfile=Arial.ttf: text=%{n}: x=( w-tw)/2: y=h-(2*lh): fontcolor=white: box=1: boxcolor=0x00000099" -y output.mov

os.system( aaa)
# os.system( bbb)











