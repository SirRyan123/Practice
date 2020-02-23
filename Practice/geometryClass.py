class Cylinder:

    pi = 3.14
    
    def __init__(self, height = 1, radius = 1):
        self.height = height
        self.radius = radius


    def findVolume(self):
        return (self.pi * (self.radius**2) * self.height)
        

    def findSurfaceArea(self):
        firstPart = (2 * self.pi) * (self.radius * self.height)
        secondPart = (2 * self.pi) * (self.radius**2)

        return (firstPart + secondPart)


class Line:

    def __init__(self, coord1, coord2):
        self.coord1 = coord1
        self.coord2 = coord2


    def findDistance(self):
        x1,y1 = self.coord1
        x2,y2 = self.coord2

        firstPart = ((x2 - x1)**2 + (y2 - 1)**2)

        return (firstPart ** 0.5)


    def findSlope(self):
        x1,y1 = self.coord1
        x2,y2 = self.coord2

        firstPart = (y2 - y1)
        secondPart = (x2 - x1)

        return (firstPart / secondPart)
