from manim import *
import numpy as np
import logging

# Set up logging to output to a file
logging.basicConfig(filename='flux_visualization.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FluxVisualization(ThreeDScene):
    def construct(self):
        logger.info("Setting up axes.")
        # Set up axes
        axes = ThreeDAxes(
            x_range=[-1, 1, 0.5],
            y_range=[-1, 1, 0.5],
            z_range=[-1, 1, 0.5],
        )

        logger.info("Creating initial surface.")
        # Create initial heatmap surface (XY plane)
        u, v = np.meshgrid(np.linspace(-1, 1, 20), np.linspace(-1, 1, 20))

        # Example vector field, e.g., representing electric/magnetic field components
        self.vector_field = np.array([np.ones_like(u), np.zeros_like(v), np.zeros_like(u)])

        # Create surface with initial opacity based on flux
        surface = self.create_opacity_surface(u, v)
        self.add(surface)

        # Add axes and surface to the scene
        self.set_camera_orientation(phi=50 * DEGREES, theta=30 * DEGREES)
        self.add(axes)

        logger.info("Animating surface opacity change.")
        # Animate the opacity change based on flux values
        self.animate_opacity_change(surface, u, v)

    def create_opacity_surface(self, u, v):
        # Calculate the flux based on the vector field and some function of u and v
        flux = self.calculate_flux(u, v)
        opacity_value = (flux - flux.min()) / (flux.max() - flux.min())  # Normalize flux to 0-1 range

        surface = Surface(
            lambda x, y: np.array([
                x,
                y,
                0  # Flat surface on XY plane
            ]),
            u_range=[-1, 1],
            v_range=[-1, 1],
            resolution=(20, 20),
            color=BLUE,
        )
        # Set initial opacity based on the normalized flux
        surface.set_fill(opacity=np.mean(opacity_value))
        return surface

    def calculate_flux(self, u, v):
        # Example flux calculation using a vector field and the grid
        # Modify this function based on the actual vector field and flux calculation logic you need
        # Here, we assume flux is influenced by the vector field and a sinusoidal function
        vector_field_x, vector_field_y, vector_field_z = self.vector_field
        flux = vector_field_x * np.sin(np.pi * u) + vector_field_y * np.cos(np.pi * v)
        return flux

    def animate_opacity_change(self, surface, u, v):
        # Example of animating opacity linked to the flux value
        def update_opacity(mob):
            # Use self.renderer.time to get the current time during animation
            current_time = self.renderer.time
            # Update the flux based on the current time and vector field
            new_flux = self.calculate_flux(u, v + current_time)
            new_opacity = (new_flux - new_flux.min()) / (new_flux.max() - new_flux.min())

            # Set the new opacity (averaged for simplicity)
            mob.set_fill(opacity=np.mean(new_opacity))

        # Animate the change over time
        self.play(UpdateFromFunc(surface, update_opacity), run_time=5, rate_func=linear)

# For testing purposes
if __name__ == "__main__":
    scene = FluxVisualization()
    scene.render()
