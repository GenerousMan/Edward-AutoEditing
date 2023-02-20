import json

class Frame:

    def __init__(self, frame_number):
        self.frame_number = frame_number

        self.alphapose = {}
        self.roi = [0, 0, 0, 0]
        self.comb_data = []

        self.view = ''
        self.pose = ''
        self.direction = ''
        self.motion = ''

    def __str__(self):
        return 'Frame {}'.format(frame_number)