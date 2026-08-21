import time
from dataclasses import dataclass
from typing import Optional, Tuple

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.constants import *

from consts import (
    BACKGROUND_COLOR,
    MAX_MODEL_NUMBER,
    TIME_TO_WAIT_FOR_NEW_MODEL,
    borders,
    model_number,
    obj_path,
    photogrammetry_data_path,
    texture_path,
    time_to_idle,
    zpos,
)
from model_gallery import ModelGallery


@dataclass
class ViewerState:
    viewport: Tuple[int, int]
    screen: object
    clock: pygame.time.Clock
    gallery: ModelGallery
    model_number: int = model_number
    current_model: object = None
    current_model_name: Optional[str] = None
    rx: float = -90
    ry: float = 180
    rz: float = 0
    last_touch: float = 0
    running: bool = True


def create_viewer_state():
    pygame.init()
    screen_info = pygame.display.Info()
    return ViewerState(
        viewport=(screen_info.current_w, screen_info.current_h),
        screen=None,
        clock=pygame.time.Clock(),
        gallery=ModelGallery(
            photogrammetry_data_path,
            obj_path,
            texture_path,
            MAX_MODEL_NUMBER,
        ),
        last_touch=time.time(),
    )


def show_error_screen(state):
    state.screen = pygame.display.set_mode(state.viewport, pygame.FULLSCREEN)
    font = pygame.font.Font(None, 36)
    text = (
        f'Cant find any 3D models in the given folder: "{photogrammetry_data_path}" '
        "please check the data folder and try again! Press ESC to exit window"
    )
    text_surface = font.render(text, True, (0, 0, 0))
    state.screen.fill((255, 255, 255))
    state.screen.blit(text_surface, (0, 0))
    pygame.display.flip()


def should_exit(event):
    return event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE)


def open_model_screen(state):
    width, height = state.viewport
    state.screen = pygame.display.set_mode(
        state.viewport,
        OPENGL | DOUBLEBUF | pygame.FULLSCREEN,
    )

    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(70.0, width / float(height), 1, 100.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glClearColor(*BACKGROUND_COLOR)


def load_current_model(state):
    state.model_number = state.gallery.clamp_index(state.model_number)
    model_files = state.gallery.get_files(state.model_number)
    if model_files is None:
        state.current_model = None
        state.current_model_name = None
        return

    if model_files.name != state.current_model_name:
        print(f"model path: {model_files.obj_file}")
        print(f"texture path: {model_files.texture_file}")

    state.current_model = state.gallery.get_loaded_model(state.model_number)
    state.current_model_name = model_files.name
    render_model(state)
    pygame.display.flip()


def handle_events(state):
    width, height = state.viewport

    for event in pygame.event.get():
        if should_exit(event):
            state.running = False
            return

        if event.type == KEYDOWN:
            if event.key == K_r:
                move_to_next_model(state)
            if event.key == K_l:
                move_to_previous_model(state)

        elif event.type == MOUSEBUTTONDOWN:
            mark_user_activity(state)

        elif event.type == MOUSEMOTION:
            mark_user_activity(state)
            if event.buttons[0] and is_inside_touch_area(event.pos, width, height):
                x, y = event.rel
                state.rx -= y * 0.3
                state.ry += x * 0.3

        elif event.type == MOUSEWHEEL:
            pass


def move_to_next_model(state):
    state.model_number = state.gallery.wrap_index(state.model_number + 1)
    load_current_model(state)


def move_to_previous_model(state):
    state.model_number = state.gallery.wrap_index(state.model_number - 1)
    load_current_model(state)


def reload_if_models_changed(state):
    if not state.gallery.refresh():
        return

    time.sleep(TIME_TO_WAIT_FOR_NEW_MODEL)
    state.gallery.refresh()
    state.model_number = 0
    load_current_model(state)


def update_idle_rotation(state):
    if time.time() - state.last_touch <= time_to_idle:
        return

    state.ry += 1
    state.rx = -90


def render_model(state):
    if state.current_model is None:
        return

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslate(0, 0, zpos)
    glRotatef(state.ry, 0.0, 1.0, 0.0)
    glRotatef(state.rx, 1.0, 0.0, 0.0)
    glRotatef(state.rz, 0.0, 0.0, 1.0)
    state.current_model.render()


def is_inside_touch_area(position, width, height):
    x, y = position
    return (
        borders[0] * width < x < (1 - borders[0]) * width
        and borders[1] * height < y < (1 - borders[1]) * height
    )


def mark_user_activity(state):
    state.last_touch = time.time()


def cleanup(state):
    state.gallery.free()
    pygame.quit()
