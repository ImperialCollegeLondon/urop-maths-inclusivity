from manim import *

def g1(x, y):
    return np.zeros_like(x)

def g2(x, y):
    return np.cos(1.4*x+1)*np.sqrt(y+1)/2+3

def f1(x):
    return 0.1*(x**2)

def f2(x):
    return 4 - (x**2) / 8

SPEED_FACTOR = 1

def generateVolume(axes, start_x, end_x, resolution_density=150):
    ## Side surface
    resolution_x = int((end_x - start_x) * resolution_density / SPEED_FACTOR)
    X = np.linspace(start_x, end_x, resolution_x)
    Y = f1(X)
    pointsTop = axes.c2p(np.vstack([X, Y, g2(X, Y)]).T)
    pointsBot = axes.c2p(np.vstack([X, Y, g1(X, Y)]).T)
    sideSurface = VGroup(*[Line(p0, p1) for (p0, p1) in zip(pointsTop, pointsBot)])

    ## Front surface
    start_y, end_y = f1(end_x), f2(end_x)
    resolution_y = int((end_y - start_y) * resolution_density / SPEED_FACTOR)
    Y = np.linspace(start_y, end_y, resolution_y)
    X = np.ones_like(Y) * end_x # looks like [end_x, end_x, end_x, ...]
    pointsTop = axes.c2p(np.vstack([X, Y, g2(X, Y)]).T)
    pointsBot = axes.c2p(np.vstack([X, Y, g1(X, Y)]).T)
    frontSurface = VGroup(*[Line(p0, p1) for (p0, p1) in zip(pointsTop, pointsBot)])

    ## Top surface
    topSurface = VGroup(
        *[ParametricFunction(
            lambda t : axes.c2p(x, t, g2(x, t)),
            t_range = (f1(x), f2(x))
        ) for x in np.linspace(start_x, end_x, resolution_x)]
    )

    stage = VGroup(topSurface, sideSurface, frontSurface)
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
class AppliedIntegration2(MyThreeDScene):
    
    def construct(self):

#Axes
        axes=ThreeDAxes(
            x_length=6,
            y_length=6,
            z_length=4.5,
            x_range=(-1,6,1),
            y_range=(-1,5,1),
            z_range=(-1,5,1)

        )
        axes_labelx = axes.get_x_axis_label("x")
        axes_labely = axes.get_y_axis_label("y")
        axes_labelz = axes.get_z_axis_label("z")


        axesgroup = VGroup(axes,axes_labelx,axes_labely,axes_labelz)
        axesgroup.shift(2*DOWN+1.5*IN+1.5*LEFT)
#Curves
        curve1 = axes.plot(lambda x: 0.1*(x**2), x_range=[0,5],color = RED)
        curve2 = axes.plot(lambda x: 4 - (x**2) / 8, x_range=[0,5],color = GOLD)

#Surfaces
        def G1(u,v):
            x = u
            y = v
            z = 0
            return axes.c2p(x,y,z)
        
        surface_G1 = Surface(
            G1,
            u_range=(0,5),
            v_range=(0,4),
            resolution=(15,15),
        ).set_style(fill_opacity=0.5)
        surface_G1.set_color_by_gradient(TEAL_E,TEAL_B)

        # Fundamental equation is cos(1.4u+1)*sqrt(v+1)/2+3
        def G2(u,v):
            x = u
            y = v
            z = np.cos(1.4*u+1)*np.sqrt(v+1)/2+3
            return axes.c2p(x,y,z)
         
        surface_G2 = Surface(
            G2,
            u_range=(0,5),
            v_range=(0,4),
            resolution=(15,15),
        ).set_style(fill_opacity=0.5)
        surface_G2.set_color_by_gradient(BLUE_E,BLUE_B)
        surface_G2.z_index = 2

