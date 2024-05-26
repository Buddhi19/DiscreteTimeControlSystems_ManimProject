from manim import *
import numpy as np

#create a controller design

class Controller(Scene):
    def construct(self):
        self.startup()

        self.write_equation_for_closed_loop()

        self.graph_input()

        self.graph_output1()

        self.what_if_we_add_controller()

        self.add_controller()

        self.play(FadeOut(self.graph_input_for_erase), FadeOut(self.graph_output_for_erase))

        self.new_system()

        self.write_equations2()

        self.graph_input()

        self.out_graph2()

        self.play(FadeOut(self.graph_input_for_erase), FadeOut(self.graph_output_for_erase))

        self.the_question()

        self.startup_digital()

        self.wait()

    def startup(self):
        analog_system = Rectangle(width=12, height=6, stroke_color = WHITE)

        analog_tf = MathTex(r"G(s) = \frac{12}{(s+2)(s+3)}").scale(2)

        analog_tf.add_updater(lambda m: analog_tf.move_to(analog_tf.get_center()))

        analog_rt = MathTex(r"r(t)")

        rt_group = VGroup(analog_rt)
        rt_group.move_to(LEFT*6)

        #plus sign inside a circle
        plus_sign = MathTex(r"+")
        circle = Circle(radius=0.25, stroke_color = WHITE)
        plus_sign.add_updater(lambda m: plus_sign.move_to(circle.get_center()))

        plus_group = VGroup(plus_sign, circle)
        plus_group.move_to(LEFT*3.5)
        
        output = MathTex(r"y(t)")
        output.move_to(RIGHT*6)
        
        arrow1 = Arrow(rt_group.get_right(), plus_group.get_left(), stroke_color = WHITE)
        arrow1.add_updater(lambda m: m.become(Arrow(rt_group.get_right(), plus_group.get_left(), stroke_color = WHITE)))

        arrow2 = Arrow(plus_group.get_right(), analog_system.get_left(), stroke_color = WHITE)
        arrow2.add_updater(lambda m: m.become(Arrow(plus_group.get_right(), analog_system.get_left(), stroke_color = WHITE)))

        arrow3 = Arrow(analog_system.get_right(), output.get_left(), stroke_color = WHITE)
        arrow3.add_updater(lambda m: m.become(Arrow(analog_system.get_right(), output.get_left(), stroke_color = WHITE)))

        # Create right-angled segments for feedback arrow
        line1 = Line(start=analog_system.get_right()+RIGHT*1, end=analog_system.get_right() + DOWN*2 +RIGHT*1, stroke_color = WHITE)
        line1.add_updater(lambda m: m.become(Line(start=analog_system.get_right()+RIGHT*1, end=analog_system.get_right() + DOWN*2 +RIGHT*1, stroke_color = WHITE)))

        line2 = Line(start=analog_system.get_right() + DOWN*2 +RIGHT*1, end=plus_group.get_center() + DOWN*2, stroke_color = WHITE)
        line2.add_updater(lambda m: m.become(Line(start=analog_system.get_right() + DOWN*2 +RIGHT*1, end=plus_group.get_center() + DOWN*2, stroke_color = WHITE)))

        line3 = Line(start=plus_group.get_center() + DOWN*2, end=plus_group.get_bottom()+DOWN*0.2, stroke_color = WHITE)
        line3.add_updater(lambda m: m.become(Line(start=plus_group.get_center() + DOWN*2, end=plus_group.get_bottom()+DOWN*0.2, stroke_color = WHITE)))

        arrow_head = Arrow(line3.get_start(), line3.get_end()+UP*0.4, stroke_color = WHITE,stroke_width=0.05).set_tip_length(0.2)

        feedback_arrow = VGroup(line1, line2, line3, arrow_head) 
        arrows = [arrow1, arrow2, arrow3, feedback_arrow]

        minus_sign = MathTex(r"-")
        minus_sign.move_to(plus_group.get_bottom()+DOWN*0.5+LEFT*0.5)

        title = Tex("Hello!").move_to(UP*2).set_color(RED).scale(3)
        self.play(Write(title))
        self.play(FadeOut(title))

        self.play(Write(analog_system), Write(analog_tf))
        self.play(analog_system.animate.scale(0.3),analog_tf.animate.scale(0.3)
                ,FadeIn(rt_group),FadeIn(output),FadeIn(plus_group),
                    run_time=2)

        self.play(*[Create(arrow) for arrow in arrows],FadeIn(minus_sign), run_time=2)

        #group everything together
        group = VGroup(analog_system, analog_tf, rt_group, output, plus_group, *arrows,minus_sign)

        self.play(group.animate.shift(UP*3).scale(0.8), run_time=2)

        self.big_picture = group


    def write_equation_for_closed_loop(self):
        title = Tex("Transfer Function of Closed Loop System").move_to(DOWN).set_color(YELLOW)
        self.play(Write(title))
        #write the equation for the closed loop system
        closed_loop = MathTex(r"G_{cl}(s) = \frac{G(s)}{1+G(s)}").move_to(DOWN*2.3).set_color(BLUE)
        self.play(Write(closed_loop))

        self.wait(1)

        solved = MathTex(r"G_{cl}(s) = \frac{12}{s^2+5s+18}").move_to(DOWN*2.3).set_color(BLUE)
        self.play(Transform(closed_loop, solved))

        self.wait(1)

        self.play(FadeOut(closed_loop, solved, title))

    def graph_input(self):
        #create a step function
        axes = Axes(
            x_range=[-1, 6, 1],
            y_range=[-1, 2, 1],
            axis_config={"include_numbers": True}
        ).scale(0.6).move_to(DOWN*2)
        labels = axes.get_axis_labels(x_label="t", y_label="r(t)")
        def step_function(x):
            return 1 if x >= 0 else 0
        
        step_graph = axes.plot(step_function, color=BLUE)
        self.play(Create(axes), Write(labels))
        self.play(Create(step_graph))

        group = VGroup(axes, labels, step_graph)
        self.play(group.animate.shift(UP*3+LEFT*5).scale(0.4), run_time=2)

        self.graph_input_for_erase = group

    def graph_output1(self):
        axes = Axes(
            x_range=[-1, 6, 1],
            y_range=[-1, 2, 1],
            axis_config={"include_numbers": True}
        ).scale(0.6).move_to(DOWN*2)

        labels = axes.get_axis_labels(x_label="t", y_label="y(t)")

        def output_function(x):
            if x < 0:
                return 0
            return 2/3 - (2*np.exp(-(5*x)/2)*(np.cos((47**(1/2)*x)/2) + (5*47**(1/2)*np.sin((47**(1/2)*x)/2))/47))/3
        
        output_graph = axes.plot(output_function, color=RED)
        self.play(Create(axes), Write(labels))
        self.play(Create(output_graph))

        group = VGroup(axes, labels, output_graph)

        self.play(group.animate.shift(UP*3+RIGHT*5).scale(0.4), run_time=2)

        self.graph_output_for_erase = group

    def what_if_we_add_controller(self):
        text = Tex("Can we achieve better control of the system??").move_to(LEFT*2).set_color(YELLOW)
        self.play(Write(text))
        text2 = Tex("Introduce a Controller to the system to control the output").move_to(DOWN).set_color(BLUE).scale(0.8)
        self.play(Write(text2))
        self.wait(1)
        self.play(FadeOut(text), FadeOut(text2))

    def add_controller(self):
        
        controller = Rectangle(width=6, height=3, stroke_color = WHITE).move_to(DOWN*2)
        controller_tf = MathTex(r"C(s) = \frac{s+2}{s+10}").scale(1.5).move_to(DOWN*2).set_color(BLUE)

        controller_tf.add_updater(lambda m: controller_tf.move_to(controller_tf.get_center()))

        self.play(FadeIn(controller), FadeIn(controller_tf))

        group = VGroup(controller, controller_tf)

        self.controller_group = group

    def new_system(self): 


        self.play(self.big_picture.animate.move_to(DOWN).scale(1.35), self.controller_group.animate.move_to(UP*2.5).scale(0.7), run_time=2)

        rt_group = self.big_picture[2]
        output = self.big_picture[3]
        plus_group = self.big_picture[4]
        
        analog_system = self.big_picture[0]

        arrow1 = Arrow(rt_group.get_right(), plus_group.get_left(), stroke_color = WHITE)
        arrow1.add_updater(lambda m: m.become(Arrow(rt_group.get_right(), plus_group.get_left(), stroke_color = WHITE)))

        arrow2 = Arrow(plus_group.get_right(), analog_system.get_left(), stroke_color = WHITE)
        # arrow2.add_updater(lambda m: m.become(Arrow(plus_group.get_right(), analog_system.get_left(), stroke_color = WHITE)))

        arrow3 = Arrow(analog_system.get_right(), output.get_left(), stroke_color = WHITE)
        arrow3.add_updater(lambda m: m.become(Arrow(analog_system.get_right(), output.get_left(), stroke_color = WHITE)))

        # Create right-angled segments for feedback arrow
        line1 = Line(start=analog_system.get_right()+RIGHT*1, end=analog_system.get_right() + DOWN*2 +RIGHT*1, stroke_color = WHITE)
        line1.add_updater(lambda m: m.become(Line(start=analog_system.get_right()+RIGHT*1, end=analog_system.get_right() + DOWN*2 +RIGHT*1, stroke_color = WHITE)))

        line2 = Line(start=analog_system.get_right() + DOWN*2 +RIGHT*1, end=plus_group.get_center() + DOWN*2, stroke_color = WHITE)
        line2.add_updater(lambda m: m.become(Line(start=analog_system.get_right() + DOWN*2 +RIGHT*1, end=plus_group.get_center() + DOWN*2, stroke_color = WHITE)))

        line3 = Line(start=plus_group.get_center() + DOWN*2, end=plus_group.get_bottom()+DOWN*0.2, stroke_color = WHITE)
        line3.add_updater(lambda m: m.become(Line(start=plus_group.get_center() + DOWN*2, end=plus_group.get_bottom()+DOWN*0.2, stroke_color = WHITE)))

        arrow_head = Arrow(line3.get_start(), line3.get_end()+UP*0.4, stroke_color = WHITE,stroke_width=0.05).set_tip_length(0.2)

        arrow5 = Arrow(self.controller_group.get_right(), analog_system.get_left(), stroke_color = WHITE)

        self.remove(self.big_picture[6],self.big_picture[7],self.big_picture[8],self.big_picture[5])
        self.add(arrow1,arrow2,arrow3,line1,line2,line3,arrow_head)

        analog = VGroup(analog_system,self.big_picture[1])

        self.play(analog.animate.shift(RIGHT*2.6).scale(0.8),self.controller_group.animate.shift(DOWN*2.595+LEFT).scale(0.5)
                  , run_time=2)
        
        self.add(arrow5)
        arrow5.add_updater(lambda m: m.become(Arrow(self.controller_group.get_right(), analog_system.get_left(), stroke_color = WHITE)))

        new_system = VGroup(analog, self.controller_group,
                             arrow1, arrow2, arrow3, line1, line2, line3, arrow_head,arrow5,
                               rt_group, output, plus_group,self.big_picture[9])

        self.play(new_system.animate.shift(UP*3).scale(0.8), run_time=2)

        self.new_system_group = new_system

    def write_equations2(self):
        title = Tex("Transfer Function of Closed Loop System").move_to(DOWN).set_color(YELLOW)
        self.play(Write(title))
        closed_loop = MathTex(r"G_{cl}(s) = \frac{G(s)C(s)}{1+G(s)C(s)}").move_to(DOWN*2.3).set_color(BLUE)
        self.play(Write(closed_loop))

        self.wait(1)

        solved = MathTex(r"G_{cl}(s) = \frac{12(s+2)}{s^3+15s^2+68s+84}").move_to(DOWN*2.3).set_color(BLUE)
        self.play(Transform(closed_loop, solved))

        self.wait(1)

        self.play(FadeOut(closed_loop, solved, title))

    def out_graph2(self):
        axes = Axes(
            x_range=[-1, 6, 1],
            y_range=[-1, 2, 1],
            axis_config={"include_numbers": True}
        ).scale(0.6).move_to(DOWN*2)

        labels = axes.get_axis_labels(x_label="t", y_label="y(t)")

        def output_function(x):
            if x < 0:
                return 0
            return (12*np.exp(-7*x))/7 - 2*np.exp(-6*x) + 2/7
        
        output_graph = axes.plot(output_function, color=RED)
        self.play(Create(axes), Write(labels))
        self.play(Create(output_graph))

        group = VGroup(axes, labels, output_graph)

        self.graph_output_for_erase = group


    def the_question(self):
        text = Tex("But the question is...").move_to(LEFT*2).set_color(YELLOW).scale(0.8)
        self.play(Write(text))
        text2 = Tex("How to Implement the Controller??").move_to(DOWN*1).set_color(BLUE).scale(0.8)
        self.play(Write(text2))
        text3 = Tex("Implementing the Controller in Analog Domain is quite DIFFICULT").move_to(DOWN*2).set_color(BLUE).scale(0.8)
        self.play(Write(text3))
        self.wait(1)
        self.play(FadeOut(text), FadeOut(text2), FadeOut(text3))


    def startup_digital(self):
        self.play(self.new_system_group.animate.shift(DOWN).scale(1.2), run_time=2)

        choose_digital = Rectangle(width=7.5, height=4, stroke_color = RED).move_to(LEFT*3+UP*1.7)
        text1 = Tex("Inside Digital Computer")
        self.add_updater(lambda m: text1.move_to(choose_digital.get_corner(UR)+DOWN*0.5+LEFT*3))

        main_group = VGroup(choose_digital, text1,self.new_system_group)

        self.play(Write(choose_digital), Write(text1))
        self.wait(1)
        self.play(main_group.animate.shift(UP*0.3), run_time=2)

        text11 = Tex("And Now We Are Working with both Analog and Digital Domains").set_color(YELLOW).scale(0.8).move_to(DOWN)
        self.play(Write(text11))
        text2 = Tex("To Convert the Analog Signals to Digital Signals, we use ADC").move_to(DOWN*2).set_color(BLUE).scale(0.8)
        self.play(Write(text2))

        self.remove(main_group)
        self.play(text11.animate.move_to(UP*3.5),text2.animate.move_to(UP*2.5))

        ADC_box = Rectangle(width=2, height=1, stroke_color = WHITE).move_to(UP*0.1)
        ADC_text = MathTex(r"ADC").move_to(ADC_box.get_center()).set_color(BLUE)

        ADCt = VGroup(ADC_box, ADC_text)

        self.play(FadeIn(ADCt))

        #plot sinusoidal signal
        axes = Axes(
            x_range=[-1, 6, 1],
            y_range=[-1, 2, 1],
            axis_config={"include_numbers": True}
        ).scale(0.3).move_to(LEFT*5)

        labels = axes.get_axis_labels(x_label="t", y_label="y(t)")

        def sinusoidal_function(x):
            return np.sin(x)
        
        sinusoidal_graph = axes.plot(sinusoidal_function, color=BLUE)
        self.play(Create(axes), Write(labels))
        self.play(Create(sinusoidal_graph))

        group = VGroup(axes, labels, sinusoidal_graph)

        arrow = Arrow(ADC_box.get_left()+LEFT*2, ADC_box.get_left(), stroke_color = WHITE)
        self.play(Create(arrow))


        axes2 = Axes(
            x_range=[-1, 6, 1],
            y_range=[-1, 2, 1],
            axis_config={"include_numbers": True}
        ).scale(0.3).move_to(RIGHT*5)

        labels2 = axes2.get_axis_labels(x_label="t", y_label="digital(t)")

        # Define the sampled function
        def sampled_function(x):
            # Sample sin(x)
            if x % 1 == 0:
                return np.sin(x)
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

        # Add axes, labels, stems, and markers to the scene
        
        
        group2 = VGroup(axes2, labels2, stems, markers)
        arrow2 = Arrow(ADC_box.get_right(), ADC_box.get_right()+RIGHT*2, stroke_color = WHITE)
        self.play(Create(arrow2))

        self.play(Create(axes2), Write(labels2))
        self.play(Create(stems), Create(markers))

        result = MathTex(r"y(0),y(1),y(2),y(3),...").move_to(DOWN*2+RIGHT*4).set_color(RED)
        self.play(Write(result))
        result2 = MathTex(r"y(kT)").move_to(DOWN*2+RIGHT*4).set_color(RED)
        self.play(Transform(result, result2))

        input = MathTex(r"y(t)").move_to(DOWN*2+LEFT*2).set_color(BLUE)
        self.play(Write(input))
        arrow4 = Arrow(input.get_right(), result2.get_left(), stroke_color = WHITE)
        self.play(Create(arrow4))

        group3 = VGroup(group2, result, result2, input, arrow4,text2,ADCt,group,arrow,arrow2)

        text3 = Tex("To Convert the Digital Signals to Analog Signals, we use DAC with ZOH").move_to(UP*2).set_color(BLUE).scale(0.8)
        self.play(FadeOut(group3))
        self.play(Write(text3))

        DAC_box = Rectangle(width=2, height=1, stroke_color = WHITE).move_to(UP*0.1)
        DAC_text = MathTex(r"DAC").move_to(DAC_box.get_center()).set_color(BLUE)

        DACt = VGroup(DAC_box, DAC_text)

        self.play(FadeIn(DACt))

        group2.shift(LEFT*10)
        self.play(FadeIn(group2))

        arrow3 = Arrow(DAC_box.get_left()+LEFT*1.5, DAC_box.get_left(), stroke_color = WHITE)
        self.play(Create(arrow3))

        arrow5 = Arrow(DAC_box.get_right(), DAC_box.get_right()+RIGHT*2, stroke_color = WHITE)
        self.play(Create(arrow5))

        axes2 = Axes(
            x_range=[-1, 6, 1],
            y_range=[-1, 2, 1],
            axis_config={"include_numbers": True}
        ).scale(0.3).move_to(RIGHT*5)

        labels2 = axes2.get_axis_labels(x_label="t", y_label="analog(t)")

        # Define the sampled function
        def sampled_function(x):
            # Sample sin(x)
            if x % 1 == 0:
                return np.sin(x)
            return 0
        
        # Create stem plot with ZOH
        stems = VGroup()
        markers = VGroup()
        zoh_lines = VGroup()

        previous_y = None

        for x in np.arange(-1, 6, 1):
            y = sampled_function(x)
            # Create a line from the x-axis to the data point
            stem = Line(start=axes2.c2p(x, 0), end=axes2.c2p(x, y), color=BLUE)
            # Create a dot at the data point
            marker = Dot(point=axes2.c2p(x, y), color=RED)
            stems.add(stem)
            markers.add(marker)
            
            # Create the ZOH line
            if previous_y is not None:
                zoh_line = Line(start=axes2.c2p(x-1, previous_y), end=axes2.c2p(x, previous_y), color=GREEN)
                zoh_lines.add(zoh_line)
            previous_y = y
        
        # Add final ZOH segment to complete the last sample
        final_zoh_line = Line(start=axes2.c2p(5, previous_y), end=axes2.c2p(6, previous_y), color=GREEN)
        zoh_lines.add(final_zoh_line)

        # Add axes, labels, stems, markers, and ZOH lines to the scene
        self.play(Create(axes2), Write(labels2))
        self.play(Create(stems), Create(markers))
        self.play(Create(zoh_lines))

        #zeroth order hold mathematical representation
        zoh = MathTex(r"analog(t) = \sum_{k=-\infty}^{\infty} y(kT).rect\left(\frac{t-T/2-kT}{T}\right)").move_to(DOWN*2).set_color(YELLOW)
        self.play(Write(zoh))


