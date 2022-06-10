import cv2
import mediapipe as mp
import math
from servo.servo import RobotArm
from servo.emulation import Emulation


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands


def get_coordinates_from_pose_results(results, idx):
    x = results.pose_landmarks.landmark[idx].x
    y = results.pose_landmarks.landmark[idx].y
    z = results.pose_landmarks.landmark[idx].z
    return x, y, z


def get_coordinates_from_hand_results(results, idx):
    x = results.multi_hand_landmarks[0].landmark[idx].x
    y = results.multi_hand_landmarks[0].landmark[idx].y
    z = results.multi_hand_landmarks[0].landmark[idx].z
    return x, y, z


def coords_to_vec(coords1, coords2):
    return coords2[0]-coords1[0], coords2[1]-coords1[1], coords2[2]-coords1[2]


def norm(coords):
    return math.sqrt(coords[0]**2 + coords[1]**2 + coords[2]**2)


def scalar_product(coords1, coords2):
    return coords1[0]*coords2[0] + coords1[1]*coords2[1] + coords1[2]*coords2[2]


def compute_angle(coords1, coords2):
    cosinus = scalar_product(coords1, coords2) / (norm(coords1)*norm(coords2))
    return int((180 / math.pi) * math.acos(cosinus))


def _angle_pipeline0(pose_results, hand_results):
    coords1 = get_coordinates_from_pose_results(pose_results, 13)
    coords2 = get_coordinates_from_pose_results(pose_results, 15)
    v = coords_to_vec(coords1, coords2)
    v = (v[0], 0, v[2])
    return 180 - compute_angle(v, (1, 0, 0))


def _angle_pipeline1(pose_results, hand_results):
    coords1 = get_coordinates_from_pose_results(pose_results, 11)
    coords2 = get_coordinates_from_pose_results(pose_results, 15)
    coords3 = get_coordinates_from_pose_results(pose_results, 12)
    v1 = coords_to_vec((coords1[0], 0, coords1[2]), (coords2[0], 0, coords2[2]))
    v2 = coords_to_vec(coords1, coords3)
    n1 = norm(v1)
    n2 = norm(v2)
    return (n1 / n2) * 40


def _angle_pipeline2(pose_results, hand_results):
    coords1 = get_coordinates_from_pose_results(pose_results, 11)
    coords2 = get_coordinates_from_pose_results(pose_results, 15)
    coords3 = get_coordinates_from_pose_results(pose_results, 12)
    v1 = coords_to_vec((0, coords1[1], 0), (0, coords2[1], 0))
    v2 = coords_to_vec(coords1, coords3)
    n1 = norm(v1)
    n2 = norm(v2)
    return 180 - (n1 / n2) * 100


def _angle_pipeline3(pose_results, hand_results):
    coords1 = get_coordinates_from_hand_results(hand_results, 0)
    coords2 = get_coordinates_from_hand_results(hand_results, 12)
    coords3 = get_coordinates_from_pose_results(pose_results, 13)
    coords4 = get_coordinates_from_pose_results(pose_results, 15)
    v12 = coords_to_vec(coords1, coords2)
    v34 = coords_to_vec(coords3, coords4)
    sign = 1 if v12[1] > v34[1] else -1
    return 180 - (90 + sign * compute_angle(v12, v34))


def _angle_pipeline4(pose_results, hand_results):
    coords1 = get_coordinates_from_hand_results(hand_results, 5)
    coords2 = get_coordinates_from_hand_results(hand_results, 17)
    v12 = coords_to_vec(coords1, coords2)
    sign = (coords1[1]-coords2[1])/abs(coords1[1]-coords2[1])
    return 90 + sign*compute_angle((v12[0], v12[1], 0), (1, 0, 0))


def _angle_pipeline5(pose_results, hand_results):
    coords1 = get_coordinates_from_hand_results(hand_results, 4)
    coords2 = get_coordinates_from_hand_results(hand_results, 8)
    coords3 = get_coordinates_from_hand_results(hand_results, 0)
    coords4 = get_coordinates_from_hand_results(hand_results, 9)
    v12 = coords_to_vec(coords1, coords2)
    v34 = coords_to_vec(coords3, coords4)
    n1 = norm(v12)
    n2 = norm(v34)
    return 120 - (n1/n2)*110


def update_pos(arm, pose_results, hand_results, env=None):
    if pose_results.pose_landmarks:
        arm.update_pos(0, _angle_pipeline0(pose_results, hand_results))
        arm.update_pos(1, _angle_pipeline1(pose_results, hand_results))
        arm.update_pos(2, _angle_pipeline2(pose_results, hand_results))
        if hand_results.multi_hand_landmarks:
            arm.update_pos(3, _angle_pipeline3(pose_results, hand_results))
            arm.update_pos(4, _angle_pipeline4(pose_results, hand_results))
            arm.update_pos(5, _angle_pipeline5(pose_results, hand_results))

            arm.send_pos(env)

        if env is not None:
            env.update_plot()


def draw_annotations(image, pose_results, hand_results):
    # Draw the pose annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if pose_results.pose_landmarks:
        mp_drawing.draw_landmarks(
            image,
            pose_results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))


def arm_tracking(arm, env=None):
    cap = cv2.VideoCapture(0)
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1024)

    with mp_pose.Pose(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as pose, mp_hands.Hands(
        model_complexity=0,
        max_num_hands=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as hands:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                raise ValueError("Empty camera frame")

            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pose_results = pose.process(image)
            hand_results = hands.process(image)

            # Compute angles and send them to Arduino
            update_pos(arm, pose_results, hand_results, env)

            # Draw the hand annotations on the image.
            draw_annotations(image, pose_results, hand_results)

            if cv2.waitKey(5) & 0xFF == 27:
                break
        cap.release()
