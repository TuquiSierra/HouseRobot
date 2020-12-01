import cell

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