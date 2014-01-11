'''
Created on Jan 11, 2014

@author: sushant
'''

import numpy as np

    
class MarchingSquareHandler:
    
    #default Values
    gridSize = 0
    winHeight = 0
    winWidth = 0
    _nSquare = 0
    radius=0
    isovalue=0
    linelist=[]
    _scVal = []
    
    def setWindow(self,w,h):
        self.winHeight = h
        self.winWidth = w
    
    def setGridSize(self,grid):
        self.gridSize = grid
        
    def setRadius(self,r):
        self.radius = r
        
    def getGridSize(self):
        return self.gridSize
    
    def getLineList(self):
        return self.linelist
        
    #define Scalar Function (Circle)
    def scalarFunc(self,x,y,r): # a circle
        return (x-200)**2 + (y-200)**2 - r**2
    
    #check if scalar function intersects
    def checkifIntersects(self,_val):
        if _val[0] > 0 and _val[1] > 0 and _val[2] > 0 and _val[3] > 0:
            return False
        if _val[0] < 0 and _val[1] < 0 and _val[2] < 0 and _val[3] < 0:
            return False
        return True
        
    #Get the intersected indexs
    def getIntersects(self,_val):
        index=[]
        if _val[0] * _val[1] < 0:
            index.append([0,1])
        if _val[1] * _val[2] < 0:
            index.append([1,2])
        if _val[2] * _val[3] < 0:
            index.append([2,3])
        if _val[3] * _val[0] < 0:
            index.append([3,0])
        return index
        
    #Compute Scalar Values
    def compSval(self):
        lenY = len(np.arange(0,self.winHeight,self.gridSize))
        lenX = len(np.arange(0,self.winWidth,self.gridSize))
        for y in range(lenY):
            for x in range(lenX):
                self._scVal[x][y] = self.scalarFunc(self.gridSize*x,self.gridSize*y,self.radius)
        
    #Find the intersection Point
    def intersectionPoint(self,p1,p2,isoValue,v1,v2):
        _p=[0,0]
        _p[0] = p1[0] + (isoValue - v1)*(p2[0] - p1[0] ) / (v2-v1)
        _p[1] = p1[1] + (isoValue - v1)*(p2[1] - p1[1] ) / (v2-v1)
        return _p
        
    #Get all the Data about square
    def getSquareData(self,n): #returns sqaures sv and vertices
        r=n/((self.winHeight/self.gridSize)-2)
        c=n%((self.winHeight/self.gridSize)-2)
        sv=[self._scVal[r][c],self._scVal[r][c+1],self._scVal[r+1][c+1],self._scVal[r+1][c]]
        vertices =[[self.gridSize*r,self.gridSize*c],[self.gridSize*r,self.gridSize*(c+1)],[self.gridSize*(r+1),self.gridSize*(c+1)],[self.gridSize*(r+1),self.gridSize*c]]    
        return [sv,vertices]
        
    #Check if Zero
    def checkSingularity(self,sv):
        found=False
        index=[]
        for i in np.arange(0,len(sv)):
            if sv[i] == 0:
                found = True
                index.append(i)
        return [found,index]
    
    #Computes the line list
    def compute(self):
        self._scVal = np.zeros(((self.winWidth/self.gridSize),(self.winHeight/self.gridSize)))
        _nSquare = ((self.winHeight/self.gridSize)-2)*((self.winWidth/self.gridSize)-2)
        self.compSval()
        for i in np.arange(0,_nSquare):
            [_sv,_vert] = self.getSquareData(i)
            if self.checkifIntersects(_sv):
                isSig=self.checkSingularity(_sv)
                if isSig[0]:
                    if len(isSig[1]) > 1: #two point Singularity
                        p1 = _vert[isSig[1][0]]
                        p2 = _vert[isSig[1][1]]
                    else: #one point Singularity
                        #check if other intersection exists
                        intPoint = self.getIntersects(_sv)
                        if len(intPoint) == 0:
                            p1 = _vert[isSig[1][0]]
                            p2 = _vert[isSig[1][0]]
                        else:
                            [_i1] = self.getIntersects(_sv)
                            p1 =self.intersectionPoint(_vert[_i1[0]],_vert[_i1[1]],self.isovalue,_sv[_i1[0]],_sv[_i1[1]])
                            p2 = _vert[isSig[1][0]]
                            
                else:
                    [_i1,_i2]=self.getIntersects(_sv)
                    p1 =self.intersectionPoint(_vert[_i1[0]],_vert[_i1[1]],self.isovalue,_sv[_i1[0]],_sv[_i1[1]])
                    p2=self.intersectionPoint(_vert[_i2[0]],_vert[_i2[1]],self.isovalue,_sv[_i2[0]],_sv[_i2[1]])
                self.linelist.append([p1,p2])
        