class DigitalController(Scene):
    def construct(self):
        
        self.startup()

        # self.find_gz()

        # self.new_system()

        self.wait()

    def startup(self):
        #re create the controller design in digital domain
        digital_rt = MathTex(r"r_d(t)").move_to(LEFT*6.5)

        digital_controller = Rectangle(width=1.5, height=1, stroke_color = WHITE).move_to(LEFT*3)
        digital_controller_tf = MathTex(r"C_d(z)").set_color(BLUE).move_to(digital_controller.get_center())

        digital_controller_tf.add_updater(lambda m: digital_controller_tf.move_to(digital_controller_tf.get_center()))

        controller_group = VGroup(digital_controller, digital_controller_tf)
        
        plus_sign = MathTex(r"+")
        circle = Circle(radius=0.25, stroke_color = WHITE)
        plus_sign.add_updater(lambda m: plus_sign.move_to(circle.get_center()))

        plus_group = VGroup(plus_sign, circle)
        plus_group.move_to(LEFT*5)
        
        output = MathTex(r"y(t)")
        output.move_to(RIGHT*6)

        DAC_sys = Rectangle(width=1.5, height=1, stroke_color = WHITE)
        DAC_txt = MathTex(r"DAC").move_to(DAC_sys.get_center()).set_color(RED)

        DAC_group = VGroup(DAC_sys, DAC_txt)

        analog_system = Rectangle(width=1.5, height=1, stroke_color = WHITE).move_to(RIGHT*3)
        analog_tf = MathTex(r"G(s)").set_color(BLUE).move_to(analog_system.get_center())
        analog_tf.add_updater(lambda m: analog_tf.move_to(analog_tf.get_center()))

        analog_system_group = VGroup(analog_system, analog_tf)

        output = MathTex(r"y(t)")
        output.move_to(RIGHT*6)

        arrow1 = Arrow(digital_rt.get_right(), plus_group.get_left(), stroke_color = WHITE)
        arrow1.add_updater(lambda m: m.become(Arrow(digital_rt.get_right(), plus_group.get_left(), stroke_color = WHITE)))

        arrow2 = Arrow(plus_group.get_right(), digital_controller.get_left(), stroke_color = WHITE)
        arrow2.add_updater(lambda m: m.become(Arrow(plus_group.get_right(), digital_controller.get_left(), stroke_color = WHITE)))

        arrow3 = Arrow(digital_controller.get_right(), DAC_sys.get_left(), stroke_color = WHITE)
        arrow3.add_updater(lambda m: m.become(Arrow(digital_controller.get_right(), DAC_sys.get_left(), stroke_color = WHITE)))

        arrow4 = Arrow(DAC_sys.get_right(), analog_system.get_left(), stroke_color = WHITE)
        arrow4.add_updater(lambda m: m.become(Arrow(DAC_sys.get_right(), analog_system.get_left(), stroke_color = WHITE)))

        arrow5 = Arrow(analog_system.get_right(), output.get_left(), stroke_color = WHITE)
        arrow5.add_updater(lambda m: m.become(Arrow(analog_system.get_right(), output.get_left(), stroke_color = WHITE)))

        # Create right-angled segments for feedback arrow
        line1 = Line(start=analog_system.get_right()+RIGHT*1, end=analog_system.get_right() + DOWN*2 +RIGHT*1, stroke_color = WHITE)
        line1.add_updater(lambda m: m.become(Line(start=analog_system.get_right()+RIGHT*1, end=analog_system.get_right() + DOWN*2 +RIGHT*1, stroke_color = WHITE)))

        ADC_sys = Rectangle(width=1.5, height=1, stroke_color = WHITE).move_to(DOWN*2)
        ADC_txt = MathTex(r"ADC").move_to(ADC_sys.get_center()).set_color(RED)

        ADC_group = VGroup(ADC_sys, ADC_txt)

        line2 = Line(start=analog_system.get_right() + DOWN*2 +RIGHT*1, end=ADC_sys.get_right(), stroke_color = WHITE)
        line2.add_updater(lambda m: m.become(Line(start=analog_system.get_right() + DOWN*2 +RIGHT*1, end=ADC_sys.get_right(), stroke_color = WHITE)))

        line4 = Line(start=ADC_sys.get_left(), end=plus_group.get_center()+DOWN*2, stroke_color = WHITE)
        line4.add_updater(lambda m: m.become(Line(start=ADC_sys.get_left(), end=plus_group.get_center()+DOWN*2, stroke_color = WHITE)))

        line3 = Line(start=plus_group.get_center() + DOWN*2, end=plus_group.get_bottom()+DOWN*0.2, stroke_color = WHITE)
        line3.add_updater(lambda m: m.become(Line(start=plus_group.get_center() + DOWN*2, end=plus_group.get_bottom()+DOWN*0.2, stroke_color = WHITE)))

        arrow_head = Arrow(line3.get_start(), line3.get_end()+UP*0.4, stroke_color = WHITE,stroke_width=0.05).set_tip_length(0.2)

        feedback_arrow = VGroup(line1, line2, line3, arrow_head,line4)

        arrows = [arrow1, arrow2, arrow3, arrow4, arrow5, feedback_arrow]

        minus_sign = MathTex(r"-")
        minus_sign.move_to(plus_group.get_bottom()+DOWN*0.5+LEFT*0.5)

        title = Tex("System with the Digital Controller").move_to(UP*2).set_color(YELLOW)

        # self.add(digital_rt, digital_controller, digital_controller_tf, plus_group, DAC_group, analog_system, analog_tf, output, minus_sign, *arrows, ADC_group)
        self.play(Write(digital_rt), Write(digital_controller), 
                  Write(digital_controller_tf), Write(plus_group), Write(DAC_group), 
                  Write(analog_system), Write(analog_tf), Write(output), Write(minus_sign), Write(ADC_group),
                  Write(arrow1),Write(arrow2),Write(arrow3),
                  Write(arrow4),Write(arrow5),Write(feedback_arrow),
                   Write(title), run_time=2)
        
        digital_group = VGroup(digital_rt, digital_controller, digital_controller_tf, plus_group, DAC_group, analog_system, analog_tf, output, minus_sign, *arrows, ADC_group)

        self.play(digital_group.animate.shift(UP*3),FadeOut(title), run_time=2)

        digital_computer = Rectangle(width=6, height=3.2, color = RED).move_to(LEFT*4+UP*2.2)
        digital_computer.set_fill(BLUE, opacity=0.5)

        digital_group.add(digital_computer)

        text = MathTex(r"\text{Digital Computer}").move_to(digital_computer.get_bottom()+DOWN*0.3).set_color(YELLOW)

        self.play(Write(digital_computer), Write(text))

        self.play(digital_computer.animate.set_fill(BLUE, opacity=1),text.animate.move_to(digital_computer.get_center()), run_time=2)

        text2 = Tex("What Digital Computer Sees is").move_to(DOWN).set_color(RED)
        self.play(Write(text2))

        text.add_updater(lambda m: m.move_to(digital_computer.get_center()))
        self.play(text2.animate.move_to(UP*3.5),digital_group.animate.shift(DOWN*2.5), run_time=2)

        # self.remove(digital_rt,digital_controller,digital_controller_tf,plus_group,arrow1,arrow2,line3,minus_sign,arrow_head,line4,arrow3) fade out all these
        self.play(FadeOut(digital_rt),FadeOut(digital_controller),FadeOut(digital_controller_tf),FadeOut(plus_group),FadeOut(arrow1),FadeOut(arrow2),FadeOut(line3),FadeOut(minus_sign),FadeOut(arrow_head),FadeOut(line4),FadeOut(arrow3), run_time=1)

        new_arrow = Arrow(DAC_group.get_left()+LEFT, DAC_group.get_left()+RIGHT*0.3, stroke_color = WHITE)

        new_arrow2 = Arrow(ADC_group.get_left()+RIGHT*0.3, ADC_group.get_left()+LEFT, stroke_color = WHITE)
        
        self.play(Create(new_arrow),Create(new_arrow2))

        discrete_analog_sys = Rectangle(width=7.5, height=4, stroke_color = BLUE).move_to(RIGHT*2.75+DOWN*0.3)
        discrete_analog_sys.set_fill(RED, opacity=0.5)

        text3 = MathTex(r"\text{Discretized Analog System}").move_to(discrete_analog_sys.get_bottom()+DOWN*0.3).set_color(YELLOW)


        self.play(Write(discrete_analog_sys), Write(text3), run_time=2)

        self.wait(2)

        #fadeout everything
        self.play(FadeOut(digital_group),FadeOut(text),FadeOut(new_arrow),FadeOut(new_arrow2),FadeOut(ADC_group),FadeOut(ADC_group),FadeOut(DAC_group),FadeOut(discrete_analog_sys),
                  FadeOut(text3),FadeOut(text2),run_time = 0.1)

        discrete_input = MathTex(r"u_d(t)").move_to(LEFT*6)
        DAC_group.move_to(LEFT*3)

        analog_system_group.move_to(LEFT*0.5)

        ADC_group.move_to(RIGHT*2)

        output = MathTex(r"y_d(t)").move_to(RIGHT*6)

        arrow_1 = Arrow(discrete_input.get_right(), DAC_group.get_left(), stroke_color = WHITE)
        arrow_1.add_updater(lambda m: m.become(Arrow(discrete_input.get_right(), DAC_group.get_left(), stroke_color = WHITE)))
        arrow_2 = Arrow(DAC_group.get_right(), analog_system_group.get_left(), stroke_color = WHITE)
        arrow_2.add_updater(lambda m: m.become(Arrow(DAC_group.get_right(), analog_system_group.get_left(), stroke_color = WHITE)))
        arrow_3 = Arrow(analog_system_group.get_right(), ADC_group.get_left(), stroke_color = WHITE)
        arrow_3.add_updater(lambda m: m.become(Arrow(analog_system_group.get_right(), ADC_group.get_left(), stroke_color = WHITE)))
        arrow_4 = Arrow(ADC_group.get_right(), output.get_left(), stroke_color = WHITE)
        arrow_4.add_updater(lambda m: m.become(Arrow(ADC_group.get_right(), output.get_left(), stroke_color = WHITE)))

        title = Tex("Discretized Analog System").move_to(UP*2).set_color(RED)
        #show
        self.play(Write(title),Write(discrete_input),Write(DAC_group), Write(analog_system_group), Write(ADC_group), Write(output),
                   Write(arrow_1), Write(arrow_2), Write(arrow_3), Write(arrow_4), run_time=2
        )

        text4 = MathTex(r"\text{As the system takes a digital signal from the computer}\\ \text{and gives back a digital signal to the computer}").move_to(DOWN*2.5).set_color(BLUE).scale(0.8)

        self.play(Write(text4))

        discrete_group = VGroup(discrete_input, DAC_group, analog_system_group, ADC_group, output, arrow_1, arrow_2, arrow_3, arrow_4)

        gz = VGroup(DAC_group, analog_system_group, ADC_group,arrow_2,arrow_3)

        self.wait(2)

        self.play(FadeOut(title),FadeOut(text4),discrete_group.animate.shift(UP*2.5), run_time=2)

        #draw a bracket to select from DAC to ADC
        bracket = Brace(gz, direction=DOWN)
        text5 = bracket.get_text("G(z)").set_color(YELLOW)

        self.play(GrowFromCenter(bracket), Write(text5))

        self.all_group = VGroup(discrete_group, bracket, text5)

    def find_gz(self):
        text1 = MathTex(r"\text{G(z) is the Z-Transformation of the}\\ \text{impulse response of the system}").move_to(DOWN*0.5).set_color(BLUE)
        self.play(Write(text1),self.all_group.animate.shift(UP))

        self.wait(2)
        self.play(FadeOut(text1))

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

        self.play(group1.animate.shift(UP*3.5+LEFT*4.5).scale(0.6), run_time=2)

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

        text = MathTex(r"\text{If the step response of G(s)}\\ \text{is } y_{step}(t)").move_to(out.get_top()+UP*1.2+LEFT).set_color(BLUE).scale(0.8)

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

        self.play(FadeOut(out),FadeOut(adc_system_group),FadeOut(arrow2),FadeOut(arrow1),out2.animate.move_to(UP*2+RIGHT*4).scale(0.8), run_time=1)

        text5 = MathTex(r"\text{Where }y_{step}(t) \text{ is the step response of the system}").set_color(BLUE)

        self.play(Write(text5))

        yt = MathTex(r"y_{step}(t) = \mathcal{L}^{-1}(G(s)\cdot U_{step}(s))").move_to(DOWN*2).set_color(RED)
        self.play(Write(yt))
        yt2 = MathTex(r"y_{step}(t) = \mathcal{L}^{-1}(G(s)\cdot \frac{1}{s})").move_to(DOWN*2).set_color(RED)
        self.play(Transform(yt, yt2))
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

        self.play(FadeOut(yt7),FadeOut(text7),FadeOut(yt8),FadeOut(out2),FadeOut(group1))

        self.play(self.all_group.animate.shift(DOWN*3), run_time=2)

        gdz = Rectangle(width=8, height=3, stroke_color = RED).move_to(UP*0.5)
        gdz.set_fill(BLACK, opacity=1)

        udt = MathTex(r"u_d(t)").move_to(gdz.get_left()+LEFT*1.5)
        outdt = MathTex(r"y_d(t)").move_to(gdz.get_right()+RIGHT*1.5)

        text8 = MathTex(r"G(z) = 6\frac{1-e^{-2T}}{z-e^{-2T}}-4\frac{1-e^{-3T}}{z-e^{-3T}}").move_to(gdz.get_center()).set_color(YELLOW)

        arrow_a = Arrow(udt.get_right(), gdz.get_left(), stroke_color = WHITE)
        arrow_b = Arrow(gdz.get_right(), outdt.get_left(), stroke_color = WHITE)

        title = Tex("Analogous Discrete Plant").move_to(UP*3).set_color(RED)

        self.remove(self.all_group)
        self.play(Write(gdz),Write(udt),Write(outdt),Write(text8),Write(arrow_a),Write(arrow_b),Write(title), run_time=2)

        self.wait(1)

        self.play(FadeOut(gdz),FadeOut(udt),FadeOut(outdt),FadeOut(text8),FadeOut(arrow_a),FadeOut(arrow_b),FadeOut(title), run_time=1)

    def new_system(self):
        title = Tex("System in Discrete Domain").move_to(UP*2).set_color(RED)
        self.play(Write(title))
        rdt = MathTex(r"r_d(t)").move_to(LEFT*6.5)

        digital_controller = Rectangle(width=1.5, height=1, stroke_color = WHITE).move_to(LEFT*3)
        digital_controller_tf = MathTex(r"C_d(z)").set_color(BLUE).move_to(digital_controller.get_center())

        digital_controller_tf.add_updater(lambda m: digital_controller_tf.move_to(digital_controller_tf.get_center()))

        controller_group = VGroup(digital_controller, digital_controller_tf)

        plus_sign = MathTex(r"+")
        circle = Circle(radius=0.25, stroke_color = WHITE)

        plus_group = VGroup(plus_sign, circle)
        plus_group.move_to(LEFT*5)

        gdz = Rectangle(width=2, height=1, stroke_color = RED).move_to(RIGHT)
        gdz_text = MathTex(r"G_d(z)").move_to(gdz.get_center()).set_color(YELLOW)

        gdz_group = VGroup(gdz, gdz_text)

        output = MathTex(r"y_d(t)")
        output.move_to(RIGHT*6)

        #feedback arrow
        line1 = Line(start=gdz.get_right()+RIGHT*1, end=gdz.get_right() + DOWN*2 +RIGHT*1, stroke_color = WHITE)
        line2 = Line(start=gdz.get_right() + DOWN*2 +RIGHT*1, end=plus_group.get_center() + DOWN*2, stroke_color = WHITE)
        line3 = Line(start=plus_group.get_center() + DOWN*2, end=plus_group.get_bottom()+DOWN*0.3, stroke_color = WHITE)

        arrow_head = Arrow(line3.get_start(), line3.get_end()+UP*0.4, stroke_color = WHITE,stroke_width=0.05).set_tip_length(0.2)

        feedback_arrow = VGroup(line1, line2, line3, arrow_head)

        arrow_k1 = Arrow(gdz.get_right(), output.get_left(), stroke_color = WHITE)
        arrow_k2 = Arrow(digital_controller.get_right(), gdz.get_left(), stroke_color = WHITE)
        arrow_k3 = Arrow(plus_group.get_right(), digital_controller.get_left(), stroke_color = WHITE)
        arrow_k4 = Arrow(rdt.get_right(), plus_group.get_left(), stroke_color = WHITE)


        arrows = [feedback_arrow, arrow_k1, arrow_k2, arrow_k3,arrow_k4]

        minus_sign = MathTex(r"-")
        minus_sign.move_to(plus_group.get_bottom()+DOWN*0.5+LEFT*0.5)

        self.play(Write(rdt),Write(digital_controller),Write(digital_controller_tf),Write(plus_group),Write(gdz_group),Write(output),
                  Write(minus_sign),Write(arrow_k1),Write(arrow_k2),
                  Write(arrow_k3),Write(feedback_arrow),Write(arrow_k4), run_time=2)




        




        


        


    










