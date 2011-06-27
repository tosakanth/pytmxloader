#!/usr/bin/python
# -*- coding: utf-8 -*-

u"""
TileMap loader for python for Tiled, a generic tile map editor
from http://mapeditor.org/ .
It loads the \*.tmx files produced by Tiled.


"""

# Versioning scheme based on: 
# http://en.wikipedia.org/wiki/Versioning#Designating_development_stage
#
#   +-- api change, probably incompatible with older versions
#   |     +-- enhancements but no api change
#   |     |
# major.minor[.build[.revision]]
#                |
#                +-|* 0 for alpha (status)
#                  |* 1 for beta (status)
#                  |* 2 for release candidate
#                  |* 3 for (public) release
#
# For instance:
#     * 1.2.0.1 instead of 1.2-a
#     * 1.2.1.2 instead of 1.2-b2 (beta with some bug fixes)
#     * 1.2.2.3 instead of 1.2-rc (release candidate)
#     * 1.2.3.0 instead of 1.2-r (commercial distribution)
#     * 1.2.3.5 instead of 1.2-r5 (commercial distribution with many bug fixes)
from __future__ import division

__revision__ = "$Rev$"
__version__ = "3.0.0." + __revision__[6:-2]
__author__ = u'DR0ID @ 2009-2011'

if __debug__:
    print __version__
    import sys
    sys.stdout.write(u'%s loading ... \n' % (__name__))
    import time
    _start_time = time.time()

#  -----------------------------------------------------------------------------


import sys
from xml.dom import minidom, Node
import StringIO
import os.path

import pygame

import tiledtmxloader

#  -----------------------------------------------------------------------------

#  -----------------------------------------------------------------------------

class ResourceLoaderPygame(tiledtmxloader.AbstractResourceLoader):
    """
    Resource loader for pygame. Loads the images as Surfaces and saves them in
    the variable indexed_tiles.
    """

    def __init__(self):
        tiledtmxloader.AbstractResourceLoader.__init__(self)

    def _load_image_parts(self, filename, margin, spacing, \
                          tile_width, tile_height, colorkey=None): #-> [images]
        source_img = self._load_image(filename, colorkey)
        width, height = source_img.get_size()
        images = []
        for ypos in xrange(margin, height, tile_height + spacing):
            for xpos in xrange(margin, width, tile_width + spacing):
                img_part = self._load_image_part(filename, xpos, ypos, \
                                            tile_width, tile_height, colorkey)
                images.append(img_part)
        return images

    def _load_image_part(self, filename, xpos, ypos, width, height, \
                                                                colorkey=None):
        """
        Loads a image from a sprite sheet.
        """
        source_img = self._load_image(filename, colorkey)
        ## ISSUE 4:
        ##  The following usage seems to be broken in pygame (1.9.1.):
        ##  img_part = pygame.Surface((tile_width, tile_height), 0, source_img)
        img_part = pygame.Surface((width, height), \
                                    source_img.get_flags(), \
                                    source_img.get_bitsize())
        source_rect = pygame.Rect(xpos, ypos, width, height)

        ## ISSUE 8:
        ## Set the colorkey BEFORE we blit the source_img
        if colorkey:
            img_part.set_colorkey(colorkey, pygame.RLEACCEL)
            img_part.fill(colorkey)

        img_part.blit(source_img, (0, 0), source_rect)

        return img_part

    def _load_image_file_like(self, file_like_obj, colorkey=None): # -> image
        # pygame.image.load can load from a path and from a file-like object
        # that is why here it is redirected to the other method
        return self._load_image(file_like_obj, colorkey)

    def _load_image(self, filename, colorkey=None):
        img = self._img_cache.get(filename, None)
        if img is None:
            img = pygame.image.load(filename)
            self._img_cache[filename] = img
        if colorkey:
            img.set_colorkey(colorkey, pygame.RLEACCEL)
        return img

    # def get_sprites(self):
        # pass



#  -----------------------------------------------------------------------------
#  -----------------------------------------------------------------------------


