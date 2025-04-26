"""
Module containing geometric shape classes with inheritance, polymorphism, and abstraction.
"""

from abc import ABC, abstractmethod
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle as MplRectangle, Circle, Polygon

class Color:
    """Represents a color with validation."""
    
    def __init__(self, color: str):
        self._color = color.lower()
    
    @property
    def color(self) -> str:
        """Get the color name."""
        return self._color
    
    @color.setter
    def color(self, value: str):
        """Set the color name with basic validation."""
        if not isinstance(value, str) or len(value) < 3:
            raise ValueError("Invalid color format")
        self._color = value.lower()

class GeometricShape(ABC):
    """Abstract base class for geometric shapes."""
    
    @abstractmethod
    def area(self) -> float:
        """Calculate the area of the shape."""
        pass
    
    @classmethod
    def shape_name(cls) -> str:
        """Get the shape's display name."""
        return cls.__name__

class Rectangle(GeometricShape):
    """Rectangle shape with width, height, and color."""
    
    SHAPE_NAME = "Rectangle"  # Static attribute
    
    def __init__(self, width: float, height: float, color: str):
        self._width = width
        self._height = height
        self.color = Color(color)  # Composition
        
    @property
    def width(self) -> float:
        return self._width
    
    @width.setter
    def width(self, value: float):
        if value <= 0:
            raise ValueError("Width must be positive")
        self._width = value
        
    @property
    def height(self) -> float:
        return self._height
    
    @height.setter
    def height(self, value: float):
        if value <= 0:
            raise ValueError("Height must be positive")
        self._height = value
    
    def area(self) -> float:
        return self._width * self._height
    
    def get_info(self) -> str:
        """Return formatted shape information."""
        return "Shape: {name}\nColor: {color}\nArea: {area:.2f}".format(
            name=self.SHAPE_NAME,
            color=self.color.color,
            area=self.area()
        )
    
    def draw(self, label: str = "", filename: str = ""):
        """Draw the shape using matplotlib."""
        fig, ax = plt.subplots()
        rect = MplRectangle((0.1, 0.1), self.width, self.height, 
                          facecolor=self.color.color, edgecolor='black')
        ax.add_patch(rect)
        plt.text(0.5 * self.width, 0.5 * self.height, label, 
                ha='center', va='center')
        ax.set_xlim(0, self.width * 2.2)
        ax.set_ylim(0, self.height * 2.2)
        plt.title(self.SHAPE_NAME)
        
        if filename:
            plt.savefig(filename)
        plt.show()

class Parallelogram(GeometricShape):
    """Parallelogram defined by two diagonals and the angle between them."""

    SHAPE_NAME = "Parallelogram"

    def __init__(self, d1: float, d2: float, angle_deg: float, color: str):
        if not (0 < angle_deg < 180):
            raise ValueError("Angle must be between 0 and 180 degrees")

        self.d1 = d1
        self.d2 = d2
        self.angle_deg = angle_deg
        self.color = Color(color)

    def area(self) -> float:
        # Area = 1/2 * d1 * d2 * sin(angle)
        angle_rad = math.radians(self.angle_deg)
        return 0.5 * self.d1 * self.d2 * math.sin(angle_rad)

    def get_info(self) -> str:
        return "Shape: {name}\nColor: {color}\nArea: {area:.2f}".format(
            name=self.SHAPE_NAME,
            color=self.color.color,
            area=self.area()
        )

    def draw(self, label: str = "", filename: str = ""):
        fig, ax = plt.subplots()

        # Center the diagonals at (0, 0)
        half_d1 = self.d1 / 2
        half_d2 = self.d2 / 2
        angle_rad = math.radians(self.angle_deg)

        # Diagonal vectors
        dx = half_d2 * math.cos(angle_rad / 2)
        dy = half_d2 * math.sin(angle_rad / 2)

        # Define 4 points of the parallelogram
        p1 = (-half_d1 + dx, dy)
        p2 = (half_d1 + dx, dy)
        p3 = (half_d1 - dx, -dy)
        p4 = (-half_d1 - dx, -dy)

        polygon = Polygon([p1, p2, p3, p4], closed=True, 
                          facecolor=self.color.color, edgecolor='black')
        ax.add_patch(polygon)

        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        ax.set_aspect('equal')
        plt.title(self.SHAPE_NAME)

        if label:
            plt.text(0, 0, label, ha='center', va='center', fontsize=12, color='black')

        if filename:
            plt.savefig(filename)
        plt.show()


class CircleShape(GeometricShape):
    """Circle shape with radius and color."""
    
    SHAPE_NAME = "Circle"
    
    def __init__(self, radius: float, color: str):
        self._radius = radius
        self.color = Color(color)
    
    @property
    def radius(self) -> float:
        return self._radius
    
    @radius.setter
    def radius(self, value: float):
        if value <= 0:
            raise ValueError("Radius must be positive")
        self._radius = value
    
    def area(self) -> float:
        return math.pi * self._radius ** 2
    
    def get_info(self) -> str:
        return "Shape: {name}\nColor: {color}\nArea: {area:.2f}".format(
            name=self.SHAPE_NAME,
            color=self.color.color,
            area=self.area()
        )
    
    def draw(self, label: str = "", filename: str = ""):
        fig, ax = plt.subplots()
        circle = Circle((0.5, 0.5), self.radius, 
                       facecolor=self.color.color, edgecolor='black')
        ax.add_patch(circle)
        plt.text(0.5, 0.5, label, ha='center', va='center')
        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        plt.title(self.SHAPE_NAME)
        
        if filename:
            plt.savefig(filename)
        plt.show()

