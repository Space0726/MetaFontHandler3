from vanilla import *
from xml.etree.ElementTree import parse , SubElement ,dump
from xml.etree.ElementTree import ElementTree
from mojo.UI import GetFolder,GetFile,PutFile
import os
import shutil

def make_dir(path, glyphpath, glyphpath2, glyphpath3):
    # glyphpath = GetFile("Pick a ufo File")
    glyphpath = glyphpath + "/glyphs"

    # glyphpath2 = GetFile("Pick a ufo File")
    glyphpath2 = glyphpath2 + "/glyphs"

    # glyphpath3 = GetFile("Pick a ufo File")
    glyphpath3 = glyphpath3 + "/glyphs"
    # path = PutFile("Put a Dir Name to use")

    path = path + '/.tmp'
    os.mkdir(path)
    shutil.copytree(glyphpath,path+"/glyphs1")
    shutil.copytree(glyphpath2,path+"/glyphs2")
    shutil.copytree(glyphpath3,path+"/glyphs3")

    return path
    
# make_dir()