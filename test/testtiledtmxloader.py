#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
p = os.path.join(os.path.dirname(__file__), os.pardir)
print p
sys.path.insert(0, p)
print sys.path


import os
import unittest

import tiledtmxloader


_has_pygame = False
try:
    import pygame
    _has_pygame = True
    import tiledtmxloader.helperspygame
except:
    pass

_has_pyglet = False
try:
    import pyglet
    _has_pyglet = True
    import tiledtmxloader.helperspyglet
except:
    pass


class MapLoadTests(unittest.TestCase):

    def setUp(self):
        os.chdir(os.path.dirname(__file__))
        if not _has_pygame and not _has_pyglet:
            self.fail("needs either module 'pyglet' or 'pygame' installed for testing")
        
    #--- pygame tests ---#
    def test_load_map_from_cur_dir_pygame(self):
        if _has_pygame:
            world_map = tiledtmxloader.tiledtmxloader.TileMapParser().parse_decode("minix.tmx")
            tiledtmxloader.helperspygame.ResourceLoaderPygame().load(world_map)

    def test_load_map_from_cur_dir_using_tsx_pygame(self):
        if _has_pygame:
            world_map = tiledtmxloader.tiledtmxloader.TileMapParser().parse_decode("minix_using_tsx.tmx")
            tiledtmxloader.helperspygame.ResourceLoaderPygame().load(world_map)

    def test_load_map_from_sub_dir_using_tsx_pygame(self):
        if _has_pygame:
            world_map = tiledtmxloader.tiledtmxloader.TileMapParser().parse_decode("mini2/mini2.tmx")
            tiledtmxloader.helperspygame.ResourceLoaderPygame().load(world_map)

    def test_load_map_from_sub_dir_pygame(self):
        if _has_pygame:
            world_map = tiledtmxloader.tiledtmxloader.TileMapParser().parse_decode("mini2/mini2_alt.tmx")
            tiledtmxloader.helperspygame.ResourceLoaderPygame().load(world_map)

    def test_load_map_from_sub_dir_using_tsx_from_sub_dir_pygame(self):
        if _has_pygame:
            world_map = tiledtmxloader.tiledtmxloader.TileMapParser().parse_decode("mini3/mini3.tmx")
            tiledtmxloader.helperspygame.ResourceLoaderPygame().load(world_map)

    def test_load_map_from_sub_dir_using_tsx_from_sub_dir_and_img_from_sub_dir_pygame(self):
        if _has_pygame:
            world_map = tiledtmxloader.tiledtmxloader.TileMapParser().parse_decode("mini4/mini4.tmx")
            tiledtmxloader.helperspygame.ResourceLoaderPygame().load(world_map)

    def test_can_load_compression_xml_pygame(self):
        if _has_pygame:
            world_map = tiledtmxloader.tiledtmxloader.TileMapParser().parse_decode("minix_xml.tmx")
            tiledtmxloader.helperspygame.ResourceLoaderPygame().load(world_map)

    def test_can_load_compression_cvs_pygame(self):
        if _has_pygame:
            world_map = tiledtmxloader.tiledtmxloader.TileMapParser().parse_decode("minix_cvs.tmx")
            tiledtmxloader.helperspygame.ResourceLoaderPygame().load(world_map)

    def test_can_load_compression_base64_zlib_pygame(self):
        if _has_pygame:
            world_map = tiledtmxloader.tiledtmxloader.TileMapParser().parse_decode("minix_base64_zlib.tmx")
            tiledtmxloader.helperspygame.ResourceLoaderPygame().load(world_map)

    def test_can_load_compression_base64_uncompressed_pygame(self):
        if _has_pygame:
            world_map = tiledtmxloader.tiledtmxloader.TileMapParser().parse_decode("minix_base64_uncompressed.tmx")
            tiledtmxloader.helperspygame.ResourceLoaderPygame().load(world_map)

    def test_can_load_compression_base64_gzip_pygame(self):
        if _has_pygame:
            world_map = tiledtmxloader.tiledtmxloader.TileMapParser().parse_decode("minix_base64_gzip.tmx")
            tiledtmxloader.helperspygame.ResourceLoaderPygame().load(world_map)

    def test_can_load_compression_base64_gzip_dtd_pygame(self):
        if _has_pygame:
            world_map = tiledtmxloader.tiledtmxloader.TileMapParser().parse_decode("minix_base64_gzip_dtd.tmx")
            tiledtmxloader.helperspygame.ResourceLoaderPygame().load(world_map)
            
    def test_get_list_of_quad_coords(self):
        if _has_pygame:
            layer = tiledtmxloader.helperspygame.RendererPygame._Layer
                                                #xpos, ypos, level=2
            coords = layer._get_list_of_neighbour_coord(0, 0, 1, 10, 10)
            expected = ((0, 0), )
            self.compare(expected, coords)
            
            coords = layer._get_list_of_neighbour_coord(0, 0, 2, 10, 10)
            expected = ((0, 0), (1, 0), (0, 1), (1, 1))
            self.compare(expected, coords)
            
            coords = layer._get_list_of_neighbour_coord(1, 1, 3, 10, 10)
            expected = ((3, 3), (4, 3), (5, 3), (3, 4), (4, 4), (5, 4), (3, 5), (4, 5), (5, 5))
            self.compare(expected, coords)
            
    def compare(self, expected, captured):
        """
        Helper method to compare to lists.
        """
        if len(expected) != len(captured):
            self.fail(str.format("Not same number of expected and captured actions! \n expected: {0} \n captured: {1}", \
                                    ", ".join(map(str, expected)), \
                                    ", ".join(map(str, captured))))
        for idx, expected_action in enumerate(expected):
            action = captured[idx]
            if action != expected_action:
                self.fail(str.format("captured action does not match with expected action! \n expected: {0} \n captured: {1}", \
                                    ", ".join(map(str, expected)), \
                                    ", ".join(map(str, captured))))

    
            

    #--- pyglet tests ---#
    def test_load_map_from_cur_dir_pyglet(self):
        if _has_pyglet:
            world_map = tiledtmxloader.tiledtmxloader.TileMapParser().parse_decode("minix.tmx")
            tiledtmxloader.helperspyglet.ResourceLoaderPyglet().load(world_map)
        
    def test_load_map_from_cur_dir_using_tsx_pyglet(self):
        if _has_pyglet:
            world_map = tiledtmxloader.tiledtmxloader.TileMapParser().parse_decode("minix_using_tsx.tmx")
            tiledtmxloader.helperspyglet.ResourceLoaderPyglet().load(world_map)

    def test_load_map_from_sub_dir_using_tsx_pyglet(self):
        if _has_pyglet:
            world_map = tiledtmxloader.tiledtmxloader.TileMapParser().parse_decode("mini2/mini2.tmx")
            tiledtmxloader.helperspyglet.ResourceLoaderPyglet().load(world_map)

    def test_load_map_from_sub_dir_pyglet(self):
        if _has_pyglet:
            world_map = tiledtmxloader.tiledtmxloader.TileMapParser().parse_decode("mini2/mini2_alt.tmx")
            tiledtmxloader.helperspyglet.ResourceLoaderPyglet().load(world_map)

    def test_load_map_from_sub_dir_using_tsx_from_sub_dir_pyglet(self):
        if _has_pyglet:
            world_map = tiledtmxloader.tiledtmxloader.TileMapParser().parse_decode("mini3/mini3.tmx")
            tiledtmxloader.helperspyglet.ResourceLoaderPyglet().load(world_map)

    def test_load_map_from_sub_dir_using_tsx_from_sub_dir_and_img_from_sub_dir_pyglet(self):
        if _has_pyglet:
            world_map = tiledtmxloader.tiledtmxloader.TileMapParser().parse_decode("mini4/mini4.tmx")
            tiledtmxloader.helperspyglet.ResourceLoaderPyglet().load(world_map)
            
    def test_can_load_compression_xml_pyglet(self):
        if _has_pyglet:
            world_map = tiledtmxloader.tiledtmxloader.TileMapParser().parse_decode("minix_xml.tmx")
            tiledtmxloader.helperspyglet.ResourceLoaderPyglet().load(world_map)

    def test_can_load_compression_cvs_pyglet(self):
        if _has_pyglet:
            world_map = tiledtmxloader.tiledtmxloader.TileMapParser().parse_decode("minix_cvs.tmx")
            tiledtmxloader.helperspyglet.ResourceLoaderPyglet().load(world_map)

    def test_can_load_compression_base64_zlib_pyglet(self):
        if _has_pyglet:
            world_map = tiledtmxloader.tiledtmxloader.TileMapParser().parse_decode("minix_base64_zlib.tmx")
            tiledtmxloader.helperspyglet.ResourceLoaderPyglet().load(world_map)

    def test_can_load_compression_base64_uncompressed_pyglet(self):
        if _has_pyglet:
            world_map = tiledtmxloader.tiledtmxloader.TileMapParser().parse_decode("minix_base64_uncompressed.tmx")
            tiledtmxloader.helperspyglet.ResourceLoaderPyglet().load(world_map)

    def test_can_load_compression_base64_gzip_pyglet(self):
        if _has_pyglet:
            world_map = tiledtmxloader.tiledtmxloader.TileMapParser().parse_decode("minix_base64_gzip.tmx")
            tiledtmxloader.helperspyglet.ResourceLoaderPyglet().load(world_map)

    def test_can_load_compression_base64_gzip_dtd_pyglet(self):
        if _has_pyglet:
            world_map = tiledtmxloader.tiledtmxloader.TileMapParser().parse_decode("minix_base64_gzip_dtd.tmx")
            tiledtmxloader.helperspyglet.ResourceLoaderPyglet().load(world_map)


if __name__ == '__main__':
    unittest.main()
            