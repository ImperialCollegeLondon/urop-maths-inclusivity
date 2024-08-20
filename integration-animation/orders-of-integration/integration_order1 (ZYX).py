from manim import *

def g1(x, y):
    return np.zeros_like(x)

def g2(x, y):
    return x

def f1(x):
    return x**2

def f2(x):
    return 1

SPEED_FACTOR = 1

def generateVolume(axes, start_x, end_x, resolution_density=250):
    ## Side surface
    resolution_x = int((end_x - start_x) * resolution_density / SPEED_FACTOR) + 1
    X = np.linspace(start_x, end_x, resolution_x)
    Y = f1(X)
    pointsTop = axes.c2p(np.vstack([X, Y, X]).T)
    pointsBot = axes.c2p(np.vstack([X, Y, g1(X, Y)]).T)
    sideSurface = VGroup(*[Line(p0, p1) for (p0, p1) in zip(pointsTop, pointsBot)])

    ## Front surface
    start_y, end_y = f1(end_x), f2(end_x)
    resolution_y = int((end_y - start_y) * resolution_density / SPEED_FACTOR) + 1
    Y = np.linspace(start_y, end_y, resolution_y)
    X = np.ones_like(Y) * end_x # looks like [end_x, end_x, end_x, ...]
    pointsTop = axes.c2p(np.vstack([X, Y, g2(X, Y)]).T)
    pointsBot = axes.c2p(np.vstack([X, Y, g1(X, Y)]).T)
    if resolution_y == 1:
        frontSurface = Line(pointsTop, pointsBot)
    else:
        frontSurface = VGroup(*[Line(p0, p1) for (p0, p1) in zip(pointsTop, pointsBot)])

    ## Top surface
    topSurface = VGroup(
        *[ParametricFunction(
            lambda t : axes.c2p(x, t, g2(x, t)),
            t_range = (f1(x), f2(x))
        ) for x in np.linspace(start_x, end_x, resolution_x)]
    )

    stage = VGroup(topSurface, sideSurface, 
                   frontSurface
                   )
    stage.z_index = 1
    stage.set_submobject_colors_by_gradient(MAROON,PURPLE)
    return stage

############################ SOME CONFIGURATION#########################
class MyCamera(ThreeDCamera):
    def transform_points_pre_display(self, mobject, points):
        if getattr(mobject, "fixed", False):
            return points
        else:
            return super().transform_points_pre_display(mobject, points)
      
class MyThreeDScene(ThreeDScene):
    def __init__(self, camera_class=MyCamera, ambient_camera_rotation=None,
                 default_angled_camera_orientation_kwargs=None, **kwargs):
        super().__init__(camera_class=camera_class, **kwargs)

def make_fixed(*mobs):
    for mob in mobs:
        mob.fixed = True
        for submob in mob.family_members_with_points():
            submob.fixed = True

#################### MAIN ####################################################
class NewIntegrationOrder1(MyThreeDScene):
    
    def construct(self):

#Axes
        axes=ThreeDAxes(
            x_length=6,
            y_length=6,
            z_length=4.5,
            x_range=(-0.5,1.5,1),
            y_range=(-0.5,1.5,1),
            z_range=(-0.5,1.5,1)

        )
        axes_labelx = axes.get_x_axis_label("x")
        axes_labely = axes.get_y_axis_label("y")
        axes_labelz = axes.get_z_axis_label("z")


        axesgroup = VGroup(axes,axes_labelx,axes_labely,axes_labelz)
#Curves
        curve1 = axes.plot(lambda x: x**2, x_range=[0,1.2],color = RED)
        curve2 = axes.plot(lambda x: 1, x_range=[0,1.5],color = GOLD)

#Surfaces
        def G1(u,v):
            x = u
            y = v
            z = 0
            return axes.c2p(x,y,z)
        
        surface_G1 = Surface(
            G1,
            u_range=(0,1.5),
            v_range=(0,1.5),
            resolution=(15,15),
        ).set_style(fill_opacity=0.3)
        surface_G1.set_color(GREY)

        # Fundamental equation is cos(1.4u+1)*sqrt(v+1)/2+3
        def G2(u,v):
            x = u
            y = v
            z = u
            return axes.c2p(x,y,z)
         
        surface_G2 = Surface(
            G2,
            u_range=(0,1.5),
            v_range=(0,1.5),
            resolution=(15,15),
        ).set_style(fill_opacity=0.3)
        surface_G2.set_color_by_gradient(BLUE_E,BLUE_B)
        surface_G2.z_index = 2

