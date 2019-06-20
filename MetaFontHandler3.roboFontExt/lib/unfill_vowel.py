from xml.etree.ElementTree import *
import os

def search_curve(contours):
	circle = []
	for contour in contours:
		count = 0
		points = contour.getchildren()
		for point in points:
			if point.get('type') == 'curve':
				count += 1
		if 4 <= count and count <= 8:
			circle.append((contour, count))

	return circle

def unfill_vowel(wd):
	path = wd
	files = os.listdir(path)
	os.chdir(path)

	for file in files:
		if os.path.isdir(file)==False:
			continue
		glifs = os.listdir(file + '/')
		for glif in glifs:
			if glif.endswith('_ieung.glif') or glif.endswith('_hieut.glif'):
				tree = parse(file + '/' + glif)
				glyph = tree.getroot()
				outline = glyph.find('outline')
				contours = outline.getchildren()

				circle = search_curve(contours)

				if len(circle) == 2:
					contour1 = circle[0][0]
					contour2 = circle[1][0]

					points1 = contour1.getchildren()
					points2 = contour2.getchildren()
					xy = []
					lxy = []

					rightmost_x = -9999
					leftmost_x = 9999
					for point in points1:
						if int(point.get('x')) > int(rightmost_x):
							rightmost_x = point.get('x')
						if int(point.get('x')) < int(leftmost_x):
							leftmost_x = point.get('x')

					radius1 = int(rightmost_x) - int(leftmost_x)
					
					rightmost_x = -9999
					leftmost_x = 9999
					for point in points2:
						if int(point.get('x')) > int(rightmost_x):
							rightmost_x = point.get('x')
						if int(point.get('x')) < int(leftmost_x):
							leftmost_x = point.get('x')
					radius2 = int(rightmost_x) - int(leftmost_x)

				if radius1 > radius2:
					small = contour2
				else:
					small = contour1

				small.getchildren()[0].attrib["innerType"] = "unfill"

				ElementTree(glyph).write('../glyphs/' + file + '/' + glif)	



						
						

