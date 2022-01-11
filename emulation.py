import matplotlib.pyplot as plt
import matplotlib.patches as patches
from math import cos, sin, pi

from servo import RobotArm


PI_180 = pi / 180
L1 = 1
L2 = .8
L3 = .8


class Emulation():

    def __init__(self):
        # Servo pos
        self.servo_pos = [0] * 6

        # For the plot
        self.main_angle = 0
        self.x = [0] * 4
        self.y = [0] * 4
        self.pince_angle = 0

        # Init figures
        plt.ion()
        # fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(1, 3)
        _, axd = plt.subplot_mosaic([['upper left', 'right'],
                                     ['lower left', 'right']],
                                    gridspec_kw={
                                        # set the height ratios between the rows
                                        "height_ratios": [1, 1],
                                        # set the width ratios between the columns
                                        "width_ratios": [1, 3],
                                    },
                                    figsize=(6.5, 5.5))
        self.ax1 = axd["upper left"]
        self.ax3 = axd["lower left"]
        self.ax2 = axd["right"]

    def update_pos(self, idx, pos):
        self.servo_pos[idx] = pos

    def update_plot(self):
        self.main_angle = 180 - self.servo_pos[0]

        self.x[1] = -cos(PI_180*self.servo_pos[1])
        self.y[1] = sin(PI_180*self.servo_pos[1])

        self.x[2] = self.x[1] - L2*cos(PI_180*(self.servo_pos[1]+180-self.servo_pos[2]))
        self.y[2] = self.y[1] + L2*sin(PI_180*(self.servo_pos[1]+180-self.servo_pos[2]))

        self.x[3] = self.x[2] - L3*cos(PI_180*(self.servo_pos[1]+180-self.servo_pos[2]+90-self.servo_pos[3]))
        self.y[3] = self.y[2] + L3*sin(PI_180*(self.servo_pos[1]+180-self.servo_pos[2]+90-self.servo_pos[3]))

        self.pince_angle = 90 - self.servo_pos[5]

        arc = patches.Arc((0, 0), 2, 2, 270, 40, 320)
        rectangle = patches.Rectangle((-0.65, -1), 1.30, .25, fill=False)
        self.ax1.clear()
        self.ax1.text(-1, 1, "Servo0: "+str(self.servo_pos[0]), color="blue")
        self.ax1.axis("off")
        self.ax1.axis("equal")
        self.ax1.axis([-1, 1, -1, 1])
        self.ax1.add_patch(arc)
        self.ax1.add_patch(rectangle)

        rectangle = patches.Rectangle((-.5, -.1), .7, .1, color="black")
        self.ax2.clear()
        self.ax2.axis("off")
        self.ax2.axis("equal")
        self.ax2.axis([-3, 3, -3, 3])
        self.ax2.text(-1, 3, "Servo1: "+str(self.servo_pos[1]), color="blue")
        self.ax2.text(-1, 2.7, "Servo2: "+str(self.servo_pos[2]), color="blue")
        self.ax2.text(-1, 2.4, "Servo3: "+str(self.servo_pos[3]), color="blue")
        self.ax2.add_patch(rectangle)

        rectangle = patches.Rectangle((-.5, -.1), .5, .2, color="black")
        self.ax3.clear()
        self.ax3.axis("off")
        self.ax3.axis("equal")
        self.ax3.axis([-1, 1, -1, 1])
        self.ax3.text(-1, 1, "Servo5: "+str(self.servo_pos[5]), color="blue")
        self.ax3.add_patch(rectangle)

        self.ax1.plot([0, cos(PI_180*self.main_angle)], [0, sin(PI_180*self.main_angle)])

        self.ax2.plot(self.x, self.y)

        self.ax3.plot(
            [
                0,
                .5*cos(.5*PI_180*self.pince_angle),
                1,
                .5*cos(.5*PI_180*self.pince_angle),
                0,
                .5*cos(.5*PI_180*self.pince_angle),
                1
            ],
            [
                0,
                .5*sin(.5*PI_180*self.pince_angle),
                .5*sin(.5*PI_180*self.pince_angle),
                .5*sin(.5*PI_180*self.pince_angle),
                0,
                .5*-sin(.5*PI_180*self.pince_angle),
                .5*-sin(.5*PI_180*self.pince_angle)
            ]
        )

        plt.show()
        plt.pause(0.05)


if __name__ == "__main__":
    env = Emulation()
    arm = RobotArm()

    def test():
        arm.update_pos(0, 90, smooth=False)
        arm.update_pos(1, 90, smooth=False)
        arm.update_pos(2, 90, smooth=False)
        arm.update_pos(3, 0, smooth=False)
        arm.update_pos(4, 90, smooth=False)
        arm.update_pos(5, 45, smooth=False)
        print(arm.send_pos(env))
        env.update_plot()
        while True:
            print(env.pince_angle)
            print("Enter pin")
            pin = int(input())
            print("Enter new pos")
            pos = int(input())
            arm.update_pos(pin, pos, smooth=False)
            print(arm.send_pos(env))
            env.update_plot()

    test()
