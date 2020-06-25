import math

"""
    My solution to https://py.checkio.org/mission/four-to-the-floor/publications/ZweiStein/python-3/perimeter-point-scan/
"""

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # check if point is inside rectangle
    def inside_rectangle(self, rectangle):
        if (self.x <= rectangle.width and self.x >= 0 and
                self.y <= rectangle.height and self.y >= 0):                 
            return True
        else:            
            return False


class Circle:
    
    TIMES_360 = 10 # Adjust how many perimeter points to check for each circle
    ITERATION_STEPS = 1 # Step size for loop
    ITERATIONS = TIMES_360 * 360
    DIVISOR = ITERATIONS / 360

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    # creates a point at the perimeter of the circle at a given degree.
    def deg_to_point(self, deg):

        px = (math.cos(math.radians(deg)) * self.radius) + self.x
        py = (math.sin(math.radians(deg)) * self.radius) + self.y
        #print(f"{px},{py}")
        return Point(px, py)
    
    # distance between circle and point
    def distance(self, point):
        delta_x = self.x - point.x
        delta_y = self.y - point.y
        return math.hypot(delta_x, delta_y)

    # is point inside the circle
    def point_in_circle(self, point):
        if self.distance(point) > self.radius:
            return False
        else:
            return True

    """
        inputs: 
            - list of circles
            - rectangle

            returns True if  All points in circle perimeter is intersecting at least one other circle or is outside rectangle.
            returns False if a  point is found inside rectangle but is not intersecting with any other circle.
    """
    def perimeter_loop(self, circles, rectangle):
        for deg in range(0, Circle.ITERATIONS, Circle.ITERATION_STEPS):
            deg = deg / Circle.DIVISOR
            point = self.deg_to_point(deg)
            if not point.inside_rectangle(rectangle):
                continue
            count_not_in = 0
            for c in circles:
                if c == self:
                    continue
                if not c.point_in_circle(point):
                    count_not_in += 1
                
                if count_not_in >= len(circles) - 1:                   
                    return False # Point inside rectangle but is not intersecting with any other circle.
        return True # All points in circle perimeter is intersecting at least one other circle or is outside rectangle.

        


"""
    Rectangle drawn from position 0.0 (lower left corner)
"""
class Rectangle:

    def __init__(self, width, height):
        self.height = height
        self.width = width


"""
    Check if a rooms area is totally covered by the input circular sensors.

    inputs:
    room:   [width, height]
    sensors: [[x0, y0, radius0],...[xn, yn, radiusn] ]

    returns True if the sensor circles covers the whole room area
    else False
"""

def is_covered(room, sensors):
    circles = []
    rectangle = Rectangle(room[0], room[1])
    for s in sensors:
        circles.append(Circle(s[0], s[1], s[2]))
    
    for c in circles:
        is_intersecting = c.perimeter_loop(circles, rectangle)
        if not is_intersecting:            
            return False
    
    return True


"""
    Unit tests provided by checkio:
"""

if __name__ == '__main__':
    print("Example:")
    print(is_covered([200, 150], [[100, 75, 130]]))

    # These "asserts" are used for self-checking and not for an auto-testing
    assert is_covered([200, 150], [[100, 75, 130]]) == True
    assert is_covered([200, 150], [[50, 75, 100], [150, 75, 100]]) == True
    assert is_covered([200, 150], [[50, 75, 100], [
                      150, 25, 50], [150, 125, 50]]) == False
    assert is_covered([200, 150], [[100, 75, 100], [0, 40, 60], [
                      0, 110, 60], [200, 40, 60], [200, 110, 60]]) == True
    assert is_covered([200, 150], [[100, 75, 100], [0, 40, 50], [
                      0, 110, 50], [200, 40, 50], [200, 110, 50]]) == False
    assert is_covered([200, 150], [[100, 75, 110], [105, 75, 110]]) == False
    assert is_covered([200, 150], [[100, 75, 110], [105, 75, 20]]) == False
    assert is_covered([3, 1], [[1, 0, 2], [2, 1, 2]]) == True
    assert is_covered([30, 10], [[0, 10, 10], [10, 0, 10],
                                 [20, 10, 10], [30, 0, 10]]) == True
    assert is_covered([30, 10], [[0, 10, 8], [10, 0, 7],
                                 [20, 10, 9], [30, 0, 10]]) == False
    print("All tests passed!")