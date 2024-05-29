from manim import *
import numpy as np

class Controller3(Scene):
    def construct(self):

        self.starter()
        self.wait()


    def starter(self):
        udt = MathTex(r"u_d(t)").move_to(LEFT*4)

        gdz_container = Rectangle(width=3, height=2, color=WHITE)
        gdz = MathTex(r"G_d(z)").move_to(gdz_container.get_center()).set_color(BLUE)
        gdz.add_updater(lambda x: x.move_to(gdz_container.get_center()))
        ydt = MathTex(r"y_d(t)").move_to(RIGHT*4)

        arrow1 = Arrow(udt.get_right(), gdz_container.get_left())
        arrow2 = Arrow(gdz_container.get_right(), ydt.get_left())

        group100 = VGroup(udt, gdz, ydt, arrow1, arrow2, gdz_container).move_to(UP)

        self.add(udt, gdz, ydt, arrow1, arrow2, gdz_container)
        self.play(group100.animate.shift(DOWN))

        self.play(FadeOut(udt),FadeOut(ydt),FadeOut(arrow1),FadeOut(arrow2),
                  gdz_container.animate.shift(RIGHT*2))

        rt = MathTex(r"r(t)").move_to(LEFT*6.5)
        yt = MathTex(r"y_d(t)").move_to(RIGHT*6.5)

        plus_sign = MathTex(r"+")   
        plus_container = Circle(radius=0.25, color=WHITE).move_to(LEFT*4.5)
        plus_sign.move_to(plus_container.get_center())
        plus_sign.add_updater(lambda x: x.move_to(plus_container.get_center()))

        minus_sign = MathTex(r"-").move_to(plus_container.get_bottom()+DOWN*0.5+LEFT*0.5)


        C_container = Rectangle(width=2.1, height=1.4, color=WHITE)
        C_container.shift(LEFT*2.5)
        C = MathTex(r"C(s) = \frac{s+2}{s+10}").set_color(BLUE).scale(0.6)
        C.move_to(C_container.get_center())
        C.add_updater(lambda m: m.move_to(C_container.get_center()))

        arrow_1 = Arrow(rt.get_right(), plus_container.get_left())
        arrow_2 = Arrow(plus_container.get_right(), C_container.get_left())
        arrow_3 = Arrow(C_container.get_right(), gdz_container.get_left())
        arrow_4 = Arrow(gdz_container.get_right(), yt.get_left())

        #feedback path
        line1 = Line(gdz_container.get_right()+RIGHT,gdz_container.get_right()+RIGHT+DOWN*2)
        line2 = Line(line1.get_end(),plus_container.get_center()+DOWN*2)
        arrow5 = Arrow(line2.get_end(),plus_container.get_bottom()+DOWN*0.3,buff=0)

        com = Rectangle(width=6.4, height=4, color=RED).set_fill(BLUE, opacity=0.5).move_to(DOWN*0.5+LEFT*3.9)
        com_label = MathTex(r"\text{Inside Digital Computer}").scale(0.8)
        com_label.move_to(com.get_corner(UR)+LEFT*3+DOWN*0.3)
        com_label.add_updater(lambda m: m.move_to(com.get_corner(UR)+LEFT*3+DOWN*0.3))


        self.play(Write(rt),Write(yt),Write(plus_sign),Write(minus_sign),
                  Create(plus_container),Write(C),Create(C_container),
                  Create(arrow_1),Create(arrow_2),Create(arrow_3),Create(arrow_4),
                  Create(line1),Create(line2),Create(arrow5),Create(com),Write(com_label),
                    )

        cdz = MathTex(r"C_d(z)").move_to(C_container.get_center()).set_color(BLUE)
        cdz.add_updater(lambda x: x.move_to(C_container.get_center()))

        rdt = MathTex(r"r_d(t)").move_to(rt.get_center())

        self.play(com.animate.set_fill(RED, opacity=0.5))

        self.wait(1)

        self.play(Transform(C,cdz),Transform(rt,rdt))

        self.wait(1)

        group = VGroup(rdt,plus_sign,minus_sign,yt,plus_container,C_container,cdz,arrow_1,arrow_2,arrow_3,arrow_4,line1,line2,arrow5,com,com_label,
                        gdz, gdz_container)

        self.play(group.animate.shift(UP*3).scale(0.8),FadeOut(C),FadeOut(rt))

        question = Tex("Now the question is, How to transform $C(s)$ to $C_d(z)$?").set_color(BLUE)
        
        self.play(Write(question))

        #forward euler
        self.wait(1)
        title_fe = MathTex(r"\text{Forward Euler Method}").set_color(YELLOW).scale(0.8).move_to(LEFT*5+DOWN)
        forward_euler = MathTex(r"s = \frac{z-1}{T}").set_color(GOLD).move_to(LEFT*5+DOWN*2)

        self.play(Write(title_fe),Write(forward_euler))

        self.wait(1)

        #backward euler
        title_be = MathTex(r"\text{Backward Euler Method}").set_color(YELLOW).scale(0.8).move_to(DOWN)
        backward_euler = MathTex(r"s = \frac{z-1}{Tz}").set_color(GOLD).move_to(DOWN*2)

        self.play(Write(title_be),Write(backward_euler))

        self.wait(1)

        #tustin
        title_tustin = MathTex(r"\text{Tustin's Method}").set_color(YELLOW).scale(0.8).move_to(RIGHT*5+DOWN)
        tustin = MathTex(r"s = \frac{2}{T} \frac{z-1}{z+1}").set_color(GOLD).move_to(RIGHT*5+DOWN*2)

        self.play(Write(title_tustin),Write(tustin))

        self.wait(1)

        tustin_group = VGroup(title_tustin,tustin)

        #lets move with tustin method
        self.play(FadeOut(title_fe),FadeOut(forward_euler),FadeOut(title_be),FadeOut(backward_euler))
        self.play(tustin_group.animate.shift(LEFT*5))

        self.wait(1)

        tustin2 = MathTex(r"C_d(z) = C(s) \Bigg|_{s = \frac{2}{T} \frac{z-1}{z+1}}").set_color(BLUE).scale(0.8).move_to(DOWN*2).set_color(GOLD)
        self.play(Transform(tustin,tustin2))
        
        self.wait(1)

        tustin3 = MathTex(r"C_d(z) = \frac{s+2}{s+10} \Bigg|_{s = \frac{2}{T} \frac{z-1}{z+1}}").set_color(BLUE).scale(0.8).move_to(DOWN*2).set_color(GOLD)

        self.play(Transform(tustin,tustin3))

        self.wait(1)

        tustin4 = MathTex(r"C_d(z) = \frac{2 + \frac{2 \left(z - 1\right)}{T \left(z + 1\right)}}{10 + \frac{2 \left(z - 1\right)}{T \left(z + 1\right)}}").scale(0.8).move_to(DOWN*2).set_color(GOLD)

        self.play(Transform(tustin,tustin4))

        self.wait(1)

        tustin5 = MathTex(r"C_d(z) = \frac{T \left(z + 1\right) + z - 1}{5 T \left(z + 1\right) + z - 1}").scale(0.8).move_to(DOWN*2).set_color(GOLD)

        self.play(Transform(tustin,tustin5))

        self.wait(1)

        self.play(FadeOut(tustin),FadeOut(question),FadeOut(title_tustin))

        self.play(group.animate.shift(DOWN*3).scale(1.25))

        title_final = Tex("Complete Discrete Domain Control System with Sampling Period $T=0.1s$").set_color(YELLOW).scale(0.8).move_to(UP*3)

        self.play(FadeOut(com),FadeOut(com_label),Write(title_final))

        cdz_new = MathTex(r"\frac{1.1 z - 0.9}{1.5 z - 0.5}").scale(0.6).move_to(C_container.get_center()).set_color(BLUE)
        # cdz_new.add_updater(lambda x: x.move_to(C_container.get_center()))

        gdz_new = MathTex(r"\frac{0.05z+0.043}{z^2-1.56z+0.606}").move_to(gdz_container.get_center()).set_color(RED).scale(0.5)
        # gdz_new.add_updater(lambda x: x.move_to(gdz_container.get_center()))

        self.play(Transform(cdz,cdz_new),Transform(gdz,gdz_new))

        self.wait(2)

        group_new = VGroup(rdt,plus_sign,minus_sign,yt,plus_container,C_container,cdz_new,arrow_1,arrow_2,arrow_3,arrow_4,line1,line2,arrow5,
                        gdz_new, gdz_container)
        
        self.play(group_new.animate.shift(UP*3).scale(0.8),FadeOut(C),FadeOut(rt),FadeOut(title_final),FadeOut(gdz_new),FadeOut(cdz_new))

        tf_txt = Tex("Transfer Function of the System").set_color(BLUE).scale(0.8).move_to(DOWN)

        self.play(Write(tf_txt))

        tf = MathTex(r"G_{cl}(z)=\frac{C_d(z)G_d(z)}{1+C_d(z)G_d(z)}").set_color(RED).scale(0.8).move_to(DOWN*2)

        self.play(Write(tf))

        self.wait(1)

        tf2 = MathTex(r"G_{cl}(z)=\frac{0.05z^2+0.026z-0.014}{z^3-1.93z^2+1.125z-0.176}").scale(0.8).move_to(DOWN*2).set_color(RED)

        self.play(Transform(tf,tf2))

        self.wait(1)

        self.play(FadeOut(tf),FadeOut(tf_txt))

        #plot discrete step response
        axes2 = Axes(
            x_range=[-1, 6, 1],
            y_range=[-1, 2, 1],
            axis_config={"include_numbers": True}
        ).scale(0.5).move_to(DOWN)

        labels2 = axes2.get_axis_labels(x_label="t", y_label=r"r_d(t)")

        # Define the sampled function
        def sampled_function(x):
            # Sample sin(x)
            if x % 1 == 0 and x>=0:
                return 1
            return 0
        
        # Create stem plot
        stems = VGroup()
        markers = VGroup()

        for x in np.arange(-1, 6, 1):
            y = sampled_function(x)
            # Create a line from the x-axis to the data point
            stem = Line(start=axes2.c2p(x, 0), end=axes2.c2p(x, y), color=BLUE)
            # Create a dot at the data point
            marker = Dot(point=axes2.c2p(x, y), color=RED)
            stems.add(stem)
            markers.add(marker)

        # Create the plot
        self.play(Create(axes2), Create(labels2))
        self.play(Create(stems), Create(markers))

        self.wait(1)

        group_graph = VGroup(axes2,labels2,stems,markers)

        self.play(group_graph.animate.shift(UP*2+LEFT*5.5).scale(0.6))

        image = ImageMobject("final.png").move_to(DOWN*1.5)
        self.play(FadeIn(image))

        self.wait(1)

        #end
        self.play(FadeOut(group_graph),FadeOut(image))

        gif = ImageMobject("finalgif.gif").scale(1).move_to(DOWN*0.5)

        self.play(FadeIn(gif))

        self.wait(1)

        self.play(FadeOut(gif))
        


