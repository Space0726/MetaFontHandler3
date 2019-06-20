import os
from  xml.etree.ElementTree import *
import json
from fontParts.world import CurrentFont


def name_attr():
	f = CurrentFont()
	path = f.path + '/glyphs'
	files = os.listdir(path)

	for file in files:
		print(file)
		tree = parse(path + "/" + file)
		glyph = tree.getroot()
		outline = glyph.find("outline")
		if outline == None:
			continue
		contours = outline.getchildren()

		for contour in contours:
			for point in contour.getchildren():
				name = (point.get("name"))
				if name != None:
					name = '{' + name.replace("'", '"') + '}'
					name = json.loads(name)
					for attr in list(name.items()):
						point.attrib[attr[0]] = attr[1]

					try:
						del point.attrib['name']
					except:
						pass

					tree.write(path + "/" + file, encoding="utf-8")
	print("--------------------End name_attr()--------------------")