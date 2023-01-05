from palettable.colorbrewer.colorbrewer import (
    _load_maps_by_type as load_colorbrewer_palette,
)  # noqa
from palettable.cubehelix.cubehelix import _get_all_maps as load_cubehelix_palettes
from palettable.palette import Palette
from palettable.tableau.tableau import _get_all_maps as load_tableau_palettes
from palettable.wesanderson.wesanderson import (
    _get_all_maps as load_wesanderson_palettes,
)


class PaletteMapper(object):
    def __init__(self):
        self._palettes = {}

    @staticmethod
    def _split_palette_name(name):
        split = name.split("_")
        if len(split) == 1:
            raise ValueError("Invalid palette description '%s'" % name)
        name = split[0]
        reverse = False
        if len(split) == 2:
            size = int(split[1])
        else:
            if split[-1] == "r":
                reverse = True
                size = int(split[-2])
            else:
                size = int(split[-1])

        return name, size, reverse

    def add_palettalbe_palette(self, name, palette):
        assert isinstance(palette, Palette)
        name, size, reverse = self._split_palette_name(name)

        if name not in self._palettes:
            self._palettes[name] = {}
        if size not in self._palettes[name]:
            self._palettes[name][size] = {}
        self._palettes[name][size][reverse] = palette

    def map_palette(self, name, n=3, reverse=False):
        try:
            name, size, reverse = self._split_palette_name(name)
        except ValueError:
            size = n

        palette = self._palettes[name]
        max_size = max(palette.keys())
        min_size = min(palette.keys())
        if size < min_size:
            size = min_size
        if size > max_size:
            size = max_size

        return palette[size][reverse]


mapper = PaletteMapper()

for key, obj in load_colorbrewer_palette("diverging").items():
    mapper.add_palettalbe_palette(key, obj)

for key, obj in load_colorbrewer_palette("sequential").items():
    mapper.add_palettalbe_palette(key, obj)

for key, obj in load_colorbrewer_palette("qualitative").items():
    mapper.add_palettalbe_palette(key, obj)

for key, obj in load_cubehelix_palettes().items():
    mapper.add_palettalbe_palette(key, obj)

for key, obj in load_tableau_palettes().items():
    mapper.add_palettalbe_palette(key, obj)

for key, obj in load_wesanderson_palettes().items():
    mapper.add_palettalbe_palette(key, obj)
