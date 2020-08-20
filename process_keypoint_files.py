import json
import math
import os
import re

import cv2
import numpy as np


class Pose:
    pose_keypoints_3d = []
    keypoint_map = {"Nose": 0,
                    "Neck": 1,
                    "RShoulder": 2,
                    "RElbow": 3,
                    "RWrist": 4,
                    "LShoulder": 5,
                    "LElbow": 6,
                    "LWrist": 7,
                    "MidHip": 8,
                    "RHip": 9,
                    "RKnee": 10,
                    "RAnkle": 11,
                    "LHip": 12,
                    "LKnee": 13,
                    "LAnkle": 14,
                    "REye": 15,
                    "LEye": 16,
                    "REar": 17,
                    "LEar": 18,
                    "LBigToe": 19,
                    "LSmallToe": 20,
                    "LHeel": 21,
                    "RBigToe": 22,
                    "RSmallToe": 23,
                    "RHeel": 24,
                    "Background": 25}

    def __init__(self, directory, keypoint_file):
        with open(directory + keypoint_file) as f:
            data = json.load(f)
            self.pose_keypoints_3d = data["people"][0]["pose_keypoints_3d"]

    def get_keypoint(self, part):
        kp_start_idx = self.keypoint_map[part] * 4
        return np.array([self.pose_keypoints_3d[kp_start_idx],
                         self.pose_keypoints_3d[kp_start_idx + 1],
                         self.pose_keypoints_3d[kp_start_idx + 2]])

    def calculate_angle(self, point1, point2, point3):
        if (point1[0] == 0 and point1[1] == 0 and point1[2] == 0) or \
                (point2[0] == 0 and point2[1] == 0 and point2[2] == 0) or \
                (point3[0] == 0 and point3[1] == 0 and point3[2] == 0):
            return 0

        ba = point1 - point2
        bc = point3 - point2

        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        return np.degrees(np.arccos(cosine_angle))

    # returns 3 keypoints containing the joint
    def get_points_containing_joint(self, joint):
        if joint == 'LElbow':
            return [self.get_keypoint('LShoulder'),
                    self.get_keypoint('LElbow'),
                    self.get_keypoint('LWrist')]
        elif joint == 'RElbow':
            return [self.get_keypoint('RShoulder'),
                    self.get_keypoint('RElbow'),
                    self.get_keypoint('RWrist')]
        elif joint == 'LShoulder':
            return [self.get_keypoint('Neck'),
                    self.get_keypoint('LShoulder'),
                    self.get_keypoint('LElbow')]
        elif joint == 'RShoulder':
            return [self.get_keypoint('Neck'),
                    self.get_keypoint('RShoulder'),
                    self.get_keypoint('RElbow')]
        elif joint == 'LHip':
            return [self.get_keypoint('MidHip'),
                    self.get_keypoint('LHip'),
                    self.get_keypoint('LKnee')]
        elif joint == 'RHip':
            return [self.get_keypoint('MidHip'),
                    self.get_keypoint('RHip'),
                    self.get_keypoint('RKnee')]
        elif joint == 'LKnee':
            return [self.get_keypoint('LHip'),
                    self.get_keypoint('LKnee'),
                    self.get_keypoint('LAnkle')]
        elif joint == 'RKnee':
            return [self.get_keypoint('RHip'),
                    self.get_keypoint('RKnee'),
                    self.get_keypoint('RAnkle')]

    def get_angle(self, joint):
        points = self.get_points_containing_joint(joint)
        return self.calculate_angle(points[0], points[1], points[2])


if __name__ == '__main__':
    directory = 'C:\\Users\\hkecl\\OneDrive\\Documents\\Summer2020Research\\openpose\\keypoints1\\'
    keypoint_files = [name for name in os.listdir(directory)]
    keypoint_files.sort(key = lambda x: int(x.split('_')[0]))
    angleListDict = {
        "LKnee": {},
        "RKnee": {},
        "LHip": {},
        "RHip": {},
        "LShoulder": {},
        "RShoulder": {},
        "LElbow": {},
        "RElbow": {}


    }

    for i in range(0, len(keypoint_files), 2):
        pose_left = Pose(directory, keypoint_files[i])
        accuracy = 0
        #exact_angles = [180, 180, 128, 160, 105, 90, 70, 60, 50, 38, 54]
        exact_angles = [180, 180, 180, 30, 90, 90, 90, 121, 121, 121, 36.5, 36.5, 36.5]
        if pose_left and i<len(keypoint_files) and len(pose_left.pose_keypoints_3d)>0:
            #pose_right = Pose(directory, keypoint_files[i + 1])
            frame_id = re.sub('\D', '', keypoint_files[i])
            filename = 'C:\\Users\\hkecl\\OneDrive\\Documents\\Summer2020Research\\openpose\\examples\\media\\' + str(
                frame_id) + '.jpg'
            image = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
            position = (10, 50)
            for key in angleListDict:
                angle = pose_left.get_angle(key)
                if key =='LElbow':
                    accuracy += pow(exact_angles[i//2] - angle, 2)
                angleListDict[key][frame_id] = angle
                cv2.putText(
                    image,  # numpy array on which text is written
                    key + ': ' + str(angle),  # text
                    position,  # position at which writing has to start
                    cv2.FONT_HERSHEY_SIMPLEX,  # font family
                    0.5,  # font size
                    (209, 80, 0, 255),  # font color
                    1)  # font stroke
                updated_y = position[1] + 15
                position = (10, updated_y)
            out_file = 'C:\\Users\\hkecl\\OneDrive\\Documents\\Summer2020Research\\openpose\\examples\\media_copy\\multiview_angles\\' \
                       + str(frame_id) + '.jpg'
            cv2.imwrite(out_file, image)
        else:
            print (i)

    print(math.sqrt(accuracy)*2/len(keypoint_files))
    with open('angles.json', 'w') as fp:
        json.dump(angleListDict, fp)
