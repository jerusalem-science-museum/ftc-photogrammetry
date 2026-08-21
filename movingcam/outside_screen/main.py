import pygame

from viewer_core import (
    cleanup,
    create_viewer_state,
    handle_events,
    load_current_model,
    open_model_screen,
    reload_if_models_changed,
    render_model,
    should_exit,
    show_error_screen,
    update_idle_rotation,
)


def run_error_screen(state):
    # Keep the exhibit in fullscreen error mode until the operator exits.
    show_error_screen(state)

    while True:
        # In error mode there is nothing to update, but pygame still needs events pumped.
        for event in pygame.event.get():
            if should_exit(event):
                cleanup(state)
                return

        # Limit CPU usage while the error message is waiting on screen.
        state.clock.tick(30)


def run_gallery(state):
    # Normal viewer flow: open OpenGL, load newest model, then tick forever.
    open_model_screen(state)
    load_current_model(state)

    while state.running:
        # One frame of the exhibit: input, new-model detection, animation, draw.
        handle_events(state)
        reload_if_models_changed(state)
        update_idle_rotation(state)
        render_model(state)

        # Swap the back buffer to the visible fullscreen display.
        pygame.display.flip()
        state.clock.tick(30)

    cleanup(state)


def main():
    # Main stays intentionally high-level; implementation details live in viewer_core.
    state = create_viewer_state()

    # First scan decides whether the gallery can start or must show an error.
    state.gallery.refresh()

    if not state.gallery.has_models():
        run_error_screen(state)
        return

    run_gallery(state)


if __name__ == "__main__":
    main()
