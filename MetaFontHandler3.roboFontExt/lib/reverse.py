from  xml.etree.ElementTree import *
import os

def reverse(dest):
	path = dest + "/glyphs"
	files = os.listdir(path)
	for file in files:

		if file.find(".glif") == -1:
		    continue
		tree = parse(path + "/" + file)
		glyph = tree.getroot()

		outline = glyph.find("outline")
		if outline == None:
		    continue
		contours = outline.getchildren()

		for contour in contours:
			for point in contour.getchildren():
				if point.get("name") != None:
				    continue
				data = ""
				attr =[]
				for a in point.attrib:
					if a == 'x' or a=='y' or a=='type' or a=='smooth':
						continue
					if data != "":
						data += ","
					
					data += "'"+a+ "'" +":"+ "'"+point.get(a)+ "'" 
					attr.append(a)

				for x in attr:
					point.attrib.pop(x)

				if data == "":
					pass
				else:
					point.set("name",data)

		tree.write(path + "/" + file, encoding="utf-8", xml_declaration=True)