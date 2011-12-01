import math
import numpy as np
import cv

class mokomokoGenerator:
  def __init__(self, g, k, end, w, fp):
    self.g = g
    self.k = k
    self.end = end
    self.w = w
    self.fp = fp
    self.x = len(w)
    self.y = len(w[0])
    self.v = np.zeros((self.x,self.y,3))
    self.f = np.zeros((self.x,self.y,3))
    self.zero = np.zeros((3))

  def run(self):
    e = self.iterate()
    for i in xrange(50):
      e = self.iterate()

  def outGnuplot(self):
    for x in xrange(self.x):
      for y in xrange(self.y):
        print "%f %f %f"%(self.w[x][y][0],self.w[x][y][1],self.w[x][y][2])

  def iterate(self):
    eMax = 0
    self.f = np.zeros((self.x,self.y,3))
    for x in xrange(1, self.x - 1):
      for y in xrange(1, self.y - 1):
        if self.fp[x][y] != 1:
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

g = np.array([0, 0, 0.0001])
k = 0.02 
end = 0.0001
w = np.zeros((20, 20, 3))
for x in xrange(20):
  for y in xrange(20):
    w[x][y][0] = x
    w[x][y][1] = y
fp = np.zeros((20, 20))
for x in xrange(10):
  for y in xrange(10):
    fp[x][y] = 1
m = mokomokoGenerator(g, k, end, w, fp)
m.run()
m.outGnuplot()()
