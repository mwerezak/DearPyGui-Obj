"""Predefined color values.

Source: `Wikipedia <https://en.wikipedia.org/wiki/Web_colors#Extended_colors>`_"""

from __future__ import annotations

from typing import TYPE_CHECKING
from dearpygui_obj.data import color_from_hex

if TYPE_CHECKING:
    pass

## Red Colors
dark_red            = color_from_hex('#8B0000')
red                 = color_from_hex('#FF0000')
firebrick           = color_from_hex('#B22222')
crimson             = color_from_hex('#DC143C')
indian_red          = color_from_hex('#CD5C5C')
light_coral         = color_from_hex('#F08080')
salmon              = color_from_hex('#FA8072')
dark_salmon         = color_from_hex('#E9967A')
light_salmon        = color_from_hex('#FFA07A')

## Orange Colors
orange_red          = color_from_hex('#FF4500')
tomato              = color_from_hex('#FF6347')
dark_orange         = color_from_hex('#FF8C00')
coral               = color_from_hex('#FF7F50')
orange              = color_from_hex('#FFA500')

## Yellow Colors
dark_khaki          = color_from_hex('#BDB76B')
gold                = color_from_hex('#FFD700')
khaki               = color_from_hex('#F0E68C')
peach_puff          = color_from_hex('#FFDAB9')
yellow              = color_from_hex('#FFFF00')
pale_goldenrod      = color_from_hex('#EEE8AA')
moccasin            = color_from_hex('#FFE4B5')
papaya_whip         = color_from_hex('#FFEFD5')
light_goldenrod_yellow = color_from_hex('#FAFAD2')
lemon_chiffon       = color_from_hex('#FFFACD')
light_yellow        = color_from_hex('#FFFFE0')

## Brown Colors
maroon              = color_from_hex('#800000')
brown               = color_from_hex('#A52A2A')
saddle_brown        = color_from_hex('#8B4513')
sienna              = color_from_hex('#A0522D')
chocolate           = color_from_hex('#D2691E')
dark_goldenrod      = color_from_hex('#B8860B')
peru                = color_from_hex('#CD853F')
rosy_brown          = color_from_hex('#BC8F8F')
goldenrod           = color_from_hex('#DAA520')
sandy_brown         = color_from_hex('#F4A460')
tan                 = color_from_hex('#D2B48C')
burlywood           = color_from_hex('#DEB887')
wheat               = color_from_hex('#F5DEB3')
navajo_white        = color_from_hex('#FFDEAD')
bisque              = color_from_hex('#FFE4C4')
blanched_almond     = color_from_hex('#FFEBCD')
cornsilk            = color_from_hex('#FFF8DC')

## Green Colors
dark_green          = color_from_hex('#006400')
green               = color_from_hex('#008000')
dark_olive_green    = color_from_hex('#556B2F')
forest_green        = color_from_hex('#228B22')
sea_green           = color_from_hex('#2E8B57')
olive               = color_from_hex('#808000')
olive_drab          = color_from_hex('#6B8E23')
medium_sea_green    = color_from_hex('#3CB371')
lime_green          = color_from_hex('#32CD32')
lime                = color_from_hex('#00FF00')
spring_green        = color_from_hex('#00FF7F')
medium_spring_green = color_from_hex('#00FA9A')
dark_sea_green      = color_from_hex('#8FBC8F')
medium_aquamarine   = color_from_hex('#66CDAA')
yellow_green        = color_from_hex('#9ACD32')
lawn_green          = color_from_hex('#7CFC00')
chartreuse          = color_from_hex('#7FFF00')
light_green         = color_from_hex('#90EE90')
green_yellow        = color_from_hex('#ADFF2F')
pale_green          = color_from_hex('#98FB98')

