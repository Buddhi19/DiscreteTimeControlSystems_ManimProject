from manim import *
import numpy as np
from scipy.signal import residue, dimpulse, dlti

class Controller2_add_part(Scene):
    def construct(self):

        self.create_system_representation_again()

        self.wait()

    def create_system_representation_again(self):

        rt = MathTex(r"r(t)")
        rt.shift(LEFT*6.5)

        yt = MathTex(r"y(t)")
        yt.shift(RIGHT*6.5)

        G_container = Rectangle(width=3, height=2, color=WHITE)
        G_container.shift(RIGHT*2.5)
        G = MathTex(r"G(s) = \frac{12}{(s+2)(s+3)}").scale(0.6)
        G.move_to(G_container.get_center())
        G.add_updater(lambda m: m.move_to(G_container.get_center()))

        C_container = Rectangle(width=2.1, height=1.4, color=WHITE)
        C_container.shift(LEFT*1.5)
        C = MathTex(r"C(s) = \frac{s+2}{s+10}").set_color(BLUE).scale(0.6)
        C.move_to(C_container.get_center())
        C.add_updater(lambda m: m.move_to(C_container.get_center()))

        plus_sign = MathTex(r"+")
        plus_container = Circle(radius=0.25, color=WHITE).move_to(LEFT*4.5)
        plus_sign.move_to(plus_container.get_center())
        plus_sign.add_updater(lambda m: m.move_to(plus_container.get_center()))

        minus_sign = MathTex(r"-")
        minus_sign.move_to(plus_container.get_bottom()+DOWN*0.5+LEFT*0.5)
        minus_sign.add_updater(lambda m: m.move_to(plus_container.get_bottom()+DOWN*0.5+LEFT*0.5))

        # Connect the blocks
        arrow1 = Arrow(rt.get_right(), plus_container.get_left())
        arrow2 = Arrow(plus_container.get_right(), C_container.get_left())
        arrow3 = Arrow(C_container.get_right(), G_container.get_left())
        arrow4 = Arrow(G_container.get_right(), yt.get_left())

        #feedback path 
        line1 = Line(start=G_container.get_right()+RIGHT, end=G_container.get_right()+RIGHT+DOWN*2)
        line2 = Line(start=line1.get_end(), end=plus_container.get_center()+DOWN*2)
        arrow5 = Arrow(line2.get_end(), plus_container.get_bottom()+DOWN*0.2,buff=0)
        
        #computer
        com = Rectangle(width=7, height=5, stroke_color = RED).move_to(LEFT*3.5+DOWN*1)
        com_label = MathTex(r"\text{Inside Digital Computer}")
        com_label.move_to(com.get_corner(UR)+LEFT*3+DOWN*0.2).scale(0.8)

        # self.add_updater(lambda m: com_label.move_to(com.get_corner(UR)+LEFT*3+DOWN*0.2))

        group = VGroup(rt, yt, G, C, plus_sign, arrow1, arrow2, arrow3, arrow4, G_container, C_container, plus_container, line1, line2, arrow5, com, com_label, minus_sign)

        group.move_to(UP*9)

        group.scale(0.8)

        self.play(group.animate.shift(DOWN*8), run_time=3)

        digital_group = VGroup(rt, plus_container, plus_sign,
                               C,C_container,arrow1,arrow2,arrow5,com,com_label,
                               minus_sign,line1,line2)
        
        analog_group = VGroup(G,G_container,arrow3,arrow4,yt)
        
        self.play(digital_group.animate.shift(LEFT),analog_group.animate.shift(RIGHT),FadeOut(line2),FadeOut(line1),
                  FadeOut(minus_sign),FadeOut(arrow3),FadeOut(arrow5), run_time=1)
        
        DAC_container = Rectangle(width=1, height=0.8, color=WHITE)
        DAC_label = MathTex(r"\text{DAC}").scale(0.6).set_color(RED)
        DAC_label.move_to(DAC_container.get_center())
        DAC_label.add_updater(lambda m: m.move_to(DAC_container.get_center()))
        DAC_container.move_to(G_container.get_left()+LEFT*1.5)

        ADC_container = Rectangle(width=1, height=0.8, color=WHITE)
        ADC_label = MathTex(r"\text{ADC}").scale(0.6).set_color(RED)
        ADC_label.move_to(ADC_container.get_center())
        ADC_label.add_updater(lambda m: m.move_to(ADC_container.get_center()))

        ADC_container.move_to(DAC_container.get_center()+DOWN*2)

        arrow_dac_1 = Arrow(C_container.get_right(), DAC_container.get_left())
        arrow_dac_2 = Arrow(DAC_container.get_right(), G_container.get_left())

        self.play(Create(DAC_container), Write(DAC_label),Create(arrow_dac_1),Create(arrow_dac_2))

        self.wait(1)

        line1 = Line(start=G_container.get_right()+RIGHT*0.5, end=G_container.get_right()+RIGHT*0.5+DOWN*2)
        arrow_adc_1 = Arrow(line1.get_end(), ADC_container.get_right()+RIGHT*0.3,buff=0)
        arrow_adc_2 = Line(ADC_container.get_left()+LEFT*0.3, plus_container.get_center()+DOWN*2)
        arrow6 = Arrow(arrow_adc_2.get_end(), plus_container.get_bottom()+DOWN*0.2,buff=0)

        self.play(Create(ADC_container), Write(ADC_label), Create(arrow_adc_1), 
                  Create(arrow_adc_2),Create(arrow6),Create(line1),FadeIn(minus_sign))
        
        self.wait(1)

        arrow_dac_new = Arrow(DAC_container.get_left()+LEFT, DAC_container.get_left())

        arrow_adc_new = Arrow(ADC_container.get_left(), ADC_container.get_left()+LEFT)

        line_new = Line(start=G_container.get_right()+RIGHT*0.3, end=line1.get_start())

        self.play(com.animate.set_fill(color = BLUE,opacity=1),com_label.animate.move_to(com.get_center()).set_color(YELLOW_A).scale(1.4),
                  FadeOut(arrow_adc_2),FadeOut(arrow6),FadeOut(minus_sign),FadeOut(arrow_dac_1)
                  ,Create(arrow_dac_new),Create(arrow_adc_new),run_time = 2)
        
        self.wait(1)

        rdt = MathTex(r"u_d(t)").scale(0.8)
        rdt.move_to(arrow_dac_new.get_start()+LEFT*0.7)

        ydt = MathTex(r"y_d(t)").scale(0.8)
        ydt.move_to(arrow_adc_new.get_end()+LEFT*0.7)

        self.play(FadeOut(rt),FadeOut(plus_container),FadeOut(plus_sign),FadeOut(C),FadeOut(C_container),
                    FadeOut(com),FadeOut(com_label),FadeOut(arrow1),FadeOut(arrow2),FadeOut(arrow4),FadeOut(yt),Create(line_new))  

        self.play(Write(rdt),Write(ydt))

        group = VGroup(DAC_container, DAC_label, arrow_dac_new, rdt,G,G_container,arrow_dac_2)

        self.play(group.animate.shift(LEFT*3),FadeOut(line_new),FadeOut(arrow_adc_new),FadeOut(arrow_adc_1),FadeOut(line1))

        arrow_new1 = Arrow(G_container.get_right(),ADC_container.get_left())
        arrow_new1.add_updater(lambda m: m.become(Arrow(G_container.get_right(),ADC_container.get_left())))

        arrow_new2 = Arrow(ADC_container.get_right(),ydt.get_left())
        arrow_new2.add_updater(lambda m: m.become(Arrow(ADC_container.get_right(),ydt.get_left())))

        self.play(ADC_container.animate.move_to(G_container.get_right()+RIGHT*1.5),ydt.animate.move_to(G_container.get_right()+RIGHT*3.7))
        
        
        self.play(Create(arrow_new1),Create(arrow_new2))

        self.wait(1)

        group23 = VGroup(ADC_container, DAC_container, G_container)
        #add a bracket with text
        brace = Brace(group23, direction=DOWN)
        brace_text = brace.get_text("G(z)").set_color(YELLOW)

        self.play(Create(brace),Write(brace_text))

        group24 = VGroup(arrow_new1,arrow_new2,arrow_dac_2,arrow_dac_new,rdt,ydt,ADC_container,DAC_container,G_container,G,ADC_label,DAC_label,brace,brace_text)

        self.play(group24.animate.shift(UP))

        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-1.5, 1.5, 0.5],
            axis_config={"color": BLUE},
            tips=False,
        ).scale(0.5).shift(LEFT*2.5+DOWN*1.5)

        axes_labels = axes.get_axis_labels(x_label="n", y_label="x[n]")

        self.play(Create(axes), Write(axes_labels))
        self.wait(1)

        # Sinusoidal function definition
        def sinusoidal(n):
            return np.sin(2 * np.pi * n / 10)
        
        # Generate points
        n_values = np.arange(0, 11, 1)
        points = [(n, sinusoidal(n)) for n in n_values]
        
        # Create the stem plot
        stems = VGroup()
        dots = VGroup()

        for n, value in points:
            dot = Dot(axes.c2p(n, value), color=RED)
            line = Line(axes.c2p(n, 0), axes.c2p(n, value), color=RED)
            stems.add(line)
            dots.add(dot)
        
        self.play(Create(stems), Create(dots))

        #write z transformation equation
        z_transform = MathTex(r"X(z) = \sum_{n=-\infty}^{\infty} x[n]z^{-n}").move_to(axes.get_right()+RIGHT*3).set_color(YELLOW).scale(0.8)
        self.play(Write(z_transform))

        self.wait(2)

        self.play(FadeOut(axes),FadeOut(axes_labels),FadeOut(stems),FadeOut(dots),FadeOut(z_transform))

        #define Gz
        Gz = MathTex(r"G(z) = \frac{\mathcal{Z}\{y_d(t)\}}{\mathcal{Z}\{u_d(t)\}}").set_color(BLUE).shift(DOWN*0.5)
        self.play(Write(Gz))

        self.wait(1)

        Gz2 = MathTex(r"G(z) = \frac{Y_d(z)}{U_d(z)}").set_color(BLUE).shift(DOWN*0.5)

        self.play(Transform(Gz,Gz2))

        self.wait(1)

        #if udt is a impulse function
        text = Tex("If $u_d(t)$ is an impulse function").move_to(DOWN*2).set_color(YELLOW).scale(0.8)
        self.play(Write(text))

        Gz3 = MathTex(r"G(z) = \frac{Y(z)}{1}").set_color(BLUE).shift(DOWN*0.5)
        self.play(Transform(Gz,Gz3))

        self.play(FadeOut(Gz),FadeOut(text))
        
        text1 = MathTex(r"\text{G(z) is the Z-Transformation of the}\\ \text{impulse response of the system}").move_to(DOWN*0.5).set_color(BLUE)
        self.play(Write(text1))

        self.wait(2)
        self.play(FadeOut(text1))

    def new(self):
        axes = Axes(
            x_range=[-1, 6, 1],
            y_range=[-1, 2, 1],
            axis_config={"include_numbers": True}
        ).scale(0.5).move_to(DOWN*2)

        labels = axes.get_axis_labels(x_label="t", y_label="impulse")

        # Define the impulse function
        def impulse_function(x):
            return 1 if x == 0 else 0
        
        # Create stem plot for discrete impulse response
        stems = VGroup()
        markers = VGroup()

        for x in range(-1, 6):
            y = impulse_function(x)
            # Create a line from the x-axis to the data point
            stem = Line(start=axes.c2p(x, 0), end=axes.c2p(x, y), color=BLUE)
            # Create a dot at the data point
            marker = Dot(point=axes.c2p(x, y), color=RED)
            stems.add(stem)
            markers.add(marker)

        # Add axes, labels, stems, and markers to the scene
        self.play(Create(axes), Write(labels))
        self.play(Create(stems), Create(markers))

        group1 = VGroup(axes, labels, stems, markers)

        self.play(group1.animate.shift(UP*3.5+LEFT*5).scale(0.4), run_time=2)

        impulse_axes = Axes(
            x_range=[-1, 6, 1],
            y_range=[-1, 2, 1],
            axis_config={"include_numbers": True}
        ).scale(0.5).move_to(DOWN*2)

        impulse_labels = impulse_axes.get_axis_labels(x_label="t", y_label="DAC")

        # Define the impulse function
        def impulse_function(x):
            return 1 if x == 0 else 0
        
        # Create stem plot for discrete impulse response with ZOH
        impulse_stems = VGroup()
        impulse_markers = VGroup()
        zoh_lines = VGroup()

        previous_value = None

        for x in range(-1, 6):
            value = impulse_function(x)
            # Create a line from the x-axis to the data point
            stem = Line(start=impulse_axes.c2p(x, 0), end=impulse_axes.c2p(x, value), color=BLUE)
            # Create a dot at the data point
            marker = Dot(point=impulse_axes.c2p(x, value), color=RED)
            impulse_stems.add(stem)
            impulse_markers.add(marker)
            
            # Create the ZOH line
            if previous_value is not None:
                zoh_line = Line(start=impulse_axes.c2p(x - 1, previous_value), end=impulse_axes.c2p(x, previous_value), color=GREEN)
                zoh_lines.add(zoh_line)
            previous_value = value
        
        # Add final ZOH segment to complete the last sample
        final_zoh_line = Line(start=impulse_axes.c2p(5, previous_value), end=impulse_axes.c2p(6, previous_value), color=GREEN)
        zoh_lines.add(final_zoh_line)

        # Add axes, labels, stems, markers, and ZOH lines to the scene
        self.play(Create(impulse_axes), Write(impulse_labels))
        self.play(Create(impulse_stems), Create(impulse_markers))
        self.play(Create(zoh_lines))

        group = VGroup(impulse_axes, impulse_labels, impulse_stems, impulse_markers, zoh_lines)

        DAC_out = MathTex(r"=U_{step}(t)-U_{step}(t-T)").move_to(group.get_bottom()+DOWN*0.2+LEFT*0.5).set_color(YELLOW).scale(0.8)
        DAC_out.add_updater(lambda m: DAC_out.move_to(group.get_bottom()+DOWN*0.2+LEFT*0.5))
        self.play(Write(DAC_out))

        self.wait(2)

        self.play(group.animate.shift(LEFT*4).scale(0.6))
        
        analog_system = Rectangle(width=1.5, height=1, stroke_color = WHITE).move_to(group.get_right()+RIGHT*2)
        analog_tf = MathTex(r"G(s)").set_color(BLUE).move_to(analog_system.get_center())
        analog_tf.add_updater(lambda m: analog_tf.move_to(analog_tf.get_center()))

        analog_system_group = VGroup(analog_system, analog_tf)

        arrow1 = Arrow(group.get_right(), analog_system.get_left(), stroke_color = WHITE)

        out = MathTex(r"y_{step}(t)-y_{step}(t-T)").move_to(analog_system.get_right()+RIGHT*3).scale(0.8)

        arrow2 = Arrow(analog_system.get_right(), out.get_left(), stroke_color = WHITE)

        text = MathTex(r"\text{If the step response of G(s) is } y_{step}(t)").move_to(out.get_top()+UP*0.7+LEFT*3).set_color(BLUE).scale(0.8)

        self.play(Write(analog_system_group),Write(out),Write(arrow1),Write(arrow2),Write(text))

        self.wait(2)

        self.play(FadeOut(analog_system_group),FadeOut(arrow2),FadeOut(arrow1),FadeOut(text),FadeOut(group),FadeOut(DAC_out),
                  out.animate.move_to(LEFT*4+DOWN*2), run_time=1)
        
        
        adc_system = Rectangle(width=1.5, height=1, stroke_color = WHITE).move_to(out.get_right()+RIGHT*2)
        adc_tf = MathTex(r"ADC").set_color(BLUE).move_to(adc_system.get_center())
        adc_tf.add_updater(lambda m: adc_tf.move_to(adc_system.get_center()))

        adc_system_group = VGroup(adc_system, adc_tf)

        arrow1 = Arrow(out.get_right(), adc_system.get_left(), stroke_color = WHITE)

        out2 = MathTex(r"y_{step}(kT)-y_{step}(kT-T)").move_to(adc_system.get_right()+RIGHT*3).scale(0.8)

        arrow2 = Arrow(adc_system.get_right(), out2.get_left(), stroke_color = WHITE)

        self.play(Write(adc_system_group),Write(out2),Write(arrow1),Write(arrow2))

        self.wait(2)

        self.play(FadeOut(out),FadeOut(adc_system_group),FadeOut(arrow2),FadeOut(arrow1),out2.animate.move_to(UP*2+RIGHT*5.5).scale(0.8), run_time=1)

        text5 = MathTex(r"\text{Where }y_{step}(t) \text{ is the step response of the system}").set_color(BLUE)

        self.play(Write(text5))

        yt = MathTex(r"y_{step}(t) = \mathcal{L}^{-1}(G(s)\cdot U_{step}(s))").move_to(DOWN*2).set_color(RED)
        self.play(Write(yt))

        self.wait(1)

        yt2 = MathTex(r"y_{step}(t) = \mathcal{L}^{-1}(G(s)\cdot \frac{1}{s})").move_to(DOWN*2).set_color(RED)
        self.play(Transform(yt, yt2))

        self.wait(1)

        yt3 = MathTex(r"y_{step}(kT)=\mathcal{L}^{-1}\left(\frac{G(s)}{s}\right)_{t=kT}").move_to(DOWN*2).set_color(RED)
        self.play(Transform(yt, yt3))

        self.wait(2)

        text6 = MathTex(r"\text{G(z) is the Z-Transform of the impulse response}").set_color(BLUE).scale(0.8)
        self.play(FadeOut(yt),FadeOut(text5),FadeIn(text6))

        yt4 = MathTex(r"G(z)=\mathcal{Z}\{y_{step}(kT)-y_{step}(kT-T)\}").move_to(DOWN*2).set_color(RED)
        self.play(Write(yt4))

        self.wait(1)

        yt5 = MathTex(r"G(z) = \mathcal{Z}\{y_{step}(kT)\} - z^{-1}\mathcal{Z}\{y_{step}(kT)\}").move_to(DOWN*2).set_color(RED)
        self.play(Transform(yt4, yt5))

        self.wait(1)

        yt6 = MathTex(r"G(z) = (1-z^{-1})\mathcal{Z}\left(\mathcal{L}^{-1}\left(\frac{G(s)}{s}\right)_{t=kT}\right)").move_to(DOWN*2).set_color(RED)
        self.play(Transform(yt4, yt6))

        self.wait(1)

        self.play(FadeOut(yt6),FadeOut(text6),FadeOut(yt4))

        text7 = MathTex(r"\text{For }G(s)=\frac{12}{(s+2)(s+3)}").set_color(BLUE).scale(0.8)
        self.play(Write(text7))

        yt7 = MathTex(r"G(z) = (1-z^{-1})\mathcal{Z}\left(\mathcal{L}^{-1}\left(\frac{12}{s(s+2)(s+3)}\right)_{t=kT}\right)").move_to(DOWN*2).set_color(RED)
        self.play(Write(yt7))

        self.wait(1)

        yt8 = MathTex(r"G(z) = 6\frac{1-e^{-2T}}{z-e^{-2T}}-4\frac{1-e^{-3T}}{z-e^{-3T}}").move_to(DOWN*2).set_color(RED)
        self.play(Transform(yt7, yt8))

        self.wait(1)

        self.play(FadeOut(yt7),FadeOut(text7),FadeOut(yt8),FadeOut(out2))

        #add image
        image = ImageMobject("image.png").move_to(DOWN*1.5).scale(1.5).set_z_index(-1)
        self.play(FadeIn(image))

        self.wait(2)

        self.play(FadeOut(image),FadeOut(group1))

        self.play(group24.animate.shift(DOWN*2))

        gdz_container = Rectangle(width=3, height=2, stroke_color = WHITE).move_to(rdt.get_right()+RIGHT*4)
        gdz = MathTex(r"G_d(z)").set_color(BLUE).move_to(gdz_container.get_center())
        gdz.add_updater(lambda m: gdz.move_to(gdz_container.get_center()))

        self.play(FadeOut(ADC_container),FadeOut(ADC_label),FadeOut(DAC_container),FadeOut(DAC_label),
                  FadeOut(arrow_dac_new),FadeOut(arrow_new1),FadeOut(arrow_new2),Create(gdz_container),Write(gdz),
                  FadeOut(brace),FadeOut(brace_text),FadeOut(G),FadeOut(G_container),FadeOut(arrow_dac_2))
        
        arrow_new_new1 = Arrow(rdt.get_right(), gdz_container.get_left())
        arrow_new_new2 = Arrow(gdz_container.get_right(), ydt.get_left())
        arrow_new_new1.add_updater(lambda m: m.become(Arrow(rdt.get_right(), gdz_container.get_left())))
        arrow_new_new2.add_updater(lambda m: m.become(Arrow(gdz_container.get_right(), ydt.get_left())))

        self.play(rdt.animate.shift(RIGHT),ydt.animate.shift(LEFT),Create(arrow_new_new1),Create(arrow_new_new2))

        text8 = Tex("Where G(z) is the analogous Discrete Transfer function of our analog domain transfer function").set_color(BLUE).scale(0.8).move_to(DOWN*2)
        self.play(Write(text8))

        self.wait(2)

        self.play(FadeOut(text8))