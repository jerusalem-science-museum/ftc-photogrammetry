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
    show_error_screen(state)

    while True:
        for event in pygame.event.get():
            if should_exit(event):
                cleanup(state)
                return

        state.clock.tick(30)


def run_gallery(state):
    open_model_screen(state)
    load_current_model(state)

    while state.running:
        handle_events(state)
        reload_if_models_changed(state)
        update_idle_rotation(state)
        render_model(state)
        pygame.display.flip()
        state.clock.tick(30)

    cleanup(state)


def main():
    state = create_viewer_state()
    state.gallery.refresh()

    if not state.gallery.has_models():
        run_error_screen(state)
        return

    run_gallery(state)


if __name__ == "__main__":
    main()
