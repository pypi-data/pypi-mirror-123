import pygame
import typing

import FangEngine.game_object.game_object as game_object


class BaseLayer(game_object.GameObject):
    """
    This object allows many objects to be grouped together and move with each other as one large object
    """
    def __init__(self, screen_parent, x: float, y: float, *args, **kwargs):
        super().__init__(screen_parent, x, y, *args, **kwargs)

        self.game_objects = []              # type: typing.List[game_object.GameObject]

        self.parallax_x = 1
        self.parallax_y = 1

        self.camera.move_callbacks.append(self.move)

    def set_parallax(self, x: float = 1, y: float = 1):
        """
        Sets the parallax factor for this layer.
        Higher factors make the layer move faster than lower factors.
        A value of 0 will cause no movement at all.
        A value of 1 will cause the elements of the layer to move normally
        The higher the parallax factor, the closer the layer can appear to the player.
        """
        self.parallax_x = x
        self.parallax_y = y

    def clear_game_objects(self):
        """
        Removes all game objects from the screen
        """
        self.game_objects.clear()

    def spawn_object(
            self, object_class_ref: 'game_object.GameObject.__class__', x: float, y: float, *args, **kwargs
    ) -> 'game_object.GameObject':
        """
        Spawns a new game object
        :param object_class_ref: the reference to the class. The class MUST extend the GameObject class
        :param x:
        :param y:
        :param args:
        :param kwargs:
        """
        obj = object_class_ref(self, x, y, *args, **kwargs)     # type: game_object.GameObject
        obj.on_create(*args, **kwargs)

        self.game_objects.append(obj)
        return obj

    def on_move(self, dx: float, dy: float):
        super().on_move(dx, dy)

        dx *= self.parallax_x
        dy *= self.parallax_y

        for child in self.game_objects:
            child.x += dx
            child.y += dy
            child.on_move(dx, dy)

    def check_collisions(self, child: 'game_object.GameObject'):
        """
        This method checks if the specified object is colliding with any other game object
        """
        for c in self.game_objects:
            if c == child:
                continue

            if not c.visible:
                continue

            if c.hitbox.is_hitbox_colliding(child.hitbox):
                child.on_collide(c)
                c.on_collide(child)

    def convert_coords(self, x: float, y: float) -> typing.Tuple[float, float]:
        # x, y = super().convert_coords(x, y)
        # return x * self.parallax_x, y * self.parallax_y
        return x, y

    def handle_input(self, keys: list, mouse: tuple, delta_t: float):
        for child in self.game_objects:
            child.handle_input(keys, mouse, delta_t)

    def update(self, delta_t: float):
        for child in self.game_objects:
            child.update(delta_t)

    def render(self, buffer: pygame.Surface):
        for child in self.game_objects:
            child.render(buffer)

    def on_key_down(self, unicode, key, mod):
        for child in self.game_objects:
            child.on_key_down(unicode, key, mod)

    def on_key_up(self, key, mod):
        for child in self.game_objects:
            child.on_key_up(key, mod)

    def on_mouse_motion(self, pos, rel, buttons):
        for child in self.game_objects:
            child.on_mouse_motion(pos, rel, buttons)

    def on_mouse_button_up(self, pos, button):
        for child in self.game_objects:
            child.on_mouse_button_up(pos, button)

    def on_mouse_button_down(self, pos, button):
        obj = self.game_objects[:]
        obj.reverse()

        for child in obj:
            child.on_mouse_button_down(pos, button)

            if child.hitbox.is_point_colliding(*pos):
                if child.on_click(pos, button) is not True:
                    break

    def on_joystick_axis_motion(self, joystick, axis, value):
        for child in self.game_objects:
            child.on_joystick_axis_motion(joystick, axis, value)

    def on_joystick_ball_motion(self, joystick, ball, rel):
        for child in self.game_objects:
            child.on_joystick_ball_motion(joystick, ball, rel)

    def on_joystick_hat_motion(self, joystick, hat, value):
        for child in self.game_objects:
            child.on_joystick_hat_motion(joystick, hat, value)

    def on_joystick_button_up(self, joystick, button):
        for child in self.game_objects:
            child.on_joystick_button_up(joystick, button)

    def on_joystick_button_down(self, joystick, button):
        for child in self.game_objects:
            child.on_joystick_button_down(joystick, button)

    def on_screen_enter(self, previous_screen: str):
        for child in self.game_objects:
            child.on_screen_enter(previous_screen)

    def on_screen_leave(self, next_screen: str):
        for child in self.game_objects:
            child.on_screen_leave(next_screen)

    def broadcast_message(self, message: typing.Union[list, tuple, str], sender=None):
        """
        Broadcasts a message to all objects in this screen
        :param message:
        :param sender: default is this object
        """
        if sender is None:
            sender = self

        for child in self.game_objects:
            child.on_message_receive(message, sender)

        super(BaseLayer, self).broadcast_message(message)
