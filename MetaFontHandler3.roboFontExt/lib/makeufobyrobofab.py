import os
import shutil
from ufoLib import UFOReader, UFOWriter
from mojo.UI import GetFolder, GetFile, PutFile
from ufoLib.glifLib import GlyphSet
from xml.etree.ElementTree import Element, SubElement, ElementTree

def makeufo(glyphsfolder, Aufofolder, ufofolder):
	uw = UFOWriter(ufofolder)
	ufoglyphsfolder = uw.makeGlyphPath()
	shutil.copy(Aufofolder+'/fontinfo.plist', ufofolder)

	ur = UFOReader(Aufofolder)
	libdic = ur.readLib()
	libdic['public.glyphOrder'] = []

	for (path, dir, files) in os.walk(glyphsfolder):
		for filename in files:
			ext = os.path.splitext(filename)[-1]
			gname = os.path.splitext(filename)[0]
			if ext == '.glif':
				shutil.copy(path+'/'+filename, ufoglyphsfolder)
				libdic['public.glyphOrder'].append(gname)

	uw.writeLib(libdic)

	ur = UFOReader(ufofolder) # creat contents.plit (key = glif name)
	ur.getGlyphSet().writeContents()