class SpriteLayer(object):

    class Sprite(object):
        def __init__(self, image, rect, source_rect=None, flags=0, key=None):
            self.image = image
            # TODO: dont use a rect for position
            self.rect = rect # blit rect
            self.source_rect = source_rect
            self.flags = flags
            self.is_flat = False
            self.z = 0
            self.key = key
            
        def get_draw_cond(self):
            if self.is_flat:
                return self.rect.top + self.z
            else:
                return self.rect.bottom

    def __init__(self, tile_layer_idx, resource_loader):
        self._resource_loader = resource_loader
        _world_map = self._resource_loader.world_map
        self.layer_idx = tile_layer_idx
        _layer = _world_map.layers[tile_layer_idx]
        
        self.tilewidth = _world_map.tilewidth
        self.tileheight = _world_map.tileheight
        self.num_tiles_x = _world_map.width
        self.num_tiles_y = _world_map.height
        self.position_x = _layer.x
        self.position_y = _layer.y


        self._level = 1 # start with an invalid level
        
        self.paralax_factor_x = 1.0
        self.paralax_factor_y = 1.0
        self.sprites = []
        self.is_object_group = _layer.is_object_group
        self.visible = _layer.visible
        self.bottom_margin = 0
        self._bottom_margin = 0
        
        
        # init data to default
        # self.content2D = []
        # generate the needed lists
        # for xpos in xrange(self.num_tiles_x):
            # self.content2D.append([None] * self.num_tiles_y)
            
        self.content2D = [None] * self.num_tiles_y
        for ypos in xrange(self.num_tiles_y):
            self.content2D[ypos] = [None] * self.num_tiles_x

        # fill them
        _img_cache = {}
        _img_cache["hits"] = 0
        for ypos_new in xrange(0, self.num_tiles_y):
            for xpos_new in xrange(0, self.num_tiles_x):
                coords = self._get_list_of_neighbour_coord(xpos_new, ypos_new, \
                                        1, self.num_tiles_x, self.num_tiles_y)
                if coords:
                    key, sprites = SpriteLayer._get_sprites_fromt_tiled_layer(\
                            coords, _layer, self._resource_loader.indexed_tiles)

                    sprite = None
                    if sprites:
                        sprite = SpriteLayer._union_sprites(sprites, key, \
                                                                    _img_cache)
                        if sprite.rect.height > self._bottom_margin:
                            self._bottom_margin = sprite.rect.height

                    self.content2D[ypos_new][xpos_new] = sprite
        self.bottom_margin = self._bottom_margin
        if __debug__: 
            print '%s: Sprite Cache hits: %d' % \
                                (self.__class__.__name__, _img_cache["hits"])
        del _img_cache

    def get_collapse_level(self):
        return self._level

    # TODO: test scale
    @staticmethod
    def scale(layer_orig, scale_w, scale_h): # -> sprite_layer
        """
        Scales a layer and returns it.
        
        scale_w, scale_h: float (0, ...]
        """
        layer = SpriteLayer(layer_orig.layer_idx, layer_orig._resource_loader)
        
        layer.tilewidth = layer_orig.tilewidth * scale_w
        layer.tileheight = layer_orig.tileheight * scale_h
        layer.num_tiles_x = layer_orig.width * scale_w
        layer.num_tiles_y = layer_orig.height * scale_h
        layer.position_x = layer_orig.position_x
        layer.position_y = layer_orig.position_y


        layer._level = layer_orig._level
        
        layer.paralax_factor_x = layer_orig.paralax_factor_x
        layer.paralax_factor_y = layer_orig.paralax_factor_y
        layer.sprites = layer_orig.sprites
        layer.is_object_group = layer_orig.is_object_group
        layer.visible = layer_orig.visible
        
        for xidx, row in enumerate(layer_orig.content2D):
            for yidx, sprite in enumerate(row):
                w, h = sprite.image.get_size()
                new_w = w * scale_w
                new_h = h * scale_h
                image = pygame.transform.smoothscale(sprite.image, \
                                                            (new_w, new_h))
                x, y = sprite.rect.topleft
                rect = pygame.Rect(x * scale_w, y * scale_h, new_w, new_h)
                layer.content2D[yidx][xidx] = SpriteLayer.Sprite(image, rect)
                
        return layer

    # TODO: implement merge
    @staticmethod
    def merge(layers): # -> sprite_layer
        raise NotImplementedError

    @staticmethod
    def uncollapse(layer):
        print "uncollapse!"
    
    @staticmethod
    def collapse(layer):

        #   +    0'        1'        2'
        #        0    1    2    3    4
        #   0' 0 +----+----+----+----+
        #        |    |    |    |    |
        #      1 +----+----+----+----+
        #        |    |    |    |    |
        #   1' 2 +----+----+----+----+
        #        |    |    |    |    |
        #      3 +----+----+----+----+
        #        |    |    |    |    |
        #   2' 4 +----+----+----+----+

        level = 2
        if layer.is_object_group:
            return layer
            
        new_tilewidth = layer.tilewidth * level
        new_tileheight = layer.tileheight * level
        new_width = int(layer.num_tiles_x / level)
        new_height = int(layer.num_tiles_y / level)
        if new_width * level < layer.num_tiles_x:
            new_width += 1
        if new_height * level < layer.num_tiles_y:
            new_height += 1

        # print "old size", layer.num_tiles_x, layer.num_tiles_y
        # print "new size", new_width, new_height
        
        _content2D = [None] * new_height
        # generate the needed lists
            
        for ypos in xrange(new_height):
            _content2D[ypos] = [None] * new_width

        # fill them
        _img_cache = {}
        _img_cache["hits"] = 0
        for ypos_new in xrange(0, new_height):
            for xpos_new in xrange(0, new_width):
                coords = SpriteLayer._get_list_of_neighbour_coord(\
                                        xpos_new, ypos_new, level, \
                                        layer.num_tiles_x, layer.num_tiles_y)
                if coords:
                    sprite = SpriteLayer._get_sprite_from(coords, layer, \
                                                                    _img_cache)
                    _content2D[ypos_new][xpos_new] = sprite

        # print "len content2D:", len(self.content2D)
        layer.tilewidth  = new_tilewidth
        layer.tileheight = new_tileheight
        layer.num_tiles_x = new_width
        layer.num_tiles_y = new_height
        layer.content2D = _content2D

        # HACK:
        layer._level *= 2
            
        if __debug__ and level > 1: 
            print '%s: Sprite Cache hits: %d' % ("collapse", _img_cache["hits"])

    @staticmethod
    def _get_list_of_neighbour_coord(xpos_new, ypos_new, level, \
                                                    num_tiles_x, num_tiles_y):
        xpos = xpos_new * level
        ypos = ypos_new * level

        coords = []
        for y in xrange(ypos, ypos + level):
            for x in xrange(xpos, xpos + level):
                if x <= num_tiles_x and y <= num_tiles_y:
                    coords.append((x, y))
        return coords

    @staticmethod
    def _union_sprites(sprites, key, _img_cache):
        key = tuple(key)
        
        # dont copy to a new image if only one sprite is in sprites 
        # (reduce memory usage)
        # NOTE: this messes up the cache hits (only on non-collapsed maps)
        if len(sprites) == 1:
            sprite = sprites[0]
            sprite.key = key
            return sprite
            
        # combine found sprites into one sprite
        rect = sprites[0].rect.unionall(sprites)

        # cache the images to save memory
        if key in _img_cache:
            image = _img_cache[key]
            _img_cache["hits"] = _img_cache["hits"] + 1
        else:
            # make new image
            image = pygame.Surface(rect.size, pygame.SRCALPHA | pygame.RLEACCEL)
            image.fill((0, 0, 0, 0))
            x, y = rect.topleft
            for spr in sprites:
                image.blit(spr.image, spr.rect.move(-x, -y))
                
            _img_cache[key] = image

        return SpriteLayer.Sprite(image, rect, key=key)

    @staticmethod
    def _get_sprites_fromt_tiled_layer(coords, layer, indexed_tiles):
        sprites = []
        key = []
        for xpos, ypos in coords:
            ## ISSUE 14: maps was displayed only sqared because wrong 
            ## boundary checks
            if xpos >= len(layer.content2D) or \
                                ypos >= len(layer.content2D[xpos]):
                # print "CONTINUE", xpos, ypos
                key.append(-1) # border and corner cases!
                continue
            idx = layer.content2D[xpos][ypos]
            if idx:
                offx, offy, img = indexed_tiles[idx]
                world_x = xpos * layer.tilewidth + offx
                world_y = ypos * layer.tileheight + offy
                w, h = img.get_size()
                rect = pygame.Rect(world_x, world_y, w, h)
                sprite = SpriteLayer.Sprite(img, rect, key=idx)
                key.append(idx)
                sprites.append(sprite)
            else:
                key.append(-1)
        return key, sprites

    @staticmethod
    def _get_sprite_from(coords, layer, _img_cache, indexed_tiles=None):
        sprites = []
        key = []
        for xpos, ypos in coords:
            if ypos >= len(layer.content2D) or \
                                    xpos >= len(layer.content2D[ypos]):
                # print "CONTINUE", xpos, ypos
                key.append(-1) # border and corner cases!
                continue
            idx = layer.content2D[ypos][xpos]
            if idx:
                sprite = idx
                key.append(sprite.key)
                sprites.append(sprite)
            else:
                key.append(-1)
        
        if sprites:
            sprite = SpriteLayer._union_sprites(sprites, key, _img_cache)
            
            if __debug__:
                x, y = sprite.rect.topleft
                pygame.draw.rect(sprite.image, (255, 0, 0), \
                                    sprite.rect.move(-x, -y), \
                                    layer.get_collapse_level())
                
            del sprites
            return sprite
            
        return None

    def add_sprite(self, sprite):
        self.sprites.append(sprite)
        if sprite.rect.height > self.bottom_margin:
            self.bottom_margin = sprite.rect.height

    def add_sprites(self, sprites):
        for sprite in sprites:
            self.add_sprite(sprite)

    def remove_sprite(self, sprite):
        if sprite in self.sprites:
            self.sprites.remove(sprite)
        
        self.bottom_margin = self._bottom_margin
        for spr in self.sprites:
            if spr.rect.height > self.bottom_margin:
                self.bottom_margin = spr.rect.height

    def remove_sprites(self, sprites):
        for sprite in sprites:
            self.remove_sprite(sprite)

    def contains_sprite(self, sprite):
        if sprite in self.sprites:
            return True
        return False

    def has_sprites(self):
        return (len(self.sprites) > 0)

    def set_layer_paralax_factor(self, factor_x=1.0, factor_y=None):
        self.paralax_factor_x = factor_x
        if factor_y:
            self.paralax_factor_y = factor_y
        else:
            self.paralax_factor_y = factor_x
        
    def get_layer_paralax_factor_x(self):
        return self.paralax_factor_x

    def get_layer_paralax_factor_y(self):
        return self.paralax_factor_y


