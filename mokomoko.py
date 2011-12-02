import math
import numpy as np
import cv
import sdxf

class mokomokoGenerator:
  def __init__(self, g, k, end, mask):
    #bind
    self.g = g
    self.k = k
    self.end = end
    self.mask = mask
    #initial setting
    self.x = len(self.mask)
    self.y = len(self.mask[0])
    self.w = np.zeros((self.x,self.y,3))
    for x in xrange(self.x):
      for y in xrange(self.y):
        self.w[x][y][0] = x
        self.w[x][y][1] = y
    self.v = np.zeros((self.x,self.y,3))
    self.f = np.zeros((self.x,self.y,3))
    self.zero = np.zeros((3))

  def run(self):
    e = self.iterate()
    for i in xrange(20):
      e = self.iterate()

  def outGnuplot(self):
    for x in xrange(self.x):
      for y in xrange(self.y):
        print "%f %f %f"%(self.w[x][y][0],self.w[x][y][1],self.w[x][y][2])
      print ""

  def iterate(self):
    eMax = 0
    self.f = np.zeros((self.x,self.y,3))
    for x in xrange(1, self.x - 1):
      for y in xrange(1, self.y - 1):
        if self.mask[x][y] != 0:
          #calculate f
          self.f[x][y] = np.zeros(3)
          self.f[x][y] += self.g
          self.f[x][y] -= k * self.getDistance(self.w[x][y], self.w[x+1][y])
          self.f[x][y] -= k * self.getDistance(self.w[x][y], self.w[x-1][y])
          self.f[x][y] -= k * self.getDistance(self.w[x][y], self.w[x][y+1])
          self.f[x][y] -= k * self.getDistance(self.w[x][y], self.w[x][y-1])
    #calculate location
    self.v += self.f
    self.w += self.v 
    return eMax

  def getDistance(self, arrayA, arrayB):
    return arrayA - arrayB

  def outDXF(self):
    d = sdxf.Drawing()
    for x in xrange(self.x-1):
      for y in xrange(self.y-1):
        d.append(sdxf.Face(points = [
        (self.w[x][y][0], self.w[x][y][1], self.w[x][y][2]),
        (self.w[x][y+1][0], self.w[x][y+1][1], self.w[x][y+1][2]),
        (self.w[x+1][y+1][0], self.w[x+1][y+1][1], self.w[x+1][y+1][2]),
        (self.w[x+1][y][0], self.w[x+1][y][1], self.w[x+1][y][2]),
        ]))
    d.saveas('out.dxf')

  def regulate(self):
    zmax = 0
    for x in xrange(self.x):
      for y in xrange(self.y):
        zmax = self.w[x][y][2] if self.w[x][y][2] > zmax else zmax
    for x in xrange(self.x):
      for y in xrange(self.y):
        self.w[x][y][2] /= zmax

g = np.array([0, 0, 0.0001])
k = 0.02 
end = 0.0001
im = cv.LoadImageM("oquno.bmp", cv.CV_LOAD_IMAGE_GRAYSCALE)
mask = np.asarray(im)
m = mokomokoGenerator(g, k, end, mask)
m.run()
m.regulate()
m.outDXF()
