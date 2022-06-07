# Emulation to see what the hand would be doing if connected. 
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from math import cos, sin, pi

from servo.servo import RobotArm


PI_180 = pi / 180
L1 = 1
L2 = .8
L3 = .8


class Emulation():

    def __init__(self):
        # Servo positions
        self.servo_pos = [0] * 6

        # Some variables for the plot
        self.main_angle = 0
        self.x = [0] * 4
        self.y = [0] * 4
        self.clamp_angle = 0

        # Initialize the plot
        plt.ion()
        _, axd = plt.subplot_mosaic([["upper left", "right"],
                                    ["middle", "right"],
                                    ["lower left", "right"]],
                                    gridspec_kw={
                                        # set the height ratios between the rows
                                        "height_ratios": [1, 1, 1],
                                        # set the width ratios between the columns
                                        "width_ratios": [1, 3],
                                    },
                                    figsize=(6.5, 5.5))
        self.ax1 = axd["upper left"]
        self.ax2 = axd["right"]
        self.ax3 = axd["lower left"]
        self.ax4 = axd["middle"]

        # Define patches
        self.ax1_arc = patches.Arc((0, 0), 2, 2, 270, 40, 320)
        self.ax1_rectangle = patches.Rectangle((-0.65, -1), 1.30, .25, fill=False)
        self.ax2_rectangle = patches.Rectangle((-.5, -.1), .7, .1, color="black")
        self.ax3_rectangle = patches.Rectangle((-.5, -.1), .5, .2, color="black")

    def update_pos(self, idx, pos):
        """ Update position of servo idx to pos """
        self.servo_pos[idx] = pos

    def update_plot(self):
        """ Update the plot """
        self.main_angle = 180 - self.servo_pos[0]

        angle1 = PI_180*self.servo_pos[1]
        angle2 = PI_180*(self.servo_pos[1]+180-self.servo_pos[2])
        angle3 = PI_180*(self.servo_pos[1]+180-self.servo_pos[2]+90-self.servo_pos[3])

        self.x[1] = -cos(angle1)
        self.y[1] = sin(angle1)

        self.x[2] = self.x[1] - L2*cos(angle2)
        self.y[2] = self.y[1] + L2*sin(angle2)

        self.x[3] = self.x[2] - L3*cos(angle3)
        self.y[3] = self.y[2] + L3*sin(angle3)

        self.claw_angle = 90 - self.servo_pos[5]

        self.ax1.clear()
        self.ax1.text(-1, 1, "Servo0: "+str(self.servo_pos[0]), color="blue")
        self.ax1.axis("off")
        self.ax1.axis("equal")
        self.ax1.axis([-1, 1, -1, 1])
        self.ax1.add_patch(self.ax1_arc)
        self.ax1.add_patch(self.ax1_rectangle)

        self.ax2.clear()
        self.ax2.axis("off")
        self.ax2.axis("equal")
        self.ax2.axis([-3, 3, -3, 3])
        self.ax2.text(-1, 3, "Servo1: "+str(self.servo_pos[1]), color="blue")
        self.ax2.text(-1, 2.7, "Servo2: "+str(self.servo_pos[2]), color="blue")
        self.ax2.text(-1, 2.4, "Servo3: "+str(self.servo_pos[3]), color="blue")
        self.ax2.add_patch(self.ax2_rectangle)

        self.ax3.clear()
        self.ax3.axis("off")
        self.ax3.axis("equal")
        self.ax3.axis([-1, 1, -1, 1])
        self.ax3.text(-1, 1, "Servo5: "+str(self.servo_pos[5]), color="blue")
        self.ax3.add_patch(self.ax3_rectangle)

        self.ax4.clear()
        self.ax4.axis("off")
        self.ax4.axis("equal")
        self.ax4.axis([-1, 1, -1, 1])
        self.ax4.text(-1, 1, "Servo4: "+str(self.servo_pos[4]), color="blue")

        self.ax1.plot([0, cos(PI_180*self.main_angle)], [0, sin(PI_180*self.main_angle)])

        self.ax2.plot(self.x, self.y)

        self.ax3.plot(
            [0, .5*cos(.5*PI_180*self.claw_angle), 1],
            [
                [0, 0],
                [.5*sin(.5*PI_180*self.claw_angle), .5*-sin(.5*PI_180*self.claw_angle)],
                [.5*sin(.5*PI_180*self.claw_angle), .5*-sin(.5*PI_180*self.claw_angle)]
            ]
        )

        claw_angle2 = PI_180 * (90 - self.servo_pos[4])
        self.ax4.plot(
            [-cos(claw_angle2), cos(claw_angle2)],
            [-sin(claw_angle2), sin(claw_angle2)]
        )

        plt.draw()
        plt.pause(0.0005)


def main():
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
            print(env.claw_angle)
            print("Enter pin")
            pin = int(input())
            print("Enter new pos")
            pos = int(input())
            arm.update_pos(pin, pos, smooth=False)
            print(arm.send_pos(env))
            env.update_plot()

    test()