#Initial integration steps
        dz_coord_start = axes.c2p(2,1,1)
        dz_coord_end = axes.c2p(2,1,1.2)
        dz = Line(dz_coord_start,dz_coord_end,color=YELLOW,stroke_width=2.5)

        start_point = axes.c2p(2,1,0)
        end_point = axes.c2p(2,1,np.cos(1.4*2+1)*np.sqrt(1+1)/2+3)
        dzline = Line(start=start_point,end=end_point,color=YELLOW, stroke_width=2.5).set_opacity(0.5)

        dzline2 = Line(start=axes.c2p(3,2,0), end=axes.c2p(3,2,np.cos(1.4*3+1)*np.sqrt(2+1)/2+3), color = YELLOW, stroke_width = 2.5).set_opacity(0.5)
        dzline3 = Line(start=axes.c2p(1,3,0), end=axes.c2p(1,3,np.cos(1.4*1+1)*np.sqrt(3+1)/2+3), color = YELLOW, stroke_width = 2.5).set_opacity(0.5)
        dzline4 = Line(start=start_point,end=end_point,color=YELLOW, stroke_width=2.5).set_opacity(0.5)

        dypoints = [
            [2,1,0],
            ]
        for i in range (0,25):
            x = 2
            y = 1+0.2*(i/24 )
            z = np.cos(1.4*x+1)*np.sqrt(y+1)/2+3
            dypoints.append([x,y,z])
        dypoints.append([2,1.2,0])   
        converted_dy = [axes.c2p(*point) for point in dypoints]
        dy = Polygon(*converted_dy,color=YELLOW).set_fill(YELLOW).set_opacity(0.5)

        ypoints = [
            [2,0.1*4,0],
        ]
        for i in range (0,200):
            x = 2
            y = 0.4+3.1*(i/200)
            z = np.cos(1.4*2+1)*np.sqrt(y+1)/2+3
            ypoints.append([x,y,z])
        ypoints.append([2,3.5,0])
        converted_y = [axes.c2p(*point) for point in ypoints]
        yplane = Polygon(*converted_y,color = YELLOW).set_fill(YELLOW).set_opacity(0.5)

        ypoints2 = [
            [1,0.1,0],
        ]
        for i in range (0,200):
            x = 1
            y = 0.1+3.775*(i/200)
            z = np.cos(1.4*1+1)*np.sqrt(y+1)/2+3
            ypoints2.append([x,y,z])
        ypoints2.append([1,3.875,0])
        converted_y2 = [axes.c2p(*point) for point in ypoints2]
        yplane2 = Polygon(*converted_y2).set_color([MAROON,PURPLE]).set_opacity(0.5)

        ypoints3 = [
            [3,0.9,0],
        ]
        for i in range (0,200):
            x = 3
            y = 0.9+1.975*(i/200)
            z = np.cos(1.4*3+1)*np.sqrt(y+1)/2+3
            ypoints3.append([x,y,z])
        ypoints3.append([3,2.875,0])
        converted_y3 = [axes.c2p(*point) for point in ypoints3]
        yplane3 = Polygon(*converted_y3).set_color([MAROON,PURPLE]).set_opacity(0.5)

        ypoints4 = [
            [2,0.1*4,0],
        ]
        for i in range (0,200):
            x = 2
            y = 0.4+3.1*(i/200)
            z = np.cos(1.4*2+1)*np.sqrt(y+1)/2+3
            ypoints4.append([x,y,z])
        ypoints4.append([2,3.5,0])
        converted_y4 = [axes.c2p(*point) for point in ypoints4]
        yplane4 = Polygon(*converted_y4).set_color([MAROON, PURPLE]).set_opacity(0.5)

#Limit Labels

        G2_label = MathTex(
            "G_2(x,y)", font_size = 30
            )
        G2_label.next_to(surface_G2,RIGHT,buff = 0.5)
        G2_label.rotate(PI/2, axis = RIGHT)
        G2_label.shift(1*DOWN)

        G1_label = MathTex(
            "G_1(x,y)", font_size = 30
            )
        G1_label.next_to(surface_G1,RIGHT,buff = 0.5)
        G1_label.rotate(PI/2, axis = RIGHT)
        G1_label.shift(1*DOWN)

        f2_label = MathTex(
            "g_2(x)", font_size = 30
            )
        f2_label.set_color(GOLD)
        f2_label.next_to(curve2,UP,buff = -0.5)
        
        f1_label = MathTex(
            "g_1(x)", font_size = 30
            )
        f1_label.set_color(RED)
        f1_label.next_to(curve1,DOWN,buff = 0.5)
    # x limits

        x_a_label = MathTex(
            "a", font_size = 30
        )
        x_a_line = DashedLine(
            start = axes.c2p(1,0,0),
            end = axes.c2p(1,3.875,0)
        )
        x_a_label.next_to(x_a_line,DOWN, buff = 0.2)
        x_a = VGroup(x_a_label,x_a_line)

        x_b_label = MathTex(
            "b", font_size = 30
        )
        x_b_line = DashedLine(
            start = axes.c2p(3,0,0),
            end = axes.c2p(3,2.875,0)
        )
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
        delta_z_label.next_to(dz,RIGHT, buff = 0.75)
        delta_z_label.rotate(PI/2, RIGHT)
        delta_z_label.rotate(PI/2,OUT)

        z_integration = MathTex(
            "\int_{z=G_1(x,y)}^{z=G_2(x,y)}\mathrm{d}z", font_size = 36
        )
        z_integration.shift(4*RIGHT+2*UP)
        make_fixed(z_integration)

        delta_y = MathTex("\delta y", font_size = 36).set_color(YELLOW)
        delta_y.next_to(z_integration, buff = 0)
        make_fixed(delta_y)

        dy_label = MathTex("\mathrm{d}y", font_size = 36)
        dy_label.next_to(z_integration, buff = 0)
        make_fixed(dy_label)

        y_integration = MathTex(
            "\int_{y=g_1(x)}^{y=g_2(x)}", font_size = 36
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
            "\int_{x=a}^{x=b}", font_size = 36
        )
        x_integration.next_to(y_integration, LEFT)
        make_fixed(x_integration)

        #Width highlighters

        delta_x_width = Line(start = axes.c2p(1.9, 2, 0), end = axes.c2p(2.1,2, 0), color = MAROON_A, stroke_width = 5 )
        delta_x_width_label = MathTex(
            "\delta x", font_size = 36
        ).set_color(MAROON_A)
        delta_x_width_label.next_to(delta_x_width)

