from manim import *
import numpy as np

class FluxVisualization(ThreeDScene):
    def construct(self):
        # Set up axes
        axes = ThreeDAxes(
            x_range=[-1, 1, 0.5],
            y_range=[-1, 1, 0.5],
            z_range=[-1, 1, 0.5],
        )

        # Create surface (XY plane)
        surface = Surface(
            lambda u, v: np.array([u, v, 0]),
            u_range=[-1, 1],
            v_range=[-1, 1],
            fill_opacity=0.3,
            color=BLUE
        )

        # Add axes and surface to the scene
        self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES)
        self.add(axes, surface)

        # Initial vector orientation
        theta = 0
        phi = 0
        vector = self.get_vector(theta, phi)
        vector_arrow = Arrow3D(start=ORIGIN, end=vector, color=RED)
        self.add(vector_arrow)

        # Create flux text and add to scene
        flux_value = self.calculate_flux(vector_arrow.get_end() - vector_arrow.get_start())
        flux_text = Text(f"Flux: {flux_value:.2f}", color=WHITE, font_size=24).to_corner(UP + LEFT)
        self.add_fixed_in_frame_mobjects(flux_text)

        # Function to update the vector and flux text
        def update_vector(mob, alpha):
            new_theta = 45 * np.sin(2 * np.pi * alpha)  # Oscillate like a pendulum
            new_phi = 0  # Keep phi constant
            new_vector = self.get_vector(new_theta, new_phi)
            mob.become(Arrow3D(start=ORIGIN, end=new_vector, color=RED))
            new_flux_value = self.calculate_flux(new_vector)
            flux_text.become(Text(f"Flux: {new_flux_value:.2f}", color=WHITE, font_size=24).to_corner(UP + LEFT))

        # Slow down the animation and make the vector oscillate
        self.play(UpdateFromAlphaFunc(vector_arrow, lambda m, alpha: update_vector(m, alpha)), run_time=10, rate_func=there_and_back_with_pause)
        self.wait()

    def get_vector(self, theta, phi):
        return np.array([
            np.sin(np.radians(theta)) * np.cos(np.radians(phi)),
            np.sin(np.radians(theta)) * np.sin(np.radians(phi)),
            np.cos(np.radians(theta))
        ])

    def calculate_flux(self, vector):
        normal = np.array([0, 0, 1])  # Normal to the XY plane
        flux = np.dot(vector[:3], normal)  # Dot product to calculate flux
        return flux
