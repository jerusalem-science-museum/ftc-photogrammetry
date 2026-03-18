import os
import cv2
import pygame
from consts import *
from pictures_consts import face_pic, camera_size_on_screen, camera_pos, face_size

cap = None

def open_camera():
    global cap
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        return False
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, camera_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, camera_height)
    return True

def run_one_frame_to_video(window):
    global cap
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?)")
        return False
    frame = cv2.resize(frame, camera_size_on_screen)

    # Convert the frame from BGR to RGB - this is necessary for Pygame to display the frame correctly
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.transpose(frame)
    frame = cv2.flip(frame, flipCode=0)
    # Convert the frame to a Pygame surface
    pygame_frame = pygame.surfarray.make_surface(frame)
    
    # camera_size_on_screen = (640, 360)
    # add the png image of "face" on the camera frame in the center
    pygame_frame.blit(face_pic, ((camera_size_on_screen[0]-face_size[0])//2 ,(camera_size_on_screen[1]-face_size[1])//2))
    window.blit(pygame_frame, camera_pos)
    return True


def take_picture(image_folder, image_name, save_to_images_folder=False, timestamp=None):
    # take a picture and save it in the images folder
    global cap
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, camera_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, camera_height)
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?)")
        return False
    cv2.imwrite(os.path.join(image_folder, image_name), frame)
    if save_to_images_folder and timestamp is not None:
        if not os.path.exists(photogrammetry_local_images_path):
            os.makedirs(photogrammetry_local_images_path, exist_ok=True)
        # if not os.path.exists(photogrammetry_drive_images_path):
        #     os.makedirs(photogrammetry_drive_images_path, exist_ok=True)
        cv2.imwrite(os.path.join(photogrammetry_local_images_path, timestamp + image_format), frame)
        # cv2.imwrite(os.path.join(photogrammetry_drive_images_path, timestamp + image_format), frame)
    return True
