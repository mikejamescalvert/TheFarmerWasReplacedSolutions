def resetPosition():
	while (get_pos_x() > 0):
		move(West)
	
	while (get_pos_y() > 0):
		move(South)

def moveToPosition(x,y):
	while (get_pos_x() != x):
		if (get_pos_x() > x):
			move(West)
		else:
			move(East)
			
	while (get_pos_y() != y):
		if (get_pos_y() > y):
			move(South)
		else:
			move(North)
			
def moveToRandomPosition():
	x = random() * get_world_size() // 1
	y = random() * get_world_size() // 1

	moveToPosition(x,y)
	
def findGoodCompanion():
	companion = get_companion()
	if companion != None:
		plant_type, (x, y) = companion

def plantCompanionAndReturn():
	currentX = get_pos_x()
	currentY = get_pos_y()
	
	companion = get_companion()
	if companion != None:
		plant_type, (x, y) = companion
		moveToPosition(x,y)
		
		print("Companion:", plant_type, "at", x, ",", y)
		
		handleSpotHarvestingProcess()
						
		plant(plant_type)
		
		moveToPosition(currentX,currentY)

def handleSpotHarvestingProcess():
	if (get_water() < 0.10):
		use_item(Items.Water)

	if (get_ground_type() != Grounds.Soil):
		till()
	if can_harvest():
		harvest()

def getEntityForSpot(x, y):
	
	
	
	if (x>0) and (x % 4) == 0:
		return Entities.Sunflower
	if (x>0) and ((x % 5) == 0 or x == 1) :
		return Entities.Pumpkin
	if (x>0) and (x % 3) == 0:
		return Entities.Tree
	if (x>0) and (x % 2) == 0:
		return Entities.Carrot
	else:
		return Entities.Grass