import time
import vedo
from vedo import *
import os
from consts import *


def get_last_obj(path):
    obj_file_path = os.path.join(max([os.path.join(path, d) for d in os.listdir(path)], key=os.path.getmtime), obj_path)
    texture_file_path = os.path.join(max([os.path.join(path, d) for d in os.listdir(path)], key=os.path.getmtime), texture_path)
    return obj_file_path, texture_file_path

def get_nth_obj_in_folder(folder_path, n):
    items = os.listdir(folder_path)
    if len(items) == 0 or n >= len(items):
        return None
    n += 1
    obj_file_path = os.path.join(folder_path, items[-n], obj_path)
    texture_file_path = os.path.join(folder_path, items[-n], texture_path)
    return obj_file_path, texture_file_path


def next(obj, ename):
    global model_number
    global plt
    model_number -= 1
    if model_number < 0:
        model_number = min(MAX_MODEL_NUMBER-1, len(os.listdir(photogrammetry_data_path)) - 1)
    plt.clear()
    obj_file_path, texture_file_path = get_nth_obj_in_folder(photogrammetry_data_path, model_number)
    if (not os.path.exists(obj_file_path)) or (not os.path.exists(texture_file_path)):
        model_number -= 1
        if model_number < 0:
            model_number = min(MAX_MODEL_NUMBER-1, len(os.listdir(photogrammetry_data_path)) - 1)
        obj_file_path, texture_file_path = get_nth_obj_in_folder(photogrammetry_data_path, model_number)
    mesh = Mesh(obj_file_path)
    mesh.texture(texture_file_path, scale=0.1)
    plt.add(mesh)
    plt.reset_camera()
    plt.reset_viewup()


def prev(obj, ename):
    global model_number
    global plt
    model_number += 1
    if model_number >= MAX_MODEL_NUMBER or model_number >= len(os.listdir(photogrammetry_data_path)):
        model_number = 0
    plt.clear()
    obj_file_path, texture_file_path = get_nth_obj_in_folder(photogrammetry_data_path, model_number)
    if (not os.path.exists(obj_file_path)) or (not os.path.exists(texture_file_path)):
        model_number += 1
        if model_number >= MAX_MODEL_NUMBER or model_number >= len(os.listdir(photogrammetry_data_path)):
            model_number = 0
        obj_file_path, texture_file_path = get_nth_obj_in_folder(photogrammetry_data_path, model_number)
    mesh = Mesh(obj_file_path)
    mesh.texture(texture_file_path, scale=0.1)
    plt.add(mesh)
    plt.reset_camera()
    plt.reset_viewup()


while (True):
    plt = Plotter(size="fullscreen")
    bu = plt.add_button(
        next,
        pos=(0.9, 0.15),  # x,y fraction from bottom left corner
        states=["-->", "error"],  # text for each state
        c=["w", "w"],  # font color for each state
        bc=["dg", "dv"],  # background color for each state
        font="courier",  # font type
        size=45,  # font size
        bold=True,  # bold font
        italic=False,  # non-italic font style
    )
    bu2 = plt.add_button(
        prev,
        pos=(0.8, 0.15),  # x,y fraction from bottom left corner
        states=["<--", "error"],  # text for each state
        c=["w", "w"],  # font color for each state
        bc=["dg", "dv"],  # background color for each state
        font="courier",  # font type
        size=45,  # font size
        bold=True,  # bold font
        italic=False,  # non-italic font style
    )
    model_number = 0
    try :    
        obj_file_path, texture_file_path = get_nth_obj_in_folder(photogrammetry_data_path, model_number)
        mesh = Mesh(obj_file_path)
        mesh.texture(texture_file_path, scale=0.1)
        plt.show(mesh, __doc__,size="fullscreen").close()
    except:
        pass