class RendererPygame(object):


    def __init__(self, resource_loader):
        self._resource_loader = resource_loader
        self._cam_rect = pygame.Rect(0, 0, 10, 10)
        self._margin = (0, 0, 0, 0) # left, right, top, bottom

    def get_layers_from_map(self):
        layers = []
        for idx, layer in enumerate(self._resource_loader.world_map.layers):
            layers.append(self.get_layer_at_index(idx))
        return layers

    def get_layer_at_index(self, layer_idx):
        layer = self._resource_loader.world_map.layers[layer_idx]
        if layer.is_object_group:
            return layer
        return SpriteLayer(layer_idx, self._resource_loader)

    def set_camera_position(self, world_pos_x, world_pos_y, alignment='center'):
        setattr(self._cam_rect, alignment, (world_pos_x, world_pos_y))
        self._render_cam_rect.center = self._cam_rect.center
        
    def set_camera_position_and_size(self, world_pos_x, world_pos_y, \
                                   width, height, alignment='center'):
        self._cam_rect.width = width
        self._cam_rect.height = height
        setattr(self._cam_rect, alignment, (world_pos_x, world_pos_y))
        self.set_camera_margin(*self._margin)
        
    def set_camera_rect(self, cam_rect_world_coord):
        self._cam_rect = cam_rect_world_coord
        self.set_camera_margin(*self._margin)
        
    def set_camera_margin(self, margin_left, margin_right, margin_top, margin_bottom):
        """
        Set the margin around the camera (in pixels).
        
        :Parameters:
            margin_left : int
                number of pixels of the left side marging
            margin_right : int
                number of pixels of the right side marging
            margin_top : int
                number of pixels of the top side marging
            margin_bottom : int
                number of pixels of the left bottom marging
        
        """
        self._margin = (margin_left, margin_right, margin_top, margin_bottom)
        self._render_cam_rect = pygame.Rect(self._cam_rect)
        # adjust left margin
        self._render_cam_rect.left = self._render_cam_rect.left - margin_left
        # adjust right margin
        self._render_cam_rect.width = self._render_cam_rect.width + margin_left + margin_right
        # adjust top margin
        self._render_cam_rect.top = self._render_cam_rect.top - margin_top
        # adjust bottom margin
        self._render_cam_rect.height = self._render_cam_rect.height + margin_top + margin_bottom
        

    def render_layer(self, surf, layer, clip_sprites=True, \
                                    sort_key=lambda spr: spr.get_draw_cond()):
        """
        Renders a layer onto the given surface.
        
        :Parameters:
            surf : Surface
                Surface to render onto.
            layer : SpriteLayer
                The layer to render. Invisible layers will be skipped.
            clip_sprites : boolean
                Clip the sprites of this layer to only draw the ones
                intersecting the visible part of the world.
            sort_key : function
                The sort function for the parameter 'key' of the sort 
                method of the list.
        
        """
        if layer.visible:

            if layer.is_object_group:
                return

            if layer.bottom_margin > self._margin[3]:
                left, right, top, bottom = self._margin
                self.set_camera_margin(left, right, top, layer.bottom_margin)

            # optimizations
            surf_blit = surf.blit
            layer_content2D = layer.content2D

            tile_h = layer.tileheight

                        # self.paralax_factor_y = 1.0
            # self.paralax_center_x = 0.0
            cam_rect = self._render_cam_rect
            # print 'cam rect:', self._cam_rect
            # print 'render r:', self._render_cam_rect

            cam_world_pos_x = cam_rect.x * layer.paralax_factor_x + \
                                                                layer.position_x
            cam_world_pos_y = cam_rect.y * layer.paralax_factor_y + \
                                                                layer.position_y

            # camera bounds, restricting number of tiles to draw
            left = int(round(float(cam_world_pos_x) // layer.tilewidth))
            right = int(round(float(cam_world_pos_x + cam_rect.width) // \
                                            layer.tilewidth)) + 1
            top = int(round(float(cam_world_pos_y) // tile_h))
            bottom = int(round(float(cam_world_pos_y + cam_rect.height) // \
                                            tile_h)) + 1

            left = left if left > 0 else 0
            right = right if right < layer.num_tiles_x else layer.num_tiles_x
            top = top if top > 0 else 0
            bottom = bottom if bottom < layer.num_tiles_y else layer.num_tiles_y
            
            # print '???', layer.num_tiles_x, layer.num_tiles_y, left, right, top, bottom, cam_rect

            # sprites
            spr_idx = 0
            len_sprites = 0
            all_sprites = layer.sprites
            if all_sprites:
                # TODO: make filter visible sprites optional (maybe sorting too)
                # use a marging around it
                if clip_sprites:
                    sprites = [all_sprites[idx] \
                                for idx in cam_rect.collidelistall(all_sprites)]
                else:
                    sprites = all_sprites

                # could happend that all sprites are not visible by the camera
                if sprites:
                    if sort_key:
                        sprites.sort(key=sort_key)
                    sprite = sprites[0]
                    len_sprites = len(sprites)
                     

            # render
            for ypos in range(top, bottom):
                # draw sprites in this layer 
                # (skip the ones outside visible area/map)
                y = ypos + 1
                while spr_idx < len_sprites and sprite.get_draw_cond() <= \
                                                                    y * tile_h:
                    surf_blit(sprite.image, \
                                sprite.rect.move(-cam_world_pos_x, \
                                                 -cam_world_pos_y - sprite.z),\
                                sprite.source_rect, \
                                sprite.flags)
                    spr_idx += 1
                    if spr_idx < len_sprites:
                        sprite = sprites[spr_idx]
                # next line of the map
                for xpos in range(left, right):
                    tile_sprite = layer_content2D[ypos][xpos]
                    # print '?', xpos, ypos, tile_sprite
                    if tile_sprite:
                        surf_blit(tile_sprite.image, \
                                    tile_sprite.rect.move( - cam_world_pos_x, \
                                                           -cam_world_pos_y), \
                                    tile_sprite.source_rect, \
                                    tile_sprite.flags)

#  -----------------------------------------------------------------------------

class Dude(SpriteLayer.Sprite):

    def __init__(self, img, rect):
        super(Dude, self).__init__(img, rect)
        self.random = __import__('random')
        self.velocity_x = 0
        self.velocity_y = 0
        self.position_x = self.random.randint(100, 4000)
        self.position_y = self.random.randint(100, 4000)
        self.rect.center = (self.position_x, self.position_y)

    def update(self, dt):
        if self.random.random() < 0.05:
            if self.velocity_x:
                self.velocity_x = 0
                self.velocity_y = 0
            else:
                self.velocity_x = self.random.randint(-10, 10) * 0.005
                self.velocity_y = self.random.randint(-10, 10) * 0.005
        self.position_x += self.velocity_x * dt
        self.position_y += self.velocity_y * dt
        self.rect.center = (self.position_x, self.position_y)



def demo_pygame(file_name):

    # parser the map (it is done here to initialize the 
    # window the same size as the map if it is small enough)
    world_map = tiledtmxloader.TileMapParser().parse_decode(file_name)

    # init pygame and set up a screen
    pygame.init()
    pygame.display.set_caption("tiledtmxloader - " + file_name)
    screen_width = min(1024, world_map.pixel_width)
    screen_height = min(768, world_map.pixel_height)
    screen = pygame.display.set_mode((screen_width, screen_height))

    # load the images using pygame
    # image_loader = ImageLoaderPygame()
    resources = ResourceLoaderPygame()
    resources.load(world_map)
    #printer(world_map)

    # prepare map rendering
    assert world_map.orientation == "orthogonal"
    renderer = RendererPygame(resources)

    # cam_offset is for scrolling
    cam_world_pos_x = 0
    cam_world_pos_y = 0

    # variables
    frames_per_sec = 60.0
    clock = pygame.time.Clock()
    running = True
    draw_obj = True
    show_message = True
    font = pygame.font.Font(None, 15)
    s = "Frames Per Second: 0.0"
    message = font.render(s, 0, (255,255,255), (0, 0, 0)).convert()

    # for timed fps update
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    # add additional sprites
    num_sprites = 1000
    my_sprites = []
    for i in range(num_sprites):
        j = num_sprites - i
        # image = pygame.Surface((20, j*40.0/num_sprites+10))
        image = pygame.Surface((50, 70), pygame.SRCALPHA)
        image.fill(((255+200*j)%255, (2*j+255)%255, (5*j)%255, 200))
        # image.fill((255, 255, 255))
        # sprite = RendererPygame.Sprite(image, image.get_rect())
        sprite = Dude(image, image.get_rect())
        my_sprites.append(sprite)
    my_sprites[-1].z = 10
    # renderer.add_sprites(1, my_sprites)

    clip_sprites = True
    hero_flat = False

    # optimizations
    num_keys = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, \
                    pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]
    pressed_layer = None
    clock_tick = clock.tick
    pygame_event_get = pygame.event.get
    pygame_key_get_pressed = pygame.key.get_pressed
    renderer_render_layer = renderer.render_layer
    renderer_set_camera_position = renderer.set_camera_position
    pygame_display_flip = pygame.display.flip
    sprite_layers = renderer.get_layers_from_map()
    renderer.set_camera_position_and_size(cam_world_pos_x, cam_world_pos_y, \
                                        screen_width, screen_height)

    t = 0

    # mainloop
    while running:
        dt = clock_tick()#60.0)
        t += dt

        # event handling
        for event in pygame_event_get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYUP:
                if event.key in num_keys:
                    pressed_layer = None
                    print "reset pressed layer", pressed_layer
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_F1:
                    print "fps:", clock.get_fps()
                    show_message = not show_message
                    print "show info:", show_message
                    # print "visible range x:", renderer._visible_x_range
                    # print "visible range y:", renderer._visible_y_range
                elif event.key == pygame.K_F2:
                    draw_obj = not draw_obj
                    print "show objects:", draw_obj
                elif event.key == pygame.K_F3:
                    clip_sprites = not clip_sprites
                    print "clip sprites:", clip_sprites
                elif event.key == pygame.K_F4:
                    hero_flat = not hero_flat
                    print "hero is flat:", hero_flat
                elif event.key == pygame.K_w:
                    cam_world_pos_y -= world_map.tileheight
                elif event.key == pygame.K_s:
                    cam_world_pos_y += world_map.tileheight
                elif event.key == pygame.K_d:
                    cam_world_pos_x += world_map.tilewidth
                elif event.key == pygame.K_a:
                    cam_world_pos_x -= world_map.tilewidth
                elif event.key in num_keys:
                    # find out which layer to manipulate
                    idx = num_keys.index(event.key)
                    # make sure this layer exists
                    if idx < len(world_map.layers):
                        pressed_layer = idx
                        print "set pressed layer", pressed_layer
                        if event.mod & pygame.KMOD_CTRL:
                            # uncollapse
                            # TODO: better interface
                            render_layer = sprite_layers[idx]
                            SpriteLayer.collapse(render_layer)
                            print "layer has uncollapsed, level:", \
                                               render_layer.get_collapse_level()
                        elif event.mod & pygame.KMOD_SHIFT:
                            # collapse
                            # TODO: better interface
                            render_layer = sprite_layers[idx]
                            sprite_layers[idx] = \
                                                renderer.get_layer_at_index(idx)
                            print "layer", idx, "RESET!"
                        elif event.mod & pygame.KMOD_ALT:
                            # hero sprites
                            # TODO: better interface
                            if sprite_layers[idx].contains_sprite(\
                                                            my_sprites[0]):
                                # renderer.remove_sprites(idx, my_sprites)
                                # TODO: better interface
                                sprite_layers[idx].remove_sprites(my_sprites)
                                print "removed hero sprites from layer", idx
                            else:
                                # renderer.add_sprites(idx, my_sprites)
                                # TODO: better interface
                                sprite_layers[idx].add_sprites(my_sprites)
                                print "added hero sprites to layer", idx
                        else:
                            # visibility
                            sprite_layers[idx].visible = \
                                                not sprite_layers[idx].visible
                            print "layer", idx, "visible:", \
                                                    sprite_layers[idx].visible
                    else:
                        print "layer", idx, " does not exist on this map!"
                elif event.key == pygame.K_UP:
                    if pressed_layer is not None:
                        # TODO: better interface
                        layer = renderer._layers[\
                                                world_map.layers[pressed_layer]]
                        layer.set_layer_paralax_factor(\
                                       layer.get_layer_paralax_factor_x() + 0.1)
                        print "increase paralax factox on layer", \
                                pressed_layer, " to:", \
                                layer.get_layer_paralax_factor_x()
                elif event.key == pygame.K_DOWN:
                    if pressed_layer is not None:
                        layer = renderer._layers[\
                                                world_map.layers[pressed_layer]]
                        layer.set_layer_paralax_factor(\
                                       layer.get_layer_paralax_factor_x() - 0.1)
                        print "reduced paralax factox on layer", pressed_layer,\
                                    " to:", layer.get_layer_paralax_factor_x()
                    
            elif event.type == pygame.USEREVENT:
                t = 0
                print clock.get_fps()

                if show_message:
                    s = "Number of layers: %i (use 0-9 to toggle)   F1-F2 for \
                                    other functions Frames Per Second: %.2f" % \
                                    (len(world_map.layers), clock.get_fps())
                    message = font.render(  s, \
                                            0, \
                                            (255, 255, 255), \
                                            (0, 0, 0)).convert()


        if pressed_layer is None:
            pressed = pygame_key_get_pressed()
            # The speed is 3 by default.
            # When left Shift is held, the speed increases.
            # The speed interpolates based on time passed, so the demo navigates
            # at a reasonable pace even on huge maps.
            speed = (3.0 + pressed[pygame.K_LSHIFT] * 36.0) * \
                                                        (dt / frames_per_sec)

            # cam movement
            if pressed[pygame.K_DOWN]:
                cam_world_pos_y += speed
            if pressed[pygame.K_UP]:
                cam_world_pos_y -= speed
            if pressed[pygame.K_LEFT]:
                cam_world_pos_x -= speed
            if pressed[pygame.K_RIGHT]:
                cam_world_pos_x += speed

        # update sprites position
        for spr in my_sprites:
            spr.update(dt)
        my_sprites[0].is_flat = hero_flat
        my_sprites[-1].is_flat = hero_flat
        my_sprites[0].rect.center = cam_world_pos_x , cam_world_pos_y
        my_sprites[-1].rect.center = cam_world_pos_x + 20 , cam_world_pos_y

        # adjust camera according the keypresses
        renderer_set_camera_position(cam_world_pos_x, cam_world_pos_y)

        # clear screen, might be left out if every pixel is redrawn anyway
        screen.fill((0,0,0))

        # render the map
        # TODO: manage render layers
        for sprite_layer in sprite_layers:
            if sprite_layer.is_object_group:
                # map objects
                if draw_obj:
                    _draw_obj_group(screen, sprite_layer, cam_world_pos_x, \
                                                        cam_world_pos_y, font)
            else:
                renderer_render_layer(screen, sprite_layer, clip_sprites)


        if show_message:
            screen.blit(message, (0,0))

        pygame_display_flip()

def _draw_obj_group(screen, obj_group, cam_world_pos_x, cam_world_pos_y, font):
    pygame = __import__('pygame')
    goffx = obj_group.x
    goffy = obj_group.y
    for map_obj in obj_group.objects:
        size = (map_obj.width, map_obj.height)
        if map_obj.image_source:
            surf = pygame.image.load(map_obj.image_source)
            surf = pygame.transform.scale(surf, size)
            screen.blit(surf, (goffx + map_obj.x - cam_world_pos_x, \
                                goffy + map_obj.y - cam_world_pos_y))
        else:
            r = pygame.Rect(\
                        (goffx + map_obj.x - cam_world_pos_x, \
                         goffy + map_obj.y - cam_world_pos_y),\
                         size)
            pygame.draw.rect(screen, (255, 255, 0), r, 1)
            text_img = font.render(map_obj.name, 1, (255, 255, 0))
            screen.blit(text_img, r.move(1, 2))
    
#  -----------------------------------------------------------------------------
# TODO:
 # - pyglet demo: redo same as for pygame demo, better rendering
 # - test if object gid is already read in and resolved


#  -----------------------------------------------------------------------------



#  -----------------------------------------------------------------------------
def main():

    args = sys.argv[1:]
    if len(args) < 1:
        #print 'usage: python test.py mapfile.tmx [pygame|pyglet]'
        print('usage: python %s your_map.tmx' % \
            os.path.basename(__file__))
        return

    demo_pygame(args[0])

#  -----------------------------------------------------------------------------

if __name__ == '__main__':
    # import cProfile
    # cProfile.run('main()', "stats.profile")
    # import pstats
    # p = pstats.Stats("stats.profile")
    # p.strip_dirs()
    # p.sort_stats('time')
    # p.print_stats()

    main()


if __debug__:
    _dt = time.time() - _start_time
    sys.stdout.write(u'%s loaded: %fs \n' % (__name__, _dt))