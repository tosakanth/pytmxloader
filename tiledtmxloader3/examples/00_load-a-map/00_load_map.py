#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

This is the pygame minimal example.

"""



#  -----------------------------------------------------------------------------


import tiledtmxloader



def demo_pygame(file_name):
    """
    Example showing how to load a map.
    """

    # parser the map (it is done here to initialize the
    # window the same size as the map if it is small enough)
    world_map = tiledtmxloader.tmxreader.TileMapParser().parse_decode(file_name)

    # print the filename
    print "loaded map:", world_map.map_file_name

    # let see how many pixels it will use
    x_pixels = world_map.pixel_width
    y_pixels = world_map.pixel_height
    print "map size in pixels:", x_pixels, y_pixels


    # let see the tilesize
    print "tile size used:",  world_map.tilewidth, world_map.tileheight

    # number of tiles
    print "tiles used:", world_map.width, world_map.height

    # count the layers
    print "found '", len(world_map.layers), "' layers on this map"

    # # just to see if the map was loaded correctly we print
    # # it on the console, warning: may be huge output!
    # # tiledtmxloader.tmxreader.printer(world_map)




#  -----------------------------------------------------------------------------
def main():
    """
    Main method.
    """
    import sys
    import os.path

    args = sys.argv[1:]
    if len(args) < 1:
        print('usage: python %s your_map.tmx' % \
            os.path.basename(__file__))
        return

    demo_pygame(args[0])

#  -----------------------------------------------------------------------------

if __name__ == '__main__':
    main()


