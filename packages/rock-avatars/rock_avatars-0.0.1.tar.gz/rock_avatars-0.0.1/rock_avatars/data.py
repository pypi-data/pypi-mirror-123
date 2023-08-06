from PIL import Image
import os
from pathlib import Path
import itertools


class Unit:
    def __init__(self, root, unit_name, unit_file):
        self._root = root
        self._unit_name = unit_name
        self._unit_file = unit_file

        self._unit = Path(self._unit_file).stem

    def _path(self):
        return os.path.join(self._root, self._unit_name, self._unit_file)

    def image(self):
        return Image.open(self._path()).convert("RGBA")

    def name(self):
        return os.path.join(self._unit_name, self._unit_file)


class UnitGroup:
    def __init__(self, root, unit_name):
        self._root = root
        self._unit_name = unit_name

        self._unit_list = []
        self._load()

    def _unit_path(self):
        return os.path.join(self._root, self._unit_name)

    def _load(self):
        for _, _, files in os.walk(self._unit_path()):
            for unit_file in files:
                self._unit_list.append(
                    Unit(self._root, self._unit_name, unit_file))


class AvatarInstance:
    def __init__(self, background, image_list, output="./output"):
        self._image_list = image_list
        self._background = background.image()
        self._output = output
        if not os.path.isdir(self._output):
            os.mkdir(self._output)

    def unit_names(self):
        return ",".join([image.name() for image in self._image_list])

    def file_path(self):
        return os.path.join(self._output, self.file_name()+".png")

    def file_name(self):
        return "_".join([image._unit for image in self._image_list])

    def blend_two(self, background, overlay):
        # return Image.blend(image1, image2, 0.5)
        _, _, _, alpha = overlay.split()
        background.paste(overlay, (0, 0), mask=alpha)
        return background

    def blend(self):
        result = self._image_list[0].image()
        for i in range(1, len(self._image_list)-1):
            result = self.blend_two(result, self._image_list[i].image())
        result = self.blend_two(self._background, result)
        result.save(self.file_path(), "PNG")


class Avatar:
    def __init__(self, root, background, unit_list):
        self._root = root
        self._background = Unit(root, "", background)
        self._unit_list = unit_list  # 顺序加载 代表涂层顺序

        self._unit_group_list = []
        self._load()

    def _load(self):
        for unit_name in self._unit_list:
            self._unit_group_list.append(
                UnitGroup(self._root, unit_name)._unit_list)

    def generate(self):
        for p in itertools.product(*self._unit_group_list):
            instance = AvatarInstance(self._background, p)
            print(instance.unit_names())
            instance.blend()
