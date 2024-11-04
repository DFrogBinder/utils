from manim import *
import random

class RandomOpacitySurface(ThreeDScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Define the surface as an instance variable
        self.surface = Surface(
            lambda u, v: np.array([
                u,
                v,
                np.sin(u) * np.cos(v)
            ]),
            u_range=[-PI, PI],
            v_range=[-PI, PI],
            resolution=(32, 32),
            color=BLUE,
        )
    
    def construct(self):
        # Generate a random opacity value between 0.1 and 0.9
        opacity_value = random.uniform(0.1, 0.9)

        # Set the fill opacity of the surface
        self.surface.set_fill(color=BLUE, opacity=opacity_value)
        
        # Set up the camera orientation
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        
        # Add the surface to the scene
        self.add(self.surface)
        
        # Animate the opacity change to create a dynamic effect
        self.play(self.surface.animate.set_fill(opacity=random.uniform(0.1, 0.9)), run_time=3)
        self.wait(2)
