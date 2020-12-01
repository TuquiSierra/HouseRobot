OBSTACLE="🔴"
KID="🔵"
CRIB="🔷"
FULL_CRIB="🚼"
DIRT="❌"
ROBOT="🤖"
ROBOT_HOLDING_KID="🚸"

class Cell:
    def __init__(self, items):
        self.items=items
        
    def __str__(self):
        s=""
        if not len(self.items):
            s+="🔲"
        else:
            c=""
            for i in self.items:
                c=i
            s=c
        return s
    
    def is_robot(self):
        return ROBOT in self.items
    
    def is_kid(self):
        return KID in self.items
    
    def is_robot_holding_kid(self):
        return ROBOT_HOLDING_KID in self.items
    
    def is_crib(self):
        return CRIB in self.items
    
    def is_dirty(self):
        return DIRT in self.items
    
    def is_stepable(self):
        return not FULL_CRIB in self.items and not OBSTACLE in self.items
    
    def is_obstacle(self):
        return OBSTACLE in self.items
    
    def is_empty(self):
        return not len(self.items)
    
    def is_any(self):
        if len(self.items):
            return True
        return False
            
        