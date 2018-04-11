import math
import matplotlib.pyplot as plt
import sys


class point2D:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.id=-1

class edgelistnode:
    def __init__(self,u,v):
        self.u = u
        self.v = v
        self.weight=0

class convexhull_jarvis:
    def __init__(self):
        self.points=list()
        self.edgelist = list()

    def addpoints(self,xcoord,ycoord,n,idtogiven):
        self.points=[0]*n
        startid=idtogiven+1
        for i in range(n):
            temp = point2D(xcoord[i],ycoord[i])
            temp.id=startid+i
            self.points[i]=temp

    def findorientation(self,p1,p2,intermediate):
        # 0 for collinear
        # -1 for counterclockwise direction
        #  1 for clockwise diretion
        check = ((p2.y- p1.y)*(intermediate.x - p2.x)) - ((p2.x-p1.x)*(intermediate.y-p2.y))
        if check==0:
            return 0
        if check > 0:
            return 1
        if check < 0 :
            return -1


    def distance(self,firstpoint,secondpoint):
        distance = math.sqrt((secondpoint.x-firstpoint.x)**2 +(secondpoint.y-firstpoint.y)**2)
        return distance

    def makehull(self,n):
        if n < 3 :
            return self.points

        hullcreated = list()

        leftindex = 0
        for i in range(1,n):
            p1=self.points[i].x
            p2=self.points[leftindex].x
            if self.points[i].x < self.points[leftindex].x :
                leftindex=i

        presentindex = leftindex
        while True:
            xpresenthere = self.points[presentindex].x
            ypresenthere =self.points[presentindex].y
            hullcreated.append(self.points[presentindex])
            nextindex = (presentindex+1)%n

            for i in range(n):
                if self.findorientation(self.points[presentindex],self.points[i],self.points[nextindex])==-1:
                    nextindex=i

            presentindex=nextindex

            if presentindex==leftindex:
                break

        return hullcreated

    def onsegment(self, firstpoint, secondpoint, thirdpoint):
        if (secondpoint.x <= max(firstpoint.x, thirdpoint.x) and secondpoint.x >= min(firstpoint.x, thirdpoint.x)) and (
                secondpoint.y <= max(firstpoint.y, thirdpoint.y) and secondpoint.y >= min(firstpoint.y, thirdpoint.y)):
            return True
        else:
            return False

    def checkifedge(self,firstpoint,secondpoint,totallist):
        x1=firstpoint.x
        y1=firstpoint.y
        x2=secondpoint.x
        y2=secondpoint.y
        flage=1
        for i in range(len(totallist)):
            for j in range(len(totallist[i])):
                if j!=len(totallist[i])-1:
                    otherfirst = totallist[i][j]
                    othersecond = totallist[i][j+1]
                    otherfirstx = otherfirst.x
                    otherfirsty=otherfirst.y
                    othersecondx = othersecond.x
                    othersecondy=othersecond.y
                    if otherfirstx==firstpoint.x and otherfirsty==firstpoint.y:
                        pass
                    elif otherfirstx==secondpoint.x and otherfirsty==secondpoint.y:
                        pass
                    elif othersecondx==firstpoint.x and othersecondy==firstpoint.y:
                        pass
                    elif othersecondx==secondpoint.x and othersecondy==secondpoint.y:
                        pass
                    else :
                        o1=self.findorientation(firstpoint,secondpoint,otherfirst)
                        o2=self.findorientation(firstpoint,secondpoint,othersecond)
                        o3=self.findorientation(otherfirst,othersecond,firstpoint)
                        o4=self.findorientation(otherfirst,othersecond,secondpoint)

                        if o1!=o2 and o3!=o4:
                            flage=0
                            return True

                        if o1==0 and self.onsegment(firstpoint,otherfirst,secondpoint):
                            flage=0
                            return True
                        if o2==0 and self.onsegment(firstpoint,othersecond,secondpoint):
                            flage=0
                            return True
                        if o3==0 and self.onsegment(otherfirst,firstpoint,othersecond):
                            flage=0
                            return True
                        if o4==0 and self.onsegment(otherfirst,secondpoint,othersecond):
                            flage=0
                            return True
                        #do something
                else:
                    otherfirst=totallist[i][j]
                    othersecond=totallist[i][0]
                    otherfirstx=otherfirst.x
                    otherfirsty=otherfirst.y
                    othersecondx=othersecond.x
                    othersecondy=othersecond.y
                    if otherfirstx==firstpoint.x and otherfirsty==firstpoint.y:
                        pass
                    elif otherfirstx==secondpoint.x and otherfirsty==secondpoint.y:
                        pass
                    elif othersecondx==firstpoint.x and othersecondy==firstpoint.y:
                        pass
                    elif othersecondx==secondpoint.x and othersecondy==secondpoint.y:
                        pass
                    else :
                        o1 = self.findorientation(firstpoint, secondpoint, otherfirst)
                        o2 = self.findorientation(firstpoint, secondpoint, othersecond)
                        o3 = self.findorientation(otherfirst, othersecond, firstpoint)
                        o4 = self.findorientation(otherfirst, othersecond, secondpoint)

                        if o1 != o2 and o3 != o4:
                            flage = 0
                            return True

                        if o1 == 0 and self.onsegment(firstpoint, otherfirst, secondpoint):
                            flage = 0
                            return True
                        if o2 == 0 and self.onsegment(firstpoint, othersecond, secondpoint):
                            flage = 0
                            return True
                        if o3 == 0 and self.onsegment(otherfirst, firstpoint, othersecond):
                            flage = 0
                            return True
                        if o4 == 0 and self.onsegment(otherfirst, secondpoint, othersecond):
                            flage = 0
                            return True
                    #do something

            if flage==0:
                break
        if flage==0:
            return True
        else:
            return False



    def findedges(self,totallist,sink):
        for i in range(len(totallist)):
            pointstocheck = list()
            currentpolygonpoints = list()
            for j in range(len(totallist)):
                for k in range(len(totallist[j])):
                    if i!=j:
                        pointstocheck.append(totallist[j][k])
                    else:
                        currentpolygonpoints.append(totallist[j][k])
            pointstocheck.append(sink)
            for j in range(len(currentpolygonpoints)):
                for k in range(len(pointstocheck)):
                    var = self.checkifedge(currentpolygonpoints[j],pointstocheck[k],totallist)
                    flag = 0
                    if var == False:
                        for w in range(len(self.edgelist)):
                            x1 = self.edgelist[w].u.x
                            y1 = self.edgelist[w].u.y
                            x2 = self.edgelist[w].v.x
                            y2 = self.edgelist[w].v.y

                            if (x1 == currentpolygonpoints[j].x and y1 == currentpolygonpoints[j].y and x2 ==
                                pointstocheck[k].x and y2 == pointstocheck[k].y) or (
                                    x2 == currentpolygonpoints[j].x and y2 == currentpolygonpoints[j].y and x1 ==
                                    pointstocheck[k].x and y1 == pointstocheck[k].y):
                                flag = 1
                                break
                        if flag == 0:
                            tempnode = edgelistnode(currentpolygonpoints[j], pointstocheck[k])
                            tempnode.weight=self.distance(currentpolygonpoints[j],pointstocheck[k])
                            self.edgelist.append(tempnode)
                    else:
                        pass


    def drawedges(self,source,sink,totallist):
        for i in range(len(totallist)):
            pointstocheck = list()
            currentpolygonpoints = list()
            for j in range(len(totallist)):
                for k in range(len(totallist[j])):
                    pointstocheck.append(totallist[j][k])

            currentpolygonpoints.append(source)
            pointstocheck.append(sink)
            for j in range(len(currentpolygonpoints)):
                for k in range(len(pointstocheck)):
                    var = self.checkifedge(currentpolygonpoints[j],pointstocheck[k],totallist)
                    flag = 0
                    if var == False:
                        for w in range(len(self.edgelist)):
                            x1 = self.edgelist[w].u.x
                            y1 = self.edgelist[w].u.y
                            x2 = self.edgelist[w].v.x
                            y2 = self.edgelist[w].v.y

                            if (x1 == currentpolygonpoints[j].x and y1 == currentpolygonpoints[j].y and x2 ==
                                pointstocheck[k].x and y2 == pointstocheck[k].y) or (
                                    x2 == currentpolygonpoints[j].x and y2 == currentpolygonpoints[j].y and x1 ==
                                    pointstocheck[k].x and y1 == pointstocheck[k].y):
                                flag = 1
                                break
                        if flag == 0:
                            tempnode = edgelistnode(currentpolygonpoints[j], pointstocheck[k])
                            tempnode.weight=self.distance(currentpolygonpoints[j],pointstocheck[k])
                            self.edgelist.append(tempnode)
                    else:
                        pass


    def dointersect(self,point1,point2,vertex,checkpoint):
        o1=self.findorientation(point1,point2,vertex)
        o2=self.findorientation(point1,point2,checkpoint)
        o3=self.findorientation(vertex,checkpoint,point1)
        o4=self.findorientation(vertex,checkpoint,point2)

        if o1!=o2 and o3!=o4:
            return True

        if o1==0 and self.onsegment(point1,vertex,point2):
            return True
        if o2==0 and self.onsegment(point1,checkpoint,point2):
            return True
        if o3==0 and self.onsegment(vertex,point1,checkpoint):
            return True
        if o4==0 and self.onsegment(vertex,point2,checkpoint):
            return True
        return False

    def checkinsidepolygon(self,vertex,totallist):
        flag = 0
        for i in range(len(totallist)):
            checkpoint=point2D(sys.maxsize,vertex.y)
            count=0
            for j in range(len(totallist[i])):
                if j!=len(totallist[i])-1:
                    point1=totallist[i][j]
                    point2=totallist[i][j+1]
                else:
                    point1=totallist[i][j]
                    point2=totallist[i][0]
                if(self.dointersect(point1,point2,vertex,checkpoint)):
                    if self.findorientation(point1,vertex,point2)==0:
                        var = self.onsegment(point1,vertex,point2)
                        if var == True:
                            flag=1
                            break
                    count+=1

            if count%2==1:
                flag=1
                break
            if flag==1:
                break

        if flag==1:
            return True
        else:
            return False

    def printhull(self,morethanonehullcreated,n):
        totallist=list()
        for i in range(len(morethanonehullcreated)):
            Xcoord = list()
            Ycoord = list()
            temp = list()
            for j in range(len(morethanonehullcreated[i])):
                print("(",morethanonehullcreated[i][j].x,",",morethanonehullcreated[i][j].y,")")
                node=morethanonehullcreated[i][j]
                Xcoord.append(morethanonehullcreated[i][j].x)
                Ycoord.append(morethanonehullcreated[i][j].y)
                temp.append(node)
            Xcoord.append(Xcoord[0])
            Ycoord.append(Ycoord[0])
            totallist.append(temp)
            for j in range(len(temp)):
                if j!=len(temp)-1:
                    nodeforedgelist=edgelistnode(temp[j],temp[j+1])
                    nodeforedgelist.weight=self.distance(temp[j],temp[j+1])
                else:
                    nodeforedgelist=edgelistnode(temp[j],temp[0])
                    nodeforedgelist.weight=self.distance(temp[j],temp[0])
                self.edgelist.append(nodeforedgelist)

            plt.fill(Xcoord,Ycoord)
            plt.scatter(Xcoord,Ycoord,c='black')

        # work remaining is finding the source and sink is valid or not and then plotting their edgelist also
        print("Enter the source and the sink vertex and be carefull that the vertex should be outside the polygon (space separated 4 integers)")
        x1,y1,x2,y2=map(int,input().split())
        source = point2D(x1,y1)
        source.id=0
        sink=point2D(x2,y2)
        sink.id=n+1
        checksource=self.checkinsidepolygon(source,totallist)
        checksink = self.checkinsidepolygon(sink,totallist)

        if checksource==True:
            print("The source point is inside the polygon obstacle")
            sys.exit(0)
        if checksink==True:
            print("The sink point is inside the polygon obstacle")
            sys.exit(0)
        Xcoordnew=list()
        Ycoordnew = list()
        Xcoordnew.append(x1)
        Xcoordnew.append(x2)
        Ycoordnew.append(y1)
        Ycoordnew.append(y2)
        plt.scatter(Xcoordnew,Ycoordnew,c='black')

        #work remaining is finding the source and the sink vertex
        self.findedges(totallist,sink)
        self.drawedges(source,sink,totallist)
        for i in range(len(self.edgelist)):
            edgelistx = list()
            edgelisty = list()
            edgelistx.append(self.edgelist[i].u.x)
            edgelistx.append(self.edgelist[i].v.x)
            edgelisty.append(self.edgelist[i].u.y)
            edgelisty.append(self.edgelist[i].v.y)
            plt.plot(edgelistx,edgelisty,c='black')
            print((self.edgelist[i].u.x,self.edgelist[i].u.y,self.edgelist[i].v.x,self.edgelist[i].v.y))
            #print((self.edgelist[i].u.id,self.edgelist[i].u.id,self.edgelist[i].v.id,self.edgelist[i].v.id))
        plt.show()

def main():
    print("Enter the number of shapes that you want to draw in boundary")
    number = int(input())
    finallist=list()
    totalnumberofpoint=0
    Convexshape = convexhull_jarvis()
    for j in range(number):
        print("Enter the number of points")
        n = int(input())
          #initializing the convex hull
        print("Start entering the coordinates of points in x and y fashion space separated")
        xcoord=list()
        ycoord=list()
        for i in range(n):
            x,y = map(int,input().split())
            xcoord.append(x)                    #storing x coordinates separately
            ycoord.append(y)
            #storing y coordinates separately
        Convexshape.addpoints(xcoord,ycoord,n,totalnumberofpoint)  #adding points to the hull to be created
        totalnumberofpoint += n
        anslist = Convexshape.makehull(n)       #making the actual hull
        finallist.append(anslist)
        Convexshape = convexhull_jarvis()

    Convexshape.printhull(finallist,totalnumberofpoint)          #printing the hull

if __name__=='__main__':
    main()