## Cyan Colors
teal                = color_from_hex('#008080')
dark_cyan           = color_from_hex('#008B8B')
lightsea_green      = color_from_hex('#20B2AA')
cadet_blue          = color_from_hex('#5F9EA0')
dark_turquoise      = color_from_hex('#00CED1')
medium_turquoise    = color_from_hex('#48D1CC')
turquoise           = color_from_hex('#40E0D0')
aqua                = color_from_hex('#00FFFF')
cyan                = color_from_hex('#00FFFF')
aquamarine          = color_from_hex('#7FFFD4')
pale_turquoise      = color_from_hex('#AFEEEE')
light_cyan          = color_from_hex('#E0FFFF')

## Blue Colors
navy                = color_from_hex('#000080')
dark_blue           = color_from_hex('#00008B')
medium_blue         = color_from_hex('#0000CD')
blue                = color_from_hex('#0000FF')
midnight_blue       = color_from_hex('#191970')
royal_blue          = color_from_hex('#4169E1')
steel_blue          = color_from_hex('#4682B4')
dodger_blue         = color_from_hex('#1E90FF')
deep_sky_blue       = color_from_hex('#00BFFF')
cornflower_blue     = color_from_hex('#6495ED')
sky_blue            = color_from_hex('#87CEEB')
light_sky_blue      = color_from_hex('#87CEFA')
light_steel_blue    = color_from_hex('#B0C4DE')
light_blue          = color_from_hex('#ADD8E6')
powder_blue         = color_from_hex('#B0E0E6')

## Magenta Colors
indigo              = color_from_hex('#4B0082')
purple              = color_from_hex('#800080')
dark_magenta        = color_from_hex('#8B008B')
dark_violet         = color_from_hex('#9400D3')
dark_slate_blue     = color_from_hex('#483D8B')
blue_violet         = color_from_hex('#8A2BE2')
dark_orchid         = color_from_hex('#9932CC')
fuchsia             = color_from_hex('#FF00FF')
magenta             = color_from_hex('#FF00FF')
slate_blue          = color_from_hex('#6A5ACD')
medium_slate_blue   = color_from_hex('#7B68EE')
medium_orchid       = color_from_hex('#BA55D3')
medium_purple       = color_from_hex('#9370DB')
orchid              = color_from_hex('#DA70D6')
violet              = color_from_hex('#EE82EE')
plum                = color_from_hex('#DDA0DD')
thistle             = color_from_hex('#D8BFD8')
lavender            = color_from_hex('#E6E6FA')

## Pink Colors
medium_violet_red   = color_from_hex('#C71585')
deep_pink           = color_from_hex('#FF1493')
pale_violet_red     = color_from_hex('#DB7093')
hot_pink            = color_from_hex('#FF69B4')
light_pink          = color_from_hex('#FFB6C1')
pink                = color_from_hex('#FFC0CB')

## White Colors
misty_rose          = color_from_hex('#FFE4E1')
antique_white       = color_from_hex('#FAEBD7')
linen               = color_from_hex('#FAF0E6')
beige               = color_from_hex('#F5F5DC')
white_smoke         = color_from_hex('#F5F5F5')
lavender_blush      = color_from_hex('#FFF0F5')
old_lace            = color_from_hex('#FDF5E6')
alice_blue          = color_from_hex('#F0F8FF')
seashell            = color_from_hex('#FFF5EE')
ghost_white         = color_from_hex('#F8F8FF')
honeydew            = color_from_hex('#F0FFF0')
floral_white        = color_from_hex('#FFFAF0')
azure               = color_from_hex('#F0FFFF')
mint_cream          = color_from_hex('#F5FFFA')
snow                = color_from_hex('#FFFAFA')
ivory               = color_from_hex('#FFFFF0')
white               = color_from_hex('#FFFFFF')

## Black Colors
black               = color_from_hex('#000000')
dark_slate_gray     = color_from_hex('#2F4F4F')
dim_gray            = color_from_hex('#696969')
slate_gray          = color_from_hex('#708090')
gray                = color_from_hex('#808080')
light_slate_gray    = color_from_hex('#778899')
dark_gray           = color_from_hex('#A9A9A9')
silver              = color_from_hex('#C0C0C0')
light_gray          = color_from_hex('#D3D3D3')
gainsboro           = color_from_hex('#DCDCDC')


__all__ = [
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