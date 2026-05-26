
photogrammetry_data_path = r'/mnt/shared_in/photogrammetry_data'
obj_path = r'output/texturedMesh.obj'  # DO NOT CHANGE
texture_path = r'output/texture_1001.png'  # DO NOT CHANGE

TIME_TO_WAIT_FOR_NEW_MODEL = 4  # seconds - the time to wait when a new model is detected in the photogrammetry_data_path (to allow the model to be fully written)
borders = [0,0]  # the precentage of screen (0.1 = 10%) from the sides (width and height axis) that will be used only for buttons (will not move the object)
# currently 0 because we allow the whole screen to be used for moving the object (no buttons)

time_to_idle = 10  # seconds - the time to wait before the model starts rotating automatically (when no user input is detected)
zpos = -2  # the distance of the object from the camera (must be negative to be in front of the camera)

model_number = 0
MAX_MODEL_NUMBER = 15
BACKGROUND_COLOR = (226/255, 233/255, 241/255, 1.0)  # the color of the background (kind of white) - must be a tuple of 4 values (r,g,b,a)