'''
Author: Vu Tran
Date: 02/08/2022
Purpose: Student prototype for lab 2
'''
import arcpy
from arcpy import env
import sys
import math


env.workspace = r"C:\Users\tuanv\Desktop\GIS_Programing\Lab4\MasterData"
sys.path[0]
env.overwriteOutput = 1

shapefile = 'watersheds_3D.shp'
dem = 'demlab4'
#Part 1

#My list of funtions
def CalPerimeter2D(Polygon):  
    Xcoord1 = []
    Ycoord1 = []
    for x in Polygon:
        Xcoord1.append(x.X)
        Ycoord1.append(x.Y)
    count = len(Xcoord1)-1
    perimeter = 0
    while count>=0:
        perimeter = perimeter + abs(math.sqrt(((Xcoord1[count]-Xcoord1[count-1])**2)+((Ycoord1[count]-Ycoord1[count-1])**2)))
        count = count - 1
    return perimeter
        
def CalArea2D(Polygon):
    Xcoord1 = []
    Ycoord1 = []
    for x in Polygon:
        Xcoord1.append(x.X)
        Ycoord1.append(x.Y)
    count2 = len(Xcoord1)-1
    area = 0
    while count2>=0:
        area = area + 0.5*(((Xcoord1[count2]-Xcoord1[count2-1]))*((Ycoord1[count2]+Ycoord1[count2-1])))
        count2 = count2 - 1
    return area

def CalCircularity2D(Polygon):
    Xcoord1 = []
    Ycoord1 = []
    for x in Polygon:
        Xcoord1.append(x.X)
        Ycoord1.append(x.Y)
    count = len(Xcoord1)-1
    perimeter = 0
    area = 0
    circularity = 0
    while count>=0:
        perimeter = perimeter + abs(math.sqrt(((Xcoord1[count]-Xcoord1[count-1])**2)+((Ycoord1[count]-Ycoord1[count-1])**2)))
        area = area + 0.5*(((Xcoord1[count]-Xcoord1[count-1]))*((Ycoord1[count]+Ycoord1[count-1])))
        count = count - 1
    circularity = (4*math.pi*area)/perimeter**2
    return circularity

def CalPerimeter3D(Polygon):
    Xcoord1 = []
    Ycoord1 = []
    Zcoord1 = []
    for x in Polygon:
        Xcoord1.append(x.X)
        Ycoord1.append(x.Y)
        Zcoord1.append(x.Z)
    count = len(Xcoord1)-1
    perimeter3D = 0
    while count>=0:
        perimeter3D = perimeter3D + math.sqrt(abs(((math.sqrt(((Xcoord1[count]-Xcoord1[count-1])**2)+((Ycoord1[count]-Ycoord1[count-1])**2)))**2) + ((Zcoord1[count]-Zcoord1[count-1])**2)))
        count = count - 1
    return perimeter3D

def CalArea3D(raster,shapefile):
    RasterDescribe = arcpy.Describe(raster)
    meanCellHeight = RasterDescribe.meanCellHeight
    arcpy.CheckOutExtension("Spatial")
    slope = arcpy.sa.Slope(raster)
    SlopeRadian = slope*(math.pi/180)
    SlopeCos =arcpy.sa.Cos(SlopeRadian)
    Area3D = (meanCellHeight**2) / SlopeCos
    arcpy.sa.ZonalStatisticsAsTable(shapefile,'ID',Area3D,'Table22')
    area3d = []
    with arcpy.da.SearchCursor('table22','SUM') as cursor:
        for row in cursor:
            area3d.append(row[0])
    return area3d

def CalCircularity3D(Polygon,Area3D):
    Xcoord1 = []
    Ycoord1 = []
    Zcoord1 = []
    for x in Polygon:
        Xcoord1.append(x.X)
        Ycoord1.append(x.Y)
        Zcoord1.append(x.Z)
    count = len(Xcoord1)-1
    perimeter3D = 0
    while count>=0:
        perimeter3D = perimeter3D + math.sqrt(abs(((math.sqrt(((Xcoord1[count]-Xcoord1[count-1])**2)+((Ycoord1[count]-Ycoord1[count-1])**2)))**2) + ((Zcoord1[count]-Zcoord1[count-1])**2)))
        count = count - 1
    circularity3D = (4*math.pi*Area3D)/perimeter3D**2
    return circularity3D

