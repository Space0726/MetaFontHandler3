import os
from xml.etree.ElementTree import parse , SubElement ,dump
from xml.etree.ElementTree import ElementTree
from mojo.UI import GetFolder
from fontParts.world import CurrentFont , CurrentGlyph

def dependAll(base_point,refer_point,dependType):
	f = CurrentFont()
	g = CurrentGlyph()

	pointXList = []
	pointYList = []

	######## data for comparing

	for contour in g:				## indexing raw data
		for point in contour.points:

			if point.x not in pointXList:
				pointXList.append(point.x)
			
			if point.y not in pointYList:
				pointYList.append(point.y)

	pointXList.sort()
	pointYList.sort()

	base_index = {}
	refer_index = {}

	for i,x in enumerate(pointXList):
		if x == base_point.x:
			base_index['x'] = i
		if x == refer_point.x:
			refer_index['x'] = i

	for i,y in enumerate(pointYList):
		if y == base_point.y:
			base_index['y'] = i
		if y == refer_point.y:
			refer_index['y'] = i

	for glyph in f:
		
		glyphXList = []
		glyphYList = []
		
		xcount = 0
		ycount = 0
		
		refer = None
		base = None

		if len(glyph) != len(g):
			continue

		for contour in glyph:
			for point in contour.points:
			
				if point.x not in glyphXList:
					glyphXList.append(point.x)
					xcount += 1

				if point.y not in glyphYList:
					glyphYList.append(point.y)
					ycount += 1	

		if xcount != len(pointXList) or ycount != len(pointYList):
			continue

		glyphYList.sort()
		glyphXList.sort()


		for contour in glyph:
			for point in contour.points:
				if point.x == glyphXList[base_index['x']] and point.y == glyphYList[base_index['y']]:
					base = point
				
				if point.x == glyphXList[refer_index['x']] and point.y == glyphYList[refer_index['y']]:
					refer = point

		if refer is not None and base is not None and get_attr(refer,'penPair') is not None: 
			if dependType == 'x':
				set_attr(base , "dependX" , get_attr(refer,'penPair').replace('z','x') )
			elif dependType == 'y':
				set_attr(base , "dependY" , get_attr(refer,'penPair').replace('z','x') )






def get_attr(point, name):
    value = None

    temp_list = point._get_labels()
    temp_set = set(temp_list)
    
    for each in temp_set:
        if each.startswith("'" + name + "'"):
            value = each[each.strip().find(":") + 2:-1]
            return value
    return None



def set_attr(point, name, value):
    removing_attr = None
    temp_list = point._get_labels()
    temp_set = set(temp_list)
    for each in temp_set:
        if each.startswith("'" + name + "'"):
            removing_attr = each
            # temp_set.remove(each)
    if removing_attr != None:
        temp_set.remove(removing_attr)

    # temp_set.add("'serif': '1'")
    # temp_set.add("'" + name + '": "' + value  + "'")
    if value != 'REMOVE':
        temp_set.add("'" + name + "': '" + value  + "'")
    point._set_labels(temp_set)
