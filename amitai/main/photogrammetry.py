import pygame
import datetime as dt
import time
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
from pygame.constants import *
import shutil
import logging

from consts import *
from pictures_consts import *
from run_camera import *
from run_meshroom import *
from objloader import *

def init_model(obj_file):
    global screen, viewport, output_directory, rx, ry, rz, zpos, obj, state
    # pygame.display.quit()
    # pygame.display.init()
    # pygame.display.set_caption("Photogrammetry")
    # screen = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF | pygame.FULLSCREEN)
    pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF | pygame.FULLSCREEN)
    glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    center_object(obj_file)
    print("centerd object")
    try:
        obj = OBJ(obj_file, swapyz=True)
        obj.generate()
    except:
        print("ERROR LOADING OBJ FILE")
        state = State.ERROR
        return
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    width, height = viewport
    gluPerspective(70.0, width/float(height), 1, 100.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)
    glTranslate(0,0,zpos)
    glRotatef(ry, 0.0, 1.0, 0.0)
    glRotatef(rx, 1.0, 0.0, 0.0)
    glRotatef(rz, 0.0, 0.0, 1.0)

def rotate_model():
    global rx, ry, rz, obj, zpos
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(226/255,233/255,241/255,1.0)
    glLoadIdentity()
    ry += 1
    glTranslate(0,0,zpos)
    glRotatef(ry, 0.0, 1.0, 0.0)
    glRotatef(rx, 1.0, 0.0, 0.0)
    glRotatef(rz, 0.0, 0.0, 1.0)
    obj.render()

def end_model_view():
    global screen
    # pygame.display.quit()
    # pygame.display.init()
    pygame.display.set_mode((0,0), pygame.FULLSCREEN)

def display_timer(time, max_time):
    global font, screen, viewport
    timer_str = f"00:{(max_time-time):02d}"
    text_size = font.size(timer_str)
    text_x = (viewport[0] - text_size[0]) // 2
    text_y = viewport[1] // 4
    text = font.render(timer_str, True, (0, 0, 0))
    screen.blit(text, (text_x, text_y))


def copy_model_to_oneDrive(session_path, drive_path):
    # ignore cache and images folders
    try:
        shutil.copytree(session_path, drive_path, ignore=shutil.ignore_patterns('cache','images'))
    except:
        print("ERROR COPYING TO ONE DRIVE")
        logging.critical('ERROR WHILE COPYING TO ONE DRIVE')

def init_log(log_file_path):
    logging.basicConfig(filename=log_file_path, filemode='a', format='%(asctime)s ; %(message)s', level=logging.INFO)
    logging.info('session started')

pygame.display.set_caption("Photogrammetry")
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
font = pygame.font.Font(None, 100)
# pygame.mouse.set_visible(False)

clock = pygame.time.Clock()
state = State.INSTRUCTIONS
session_name = "none" # default value, will be changed later
timeString = "none"
input_directory = "none"
output_directory = "none"
cache_directory = "none"
image_number = 0
rx, ry, rz = (-90,45,0)
zpos = -2
obj = None
error_stopwatch = None
model_stopwatch = None
processing_stopwatch = None
timer = None
timers = [50,20]  # fake times to be displayed in timer for processing model state
max_timer_index = 0
last_timer = 0

ret = open_camera()
if not ret:
    state = State.CAMERA_ERROR
    screen.blit(camera_error_pic, (0, 0))
    pygame.display.flip()

