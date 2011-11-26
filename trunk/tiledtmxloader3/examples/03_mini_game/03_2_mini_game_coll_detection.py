#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

This is the pygame minimal example.

"""
from __future__ import division

__revision__ = "$Rev: 82 $"
__version__ = "3.0.0." + __revision__[6:-2]
__author__ = u'DR0ID @ 2009-2011'


#  -----------------------------------------------------------------------------


import pygame

import tiledtmxloader



def demo_pygame(file_name):

    class Dude(tiledtmxloader.helperspygame.SpriteLayer.Sprite):

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



    # parser the map (it is done here to initialize the
    # window the same size as the map if it is small enough)
    world_map = tiledtmxloader.tmxreader.TileMapParser().parse_decode(file_name)

    # init pygame and set up a screen
    pygame.init()
    pygame.display.set_caption("tiledtmxloader - " + file_name)
    screen_width = min(1024, world_map.pixel_width)
    screen_height = min(768, world_map.pixel_height)
    screen = pygame.display.set_mode((screen_width, screen_height))

    # load the images using pygame
    # image_loader = ImageLoaderPygame()
    resources = tiledtmxloader.helperspygame.ResourceLoaderPygame()
    resources.load(world_map)
    #printer(world_map)

    # prepare map rendering
    assert world_map.orientation == "orthogonal"
    renderer = tiledtmxloader.helperspygame.RendererPygame()

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
    num_sprites = 4
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
    sprite_layers = tiledtmxloader.helperspygame.get_layers_from_map(resources)
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
                            render_layer = SpriteLayer.collapse(render_layer)
                            sprite_layers[idx] = render_layer
                            print "layer has uncollapsed, level:", \
                                               render_layer.get_collapse_level()
                        elif event.mod & pygame.KMOD_SHIFT:
                            # collapse
                            # TODO: better interface
                            render_layer = sprite_layers[idx]
                            sprite_layers[idx] = \
                                                renderer.get_layer_at_index(idx, resources)
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
                        layer = sprite_layers[pressed_layer]
                        layer.set_layer_paralax_factor(\
                                       layer.get_layer_paralax_factor_x() + 0.1)
                        print "increase paralax factox on layer", \
                                pressed_layer, " to:", \
                                layer.get_layer_paralax_factor_x()
                elif event.key == pygame.K_DOWN:
                    if pressed_layer is not None:
                        layer = sprite_layers[pressed_layer]
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

        sprites = []
        for layer in sprite_layers:
            spr = renderer.pick_layer(layer, *pygame.mouse.get_pos())
            if spr:
                sprites.insert(0, spr)
        for idx, spr in enumerate(sprites):
            dud = my_sprites[2]
            dud.rect.topleft = spr.rect.topleft

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

        # print '??', len(sprites)
        for idx, spr in enumerate(sprites):
            screen.blit(spr.image, (idx * spr.rect.w, screen.get_size()[1] - spr.rect.h))
            # print '>>>>>', dud.rect.topleft


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
    import sys
    import os.path

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


