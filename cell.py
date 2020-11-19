OBSTACLE="O"
KID="K"
CRIB="C"
FULL_CRIB="F"
DIRT="D"
ROBOT="R"
ROBOT_HOLDING_KID="H"

class Cell:
    def __init__(self, items):
        self.items=items
        
    def __str__(self):
        s="|"
        for i in self.items:
            s+=i
        s+="_"*(3-len(self.items))
        return s+"|"
    
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
            
        