#Initial integration steps
        dz_coord_start = axes.c2p(0.5,0.5,0.15)
        dz_coord_end = axes.c2p(0.5,0.5,0.25)
        dz = Line(dz_coord_start,dz_coord_end,color=YELLOW,stroke_width=2.5)

        start_point = axes.c2p(0.5,0.5,0)
        end_point = axes.c2p(0.5,0.5,0.5)
        dzline = Line(start=start_point,end=end_point,color=YELLOW, stroke_width=2.5).set_opacity(0.5)

        dypoints = [
            [0.5,0.5,0],
            [0.5,0.5,0.5],
            [0.5,0.55,0.5],
            [0.5,0.55,0]
            ]
        converted_dy = [axes.c2p(*point) for point in dypoints]
        dy = Polygon(*converted_dy,color=YELLOW).set_fill(YELLOW).set_opacity(0.5)

        ypoints = [
            [0.5,0.25,0],
            [0.5,0.25,0.5],
            [0.5,1,0.5],
            [0.5,1,0]
        ]
        converted_y = [axes.c2p(*point) for point in ypoints]
        yplane = Polygon(*converted_y,color = YELLOW).set_fill(YELLOW).set_opacity(0.5)


#Limit Labels

        G2_label = MathTex(
            "z=x", font_size = 30
            )
        G2_label.next_to(surface_G2,OUT,buff = -0.5)
        G2_label.rotate(PI/2, axis = RIGHT)
        G2_label.shift(1*DOWN)

        G1_label = MathTex(
            "z=0", font_size = 30
            )
        G1_label.next_to(surface_G1,RIGHT,buff = 0.5)
        G1_label.rotate(PI/2, axis = RIGHT)
        G1_label.shift(1*DOWN)

        f2_label = MathTex(
            r"y=1", font_size = 30
            )
        f2_label.set_color(GOLD)
        f2_label.next_to(curve2,UP,buff = -0.5)
        
        f1_label = MathTex(
            "y=x^2", font_size = 30
            )
        f1_label.set_color(RED)
        f1_label.next_to(curve1,DOWN,buff = 0.5)
    # x limits

        x_a_label = MathTex(
            "0", font_size = 30
        ).set_color(BLUE)
        x_a_line = DashedLine(
            start = axes.c2p(0,0,0),
            end = axes.c2p(0,1.5,0)
        ).set_color(BLUE)
        x_a_label.next_to(x_a_line,DOWN, buff = 0.2)
        x_a = VGroup(x_a_label,x_a_line)

        x_b_label = MathTex(
            "1", font_size = 30
        ).set_color(BLUE)
        x_b_line = DashedLine(
            start = axes.c2p(1,0,0),
            end = axes.c2p(1,1.5,0)
        ).set_color(BLUE)
        x_b_label.next_to(x_b_line,DOWN, buff = 0.2)
        x_b = VGroup(x_b_label,x_b_line)

