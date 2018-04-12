import math
import matplotlib.pyplot as plt
import sys
import heapq

class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.id=-1
        self.cost=99999999999999
        self.previous=-1
    def __lt__(self,other):
        return self.cost<other.cost

#listnode of the edge
class edgelistnode:
    def __init__(self,u,v):
        self.u = u
        self.v = v
        self.weight=0

class hashlist:
        def __init__(self):
            self.hl=[]
            self.hl.append(None)
        def add(self,p):
            self.hl.append(p)

class Solution:
    #p is the point (Class Point )
    def __init__(self):
        self.edgelist = list()
        self.checklist = list()

    #for finding the edge weight distance formula
    def distance(self,firstpoint,secondpoint):
        distance = math.sqrt((secondpoint.x-firstpoint.x)**2 +(secondpoint.y-firstpoint.y)**2)
        return distance

    def orientation(self,p,q,r):
        val=((q.y-p.y)*(r.x-q.x))-((q.x-p.x)*(r.y-q.y))
        #checking by the slopes for orientation
        if val==0:
            return 0                                                #coloiner points
        if val>0:
            return 1                                                 #clockwise points
        else:
            return 2                                                #counterclockwise points

    def MergeSort(self,points,low,high,comparsion_point):
        if low<high:
            mid=(low+high)//2
            self.MergeSort(points,low,mid,comparsion_point)         #sort the left part of the array according to the slope
            self.MergeSort(points,mid+1,high,comparsion_point)      #sort the right part of the array according to the slope
            self.Merge(points,low,mid,high,comparsion_point)        #finally merge two sorted parts of the array
        else:
            return

    def Merge(self,points,low,mid,high,comparsion_point):
        Left=points[low:mid+1]
        Right=points[mid+1:high+1]
        left=0
        right=0
        k=low
        while left<=mid-low and right<high-mid:
            div1=comparsion_point.x-Left[left].x                    #finding the first division factor
            div2=comparsion_point.x-Right[right].x                  #find the second division factor
            m1=0
            m2=0
            angle1=0
            angle2=0
            if div1!=0:
                m1=((comparsion_point.y-Left[left].y)/(comparsion_point.x-Left[left].x))
                angle1=math.atan(m1)
            else:
                angle1=(3.14159265359)/2
            if div2!=0:
                m2=((comparsion_point.y-Right[right].y)/(comparsion_point.x-Right[right].x))
                angle2=math.atan(m2)
            else:
                angle2=(3.14159265359)/2
            if angle1<0:
                angle1+=3.14159265359
            if angle2<0:
                angle2+=3.14159265359
            if angle1>angle2:
                points[k]=Left[left]
                left+=1
            else:
                points[k]=Right[right]
                right+=1
            k+=1
        while left<=(mid-low):
            points[k]=Left[left]
            k+=1
            left+=1
        while right<(high-mid):
            points[k]=Right[right]
            right+=1
            k+=1

    def swap(self,x,y):
        temp=x
        x=y
        y=temp

    def ConvexHull(self,points,n):
        global discardednodes
        #iam using duplicate list in case not to change points list

        duplicate=[]
        for i in range(n):
            duplicate.append(points[i])
        bottom_most_left_y=points[0].y               #finding the bottommost point
        min_point=0

        #finding the leftmost point

        for i in range(n):
            y=points[i].y
            if ((y<bottom_most_left_y) or (bottom_most_left_y==y and points[i].x<points[min_point].x)):
                bottom_most_left_y=points[i].y
                min_point=i

        #place the bottommost point at the first position in the list
        #self.swap(points[0],points[min_point])

        temp=points[0]
        points[0]=points[min_point]
        points[min_point]=temp

        #calling MergeSort function in the format of the function
        #MergeSort(array_to_be_sorted,starting_index,ending_index)

        comparsion_point=points[0]
        p0=points[0]
        points.remove(points[0])
        self.MergeSort(points,0,len(points)-1,comparsion_point)

        points=points[::-1]
        i=0
        while i<len(points)-1:
            m1=0
            m2=0
            div1=(comparsion_point.x-points[i].x)
            div2=(comparsion_point.x-points[i+1].x)
            if div1!=0 and div2!=0:
                m1=((comparsion_point.y-points[i].y)/(comparsion_point.x-points[i].x))
                m2=((comparsion_point.y-points[i+1].y)/(comparsion_point.x-points[i+1].x))
                if m1==m2:
                    x1_differ=comparsion_point.x-points[i].x
                    y1_differ=comparsion_point.y-points[i].y
                    x2_differ=comparsion_point.x-points[i+1].x
                    y2_differ=comparsion_point.y-points[i+1].y
                    distance_1=math.sqrt((x1_differ**2)+(y1_differ**2))
                    distance_2=math.sqrt((x2_differ**2)+(y2_differ**2))
                    if distance_1>distance_2:
                        points.pop(i+1)
                    else:
                        points.pop(i)
            i+=1
        dup=[]
        dup.append(p0)
        for i in range(len(points)):
            dup.append(points[i])
        stack=list()
        stack.append(dup[0])
        stack.append(dup[1])
        stack.append(dup[2])
        for i in range(3,len(dup)):
            while self.orientation(stack[-2],stack[-1],dup[i])!=2:
                stack.pop()
            stack.append(dup[i])
        lis=stack[::-1]
        return lis

    #Will do the documentation later after i finish all of these functions

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
                else:
                    otherfirst=totallist[i][j]
                    othersecond=totallist[i][0]

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
                    o1=self.orientation(firstpoint,secondpoint,otherfirst)
                    o2=self.orientation(firstpoint,secondpoint,othersecond)
                    o3=self.orientation(otherfirst,othersecond,firstpoint)
                    o4=self.orientation(otherfirst,othersecond,secondpoint)

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
                        if self.checklist[currentpolygonpoints[j].id][pointstocheck[k].id]==0:
                            self.checklist[currentpolygonpoints[j].id][pointstocheck[k].id]=1
                            self.checklist[pointstocheck[k].id][currentpolygonpoints[j].id]=1
                            tempnode = edgelistnode(currentpolygonpoints[j], pointstocheck[k])
                            tempnode.weight = self.distance(currentpolygonpoints[j], pointstocheck[k])
                            self.edgelist.append(tempnode)
                    else:
                        pass

    def dointersect(self,point1,point2,vertex,checkpoint):
        o1=self.orientation(point1,point2,vertex)
        o2=self.orientation(point1,point2,checkpoint)
        o3=self.orientation(vertex,checkpoint,point1)
        o4=self.orientation(vertex,checkpoint,point2)

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
            checkpoint=Point(sys.maxsize,vertex.y)
            count=0
            for j in range(len(totallist[i])):
                if j!=len(totallist[i])-1:
                    point1=totallist[i][j]
                    point2=totallist[i][j+1]
                else:
                    point1=totallist[i][j]
                    point2=totallist[i][0]
                if(self.dointersect(point1,point2,vertex,checkpoint)):
                    if self.orientation(point1,vertex,point2)==0:
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
                        if self.checklist[currentpolygonpoints[j].id][pointstocheck[k].id] == 0:
                            self.checklist[currentpolygonpoints[j].id][pointstocheck[k].id] = 1
                            self.checklist[pointstocheck[k].id][currentpolygonpoints[j].id] = 1
                            tempnode = edgelistnode(currentpolygonpoints[j], pointstocheck[k])
                            tempnode.weight = self.distance(currentpolygonpoints[j], pointstocheck[k])
                            self.edgelist.append(tempnode)
                    else:
                        pass

    def printhull(self, morethanonehullcreated,number,H):
        global discardednodes
        totallist = list()
        for i in range(len(morethanonehullcreated)):
            Xcoord = list()
            Ycoord = list()
            temp = list()
            print("The end point of the convex hull formed by",i+1,"Polygon are ")
            for j in range(len(morethanonehullcreated[i])):
                print("(", morethanonehullcreated[i][j].x, ",", morethanonehullcreated[i][j].y, ")")
                node = morethanonehullcreated[i][j]
                Xcoord.append(morethanonehullcreated[i][j].x)
                Ycoord.append(morethanonehullcreated[i][j].y)
                temp.append(node)
            Xcoord.append(Xcoord[0])
            Ycoord.append(Ycoord[0])
            totallist.append(temp)
            for j in range(len(temp)):
                if j != len(temp) - 1:
                    nodeforedgelist = edgelistnode(temp[j], temp[j + 1])
                    nodeforedgelist.weight = self.distance(temp[j], temp[j + 1])
                    self.checklist[temp[j].id][temp[j+1].id]=1
                    self.checklist[temp[j+1].id][temp[j].id] = 1
                else:
                    nodeforedgelist = edgelistnode(temp[j], temp[0])
                    nodeforedgelist.weight = self.distance(temp[j], temp[0])
                    self.checklist[temp[j].id][temp[0].id] = 1
                    self.checklist[temp[0].id][temp[j].id] = 1
                self.edgelist.append(nodeforedgelist)
            plt.fill(Xcoord, Ycoord,c='black')
            plt.scatter(Xcoord, Ycoord, c='magenta')


        print("Enter the source and the sink vertex and be carefull that the vertex should be outside the polygon (space separated 4 integers)")
        x1, y1, x2, y2 = map(float, input().split())
        source = Point(x1, y1)
        source.id=0
        H.hl[0]=source
        sink = Point(x2, y2)
        sink.id=number+1
        H.add(sink)
        checksource = self.checkinsidepolygon(source, totallist)
        checksink = self.checkinsidepolygon(sink, totallist)

        if x1==x2 and y1==y2:
            print("The coordinates of source and sink are same")
            sys.exit(0)
        if checksource == True:
            print("The source point is inside the polygon obstacle")
            sys.exit(0)
        if checksink == True:
            print("The sink point is inside the polygon obstacle")
            sys.exit(0)
        Xcoordnew = list()
        Ycoordnew = list()
        Xcoordnew.append(x1)
        Xcoordnew.append(x2)
        Ycoordnew.append(y1)
        Ycoordnew.append(y2)
        plt.scatter(Xcoordnew, Ycoordnew, c='red')
        self.findedges(totallist, sink)
        self.drawedges(source, sink, totallist)
        for i in range(len(self.edgelist)):
            edgelistx = list()
            edgelisty = list()
            edgelistx.append(self.edgelist[i].u.x)
            edgelistx.append(self.edgelist[i].v.x)
            edgelisty.append(self.edgelist[i].u.y)
            edgelisty.append(self.edgelist[i].v.y)
            plt.plot(edgelistx, edgelisty, c='grey')
        dest=self.dijsktra(number+2,H)
        route=[]
        route.append(H.hl[dest.id])
        while(dest.id!=0):
            dest=H.hl[dest.previous]
            route.append(H.hl[dest.id])
        shortestx = list()
        shortesty = list()
        for i in range(len(route)):
            shortestx.append(route[i].x)
            shortesty.append(route[i].y)
            print(route[i].x,route[i].y)
        plt.plot(shortestx,shortesty,c='cyan')
        plt.show()


    def dijsktra(self,totalnumberofpoints,H):
        adj_list=[0]*totalnumberofpoints                            #making adjacency list
        wt_list=[0]*totalnumberofpoints
        for i in range(totalnumberofpoints):
            adj_list[i]=[]
            wt_list[i]=[]
        for i in range(len(self.edgelist)):
            adj_list[self.edgelist[i].u.id].append(self.edgelist[i].v.id)
            wt_list[self.edgelist[i].u.id].append(self.edgelist[i].weight)
            adj_list[self.edgelist[i].v.id].append(self.edgelist[i].u.id)
            wt_list[self.edgelist[i].v.id].append(self.edgelist[i].weight)
        H.hl[0].cost=0                                        #source cost =0
        H.hl[0].previous=0
        graph_nodes=[0]*totalnumberofpoints
        for i in range(totalnumberofpoints):
            graph_nodes[i]=H.hl[i]
        heapq.heapify(graph_nodes)
        while len(graph_nodes)>0:
            sor=heapq.heappop(graph_nodes)
            if sor.id==totalnumberofpoints-1:
                break
            for v in range(len(adj_list[sor.id])):
                if H.hl[adj_list[sor.id][v]].cost > H.hl[sor.id].cost+wt_list[sor.id][v]:
                    H.hl[adj_list[sor.id][v]].cost=H.hl[sor.id].cost+wt_list[sor.id][v]
                    H.hl[adj_list[sor.id][v]].previous=sor.id
            heapq.heapify(graph_nodes)
        return sor

