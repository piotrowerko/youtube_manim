from manim import *


# Correction shown while recording 16 says "od x równego minus 1": the outer
# integral of K2 runs over x from -2 to 0. Drawn inside a band of the 1920x1080
# frame (px x 560..1360, y 280..480), empty at that moment; cropped with ffmpeg
# and laid over the main scene.
#
#   manim -qh --frame_rate 30 x_limit_fix.py XLimitFix
#   ffmpeg -i XLimitFix.mp4 -vf crop=800:200:560:280 ...

DURATION = 4.0


def px(x, y):
    return np.array([(x - 960) / 1920 * config.frame_width, (540 - y) / 1080 * config.frame_height, 0])


class XLimitFix(Scene):
    def construct(self):
        fix = MathTex(r"{}^{*}\;\; x \in [-2,\; 0]", font_size=84, color=ORANGE)
        fix.move_to(px(960, 380))
        self.play(FadeIn(fix, scale=1.3), run_time=0.35)
        self.play(Indicate(fix, color=ORANGE, scale_factor=1.08), run_time=0.8)
        self.wait(DURATION - 0.35 - 0.8 - 0.4)
        self.play(FadeOut(fix), run_time=0.4)
