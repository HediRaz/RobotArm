import argparse
from servo import RobotArm
from servo.emulation import Emulation
from tracking import handtracking_lever
from tracking import armtracking
from tracking import handtracking_realistic


parser = argparse.ArgumentParser()
parser.add_argument("--emulation", action="store_true", help="display robot arm emulation")
parser.add_argument("--program", default="hand tracking", type=str, help="wich program to launch")
args = parser.parse_args()

arm = RobotArm()
env = None if not args.emulation else Emulation()

if args.program == "hand tracking":
    handtracking_lever.hand_tracking(arm, env=env)
elif args.program == "arm tracking":
    armtracking.arm_tracking()
