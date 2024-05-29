from manim import *

class Thumbnail(Scene):
    def construct(self):
        image = ImageMobject("G(z).png").set_z_index(-1).set_opacity(0.25)
        self.add(image)
        title = Text("BUT, HOW DOES").scale(1).set_color(GOLD)
        title.move_to(UP*1)
        title2 = Text("DISCRETE TIME CONTROL SYSTEMS").scale(1).set_color(GOLD)
        title3 = Text("WORK?").scale(1).set_color(GOLD).move_to(DOWN*1)

        self.add(title,title2,title3)

        self.wait()