def CalLca(Polygon):
    Xcoord1 = []
    Ycoord1 = []
    Zcoord1 = []
    outflow = []
    for x in Polygon:
        Xcoord1.append(x.X)
        Ycoord1.append(x.Y)
        Zcoord1.append(x.Z)
    count1 = len(Xcoord1)-1
    count = len(Xcoord1)-1
    CentroidX = 0
    CentroidY = 0
    area = 0
    while count1>=0:
        area = area + 0.5*(((Xcoord1[count1]-Xcoord1[count1-1]))*((Ycoord1[count1]+Ycoord1[count1-1])))
        count1 = count1 - 1
    while count>=0:
        CentroidX += (-1/(6*area))*(Xcoord1[count-1]+Xcoord1[count])*(((Xcoord1[count-1]*Ycoord1[count]))-(Xcoord1[count]*Ycoord1[count-1]))
        CentroidY += (-1/(6*area))*(Ycoord1[count-1]+Ycoord1[count])*(((Xcoord1[count-1]*Ycoord1[count]))-(Xcoord1[count]*Ycoord1[count-1]))
        count = count-1
    Zmin = min(Zcoord1)
    for z in Polygon:
        if z.Z == Zmin:
            outflow.append(z.X)
            outflow.append(z.Y)
    Lca = math.sqrt(abs(((CentroidX-outflow[0])**2)+((CentroidY-outflow[1])**2)))
    return Lca

def CalReliefRatio(Polygon):
    Zcoord1 = []
    minZpoint = []
    for x in Polygon:
        Zcoord1.append(x.Z)
    
    
    Zmin = min(Zcoord1)
    Zmax = max(Zcoord1)
    for z1 in Polygon:
        if z1.Z == Zmin:
            minZpoint.append(z1.X)
            minZpoint.append(z1.Y)
      
    maxStream = 0      
    for x1 in Polygon:
        length = math.sqrt(((x1.X-minZpoint[0])**2)+((x1.Y-minZpoint[1])**2))
        if (length > maxStream):
            maxStream = length
    
    reliefRatio = (Zmax-Zmin)/maxStream
    return reliefRatio



#Create list of arrays
arrays = []
with arcpy.da.SearchCursor(shapefile,['SHAPE@']) as cursor:
    for i in cursor:
        arrays.append(i[0].getPart(0)) #append each Polygon's array into arrays list to calculate values for each Polygon

#Create empty list of values that need to be calculated
Polygon2DArea = []
PolygonPerimeter2D = []
PolygonCircularity2D = []

PolygonPerimeter3D = []
Polygon3DArea = []
PolygonCircularity3D = []

PolygonLca = []
PolygonReliefRatio = []


Polygon3DArea.append(CalArea3D(dem,shapefile)) #Calculate 3D Area outside of the loop, because I would need it to put in as parameter for my Circularity 3D function

#Calculate all of my values using functions and by looping through each Polygon's array
count = 0
for array in arrays:
    Polygon2DArea.append(CalArea2D(array))
    PolygonPerimeter2D.append(CalPerimeter2D(array))
    PolygonCircularity2D.append(CalCircularity2D(array))
    PolygonPerimeter3D.append(CalPerimeter3D(array))
    PolygonLca.append((CalLca(array)))
    PolygonReliefRatio.append(CalReliefRatio(array))
    PolygonCircularity3D.append(CalCircularity3D(array,Polygon3DArea[0][count]))
    print 'Circularity Ratio 2D for Polygon',count, 'is:',PolygonCircularity2D[count]
    print 'Circularity Ratio 3D for Polygon',count, 'is:',PolygonCircularity3D[count]
    print 'Length to Center of Area (Lca) for Polygon',count, 'is:',PolygonLca[count]
    print 'Relief Ratio for Polygon',count, 'is:',PolygonReliefRatio[count]
    print ''
    count = count+1



#Add circularity 2D to the Attribute table
arcpy.management.AddField(shapefile, 'Cir2D','FLOAT')
with arcpy.da.UpdateCursor(shapefile,'Cir2D') as cursor:
    count = 0
    for row in cursor:
        row[0] = PolygonCircularity2D[count]
        cursor.updateRow(row)
        count = count+1
#Add circularity 3D to the Attribute table
arcpy.management.AddField(shapefile, 'Cir3D','FLOAT')
with arcpy.da.UpdateCursor(shapefile,'Cir3D') as cursor:
    count1 = 0
    for row in cursor:
        row[0] = PolygonCircularity3D[count1]
        cursor.updateRow(row)
        count1 = count1+1
#Add Lca to the Attribute table
arcpy.management.AddField(shapefile, 'Lca','FLOAT')
with arcpy.da.UpdateCursor(shapefile,'Lca') as cursor:
    count2 = 0
    for row in cursor:
        row[0] = PolygonLca[count2]
        cursor.updateRow(row)
        count2 = count2+1
#Add Relief Ratio to the Attribute table
arcpy.management.AddField(shapefile, 'Relief','FLOAT')
with arcpy.da.UpdateCursor(shapefile,'Relief') as cursor:
    count3 = 0
    for row in cursor:
        row[0] = PolygonReliefRatio[count3]
        cursor.updateRow(row)
        count3 = count3+1
