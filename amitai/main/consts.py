from enum import Enum
import pygame

photogrammetry_local_data_path = r'/home/mada/photogrammetry_data'
photogrammetry_local_images_path = r'/home/mada/photogrammetry_images'
photogrammetry_drive_data_path = r'/home/mada/photogrammetry_shared_folder/photogrammetry_data'  # NOT WORKING YET
photogrammetry_drive_images_path = r'/home/mada/photogrammetry_shared_folder/photogrammetry_images'  # NOT WORKING YET
meshroom_batch_path = r'/home/mada/Meshroom-2023.3.0/meshroom_batch'
config_file = r"/home/mada/Photogrammetry/main/settings_override"

images_folder_name = "images"
output_folder_name = "output"
cache_folder_name = "cache"
image_format = ".png"
texture_name = "texture_1001.png"
obj_file_name = "texturedMesh.obj"
log_file_name = "log.txt"
# ignore_items = set('cache','0.png','1.png','2.png','3.png','4.png','5.png','7.png','8.png','9.png', '10.png', '11.png')

class State(Enum):
    INSTRUCTIONS = 0
    TAKING_PICTURES = 1
    PROCESSING = 2
    MODEL_VIEW = 3
    ERROR = 4
    CAMERA_ERROR = 5

START_KEY = pygame.K_0
END_KEY = pygame.K_1
MIDDLE_KEY = pygame.K_CAPSLOCK

ERROR_SHOW_TIME = 8
MODEL_VIEW_TIME = 15
PROCESSING_TIMEOUT = 120

pygame.init()
screen_info = pygame.display.Info()
viewport = (screen_info.current_w,screen_info.current_h)

camera_width, camera_height = 1280, 720
camera_size_on_screen = (800, 450)
camera_pos = (150, (viewport[1]-camera_size_on_screen[1])//2)
face_size = (350,350)
