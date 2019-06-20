from xml.etree.ElementTree import *
import sys
import os

def point_rotator(wd, sung):
	path = wd + '/glyphs' + str(sung)
	files = os.listdir(path)
	os.chdir(path)

	for file in files:
		if file.endswith('glif'):
			tree = parse(file)
			glyph = tree.getroot()
			outline = glyph.find("outline")
			contours = outline.getchildren()
	
			for contour in contours:
				points = contour.findall("point")
				for point in points:
					if "penPair" not in point.keys():
						contour.append(point)
						contour.remove(point)
					else:
						break
	
			ElementTree(glyph).write("../glyphs" + str(sung) + "/"  + file, encoding='UTF-8', xml_declaration=True)