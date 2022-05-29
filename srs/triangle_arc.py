import kivy.clock
import pyglet
import math
import time


class Triangle(object):
    def __init__(self, vertices, vertices_dir=(1, -1, -1)):
        # The vertices of the triangle
        self.vertices = None

        # Set vertices for the first time
        self.set_vertices(vertices)

    def set_vertices(self, vertices):
        # Change the triangles vertices
        self.vertices = pyglet.graphics.vertex_list(3, ('v2f', vertices),
                                                    ('c3B', (100, 200, 220, 200, 100, 160, 200, 100, 250)))


class RotatingTriangle(Triangle):
    def __init__(self, vertices_x: tuple, radius, center=(0, 0)):
        # The radius of the circle the triangle lays upon
        self.radius = radius
        # The center of the triangle
        self.center = center

        # List with coordinates of all vertices
        self.vertices_cords = [vertices_x[0], 0, vertices_x[1], 0, vertices_x[2], 0]
        # Calculate the y coordinates for all the x coordinates
        self.update_y_cords()

        # Create triangle
        super().__init__(vertices=self.vertices_cords)

    def update_y_cords(self):
        # Calculate all y coordinates for the x coordinates of all vertices
        for i in range(0, len(self.vertices_cords), 2):
            self.vertices_cords[i + 1] = self.calc_y(self.vertices_cords[i])
        # Update triangle cords
        self.set_vertices(self.vertices_cords)

    def convert_x(self, x):
        # Remove any offset
        x -= (self.center[0])
        return x

    def calc_y(self, x) -> int:
        # Change x to be relative to center
        x = self.convert_x(x)
        # Calculate y with y = sqrt(r^2-x^1)
        y = round(math.sqrt(math.fabs(self.radius * self.radius - x * x)), 1)
        # Add center offset
        y += self.center[1]
        # Return the y coordinate
        return y

    def rotate(self):
        # Change each x coordinate by 1
        for i in range(0, len(self.vertices_cords), 2):
            # Figure out direction
            x = self.vertices_cords[i]-(self.center[0])
            if self.vertices_cords[i] - self.center[0] < self.radius:
                self.vertices_cords[i] += 1
            else:
                self.vertices_cords[i] = self.center[0]-self.radius


class Window(pyglet.window.Window):
    def __init__(self, debug=False):
        # Call __init__ on superclass as well
        super().__init__()

        # Debug parameter
        self.debug = debug

        # Debug statement
        if self.debug:
            print('DEBUG: Creating window')

        # Configure window size
        self.set_size(900, 480)

        # Create a triangle
        self.triangle = RotatingTriangle(vertices_x=(325.0, 450.0, 665.0), radius=350, center=(450, 100))

        # Set window title
        self.set_caption('Triangle Arc: Practice')

        # Schedule Update event to run every 50ms
        pyglet.clock.schedule_interval(func=self.update, interval=0.01)

    def on_draw(self):
        self.clear()
        self.triangle.vertices.draw(pyglet.graphics.GL_TRIANGLES)

    def update(self, event=None):
        self.triangle.rotate()
        self.triangle.update_y_cords()
        self.on_draw()

def main():
    window = Window()
    window.on_draw()
    pyglet.app.run()


if __name__ == '__main__':
    main()
