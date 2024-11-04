from manim import *

import numpy as np
import logging

# Set up logging to output to a file
logging.basicConfig(filename='flux_visualization.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FluxVisualization(ThreeDScene):
    def construct(self):
        logger.info("Setting up axes.")
        config.background_color = WHITE
        # Set up axes
        axes = ThreeDAxes(
            x_range=[-1, 1, 0.5],
            y_range=[-1, 1, 0.5],
            z_range=[-1, 1, 0.5],
        )

        logger.info("Creating initial surface.")
        # Create initial heatmap surface (XY plane)
        u, v = np.meshgrid(np.linspace(-1, 1, 20), np.linspace(-1, 1, 20))

        # Creating a red sphere instead of a plane surface
        sphere = Sphere(radius=0.25, resolution=(32, 32))
        sphere.set_fill(rgb_to_color([1, 0, 0]), opacity=1.00)  # Initial color and opacity
        self.add(sphere)

        # Add axes and surface to the scene
        self.set_camera_orientation(phi=50 * DEGREES, theta=30 * DEGREES)
        self.add(axes)

        logger.info("Setting initial vector orientation.")
        # Initial vector orientation
        theta = 0
        vector = self.get_vector(theta)
        vector_arrow = Arrow3D(start=ORIGIN, end=vector, color=RED)
        self.add(vector_arrow)

        # Create flux text and add to scene
        flux_value = self.calculate_flux(vector_arrow.get_end() - vector_arrow.get_start())
        flux_text = Text(f"Flux: {flux_value:.2f}", color=WHITE, font_size=24).to_corner(UP + LEFT)
        self.add_fixed_in_frame_mobjects(flux_text)

        # Function to update the vector, flux text, and surface opacity
        def update_vector_and_surface(mob):
            # Update the vector orientation based on time
            current_time = self.renderer.time
            new_theta = 90 * np.sin(2 * np.pi * current_time / 5)  # Oscillate like a pendulum
            new_vector = self.get_vector(new_theta)
            mob.become(Arrow3D(start=ORIGIN, end=new_vector, color=RED))
            new_flux_value = self.calculate_flux(new_vector)

            logger.debug(f"Updating vector angle to {new_theta:.2f} degrees, flux value to {new_flux_value:.2f}.")
            flux_text.become(Text(f"Flux: {new_flux_value:.2f}", color=WHITE, font_size=24).to_corner(UP + LEFT))

            # Normalize and set the RGB color based on the flux value
            normalized_flux = np.clip(new_flux_value, 0, 1)  # Ensure value is between 0 and 1
            sphere.set_fill(rgb_to_color([1 - normalized_flux, 0, normalized_flux]), opacity=1.00)
            logger.debug(f"New RGB value: {[1 - normalized_flux, 0, normalized_flux]}")

        logger.info("Starting animation.")
        # Animate the vector and surface together
        self.play(UpdateFromFunc(vector_arrow, update_vector_and_surface), run_time=5, rate_func=linear)
        self.wait()

    def get_vector(self, theta):
        logger.debug(f"Calculating vector for theta = {theta:.2f} degrees.")
        return np.array([
            np.sin(np.radians(theta)),
            0,
            np.cos(np.radians(theta))
        ])

    def calculate_flux(self, vector):
        logger.debug(f"Calculating flux for vector: {vector}.")
        normal = np.array([0, 0, 1])  # Normal to the XY plane
        flux = np.dot(vector[:3], normal)  # Dot product to calculate flux
        return flux

    def create_opacity_surface(self, u, v, opacity=1):
        logger.info("Creating opacity surface.")
        # Create the surface with the given opacity
        surface = Surface(
            lambda u, v: np.array([u, v, 0]),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(80, 80),
            color=BLUE,
        )
        surface.set_fill(fill_opacity=opacity)
        return surface
