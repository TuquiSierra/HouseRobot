import utils
import cell
from actions import *

def decide_with_dirt_priority(env, x, y, new_x, new_y, steps):
        if env.is_dirty(new_x, new_y):
            move(env.environment[x][y],env.environment[new_x][new_y])
            env.robot_position=(new_x, new_y)
            env.robot_prev=(x, y)
            return True
        
        if env.is_crib(new_x, new_y) and env.is_robot_holding_kid(x, y):
            leaveKid(env.environment[x][y],env.environment[new_x][new_y])
            env.kids-=1
            env.robot_position=(new_x, new_y)
            env.robot_prev=(x, y)
            return True
            
        if env.is_kid(new_x, new_y) and env.is_robot(x, y):
            takeKid(env.environment[x][y], env.environment[new_x][new_y])
            env.robot_position=(new_x, new_y)
            env.robot_prev=(x, y)
            return True
        
        return False
    
def decide_with_kid_priority(env, x, y, new_x, new_y, steps):
        if env.is_kid(new_x, new_y) and env.is_robot(x, y):
            takeKid(env.environment[x][y], env.environment[new_x][new_y])
            env.robot_position=(new_x, new_y)
            env.robot_prev=(x, y)
            return True
        
        if env.is_dirty(new_x, new_y):
            move(env.environment[x][y],env.environment[new_x][new_y])
            env.robot_position=(new_x, new_y)
            env.robot_prev=(x, y)
            return True
        
        if env.is_crib(new_x, new_y) and env.is_robot_holding_kid(x, y):
            leaveKid(env.environment[x][y],env.environment[new_x][new_y])
            env.kids-=1
            env.robot_position=(new_x, new_y)
            env.robot_prev=(x, y)
            return True  
        return False
    
    
def decide_with_best_priority(env, x, y, new_x, new_y, steps):
    if env.kids>env.dirt:
        return decide_with_kid_priority(env, x, y, new_x, new_y, steps)
    else:
        return decide_with_dirt_priority(env, x, y, new_x, new_y, steps)    

def action(env, steps=0, _decide="best"):
    if _decide=="kid":
        decide=decide_with_kid_priority
    elif _decide=="dirt":
        decide=decide_with_dirt_priority
    else:
        decide=decide_with_best_priority
    x, y=env.robot_position
    environment=env.environment
    if env.is_dirty(x, y):
        clean(environment[x][y])
        env.dirt-=1     
    for neighbor in utils.NEIGHBORHOOD:
        new_x=x+neighbor[0]
        new_y=y+neighbor[1]
        
        if not env.is_stepable(new_x, new_y):
            continue
        
        if decide(env,x, y, new_x, new_y, steps):
            break
    else:
        for neighbor in utils.NEIGHBORHOOD:
            new_x=x+neighbor[0]
            new_y=y+neighbor[1]
            if not env.is_stepable(new_x, new_y) or (env.robot_prev==(new_x, new_y) and steps==1):
                continue
            move(environment[x][y],environment[new_x][new_y])
            env.robot_position=(new_x, new_y)
            env.robot_prev=(x, y)
            if env.is_robot_holding_kid(new_x, new_y) and steps==0:
                action(env, 1)
            break
        
        
    
    
    