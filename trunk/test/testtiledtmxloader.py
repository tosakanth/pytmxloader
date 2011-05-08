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
except:
    pass

_has_pyglet = False
try:
    import pyglet
    _has_pyglet = True
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
            world_map = tiledtmxloader.TileMapParser().parse_decode("minix.tmx")
            tiledtmxloader.ResourceLoaderPygame().load(world_map)

    def test_load_map_from_cur_dir_using_tsx_pygame(self):
        if _has_pygame:
            world_map = tiledtmxloader.TileMapParser().parse_decode("minix_using_tsx.tmx")
            tiledtmxloader.ResourceLoaderPygame().load(world_map)

    def test_load_map_from_sub_dir_using_tsx_pygame(self):
        if _has_pygame:
            world_map = tiledtmxloader.TileMapParser().parse_decode("mini2/mini2.tmx")
            tiledtmxloader.ResourceLoaderPygame().load(world_map)

    def test_load_map_from_sub_dir_pygame(self):
        if _has_pygame:
            world_map = tiledtmxloader.TileMapParser().parse_decode("mini2/mini2_alt.tmx")
            tiledtmxloader.ResourceLoaderPygame().load(world_map)

    def test_load_map_from_sub_dir_using_tsx_from_sub_dir_pygame(self):
        if _has_pygame:
            world_map = tiledtmxloader.TileMapParser().parse_decode("mini3/mini3.tmx")
            tiledtmxloader.ResourceLoaderPygame().load(world_map)

    def test_load_map_from_sub_dir_using_tsx_from_sub_dir_and_img_from_sub_dir_pygame(self):
        if _has_pygame:
            world_map = tiledtmxloader.TileMapParser().parse_decode("mini4/mini4.tmx")
            tiledtmxloader.ResourceLoaderPygame().load(world_map)

    def test_can_load_compression_xml_pygame(self):
        if _has_pygame:
            world_map = tiledtmxloader.TileMapParser().parse_decode("minix_xml.tmx")
            tiledtmxloader.ResourceLoaderPygame().load(world_map)

    def test_can_load_compression_cvs_pygame(self):
        if _has_pygame:
            world_map = tiledtmxloader.TileMapParser().parse_decode("minix_cvs.tmx")
            tiledtmxloader.ResourceLoaderPygame().load(world_map)

    def test_can_load_compression_base64_zlib_pygame(self):
        if _has_pygame:
            world_map = tiledtmxloader.TileMapParser().parse_decode("minix_base64_zlib.tmx")
            tiledtmxloader.ResourceLoaderPygame().load(world_map)

    def test_can_load_compression_base64_uncompressed_pygame(self):
        if _has_pygame:
            world_map = tiledtmxloader.TileMapParser().parse_decode("minix_base64_uncompressed.tmx")
            tiledtmxloader.ResourceLoaderPygame().load(world_map)

    def test_can_load_compression_base64_gzip_pygame(self):
        if _has_pygame:
            world_map = tiledtmxloader.TileMapParser().parse_decode("minix_base64_gzip.tmx")
            tiledtmxloader.ResourceLoaderPygame().load(world_map)

    def test_can_load_compression_base64_gzip_dtd_pygame(self):
        if _has_pygame:
            world_map = tiledtmxloader.TileMapParser().parse_decode("minix_base64_gzip_dtd.tmx")
            tiledtmxloader.ResourceLoaderPygame().load(world_map)

    #--- pyglet tests ---#
    def test_load_map_from_cur_dir_pyglet(self):
        if _has_pyglet:
            world_map = tiledtmxloader.TileMapParser().parse_decode("minix.tmx")
            tiledtmxloader.ResourceLoaderPyglet().load(world_map)
        
    def test_load_map_from_cur_dir_using_tsx_pyglet(self):
        if _has_pyglet:
            world_map = tiledtmxloader.TileMapParser().parse_decode("minix_using_tsx.tmx")
            tiledtmxloader.ResourceLoaderPyglet().load(world_map)

    def test_load_map_from_sub_dir_using_tsx_pyglet(self):
        if _has_pyglet:
            world_map = tiledtmxloader.TileMapParser().parse_decode("mini2/mini2.tmx")
            tiledtmxloader.ResourceLoaderPyglet().load(world_map)

    def test_load_map_from_sub_dir_pyglet(self):
        if _has_pyglet:
            world_map = tiledtmxloader.TileMapParser().parse_decode("mini2/mini2_alt.tmx")
            tiledtmxloader.ResourceLoaderPyglet().load(world_map)

    def test_load_map_from_sub_dir_using_tsx_from_sub_dir_pyglet(self):
        if _has_pyglet:
            world_map = tiledtmxloader.TileMapParser().parse_decode("mini3/mini3.tmx")
            tiledtmxloader.ResourceLoaderPyglet().load(world_map)

    def test_load_map_from_sub_dir_using_tsx_from_sub_dir_and_img_from_sub_dir_pyglet(self):
        if _has_pyglet:
            world_map = tiledtmxloader.TileMapParser().parse_decode("mini4/mini4.tmx")
            tiledtmxloader.ResourceLoaderPyglet().load(world_map)
            
    def test_can_load_compression_xml_pyglet(self):
        if _has_pyglet:
            world_map = tiledtmxloader.TileMapParser().parse_decode("minix_xml.tmx")
            tiledtmxloader.ResourceLoaderPyglet().load(world_map)

    def test_can_load_compression_cvs_pyglet(self):
        if _has_pyglet:
            world_map = tiledtmxloader.TileMapParser().parse_decode("minix_cvs.tmx")
            tiledtmxloader.ResourceLoaderPyglet().load(world_map)

    def test_can_load_compression_base64_zlib_pyglet(self):
        if _has_pyglet:
            world_map = tiledtmxloader.TileMapParser().parse_decode("minix_base64_zlib.tmx")
            tiledtmxloader.ResourceLoaderPyglet().load(world_map)

    def test_can_load_compression_base64_uncompressed_pyglet(self):
        if _has_pyglet:
            world_map = tiledtmxloader.TileMapParser().parse_decode("minix_base64_uncompressed.tmx")
            tiledtmxloader.ResourceLoaderPyglet().load(world_map)

    def test_can_load_compression_base64_gzip_pyglet(self):
        if _has_pyglet:
            world_map = tiledtmxloader.TileMapParser().parse_decode("minix_base64_gzip.tmx")
            tiledtmxloader.ResourceLoaderPyglet().load(world_map)

    def test_can_load_compression_base64_gzip_dtd_pyglet(self):
        if _has_pyglet:
            world_map = tiledtmxloader.TileMapParser().parse_decode("minix_base64_gzip_dtd.tmx")
            tiledtmxloader.ResourceLoaderPyglet().load(world_map)


if __name__ == '__main__':
    unittest.main()
            