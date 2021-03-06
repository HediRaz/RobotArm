# Usefull classes to simply control servos with Python
# The RobootArm class has been especially designed to control the robot arm in the HubIA of CentraleSupélec
from servo.comm import sendPosToArduino


class Servo():

    def __init__(self, idx, pos_buffer_size=20):
        """
        Servo class
        pos_buffer is to avoid making sudden movements

        """
        self.idx = idx
        self.pos = 0
        self.pos_buffer_size = pos_buffer_size
        self.pos_buffer = [0] * pos_buffer_size

    def update_pos(self, pos, smooth=True):
        """ Update the position of the servo
        Args:
        pos (int): new position of the servo
        smooth (bool): if True, the position is updated by averaging the last

        """
        if smooth:
            self.pos_buffer.pop(0)
            self.pos_buffer.append(pos)
        else:
            self.pos_buffer = [pos] * self.pos_buffer_size
        self.pos = int(sum(self.pos_buffer)/self.pos_buffer_size)


class RobotArm():

    def __init__(self, pos_buffer_size=20):
        """
        Create a RobotArm object with 6 servos designed for the HubIA of CentraleSupélec

        """
        self.pos_buffer_size = pos_buffer_size
        self.servos = [Servo(i, pos_buffer_size=pos_buffer_size) for i in range(6)]
        self.servos[5] = Servo(5, 3)
        self.servos[0].update_pos(90, smooth=False)  # at bottom
        self.servos[1].update_pos(90, smooth=False)  # first arm
        self.servos[2].update_pos(90, smooth=False)  # second arm
        self.servos[3].update_pos(90, smooth=False)  # third arm
        self.servos[4].update_pos(90, smooth=False)  # hand rotation
        self.servos[5].update_pos(45, smooth=False)  # hand

        self.send_pos()

    def check_pos(self):
        """
        So the robot can't harm the table

        """
        self.servos[0].pos = max(0, self.servos[0].pos)
        self.servos[1].pos = max(0, self.servos[1].pos)
        self.servos[2].pos = max(10 + self.servos[1].pos, self.servos[2].pos, 45)
        self.servos[3].pos = int(max(10 + 90 - .5*self.servos[2].pos - 90 + self.servos[1].pos, self.servos[3].pos))
        self.servos[4].pos = max(0, self.servos[4].pos)
        self.servos[5].pos = max(0, self.servos[5].pos)

        self.servos[0].pos_buffer[-1] = max(0, self.servos[0].pos_buffer[-1])
        self.servos[1].pos_buffer[-1] = max(0, self.servos[1].pos_buffer[-1])
        self.servos[2].pos_buffer[-1] = max(self.servos[1].pos_buffer[-1], self.servos[2].pos_buffer[-1], 45)
        self.servos[3].pos_buffer[-1] = int(max(90 - .5*self.servos[2].pos_buffer[-1] - 90 + self.servos[1].pos_buffer[-1], self.servos[3].pos_buffer[-1]))
        self.servos[4].pos_buffer[-1] = max(0, self.servos[4].pos_buffer[-1])
        self.servos[5].pos_buffer[-1] = max(0, self.servos[5].pos_buffer[-1])

        self.servos[0].pos = min(180, self.servos[0].pos)
        self.servos[1].pos = min(180, self.servos[1].pos)
        self.servos[2].pos = min(180, self.servos[2].pos)
        self.servos[3].pos = min(180 - (90 - self.servos[2].pos + abs(90 - self.servos[1].pos)), self.servos[3].pos_buffer[-1])
        self.servos[4].pos = min(180, self.servos[4].pos)
        self.servos[5].pos = min(90, self.servos[5].pos)

        self.servos[0].pos_buffer[-1] = min(180, self.servos[0].pos_buffer[-1])
        self.servos[1].pos_buffer[-1] = min(180, self.servos[1].pos_buffer[-1])
        self.servos[2].pos_buffer[-1] = min(180, self.servos[2].pos_buffer[-1])
        self.servos[3].pos_buffer[-1] = min(180 - (90 - self.servos[2].pos_buffer[-1] + abs(90 - self.servos[1].pos_buffer[-1])), self.servos[3].pos)
        self.servos[4].pos_buffer[-1] = min(180, self.servos[4].pos_buffer[-1])
        self.servos[5].pos_buffer[-1] = min(90, self.servos[5].pos_buffer[-1])

    def update_pos(self, idx, pos, smooth=True):
        """ Update the position of a servo 
        Args:
        idx (int): index of the servo
        pos (int): new position of the servo
        smooth (bool): if True, the position is updated by averaging the last
        """
        self.servos[idx].update_pos(pos, smooth)

    def send_pos(self, env=None):
        """ Send the position of all servos to the Arduino
        Args:
        env (optional)(str): environment to send the position to
                the environnement must have a method update_pos(idx, pos)
        """
        self.check_pos()
        if env is not None:
            for servo in self.servos:
                env.update_pos(servo.idx, servo.pos)
        return sendPosToArduino([servo.pos for servo in self.servos])
