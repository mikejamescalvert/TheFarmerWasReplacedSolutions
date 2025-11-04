import f1
f1.resetPosition()
x, y = get_pos_x(), get_pos_y()
companion_dict = {(x,y):get_entity_type()}

while True:
	for i in range(get_world_size()):
		for j in range(get_world_size()):

			f1.handleSpotHarvestingProcess()
			plant(f1.getEntityForSpot(i,j))

			move(East)
		move(North)