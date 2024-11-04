from manim import *

class SuperconvergentPatchRecovery(Scene):
    def construct(self):
        # Title
        title = Text("Superconvergent Patch Recovery (SPR) Method", font_size=32)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))
        
        # Creating nodes and elements
        nodes = [
            Dot(LEFT + UP, color=BLUE),
            Dot(LEFT + DOWN, color=BLUE),
            Dot(RIGHT + UP, color=BLUE),
            Dot(RIGHT + DOWN, color=BLUE),
            Dot(ORIGIN, color=YELLOW)  # Central node to be interpolated
        ]
        
        # Labels for nodes
        labels = [
            MathTex("N_1").next_to(nodes[0], LEFT),
            MathTex("N_2").next_to(nodes[1], LEFT),
            MathTex("N_3").next_to(nodes[2], RIGHT),
            MathTex("N_4").next_to(nodes[3], RIGHT),
            MathTex("N_i").next_to(nodes[4], UP)
        ]
        
        # Creating triangular elements
        elements = [
            Polygon(nodes[0].get_center(), nodes[1].get_center(), nodes[4].get_center(), color=GREEN, fill_opacity=0.3),
            Polygon(nodes[1].get_center(), nodes[3].get_center(), nodes[4].get_center(), color=GREEN, fill_opacity=0.3),
            Polygon(nodes[3].get_center(), nodes[2].get_center(), nodes[4].get_center(), color=GREEN, fill_opacity=0.3),
            Polygon(nodes[2].get_center(), nodes[0].get_center(), nodes[4].get_center(), color=GREEN, fill_opacity=0.3)
        ]
        
        # Show nodes
        for node in nodes:
            self.play(FadeIn(node))
        
        # Show labels
        for label in labels:
            self.play(Write(label))
        
        # Show elements
        for element in elements:
            self.play(FadeIn(element))
        
        self.wait(2)
        
        # Highlight central node and its patch
        self.play(nodes[4].animate.set_color(RED))
        patch = VGroup(*elements)
        self.play(patch.animate.set_color(YELLOW))
        
        # Show fitting process
        fitting_text = Text("Fitting interpolant to minimize error", font_size=24).to_edge(DOWN)
        self.play(Write(fitting_text))
        
        # Arrows to show influence from surrounding elements
        arrows = [
            Arrow(start=nodes[i].get_center(), end=nodes[4].get_center(), buff=0.1, color=WHITE)
            for i in range(4)
        ]
        for arrow in arrows:
            self.play(GrowArrow(arrow))
        
        self.wait(2)
        
        # Show resulting interpolation
        interpolant_text = Text("Recovered value at node $N_i$", font_size=24).to_edge(DOWN)
        self.play(Transform(fitting_text, interpolant_text))
        self.play(nodes[4].animate.set_color(GOLD))
        
        self.wait(3)
        
        # Fade out everything
        self.play(FadeOut(VGroup(*nodes, *elements, *labels, patch, fitting_text, *arrows)))
        self.wait(1)

# To render this animation, save the code in a .py file and run it with manim:
# manim -pql your_file_name.py SuperconvergentPatchRecovery
