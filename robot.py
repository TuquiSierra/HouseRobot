import utils
import cell
         
def decide_with_dirt_priority(env, x, y, new_x, new_y, steps):
        if env.is_dirty(new_x, new_y):
            move(env.environment[x][y],env.environment[new_x][new_y])
            env.robot_position=(new_x, new_y)
            if env.is_robot_holding_kid(new_x, new_y) and steps==0:
                action(env, 1)
            return True
        
        if env.is_crib(new_x, new_y) and env.is_robot_holding_kid(x, y):
            leaveKid(env.environment[x][y],env.environment[new_x][new_y])
            env.kids-=1
            env.robot_position=(new_x, new_y)
            return True
            
        if env.is_kid(new_x, new_y) and env.is_robot(x, y):
            takeKid(env.environment[x][y], env.environment[new_x][new_y])
            env.robot_position=(new_x, new_y)
            return True
        
        return False
    
def decide_with_kid_priority(env, x, y, new_x, new_y, steps):
        if env.is_crib(new_x, new_y) and env.is_robot_holding_kid(x, y):
            leaveKid(env.environment[x][y],env.environment[new_x][new_y])
            env.kids-=1
            env.robot_position=(new_x, new_y)
            return True
            
        if env.is_kid(new_x, new_y) and env.is_robot(x, y):
            takeKid(env.environment[x][y], env.environment[new_x][new_y])
            env.robot_position=(new_x, new_y)
            return True
        
        if env.is_dirty(new_x, new_y):
            move(env.environment[x][y],env.environment[new_x][new_y])
            env.robot_position=(new_x, new_y)
            if env.is_robot_holding_kid(new_x, new_y) and steps==0:
                action(env, 1)
            return True
        
        return False
    
def decide_with_no_priority(env, x, y, new_x, new_y, steps):
    if env.is_crib(new_x, new_y) and env.is_robot_holding_kid(x, y):
        leaveKid(env.environment[x][y],env.environment[new_x][new_y])
        env.kids-=1
        env.robot_position=(new_x, new_y)
        
    elif env.is_kid(new_x, new_y) and env.is_robot(x, y):
        takeKid(env.environment[x][y], env.environment[new_x][new_y])
        env.robot_position=(new_x, new_y)
    
    else:
        move(env.environment[x][y],env.environment[new_x][new_y])
        env.robot_position=(new_x, new_y)
        if env.is_robot_holding_kid(new_x, new_y) and steps==0:
            action(env, 1)
        
    return True
    
    
            
def move(cell_one, cell_two):
    if cell_one.is_robot_holding_kid():
        cell_one.items.remove(cell.ROBOT_HOLDING_KID)
        cell_two.items.append(cell.ROBOT_HOLDING_KID)
    else:
        cell_one.items.remove(cell.ROBOT)
        cell_two.items.append(cell.ROBOT)
        
def leaveKid(old_cell, crib):
    old_cell.items.remove(cell.ROBOT_HOLDING_KID)
    crib.items=[cell.FULL_CRIB, cell.ROBOT]
    
def takeKid(old_cell, kid_cell):
    old_cell.items.remove(cell.ROBOT)
    kid_cell.items.append(cell.ROBOT_HOLDING_KID)
    kid_cell.items.remove(cell.KID)
    
def clean(dirty_cell):
    dirty_cell.items.remove(cell.DIRT)
    
def decide_with_best_priority(env, x, y, new_x, new_y, steps):
    if env.kids>env.dirt:
        return decide_with_kid_priority(env, x, y, new_x, new_y, steps)
    else:
        return decide_with_dirt_priority(env, x, y, new_x, new_y, steps)    

def action(env, steps=0, decide=decide_with_kid_priority):
    x, y=env.robot_position
    environment=env.environment
    if env.is_dirty(x, y):
        clean(environment[x][y])
        env.dirt-=1
        return x, y      
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
            if not env.is_stepable(new_x, new_y):
                continue
            move(environment[x][y],environment[new_x][new_y])
            env.robot_position=(new_x, new_y)
            if env.is_robot_holding_kid(new_x, new_y) and steps==0:
                action(env, 1)
            break
        
        
    
    
    