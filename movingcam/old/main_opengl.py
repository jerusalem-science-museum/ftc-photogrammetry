import pygame
import datetime as dt
import time
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
from pygame.constants import *
from objloader import *
from consts import *


def init_model(obj_file):
    global viewport, output_directory, rx, ry, rz, zpos, obj, state
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(226/255,233/255,241/255,1.0)
    glLoadIdentity()

    center_object(obj_file)
    obj = OBJ(obj_file, swapyz=True)
    obj.generate()
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
    obj.render()

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
    # obj.render()

def render_model():
    global rx, ry, rz, obj, zpos
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(226/255,233/255,241/255,1.0)
    glLoadIdentity()
    glTranslate(0,0,zpos)
    glRotatef(ry, 0.0, 1.0, 0.0)
    glRotatef(rx, 1.0, 0.0, 0.0)
    glRotatef(rz, 0.0, 0.0, 1.0)
    obj.render()

def end_model_view():
    global screen
    # pygame.display.quit()
    # pygame.display.init()
    print("end_model_view called - doing nothing")

def get_nth_obj_in_folder(folder_path, n):
    items = os.listdir(folder_path)
    if len(items) == 0 or n >= len(items):
        return None
    n += 1
    obj_file_path = os.path.join(folder_path, items[-n], obj_path)
    texture_file_path = os.path.join(folder_path, items[-n], texture_path)
    return obj_file_path, texture_file_path


pygame.init()
screen_info = pygame.display.Info()
viewport = (screen_info.current_w,screen_info.current_h)
width = screen_info.current_w
height = screen_info.current_h

screen = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF | pygame.FULLSCREEN)
gluPerspective(70.0, width/float(height), 1, 100.0)
glMatrixMode(GL_PROJECTION)
glEnable(GL_DEPTH_TEST)
glMatrixMode(GL_MODELVIEW)
glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
glEnable(GL_LIGHT0)
glEnable(GL_LIGHTING)
glEnable(GL_COLOR_MATERIAL)
glEnable(GL_DEPTH_TEST)
glShadeModel(GL_SMOOTH)
glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
glClearColor(226/255,233/255,241/255,1.0)

glViewport(0, 0, width, height)
glLoadIdentity()
glOrtho(0, width, height, 0, -1, 1)
glLoadIdentity()

clock = pygame.time.Clock()
rx, ry, rz = (-90,180,0)
zpos = -4
obj = None

last_touch = time.time()
time_to_idle = 10
idle = False

files_in_data_folder = os.listdir(photogrammetry_data_path)

obj_file_path, texture_file_path = get_nth_obj_in_folder(photogrammetry_data_path, model_number)
print(f"model path: {obj_file_path}")
print(f"texture path: {texture_file_path}")
init_model(obj_file_path)
pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            break

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
                break

            if event.key == K_r:
                model_number += 1
                if model_number >= MAX_MODEL_NUMBER or model_number >= len(os.listdir(photogrammetry_data_path)):
                    model_number = 0
                obj_file_path, texture_file_path = get_nth_obj_in_folder(photogrammetry_data_path, model_number)
                # print(f"model path: {obj_file_path}")
                init_model(obj_file_path)

            if event.key == K_l:
                model_number -= 1
                if model_number < 0:
                    model_number = min(MAX_MODEL_NUMBER-1, len(os.listdir(photogrammetry_data_path)) - 1)
                obj_file_path, texture_file_path = get_nth_obj_in_folder(photogrammetry_data_path, model_number)
                # print(f"model path: {obj_file_path}")
                init_model(obj_file_path)      

        elif event.type == MOUSEBUTTONDOWN:  # if mouse is CLICKED and dragged then rotate the model accordingly
            last_touch = time.time()
            idle = False
            if event.button == 4:
                # zpos = max(zpos - 1, -30)
                pass
            elif event.button == 5:
                # zpos = min(zpos + 1, -1)
                pass
            elif event.button == 1:
                # x, y = event.pos
                # rx += (y - ry)
                # ry += (x - rx)
                pass

        elif event.type == MOUSEMOTION:
            last_touch = time.time()
            idle = False
            if event.buttons[0]:
                x, y = event.rel
                if borders[0] * width < event.pos[0] < (1 - borders[0]) * width and borders[1] * height < event.pos[1] < (1 - borders[1]) * height: 
                    rx -= y * 0.3
                    ry += x * 0.3
                    
        elif event.type == MOUSEWHEEL:
            # zpos += event.y
            pass

    if files_in_data_folder != os.listdir(photogrammetry_data_path):
        files_in_data_folder = os.listdir(photogrammetry_data_path)
        model_number = 0
        time.sleep(2)
        obj_file_path, texture_file_path = get_nth_obj_in_folder(photogrammetry_data_path, model_number)
        init_model(obj_file_path)
    
    if time.time() - last_touch > time_to_idle:
        idle = True
    if idle:
        rotate_model()
        rx = -90
    
    render_model()
    pygame.display.flip()
    clock.tick(30)


