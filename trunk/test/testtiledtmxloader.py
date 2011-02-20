#!/usr/bin/python
# -*- coding: utf-8 -*-


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
        
    def test_load_map_from_cur_dir_pygame(self):
        if _has_pygame:
            world_map = tiledtmxloader.TileMapParser().parse_decode("minix.tmx")
            world_map.load(tiledtmxloader.ImageLoaderPygame())

    def test_load_map_from_cur_dir_pyglet(self):
        if _has_pyglet:
            world_map = tiledtmxloader.TileMapParser().parse_decode("minix.tmx")
            world_map.load(tiledtmxloader.ImageLoaderPyglet())
        
    def test_load_map_from_cur_dir_using_tsx_pygame(self):
        if _has_pygame:
            world_map = tiledtmxloader.TileMapParser().parse_decode("minix_using_tsx.tmx")
            world_map.load(tiledtmxloader.ImageLoaderPygame())

    def test_load_map_from_cur_dir_using_tsx_pyglet(self):
        if _has_pyglet:
            world_map = tiledtmxloader.TileMapParser().parse_decode("minix_using_tsx.tmx")
            world_map.load(tiledtmxloader.ImageLoaderPyglet())

    def test_load_map_from_sub_dir_using_tsx_pygame(self):
        if _has_pygame:
            world_map = tiledtmxloader.TileMapParser().parse_decode("mini2/mini2.tmx")
            world_map.load(tiledtmxloader.ImageLoaderPygame())

    def test_load_map_from_sub_dir_using_tsx_pyglet(self):
        if _has_pyglet:
            world_map = tiledtmxloader.TileMapParser().parse_decode("mini2/mini2.tmx")
            world_map.load(tiledtmxloader.ImageLoaderPyglet())

    def test_load_map_from_sub_dir_pygame(self):
        if _has_pygame:
            world_map = tiledtmxloader.TileMapParser().parse_decode("mini2/mini2_alt.tmx")
            world_map.load(tiledtmxloader.ImageLoaderPygame())

    def test_load_map_from_sub_dir_pyglet(self):
        if _has_pyglet:
            world_map = tiledtmxloader.TileMapParser().parse_decode("mini2/mini2_alt.tmx")
            world_map.load(tiledtmxloader.ImageLoaderPyglet())

    def test_load_map_from_sub_dir_using_tsx_from_sub_dir_pygame(self):
        if _has_pygame:
            world_map = tiledtmxloader.TileMapParser().parse_decode("mini3/mini3.tmx")
            world_map.load(tiledtmxloader.ImageLoaderPygame())

    def test_load_map_from_sub_dir_using_tsx_from_sub_dir_pyglet(self):
        if _has_pyglet:
            world_map = tiledtmxloader.TileMapParser().parse_decode("mini3/mini3.tmx")
            world_map.load(tiledtmxloader.ImageLoaderPyglet())

    def test_load_map_from_sub_dir_using_tsx_from_sub_dir_and_img_from_sub_dir_pygame(self):
        if _has_pygame:
            world_map = tiledtmxloader.TileMapParser().parse_decode("mini4/mini4.tmx")
            world_map.load(tiledtmxloader.ImageLoaderPygame())

    def test_load_map_from_sub_dir_using_tsx_from_sub_dir_and_img_from_sub_dir_pyglet(self):
        if _has_pyglet:
            world_map = tiledtmxloader.TileMapParser().parse_decode("mini4/mini4.tmx")
            world_map.load(tiledtmxloader.ImageLoaderPyglet())