"""Predefined color values.

Source: `Wikipedia <https://en.wikipedia.org/wiki/Web_colors#Extended_colors>`_"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

from dearpygui_obj.data import (
    color_from_float as from_float,
    color_from_rgba8 as from_rgba8,
    color_from_hex as from_hex,
)

## Red Colors
dark_red            = from_hex('#8B0000')
red                 = from_hex('#FF0000')
firebrick           = from_hex('#B22222')
crimson             = from_hex('#DC143C')
indian_red          = from_hex('#CD5C5C')
light_coral         = from_hex('#F08080')
salmon              = from_hex('#FA8072')
dark_salmon         = from_hex('#E9967A')
light_salmon        = from_hex('#FFA07A')

## Orange Colors
orange_red          = from_hex('#FF4500')
tomato              = from_hex('#FF6347')
dark_orange         = from_hex('#FF8C00')
coral               = from_hex('#FF7F50')
orange              = from_hex('#FFA500')

## Yellow Colors
dark_khaki          = from_hex('#BDB76B')
gold                = from_hex('#FFD700')
khaki               = from_hex('#F0E68C')
peach_puff          = from_hex('#FFDAB9')
yellow              = from_hex('#FFFF00')
pale_goldenrod      = from_hex('#EEE8AA')
moccasin            = from_hex('#FFE4B5')
papaya_whip         = from_hex('#FFEFD5')
light_goldenrod_yellow = from_hex('#FAFAD2')
lemon_chiffon       = from_hex('#FFFACD')
light_yellow        = from_hex('#FFFFE0')

## Brown Colors
maroon              = from_hex('#800000')
brown               = from_hex('#A52A2A')
saddle_brown        = from_hex('#8B4513')
sienna              = from_hex('#A0522D')
chocolate           = from_hex('#D2691E')
dark_goldenrod      = from_hex('#B8860B')
peru                = from_hex('#CD853F')
rosy_brown          = from_hex('#BC8F8F')
goldenrod           = from_hex('#DAA520')
sandy_brown         = from_hex('#F4A460')
tan                 = from_hex('#D2B48C')
burlywood           = from_hex('#DEB887')
wheat               = from_hex('#F5DEB3')
navajo_white        = from_hex('#FFDEAD')
bisque              = from_hex('#FFE4C4')
blanched_almond     = from_hex('#FFEBCD')
cornsilk            = from_hex('#FFF8DC')

## Green Colors
dark_green          = from_hex('#006400')
green               = from_hex('#008000')
dark_olive_green    = from_hex('#556B2F')
forest_green        = from_hex('#228B22')
sea_green           = from_hex('#2E8B57')
olive               = from_hex('#808000')
olive_drab          = from_hex('#6B8E23')
medium_sea_green    = from_hex('#3CB371')
lime_green          = from_hex('#32CD32')
lime                = from_hex('#00FF00')
spring_green        = from_hex('#00FF7F')
medium_spring_green = from_hex('#00FA9A')
dark_sea_green      = from_hex('#8FBC8F')
medium_aquamarine   = from_hex('#66CDAA')
yellow_green        = from_hex('#9ACD32')
lawn_green          = from_hex('#7CFC00')
chartreuse          = from_hex('#7FFF00')
light_green         = from_hex('#90EE90')
green_yellow        = from_hex('#ADFF2F')
pale_green          = from_hex('#98FB98')

## Cyan Colors
teal                = from_hex('#008080')
dark_cyan           = from_hex('#008B8B')
lightsea_green      = from_hex('#20B2AA')
cadet_blue          = from_hex('#5F9EA0')
dark_turquoise      = from_hex('#00CED1')
medium_turquoise    = from_hex('#48D1CC')
turquoise           = from_hex('#40E0D0')
aqua                = from_hex('#00FFFF')
cyan                = from_hex('#00FFFF')
aquamarine          = from_hex('#7FFFD4')
pale_turquoise      = from_hex('#AFEEEE')
light_cyan          = from_hex('#E0FFFF')

## Blue Colors
navy                = from_hex('#000080')
dark_blue           = from_hex('#00008B')
medium_blue         = from_hex('#0000CD')
blue                = from_hex('#0000FF')
midnight_blue       = from_hex('#191970')
royal_blue          = from_hex('#4169E1')
steel_blue          = from_hex('#4682B4')
dodger_blue         = from_hex('#1E90FF')
deep_sky_blue       = from_hex('#00BFFF')
cornflower_blue     = from_hex('#6495ED')
sky_blue            = from_hex('#87CEEB')
light_sky_blue      = from_hex('#87CEFA')
light_steel_blue    = from_hex('#B0C4DE')
light_blue          = from_hex('#ADD8E6')
powder_blue         = from_hex('#B0E0E6')

## Magenta Colors
indigo              = from_hex('#4B0082')
purple              = from_hex('#800080')
dark_magenta        = from_hex('#8B008B')
dark_violet         = from_hex('#9400D3')
dark_slate_blue     = from_hex('#483D8B')
blue_violet         = from_hex('#8A2BE2')
dark_orchid         = from_hex('#9932CC')
fuchsia             = from_hex('#FF00FF')
magenta             = from_hex('#FF00FF')
slate_blue          = from_hex('#6A5ACD')
medium_slate_blue   = from_hex('#7B68EE')
medium_orchid       = from_hex('#BA55D3')
medium_purple       = from_hex('#9370DB')
orchid              = from_hex('#DA70D6')
violet              = from_hex('#EE82EE')
plum                = from_hex('#DDA0DD')
thistle             = from_hex('#D8BFD8')
lavender            = from_hex('#E6E6FA')

## Pink Colors
medium_violet_red   = from_hex('#C71585')
deep_pink           = from_hex('#FF1493')
pale_violet_red     = from_hex('#DB7093')
hot_pink            = from_hex('#FF69B4')
light_pink          = from_hex('#FFB6C1')
pink                = from_hex('#FFC0CB')

## White Colors
misty_rose          = from_hex('#FFE4E1')
antique_white       = from_hex('#FAEBD7')
linen               = from_hex('#FAF0E6')
beige               = from_hex('#F5F5DC')
white_smoke         = from_hex('#F5F5F5')
lavender_blush      = from_hex('#FFF0F5')
old_lace            = from_hex('#FDF5E6')
alice_blue          = from_hex('#F0F8FF')
seashell            = from_hex('#FFF5EE')
ghost_white         = from_hex('#F8F8FF')
honeydew            = from_hex('#F0FFF0')
floral_white        = from_hex('#FFFAF0')
azure               = from_hex('#F0FFFF')
mint_cream          = from_hex('#F5FFFA')
snow                = from_hex('#FFFAFA')
ivory               = from_hex('#FFFFF0')
white               = from_hex('#FFFFFF')

## Black Colors
black               = from_hex('#000000')
dark_slate_gray     = from_hex('#2F4F4F')
dim_gray            = from_hex('#696969')
slate_gray          = from_hex('#708090')
gray                = from_hex('#808080')
light_slate_gray    = from_hex('#778899')
dark_gray           = from_hex('#A9A9A9')
silver              = from_hex('#C0C0C0')
light_gray          = from_hex('#D3D3D3')
gainsboro           = from_hex('#DCDCDC')


__all__ = [
    'from_float',
    'from_rgba8',
    'from_hex',

    'dark_red',
    'red',
    'firebrick',
    'crimson',
    'indian_red',
    'light_coral',
    'salmon',
    'dark_salmon',
    'light_salmon',

    'orange_red',
    'tomato',
    'dark_orange',
    'coral',
    'orange',

    'dark_khaki',
    'gold',
    'khaki',
    'peach_puff',
    'yellow',
    'pale_goldenrod',
    'moccasin',
    'papaya_whip',
    'light_goldenrod_yellow',
    'lemon_chiffon',
    'light_yellow',

    'maroon',
    'brown',
    'saddle_brown',
    'sienna',
    'chocolate',
    'dark_goldenrod',
    'peru',
    'rosy_brown',
    'goldenrod',
    'sandy_brown',
    'tan',
    'burlywood',
    'wheat',
    'navajo_white',
    'bisque',
    'blanched_almond',
    'cornsilk',

    'dark_green',
    'green',
    'dark_olive_green',
    'forest_green',
    'sea_green',
    'olive',
    'olive_drab',
    'medium_sea_green',
    'lime_green',
    'lime',
    'spring_green',
    'medium_spring_green',
    'dark_sea_green',
    'medium_aquamarine',
    'yellow_green',
    'lawn_green',
    'chartreuse',
    'light_green',
    'green_yellow',
    'pale_green',

    'teal',
    'dark_cyan',
    'lightsea_green',
    'cadet_blue',
    'dark_turquoise',
    'medium_turquoise',
    'turquoise',
    'aqua',
    'cyan',
    'aquamarine',
    'pale_turquoise',
    'light_cyan',

    'navy',
    'dark_blue',
    'medium_blue',
    'blue',
    'midnight_blue',
    'royal_blue',
    'steel_blue',
    'dodger_blue',
    'deep_sky_blue',
    'cornflower_blue',
    'sky_blue',
    'light_sky_blue',
    'light_steel_blue',
    'light_blue',
    'powder_blue',

    'indigo',
    'purple',
    'dark_magenta',
    'dark_violet',
    'dark_slate_blue',
    'blue_violet',
    'dark_orchid',
    'fuchsia',
    'magenta',
    'slate_blue',
    'medium_slate_blue',
    'medium_orchid',
    'medium_purple',
    'orchid',
    'violet',
    'plum',
    'thistle',
    'lavender',

    'medium_violet_red',
    'deep_pink',
    'pale_violet_red',
    'hot_pink',
    'light_pink',
    'pink',

    'misty_rose',
    'antique_white',
    'linen',
    'beige',
    'white_smoke',
    'lavender_blush',
    'old_lace',
    'alice_blue',
    'seashell',
    'ghost_white',
    'honeydew',
    'floral_white',
    'azure',
    'mint_cream',
    'snow',
    'ivory',
    'white',

    'black',
    'dark_slate_gray',
    'dim_gray',
    'slate_gray',
    'gray',
    'light_slate_gray',
    'dark_gray',
    'silver',
    'light_gray',
    'gainsboro',
]