while True: 
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    if state == State.CAMERA_ERROR:
        screen.blit(camera_error_pic, (0, 0))
        pygame.display.flip()
        continue

    if state == State.ERROR:
        if error_stopwatch is None:
            error_stopwatch = time.time()
            screen.blit(error_pic, (0, 0))
            pygame.display.flip()
        elif time.time() - error_stopwatch > ERROR_SHOW_TIME:
            logging.info('ending session from error - returning to instructions...')
            state = State.INSTRUCTIONS
            screen.blit(instructions_pic, (0, 0))
            error_stopwatch = None
            pygame.display.flip()

    if state == State.INSTRUCTIONS:
        screen.blit(instructions_pic, (0, 0))
        ret = run_one_frame_to_video(screen)
        if not ret:
            state = State.CAMERA_ERROR
            break
        pygame.display.flip()
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == START_KEY:
                state = State.TAKING_PICTURES
                screen.blit(taking_pictures_pic, (0, 0))
                pygame.display.flip()
                timeString = dt.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                session_name = os.path.join(photogrammetry_local_data_path, timeString)
                input_directory = os.path.join(session_name, images_folder_name)
                output_directory = os.path.join(session_name, output_folder_name)
                cache_directory = os.path.join(session_name, cache_folder_name)
                os.makedirs(input_directory)
                os.makedirs(output_directory)
                os.makedirs(cache_directory)
                init_log(os.path.join(session_name, log_file_name))
                image_number = 0
                logging.info('taking pictures...')

    
    if state == State.TAKING_PICTURES:
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == MIDDLE_KEY:
                print("taking picture " + str(image_number))
                if image_number != 6:
                    ret = take_picture(input_directory, str(image_number) + image_format)
                else:
                    ret = take_picture(input_directory, str(image_number) + image_format, save_to_images_folder=True, timestamp=timeString)
                if not ret:
                    print("ERROR TAKING PICTURE " + str(image_number))
                    logging.critical('ERROR TAKING PICTURE ' + str(image_number))
                    state = State.CAMERA_ERROR
                    break
                image_number += 1
            if event.type == pygame.KEYDOWN and event.key == END_KEY:
                logging.info('pictures taken successfully')
                state = State.PROCESSING
                logging.info('processing...')

    if state == State.PROCESSING:
        if processing_stopwatch is None:
            processing_stopwatch = time.time()
            last_timer = processing_stopwatch
            screen.blit(processing_pic0, (0, 0))
            timer = 0
            max_timer_index = 0
            display_timer(timer, timers[max_timer_index])
            pygame.display.flip()
            # input_directory = "C:/Users/mada/Documents/photogrammetry/photogrammetry_data/2024-01-04-11-56-57-3854/images"  # for testing
            ret = run_meshroom(input_directory, output_directory, cache_directory)
            if not ret:
                logging.critical('ERROR WHILE STARTING MESHROOM PROCESS')
                state = State.ERROR
                error_stopwatch = None
        if is_meshroom_done() and not is_meshroom_success():
            logging.error('meshroom failed')
            state = State.ERROR
            error_stopwatch = None
            processing_stopwatch = None
        elif is_meshroom_done() and is_meshroom_success():
            logging.info('meshroom done successfully in ; ' + "{:.1f}".format(time.time() - processing_stopwatch) + ' ; seconds')
            state = State.MODEL_VIEW
            model_stopwatch = None
            processing_stopwatch = None
            logging.info('copying object files to one drive...')
            # copy_model_to_oneDrive(session_name, os.path.join(photogrammetry_drive_data_path, timeString))
            logging.info('showing model on screen')
        elif time.time() - processing_stopwatch > PROCESSING_TIMEOUT: # if got to here then meshroom is still running
            logging.error('meshroom exceeded timeout - killing process')
            state = State.ERROR
            error_stopwatch = None
            processing_stopwatch = None
            terminate_meshroom()
        else:
            screen.blit(processing_pics[(int(time.time() - processing_stopwatch)) % len(processing_pics)], (0, 0))
            timer = (int(time.time() - last_timer))
            if timer > timers[max_timer_index] - 5:
                max_timer_index += 1
                timer = 0
                last_timer = time.time()
                if max_timer_index >= len(timers):
                    max_timer_index = len(timers) - 1
            display_timer(timer, timers[max_timer_index])
            pygame.display.flip()
                
    if state == State.MODEL_VIEW:
        if model_stopwatch is None:
            model_stopwatch = time.time()
            # screen.blit(model_view_pic, (0, 0))
            init_model(os.path.join(output_directory, obj_file_name))
        elif time.time() - model_stopwatch > MODEL_VIEW_TIME:
            model_stopwatch = None
            end_model_view()
            state = State.INSTRUCTIONS
            screen.blit(instructions_pic, (0, 0))
            logging.info('ending session - returning to instructions...')
        else:
            # show the model and rotate it one degree
            rotate_model()
        clock.tick(30)
        pygame.display.flip()
