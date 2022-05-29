import pyglet
import math
import time


class Triangle(object):
    def __init__(self, vertices, vertices_dir=(1, -1, -1)):
        # The vertices of the triangle
        self.vertices = None

        # Set vertices for the first time
        self.set_vertices(vertices)
        print(vertices)

    def set_vertices(self, vertices):
        # Change the triangles vertices
        self.vertices = pyglet.graphics.vertex_list(3, ('v2f', vertices),
                                                    ('c3B', (100, 200, 220, 200, 100, 160, 200, 100, 250)))

    """
    def rotate(self, radius=100, offset=(0, 0)):
        # y = sqrt(r^2-x^1)

        for i in range(0, len(self.vertices_x)):
            if self.vertices_x[i] - offset[0] > -radius and self.vertices_dir[i] == -1:
                self.vertices_x[i] -= 1 - 0
            elif self.vertices_x[i] - offset[0] <= -radius and self.vertices_dir[i] == -1:
                self.vertices_x[i] += 1.0
                self.vertices_dir[i] = -1
            if self.vertices_x[i] - offset[0] < radius and self.vertices_dir[i] == 1:
                self.vertices_x[i] += 1.0
            elif self.vertices_x[i] - offset[0] >= radius and self.vertices_dir[i] == 1:
                self.vertices_x[i] -= 1.0
                self.vertices_dir[i] = 1

        # Corresponding y vertices to the x vertices
        vertices_y = list()
        for x in self.vertices_x:
            x -= offset[0]
            vertices_y.append(round(math.sqrt(math.fabs(radius * radius - x * x + offset[1])), 1))

        self.set_vertices((self.vertices_x[0], vertices_y[0],
                           self.vertices_x[1], vertices_y[1],
                           self.vertices_x[2], vertices_y[2]))"""


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

    def calc_y(self, x):
        # Change x to be relative to center
        x -= self.center[1]
        # Calculate y with y = sqrt(r^2-x^1)
        y = round(math.sqrt(math.fabs(self.radius * self.radius - x * x + self.center[1])), 1)
        # Return the y coordinates
        return y


class Window(pyglet.window.Window):
    def __init__(self, debug=False):
        # Call __init__ on superclass as well
        super().__init__()

        # Debug parameter
        self.debug = debug

        # Configure window size
        self.set_size(900, 480)

        # Create a triangle
        self.triangle = RotatingTriangle(vertices_x=(320.0, 450.0, 670.0), radius=150, center=(450, 240))

        # Set window title
        self.set_caption('Triangle: Practice')

    def on_draw(self):
        self.clear()
        self.triangle.vertices.draw(pyglet.graphics.GL_TRIANGLES)

    def on_key_press(self, symbol, modifiers):
        # Rotate triangles on key press 'r'
        if symbol == pyglet.window.key.R:
            #self.triangle.rotate(radius=250, offset=(200, 190))
            pass

def main():
    window = Window()
    window.on_draw()
    pyglet.app.run()


if __name__ == '__main__':
    main()
