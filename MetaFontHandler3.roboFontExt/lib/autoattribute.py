import os
from xml.etree.ElementTree import parse , SubElement ,dump
from xml.etree.ElementTree import ElementTree
from mojo.UI import GetFolder

def addVowelAttr(self):
    glyphpath = GetFolder("Pick a directory")
    filelist = os.listdir(glyphpath)

    for f in filelist:
    	if f.endswith(".glif"):
    		print(f + " <- glif file\n")
    		doc = parse(f)
    		root = doc.getroot()

    		for outline in root.iter("outline"):
    			serifCount = 1
    			roundCount = 1
    			
    			for contour in outline.iter("contour"):
    				minX = 1000
    				minY = 1000
    				maxX = -1000
    				maxY = -1000

    				for point in contour.iter("point"):
    					pointX = int(float(point.get('x')))
    					pointY = int(float(point.get('y')))
    					if minX > pointX:
    						minX = pointX
    					if maxX <= pointX:
    						maxX = pointX
    					if minY > pointY:
    						minY = pointY
    					if maxY <= pointY:
    						maxY = pointY

    				horizontalLine = maxX - minX
    				verticalLine = maxY - minY

    				if horizontalLine * 6 < verticalLine:
    					for point in contour.iter("point"):
    						pointX = int(float(point.get('x')))
    						pointY = int(float(point.get('y')))
    						if pointX == minX and pointY == maxY:
    							point.set("serif",str(serifCount))
    							serifCount+=1
    						elif pointX == minX and pointY == minY:
    							point.set("round",str(roundCount))
    							roundCount+=1
    		doc.write(f, encoding="utf-8", xml_declaration=True)
    	else:
            pass

def addConsonantAttr(self):
    glyphpath = GetFolder("Pick a directory")
    filelist = os.listdir(glyphpath)
    
    for f in filelist:
    	if f.endswith(".glif"):
    		doc = parse(f)
    		root = doc.getroot()
    		totalminX=1000
    		for outline in root.iter("outline"):
    			for contour in outline.iter("contour"):
    				minX = 1000
    				minY = 1000
    				maxX = 0
    				maxY = 0
    				for point in contour.iter("point"):
    					pointX = int(float(point.get('x')))
    					pointY = int(float(point.get('y')))
    					if minX > pointX:
    						minX = pointX
    					if maxX < pointX:
    						maxX = pointX
    					if minY > pointY:
    						minY = pointY
    					if maxY < pointY:
    						maxY = pointY
    					if totalminX > minX:
    						totalminX = minX
    						
    		for outline in root.iter("outline"):
    			connerCount = 1
    			for contour in outline.iter("contour"):
    				minX = 1000
    				minY = 1000
    				maxX = 0
    				maxY = 0

    				vessel = []
    				for point in contour.iter("point"):
    					pointX = int(float(point.get('x')))
    					pointY = int(float(point.get('y')))
    					if minX > pointX:
    						minX = pointX
    					if maxX < pointX:
    						maxX = pointX
    					if minY > pointY:
    						minY = pointY
    					if maxY < pointY:
    						maxY = pointY

    				horizontalLine = maxX - minX
    				verticalLine = maxY - minY
    				for point in contour.iter("point"):
    					x = int(float(point.get('x')))
    					y = int(float(point.get('y')))

    					dx = 0
    					dy = 0
    					for point2 in contour.iter("point"):
    						compX = int(float(point2.get('x')))
    						compY = int(float(point2.get('y')))

    						if x == compX:
    							if y == compY:
    								continue
    							elif y > compY:
    								dy = -1
    							else:
    								dy = 1

    						if y == compY:
    							if x == compX:
    								continue
    							elif x > compX:
    								dx = -1
    							else:
    								dx = 1

    					if dx == 1 and dy == 1:
    						vessel.append(point)

    				result = sorted(vessel,key=lambda vessel: int(float(vessel.get('x'))))
    				result2 = sorted(vessel,key=lambda vessel: int(float(vessel.get('y'))))
    				if len(vessel) ==0:
    					pass
    				elif len(vessel) == 1:
    					if horizontalLine*3  < verticalLine:
    						tmpx = int(float(result[0].get('x')))
    						if tmpx == totalminX:
    							result[0].set('corner',str(connerCount))
    							connerCount+=1
    				elif int(float(result[0].get('x'))) == int(float(result2[0].get('x'))) :
    					result[0].set('corner',str(connerCount))
    					connerCount+=1
    		doc.write(f, encoding="utf-8", xml_declaration=True)