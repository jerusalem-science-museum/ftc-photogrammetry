import os
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from objloader import OBJ, center_object


@dataclass(frozen=True)
class ModelFiles:
    name: str
    obj_file: str
    texture_file: str


def find_models(folder_path: str, obj_path: str, texture_path: str) -> List[ModelFiles]:
    """
    Return valid model folders sorted by folder name from oldest to newest.
    Timestamp folder names sort correctly as strings.
    """
    if not os.path.isdir(folder_path):
        return []

    models = []
    for name in sorted(os.listdir(folder_path)):
        model_folder = os.path.join(folder_path, name)
        model_obj = os.path.join(model_folder, obj_path)
        if not os.path.isdir(model_folder) or not os.path.isfile(model_obj):
            continue

        models.append(
            ModelFiles(
                name=name,
                obj_file=model_obj,
                texture_file=os.path.join(model_folder, texture_path),
            )
        )

    return models


def get_nth_obj_in_folder(folder_path, n, obj_path, texture_path, max_models):
    """
    Compatibility helper: n=0 returns the newest model, n=1 the previous one, etc.
    """
    gallery = ModelGallery(folder_path, obj_path, texture_path, max_models)
    gallery.refresh()
    return gallery.get_obj_paths(n)


class ModelGallery:
    def __init__(self, folder_path, obj_path, texture_path, max_models):
        self.folder_path = folder_path
        self.obj_path = obj_path
        self.texture_path = texture_path
        self.max_models = max_models
        self.models: List[ModelFiles] = []
        self.cache: Dict[str, OBJ] = {}

    def refresh(self) -> bool:
        previous_names = self.names
        self.models = find_models(self.folder_path, self.obj_path, self.texture_path)[
            -self.max_models:
        ]
        self.evict_old_models()
        return self.names != previous_names

    @property
    def names(self):
        return [model.name for model in self.models]

    def has_models(self):
        return len(self.models) > 0

    def count(self):
        return len(self.models)

    def clamp_index(self, index):
        if not self.models:
            return 0
        return max(0, min(index, len(self.models) - 1))

    def wrap_index(self, index):
        if not self.models:
            return 0
        return index % len(self.models)

    def get_files(self, index) -> Optional[ModelFiles]:
        if not self.models:
            return None
        return self.models[-(self.clamp_index(index) + 1)]

    def get_obj_paths(self, index) -> Tuple[Optional[str], Optional[str]]:
        model = self.get_files(index)
        if model is None:
            return None, None
        return model.obj_file, model.texture_file

    def get_loaded_model(self, index) -> Optional[OBJ]:
        model = self.get_files(index)
        if model is None:
            return None

        if model.name not in self.cache:
            center_object(model.obj_file)
            self.cache[model.name] = OBJ(model.obj_file, swapyz=True)

        return self.cache[model.name]

    def evict_old_models(self):
        active_names = set(self.names)
        for name in list(self.cache):
            if name not in active_names:
                self.cache[name].free()
                del self.cache[name]

    def free(self):
        for model in self.cache.values():
            model.free()
        self.cache.clear()
