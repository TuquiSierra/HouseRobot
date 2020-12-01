import random
import utils
from cell import *

class Environment:
    def __init__(self,m, n, kids, obstacles_percentage, dirt_percentage, dirt_prob=0.6, move_kid_prob=0.5):
        self.kids=kids
        self.initial_kids=kids
        self.move_kid_prob=move_kid_prob
        self.dirt_prob=dirt_prob
        self.obstacles=obstacles_percentage*n*m//100
        self.dirt=dirt_percentage*(n*m-self.obstacles-2*self.initial_kids)//100
        if 2*self.kids+self.obstacles+self.dirt+1>=m*n:
            raise Exception("INVALID ENVIRONMENT SPECIFICATIONS")
        self.environment=[]
        for _ in range(m):
            cols=[]
            for _ in range(n):
                cols.append(Cell([]))
            self.environment.append(cols)
        self.__crib_collocation__() 
        self.__item_collocation__(self.obstacles,OBSTACLE)
        self.__item_collocation__(self.dirt, DIRT)
        self.__item_collocation__(self.kids,KID) 
        self.__robot_collocation__()

    def __str__(self):
        board_string=""
        for i in range(len(self.environment)):
            for j in range(len(self.environment[0])):
                board_string+=str(self.environment[i][j])
            board_string+="\n"
        return board_string

    def is_chaos(self):
        return (self.dirt*100)/((len(self.environment)*len(self.environment[0])-2*self.initial_kids-self.obstacles))>=60
    
    def is_neat(self):
        return self.dirt==0 and self.kids==0
    
    def inside(self, x, y):
        return x>=0 and y>=0 and x<len(self.environment) and y <len(self.environment[0])

    def __robot_collocation__(self):
        while True:
            x=random.randint(0, len(self.environment)-1)
            y=random.randint(0, len(self.environment[0])-1)
            if not len(self.environment[x][y].items):
                self.environment[x][y].items.append(ROBOT)
                self.robot_position=(x, y)
                self.robot_prev=(x, y)
                break

    def __item_collocation__(self, elem_count, item):
        count=elem_count
        while count>0:
            x=random.randint(0, len(self.environment)-1)
            y=random.randint(0, len(self.environment[0])-1)
            if not len(self.environment[x][y].items):
                self.environment[x][y].items.append(item)
                count-=1
                
    def __crib_collocation__(self):
        count=self.kids
        origin_x=random.randint(0, len(self.environment)-1)
        origin_y=random.randint(0, len(self.environment[0])-1)
        queue=[(origin_x, origin_y)]
        marked=[[False]*len(self.environment[0]) for _ in range(len(self.environment))]
        while count>0:
            x, y=queue[0]
            queue=queue[1:]
            marked[x][y]=True
            self.environment[x][y]=Cell([CRIB])
            count-=1
            for neighbor in utils.NEIGHBORHOOD[:4]:
                new_x=x+neighbor[0]
                new_y=y+neighbor[1]
                if self.inside(new_x, new_y) and not marked[new_x][new_y]:
                    queue.append((new_x, new_y))
            
                    
                    
    def variate(self):
        kid_dirt=[[False for i in range(len(self.environment[0]))] for i in range(len(self.environment))]
        for i,row in enumerate(self.environment):
            for j,item in enumerate(row):
                if KID in item.items:
                    rnd=random.random()
                    if rnd<self.move_kid_prob:
                        self.__move_kid__(i, j, kid_dirt)
                    
        
                                          
    def __move_kid__(self, i, j, kid_dirt):
        rnd=random.randint(0,7)
        new_i=i+utils.NEIGHBORHOOD[rnd][0]
        new_j=j+utils.NEIGHBORHOOD[rnd][1]
        if self.inside(new_i, new_j):
            if self.environment[new_i][new_j].is_obstacle():
                if self.__move_obstacle__(new_i, new_j, rnd):
                    self.environment[new_i][new_j].items=[KID]
                    self.environment[i][j].items.remove(KID)
                    self.__put_dirt__(i,j, kid_dirt)
            if self.environment[new_i][new_j].is_empty():
                self.environment[new_i][new_j].items=[KID]
                self.environment[i][j].items.remove(KID)
                self.__put_dirt__(i,j, kid_dirt)
            
    def __move_obstacle__(self, i, j, direction):
        new_i=i+utils.NEIGHBORHOOD[direction][0]
        new_j=j+utils.NEIGHBORHOOD[direction][1]
        if not self.inside(new_i, new_j):
            return False
        if self.environment[new_i][new_j].is_empty():
            self.environment[new_i][new_j].items=[OBSTACLE]
            return True
        if self.environment[new_i][new_j].is_obstacle():
            return self.__move_obstacle__(new_i, new_j, direction)
        return False
        
    def __put_dirt__(self, i, j, kid_dirt):
        kd=0
        for neighbor in utils.NEIGHBORHOOD:
            new_i=i+neighbor[0]
            new_j=j+neighbor[1]
            if self.inside(new_i, new_j) and kid_dirt[new_i][new_j]:
                kd+=1
        for neighbor in utils.NEIGHBORHOOD:
            new_i=i+neighbor[0]
            new_j=j+neighbor[1]
            if not self.inside(new_i, new_j) or self.environment[new_i][new_j].is_any():
                continue
            count=0
            if kd==0:
                count=1
            elif kd==1:
                count=2
            else:
                count=6-kd          
            while count>0:
                rnd=random.random()
                if rnd<self.dirt_prob:
                    self.environment[new_i][new_j].items=[DIRT]
                    self.dirt+=1
                    count-=1
                    kid_dirt[new_i][new_j]=True
                    break
            
    def is_robot(self, x, y):
        return self.environment[x][y].is_robot()
    
    def is_kid(self, x, y):
        return self.environment[x][y].is_kid()
    
    def is_dirty(self, x, y):
        return self.environment[x][y].is_dirty()
    
    def is_robot_holding_kid(self, x, y):
        return self.environment[x][y].is_robot_holding_kid()
    
    def is_stepable(self, x, y):
        return self.inside(x, y) and self.environment[x][y].is_stepable()
    
    def is_crib(self, x, y):
        return self.environment[x][y].is_crib()
                
            
                
            

                    
                    