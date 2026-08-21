# Outside Screen

The outside screen is the gallery viewer for completed photogrammetry models.
It runs on the outside computer and watches the shared model directory. The
newest model is shown first, and visitors can move through the gallery with the
physical left/right controls, which currently send keyboard input.

## Run

From this directory:

```bash
./run.sh
```

For development, you can also run:

```bash
python3 main.py
```

The program opens a fullscreen OpenGL window. Press `ESC` to exit.

## Controls

- `R`: move to the next older model.
- `L`: move to the previous/newer model.
- mouse/touch drag: rotate the current model.
- idle: after `time_to_idle` seconds, the model rotates automatically.

## Model Directory

The model directory is configured in `consts.py` with
`photogrammetry_data_path`.

Each model should be stored in a timestamp-named folder. For example:

```text
photogrammetry_data/
  20260821183001/
    output/
      texturedMesh.obj
      texture_1001.png
```

Folder names are sorted by name. Because the names are timestamps, this means
the highest folder name is treated as the newest model.

Only folders that contain `output/texturedMesh.obj` are included in the gallery.
This avoids loading stray files or incomplete model folders.

## Code Layout

- `main.py`: the program workflow. It creates the viewer state, decides whether
  to show the error screen or gallery, and runs the main loop.
- `viewer_core.py`: the core viewer operations: loading models, switching
  models, handling events, rendering, idle rotation, error screen, and cleanup.
- `model_gallery.py`: model discovery, sorted newest-first access, and the OBJ
  cache.
- `objloader.py`: OBJ/MTL parsing, OpenGL texture upload, display-list creation,
  and OpenGL resource cleanup.
- `consts.py`: paths and runtime settings.
- `pictures/`: static image assets.
- `docs/`: hardware/control documentation.

## Cache Behavior

`ModelGallery` keeps a cache of loaded OBJ models so gallery navigation is
faster after a model has been viewed once.

The gallery only keeps the newest `MAX_MODEL_NUMBER` model folders available.
When a new model appears, the gallery refreshes, resets to the newest model, and
evicts cached models that are no longer inside that newest set.

This cache speeds up repeated navigation because the OBJ parsing, texture
upload, and OpenGL display-list creation do not need to run again for cached
models.

## Important Settings

In `consts.py`:

- `photogrammetry_data_path`: shared folder containing timestamp model folders.
- `obj_path`: relative path to the OBJ inside each model folder.
- `texture_path`: relative path to the texture inside each model folder.
- `MAX_MODEL_NUMBER`: maximum number of newest models available in the gallery
  and cache.
- `TIME_TO_WAIT_FOR_NEW_MODEL`: delay after detecting a new model so writing can
  finish.
- `time_to_idle`: seconds before automatic rotation starts.
- `zpos`: model distance from camera. This must be negative.

For production, `photogrammetry_data_path` should usually point to the shared
directory. For local testing, it can point to `test_models`.
