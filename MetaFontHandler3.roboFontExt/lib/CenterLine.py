from mojo.events import BaseEventTool, installTool, EditingTool
from mojo.drawingTools import *
from mojo.roboFont import CurrentFont,CurrentGlyph
from defconAppKit.windows.baseWindow import BaseWindowController
from mojo.roboFont import CurrentGlyph

from AppKit import *

class CenterLine(BaseEventTool, BaseWindowController):
    def get_penPair(self, point):
        attribute = "penPair"
        if point.name == None:     
            return ""
        if point.name.find(attribute) == -1:   
            return ""
        penPairIndex = point.name.index(attribute) + 10
        if point.name[penPairIndex + 2].isdigit():        
            return point.name[penPairIndex:penPairIndex + 4]
        else:
            return point.name[penPairIndex:penPairIndex + 3]
            
    def get_innerType(self, point):
        attribute = "innerType"
        if point.name == None:
            return ""
        if point.name.find(attribute) == -1:
            return ""
        innerTypeIndex = point.name.index(attribute) + 12
        innerType = point.name[innerTypeIndex : innerTypeIndex + 6]
        if innerType.find(",") != -1:
            innerType = innerType[:innerType.index(",") - 1]
        return innerType
            
    def extDigit(self, penPair):
        if penPair == "":
            return
        if penPair[2].isdigit():    
            return penPair[1:3]
        else:
            return penPair[1]
            
    def isPair(self, penPair1, penPair2):
        pair1 = self.extDigit(penPair1)
        pair2 = self.extDigit(penPair2)
        if pair1 == pair2:
            return True
        else:
            return False
            
    def isCirclePair(self, contour1, contour2):
        penPair1 = ""
        while penPair1 == "":
            i = 0
            pair = self.get_penPair(contour1.points[i])
            if pair != "":
                penPair1 = pair
            else:
                i = i + 1
        for point in contour2.points:
            if penPair1[:2] == self.get_penPair(point)[:2]:
                return True
        return False

    def drawCircleLine(self, contour1, contour2):
        curveSet = []
        for i in range(0, len(contour1.points)):
            if i == len(contour1.points) - 1:
                break
            if (contour1.points[i].type == "line" or contour1.points[i].type == "curve") and contour1.points[i + 1].type == "offcurve":
                curve = []
                for j in range(0, 4):
                    try:
                        curve.append(contour1.points[i + j])
                    except IndexError:
                        curve.append(contour1.points[0])
                curveSet.append(curve)
        for i in range(0, len(contour2.points)):
            if i == len(contour2.points) - 1:
                break
            if (contour2.points[i].type == "line" or contour2.points[i].type == "curve") and contour2.points[i + 1].type == "offcurve":
                curve = []
                for j in range(0, 4):
                    try:
                        curve.append(contour2.points[i + j])
                    except IndexError:
                        curve.append(contour2.points[0])
                curveSet.append(curve)
        for currentSet in curveSet:
            penPair1_1 = self.get_penPair(currentSet[0])
            penPair1_2 = self.get_penPair(currentSet[-1])
            for otherSet in curveSet:
                if currentSet == otherSet:
                    continue
                penPair2_1 = self.get_penPair(otherSet[0])
                penPair2_2 = self.get_penPair(otherSet[-1])
                if (self.isPair(penPair1_1, penPair2_1) and self.isPair(penPair1_2, penPair2_2)) or (self.isPair(penPair1_2, penPair2_1) and self.isPair(penPair1_1, penPair2_2)):
                    path = NSBezierPath.bezierPath()
                    currentColor = NSColor.redColor()
                    currentColor.set()
                    path.moveToPoint_(((currentSet[0].x + otherSet[3].x) / 2, (currentSet[0].y + otherSet[3].y) / 2))
                    path.curveToPoint_controlPoint1_controlPoint2_(((currentSet[3].x + otherSet[0].x) / 2, (currentSet[3].y + otherSet[0].y) / 2), 
                        ((currentSet[1].x + otherSet[2].x) / 2 , (currentSet[1].y + otherSet[2].y) / 2), 
                        ((currentSet[2].x + otherSet[1].x) / 2, (currentSet[2].y + otherSet[1].y) / 2))
                    path.stroke()

    def isCircle(self, contour):
        for point in contour.points:
            if point.type == "line":
                return False
        return True
        
    def isInside(self, x, y, contour):
        crosses = 0
        for i in range(0, len(contour.points)):
            j = (i + 1) % len(contour.points)
            if contour.points[i].y > y != contour.points[j].y > y:
                try:
                    atX = (contour.points[j].x - contour.points[i].x) * (y - contour.points[i].y) / (contour.points[j].y - contour.points[i].y) + contour.points[i].x
                except ZeroDivisionError:
                    atX = contour.points[i].x
                if(x < atX):
                    crosses = crosses + 1
        return crosses % 2 > 0

    def isContourInside(self, contourSet, contour):
        for c in contourSet:
            if c is contour:
                continue
            if contour.contourInside(c):
                return c
        return False

    def getPointIndex(self, point, contour):
        for index in range(0, len(contour.points)):
            if point == contour.points[index]:
                return index
        return -1

    def drawDoubleContourLine(self, contourSet, contour):
        path = NSBezierPath.bezierPath()
        currentColor = NSColor.redColor()
        currentColor.set()
        pairContour = self.isContourInside(contourSet, contour)
        prevMiddlePoint = None
        found = False
        for p in contour.points:
            penPair = self.get_penPair(p)
            for pair in contour.points:
                if p == pair:
                    continue
                elif self.isPair(penPair, self.get_penPair(pair)):
                    if prevMiddlePoint:
                        path.moveToPoint_(prevMiddlePoint)
                        middlePoint = ((p.x + pair.x) / 2, (p.y + pair.y) / 2)
                        path.lineToPoint_(middlePoint)
                        path.stroke()
                        prevMiddlePoint = middlePoint
                        found = True
                    else:
                        prevMiddlePoint = ((p.x + pair.x) / 2, (p.y + pair.y) / 2)
            if not found:
                for pair in pairContour.points:
                    if self.isPair(penPair, self.getPenPair(pair)):
                        path.moveToPoint_(prevMiddlePoint)
                        middlePoint = ((p.x + pair.x) / 2, (p.y + pair.y) / 2)
                        path.lineToPoint_(middlePoint)
                        path.stroke()
                        prevMiddlePoint = middlePoint
                    else:
                        prevMiddlePoint = ((p.x + pair.x) / 2, (p.y + pair.y) / 2)
        return pairContour
    
    def draw(self, scale):
        G = CurrentGlyph()
        doneContour = []   
        circleContour = None
        for currentContour in G.contours:
            try:
                if currentContour in doneContour:
                    continue
                # if self.isContourInside(G.contours, currentContour):
                #     doneContour.append(self.drawDoubleContourLine(G.contours, currentContour))
                if self.isCircle(currentContour):
                    if circleContour == None:
                        circleContour = currentContour
                        continue
                    else:
                        if self.isCirclePair(circleContour, currentContour):
                            self.drawCircleLine(circleContour, currentContour)
                            doneContour.append(circleContour)
                            doneContour.append(currentContour)
                            circleContour = None
                            continue
                pairPoints = {}
                for currentPoint in currentContour.points:
                    penPair1 = self.get_penPair(currentPoint)
                    if penPair1 == "":
                        continue
                    else:
                        for nextPoint in currentContour.points:
                            if currentPoint == nextPoint:
                                continue
                            penPair2 = self.get_penPair(nextPoint)
                            if self.isPair(penPair1, penPair2) and not (currentPoint in pairPoints or nextPoint in pairPoints):
                                pairPoints[currentPoint] = nextPoint
                                break
                drawed = 0      
                for currentIndex in range(0, len(currentContour.points)):
                    curve = False
                    nextIndex = (currentIndex + 1) % len(currentContour.points)
                    while currentContour.points[nextIndex].type == "offcurve":
                        nextIndex = (nextIndex + 1) % len(currentContour.points)
                        curve = True
                    currentPoint = currentContour.points[currentIndex]
                    nextPoint = currentContour.points[nextIndex]
                    currentPenPair = self.get_penPair(currentPoint)
                    nextPenPair = self.get_penPair(nextPoint)
                    if currentPenPair != "" and nextPenPair != "" and not self.isPair(currentPenPair, nextPenPair):
                        currentPairPoint = None
                        nextPairPoint = None
                        for cp in pairPoints:
                            if cp == currentPoint:
                                currentPairPoint = pairPoints[cp]
                                break
                            elif pairPoints[cp] == currentPoint:
                                currentPairPoint = cp
                                break
                        for np in pairPoints:
                            if np == nextPoint:
                                nextPairPoint = pairPoints[np]
                                break
                            elif pairPoints[np] == nextPoint:
                                nextPairPoint = np
                                break
                        currentPairIndex = self.getPointIndex(currentPairPoint, currentContour)
                        nextPairIndex = self.getPointIndex(nextPairPoint, currentContour)
                        pairCurve = False
                        if currentContour.points[(nextPairIndex + 1) % len(currentContour.points)].type == "offcurve" and currentContour.points[currentPairIndex - 1].type == "offcurve":
                            pairCurve = True
                        else:
                            pairCurve = False
                        if curve == False:
                            if pairCurve == False:
                                path = NSBezierPath.bezierPath()
                                currentColor = NSColor.redColor()
                                currentColor.set()
                                path.moveToPoint_(((currentPoint.x + currentPairPoint.x) / 2, (currentPoint.y + currentPairPoint.y) / 2))
                                path.lineToPoint_(((nextPoint.x + nextPairPoint.x) / 2, (nextPoint.y + nextPairPoint.y) / 2))
                                path.stroke()
                            else:
                                ccp = currentContour.points
                                path = NSBezierPath.bezierPath()
                                currentColor = NSColor.redColor()
                                currentColor.set()
                                path.moveToPoint_(((currentPoint.x + currentPairPoint.x) / 2, (currentPoint.y + currentPairPoint.y) / 2))
                                path.curveToPoint_controlPoint1_controlPoint2_(((nextPoint.x + nextPairPoint.x) / 2, (nextPoint.y + nextPairPoint.y) / 2), 
                                    (((currentPoint.x + nextPoint.x) / 2 + ccp[currentPairIndex - 1].x) / 2, ((currentPoint.y + nextPoint.y) / 2 + ccp[currentPairIndex - 1].y) / 2), 
                                    (((currentPoint.x + nextPoint.x) / 2 + ccp[currentPairIndex - 2].x) / 2, ((currentPoint.y + nextPoint.y) / 2 + ccp[currentPairIndex - 2].y) / 2))
                                path.stroke()
                        else:
                            if pairCurve == False:
                                ccp = currentContour.points
                                path = NSBezierPath.bezierPath()
                                currentColor = NSColor.redColor()
                                currentColor.set()
                                path.moveToPoint_(((currentPoint.x + currentPairPoint.x) / 2, (currentPoint.y + currentPairPoint.y) / 2))
                                path.curveToPoint_controlPoint1_controlPoint2_(((nextPoint.x + nextPairPoint.x) / 2, (nextPoint.y + nextPairPoint.y) / 2), 
                                    (((currentPairPoint.x + nextPairPoint.x) / 2 + ccp[currentIndex + 1].x) / 2, ((currentPairPoint.y + nextPairPoint.y) / 2 + ccp[currentIndex + 1].y) / 2), 
                                    (((currentPairPoint.x + nextPairPoint.x) / 2 + ccp[currentIndex + 2].x) / 2, ((currentPairPoint.y + nextPairPoint.y) / 2 + ccp[currentIndex + 2].y) / 2))
                                path.stroke()
                            else:
                                ccp = currentContour.points
                                path = NSBezierPath.bezierPath()
                                currentColor = NSColor.redColor()
                                currentColor.set()
                                path.moveToPoint_(((currentPoint.x + currentPairPoint.x) / 2, (currentPoint.y + currentPairPoint.y) / 2))
                                path.curveToPoint_controlPoint1_controlPoint2_(((nextPoint.x + nextPairPoint.x) / 2, (nextPoint.y + nextPairPoint.y) / 2), 
                                    ((ccp[currentIndex + 1].x + ccp[currentPairIndex - 1].x) / 2, (ccp[currentIndex + 1].y + ccp[currentPairIndex - 1].y) / 2), 
                                    ((ccp[currentIndex + 2].x + ccp[currentPairIndex - 2].x) / 2, (ccp[currentIndex + 2].y + ccp[currentPairIndex - 2].y) / 2))
                                path.stroke()
                        drawed = drawed + 1
            except AttributeError:
                continue
        
installTool(CenterLine())