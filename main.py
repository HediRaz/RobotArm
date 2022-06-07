from servo import RobotArm
from servo.emulation import Emulation
from tracking import handtracking_lever


arm = RobotArm()
env = Emulation()


handtracking_lever.hand_tracking(arm, env)
