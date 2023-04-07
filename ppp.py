from manim import *


class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        square.flip(RIGHT)
        square.rotate(-3 * TAU / 8)
        circle.set_fill(PINK, opacity=0.5)

        self.play(Create(square))
        self.play(Transform(square, circle))
        self.play(FadeOut(square))
    
        


def main():
    ppp = {'aaa': 1, 'bbb': 2}
    # moje_kola = SquareToCircle()
    # moje_kola.construct()
    print(ppp.items())
    print(take(1, ppp.items()))


if __name__ == '__main__':
    main()