################################  MAIN LATEX  ############################################

        # Fundamental equations
        generaleq = MathTex(
            " \int_{R} \mathrm{d}V"
        )

        iteq = MathTex(
            " \int_{x}\int_{y}^{}\int_{z} \mathrm{ d}z\mathrm{d}y\mathrm{d}x"
        )

        iteq1 = MathTex(
            " \int_{x=a}^{x=b}\int_{y=g_1(x)}^{y=g_2(x)}\int_{z=G_1(x,y)}^{z=G_2(x,y)} \mathrm{ d}z\mathrm{d}y\mathrm{d}x"
        )

        iteq1.scale(0.75)
        iteq1.to_corner(UR)
        make_fixed(iteq1)

        #Animation equations

        delta_z_label = MathTex("\delta z", font_size = 36)
        delta_z_label.next_to(dz,RIGHT, buff = 0.1)
        delta_z_label.rotate(PI/2, RIGHT)
        delta_z_label.rotate(PI/2,OUT)

        z_integration = MathTex(
            "\int_{z=0}^{z=x}\mathrm{d}z", font_size = 36
        )
        z_integration.shift(4*RIGHT+3*DOWN)
        make_fixed(z_integration)

        delta_y = MathTex("\delta y", font_size = 36).set_color(YELLOW)
        delta_y.next_to(z_integration, buff = 0)
        make_fixed(delta_y)

        dy_label = MathTex("\mathrm{d}y", font_size = 36)
        dy_label.next_to(z_integration, buff = 0)
        make_fixed(dy_label)

        y_integration = MathTex(
            r"\int_{y=x^2}^{y=1}", font_size = 36
        )
        y_integration.next_to(z_integration,LEFT)
        make_fixed(y_integration)

        delta_x_label = MathTex(
            "\delta x", font_size = 36
        ).set_color_by_gradient(MAROON,PURPLE)
        delta_x_label.next_to(dy_label, buff = 0)
        make_fixed(delta_x_label)

        dx_label = MathTex(
            "\mathrm{d}x", font_size = 36
        )
        dx_label.next_to(dy_label,RIGHT, buff = 0)
        make_fixed(dx_label)

        x_integration = MathTex(
            "\int_{x=0}^{x=1}", font_size = 36
        )
        x_integration.next_to(y_integration, LEFT)
        make_fixed(x_integration)

        #Width highlighters

        delta_x_width = Line(start = axes.c2p(1.9, 2, 0), end = axes.c2p(2.1,2, 0), color = MAROON_A, stroke_width = 5 )
        delta_x_width_label = MathTex(
            "\delta x", font_size = 36
        ).set_color(MAROON_A)
        delta_x_width_label.next_to(delta_x_width)

################################  THE VOLUME SWEEP  ######################################

        stage1 = generateVolume(axes, 0.48, 0.52)
        stage2 = generateVolume(axes, 0.35, 0.65)
        stage3 = generateVolume(axes, 0.25, 0.75)
        stage4 = generateVolume(axes, 0.1,0.9)
        stage5 = generateVolume(axes, 0.0, 0.99)

#####################################   RUNNING THE SCENE ##############################

        self.move_camera(phi=70*DEGREES,theta=-55*DEGREES)
        self.play(Create(axesgroup))
        self.play(Write(surface_G1),Write(surface_G2))
        self.play(Write(G2_label),Write(G1_label))
        self.wait(4)
        self.play(Write(curve1),Write(curve2),Write(f1_label),Write(f2_label))
        self.wait(2)
        self.add(dz)
        self.play(Write(delta_z_label))
        self.wait(3)
        self.play(Create(dzline),FadeOut(dz),FadeOut(delta_z_label))
        self.play(Write(z_integration))
        self.wait(4)
        self.move_camera(phi=70*DEGREES,theta=-45*DEGREES)
        self.play(Create(dy),Write(delta_y))
        self.remove(dzline)
        self.wait(5)
        self.remove(G2_label,G1_label)
        self.play(ReplacementTransform(dy,yplane,run_time = 3),ReplacementTransform(delta_y,dy_label),Write(y_integration))
        self.remove(surface_G2)
        self.wait(2)        
        self.play(FadeOut(yplane),FadeIn(stage1),Write(delta_x_label))
        self.wait(4)
        self.move_camera(theta=-90*DEGREES, phi = 60*DEGREES)
        self.play(Write(x_a),Write(x_b))
        self.wait(5)
        self.play(ReplacementTransform(stage1,stage2, run_time = 1.5, rate_func = linear))
        self.play(ReplacementTransform(stage2,stage3, run_time = 1.5, rate_func = linear),ReplacementTransform(delta_x_label,dx_label),Write(x_integration))
        self.play(ReplacementTransform(stage3,stage4, run_time = 1.5, rate_func = linear))
        self.play(ReplacementTransform(stage4,stage5, run_time = 1.5, rate_func = linear))
        self.wait(1)
        self.play(Create(surface_G2))
        self.play(Uncreate(surface_G2))
        self.wait()
        self.move_camera(theta = -105*DEGREES, phi = 60*DEGREES)
        self.wait(5)
    
