import manim as mn


class SquareToCircle(mn.Scene):
    # def __init__(self):
    #     super().__init__()
    
    def construct(self):
        self.circle = mn.Circle(mn.BLUE)            # create a circle
        self.circle.set_fill(mn.BLUE, opacity=0.5)  # set the color and transparency
        #self.play(mn.ShowCreation(circle))     # show the circle on screen


def main():
    moje_kolo = SquareToCircle()
    moje_kolo.construct()
    moje_kolo.play(mn.ShowCreation(moje_kolo.circle))

if __name__ == '__main__':
    main()