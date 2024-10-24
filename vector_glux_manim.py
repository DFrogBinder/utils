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

        # Create initial heatmap surface (XY plane)
        u, v = np.meshgrid(np.linspace(-1, 1, 20), np.linspace(-1, 1, 20))
        heatmap_data = self.calculate_heatmap(u, v)

        # Normalize the heatmap data between 0 and 1 for opacity (fixed for the entire animation)
        norm_heatmap_data = (heatmap_data - heatmap_data.min()) / (heatmap_data.max() - heatmap_data.min())

        # Determine min and max flux values for the entire animation
        min_flux = 0  # Minimum possible flux value when vector is parallel to surface
        max_flux = 1   # Maximum possible flux value when vector is normal to surface

        # Create surface with initial opacity based on flux
        surface = self.create_opacity_surface(u, v, norm_heatmap_data)
        self.add(surface)

        # Add axes and surface to the scene
        self.set_camera_orientation(phi=30 * DEGREES, theta=20 * DEGREES)
        self.add(axes)

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
        def update_vector(mob, alpha):
            new_theta = 90 * np.sin(2 * np.pi * alpha)  # Oscillate like a pendulum
            new_vector = self.get_vector(new_theta)
            mob.become(Arrow3D(start=ORIGIN, end=new_vector, color=RED))
            new_flux_value = self.calculate_flux(new_vector)
            flux_text.become(Text(f"Flux: {new_flux_value:.2f}", color=WHITE, font_size=24).to_corner(UP + LEFT))

            # Update surface opacity based on flux without normalizing heatmap data again
            self.update_surface_opacity(surface, norm_heatmap_data, new_flux_value, min_flux, max_flux)

        # Slow down the animation and make the vector oscillate
        self.play(UpdateFromAlphaFunc(vector_arrow, lambda m, alpha: update_vector(m, alpha)), run_time=10, rate_func=there_and_back_with_pause)
        self.wait()

    def get_vector(self, theta):
        return np.array([
            np.sin(np.radians(theta)),
            0,
            np.cos(np.radians(theta))
        ])

    def calculate_flux(self, vector):
        normal = np.array([0, 0, 1])  # Normal to the XY plane
        flux = np.dot(vector[:3], normal)  # Dot product to calculate flux
        return flux

    def calculate_heatmap(self, u, v, vector=None):
        if vector is None:
            vector = self.get_vector(0)
        flux_values = np.zeros_like(u)
        for i in range(u.shape[0]):
            for j in range(u.shape[1]):
                test_vector = np.array([u[i, j], v[i, j], vector[2]])
                flux_values[i, j] = self.calculate_flux(test_vector)
        return flux_values

    def create_opacity_surface(self, u, v, norm_heatmap_data):
        # Create the surface with varying opacity based on flux
        surface = Surface(
            lambda u, v: np.array([u, v, 0]),
            u_range=[-1, 1],
            v_range=[-1, 1],
            resolution=(20, 20),
            fill_opacity=0.8
        )

        # Apply opacity to each piece of the surface
        num_pieces_u, num_pieces_v = norm_heatmap_data.shape
        for i in range(num_pieces_u):
            for j in range(num_pieces_v):
                opacity_value = float(norm_heatmap_data[i, j])
                surface[i * num_pieces_v + j].set_fill(color=WHITE, opacity=opacity_value)

        return surface

    def update_surface_opacity(self, surface, norm_heatmap_data, flux_value, min_flux, max_flux):
        # Scale the flux value to determine the opacity adjustment
        flux_scaling = (flux_value - min_flux) / (max_flux - min_flux)

        # Update the opacity of each piece of the surface
        num_pieces_u, num_pieces_v = norm_heatmap_data.shape
        for i in range(num_pieces_u):
            for j in range(num_pieces_v):
                opacity_value = float(norm_heatmap_data[i, j]) * flux_scaling
                surface[i * num_pieces_v + j].set_fill(opacity=opacity_value)