################################  DX HIGHLIGHTER #########################################

        dxplane1 = [
            [1.9,0.361,0],
        ]
        for i in range (0,200):
            x = 1.9
            y = 0.361+3.18775*(i/200)
            z = np.cos(1.4*1.9+1)*np.sqrt(y+1)/2+3
            dxplane1.append([x,y,z])
        dxplane1.append([1.9,3.54875,0])
        converted_dx1 = [axes.c2p(*point) for point in dxplane1]
        dxplane1_final = Polygon(*converted_dx1).set_color([MAROON, PURPLE]).set_opacity(0.5)

        dxplane2 = [
            [2.1,0.441,0],
        ]
        for i in range (0,200):
            x = 2.1
            y = 0.441+3.00775*(i/200)
            z = np.cos(1.4*2.1+1)*np.sqrt(y+1)/2+3
            dxplane2.append([x,y,z])
        dxplane2.append([2.1,3.44875,0])
        converted_dx2 = [axes.c2p(*point) for point in dxplane2]
        dxplane2_final = Polygon(*converted_dx2).set_color([MAROON, PURPLE]).set_opacity(0.5)



################################  THE VOLUME SWEEP  ######################################

        stage1 = generateVolume(axes, 1.9, 2.1)
        stage2 = generateVolume(axes, 1.7, 2.3)
        stage3 = generateVolume(axes, 1.5, 2.5)
        stage4 = generateVolume(axes, 1.25, 2.75)
        stage5 = generateVolume(axes, 1, 3)

        stage1.set_opacity(0.01)
#####################################   RUNNING THE SCENE ##############################

        self.play(Write(generaleq))
        self.wait(2)
        self.play(ReplacementTransform(generaleq,iteq, run_time = 2))
        self.wait(2)
        self.play(ReplacementTransform(iteq,iteq1))
        self.move_camera(phi=70*DEGREES,theta=-30*DEGREES)
        self.play(Create(axesgroup))
        self.play(Write(surface_G1),Write(surface_G2))
        self.play(Write(G2_label),Write(G1_label))
        self.wait(4)
        self.move_camera(phi=90*DEGREES)
        self.add(dz)
        self.play(Write(delta_z_label))
        self.wait(3)
        self.play(Create(dzline),FadeOut(dz),FadeOut(delta_z_label),FadeOut(iteq1))
        self.play(Write(z_integration))
        self.wait(8)
        self.play(ReplacementTransform(dzline,dzline2))
        self.play(ReplacementTransform(dzline2,dzline3))
        self.play(ReplacementTransform(dzline3,dzline4))
        self.wait(5)
        self.move_camera(phi=70*DEGREES,theta=-45*DEGREES)
        self.play(Write(curve1),Write(curve2),Write(f1_label),Write(f2_label))
        self.wait(2)
        self.play(Create(dy),FadeOut(dzline4),Write(delta_y))
        self.wait(5)
        self.remove(G2_label,G1_label)
        self.move_camera(phi=20*DEGREES, theta = -30*DEGREES)
        self.play(ReplacementTransform(dy,yplane,run_time = 3),ReplacementTransform(delta_y,dy_label), Write(y_integration))
        self.remove(surface_G2)
        self.wait(2)        
        self.move_camera(phi=60*DEGREES,theta=-45*DEGREES)
        self.play(yplane.animate.set_color([MAROON,PURPLE]))
        self.play(ReplacementTransform(yplane,yplane2))
        self.play(ReplacementTransform(yplane2,yplane3))
        self.play(ReplacementTransform(yplane3,yplane4))
        self.wait(5)
        self.play(FadeIn(stage1),
            FadeIn(dxplane1_final),
            FadeOut(yplane4),FadeIn(dxplane2_final), Create(delta_x_width),Create(delta_x_width_label), Write(delta_x_label))
        self.play(Write(x_a),Write(x_b))
        self.wait(5)
        self.remove(delta_x_label,delta_x_width,delta_x_width_label)
        self.move_camera(phi=55*DEGREES, theta=-55*DEGREES)
        self.play(FadeOut(dxplane1_final),FadeOut(dxplane2_final),ReplacementTransform(stage1,stage2, run_time = 1.5, rate_func = linear))
        self.play(ReplacementTransform(stage2,stage3, run_time = 1.5, rate_func = linear))
        self.play(Write(x_integration),Write(dx_label))
        self.play(ReplacementTransform(stage3,stage4, run_time = 3, rate_func = linear))
        self.play(ReplacementTransform(stage4,stage5, run_time = 2, rate_func = linear))
        self.wait(1)
        self.play(Create(surface_G2))
        self.play(Uncreate(surface_G2))
        self.wait(5)
    