def main():
    H=hashlist()
    print("Enter the number of polygons")
    number = int(input())
    finallist = list()
    totalnumberofpoints=0
    s = Solution()
    for t in range(number):
        p=list()                                        #defining a empty list of points
        print("Give the no of points")
        n=int(input())
        print("Enter points")
        idofpoint=totalnumberofpoints+1
        discardednodes=list()
        for i in range(n):
            x,y=map(float,input().split(","))
            pointnode=Point(x,y)
            pointnode.id=idofpoint+i
            H.add(pointnode)
            discardednodes.append(pointnode)
            p.append(pointnode)
        temp = s.ConvexHull(p,n)
        discardedx = list()
        discardedy = list()
        for i in range(len(discardednodes)):
            discardedx.append(discardednodes[i].x)
            discardedy.append(discardednodes[i].y)
        discardedx.append(discardednodes[0].x)
        discardedy.append(discardednodes[0].y)
        plt.plot(discardedx, discardedy, c='yellow')
        totalnumberofpoints += n
        finallist.append(temp)
        s = Solution()
    s.checklist=[ [ 0 for i in range(totalnumberofpoints+2) ]for j in range(totalnumberofpoints+2)]
    s.printhull(finallist,totalnumberofpoints,H)

if __name__ == "__main__":
    main()