import json
from datetime import datetime


class ActionRequest:
    def __init__(self, cid=None, o=None, p=None):
        self.cid = cid
        self.o = o
        self.p = p or {}

    @staticmethod
    def hero_list():
        p = {}

        return ActionRequest(cid=861, o="4", p=p)

    @staticmethod
    def map_info(x=100, y=100, k=1037, width=7, height=16, march_info=True):
        p = {"x": x, "y": y, "k": k, "width": width, "height": height, "marchInfo": march_info}
        # {"c":901,"o":"242","p":{"x":508,"y":384,"k":1037,"width":7,"height":16,"marchInfo":true}}

        return ActionRequest(cid=901, o="242", p=p)

    def __str__(self):
        return f'{"c": {self.cid}, "o": {str(self.o)}, "p": {json.dumps(self.p)}}'


class ActionResponse:
    def __init__(self, data=None):
        self.cid = None
        self.data = None
        self.time = None
        self.s = None
        self.o = None

        self.parse(data)

    def parse(self, data=None):
        if data is None:
            return

        data = json.loads(data)

        if len(set(data.keys()) - set('c,s,d,t,o'.split(','))) > 0:
            print(data.keys())

        self.cid = data['c']
        self.data = data['d']
        self.time = datetime.fromtimestamp(data['t'] / 1000.)
        self.s = data['s']
        self.o = data['o']

    def __str__(self):
        return f'{self.time}\t{self.cid}\t{self.s}\t{len(self.data)}'


class User:
    def __init__(self, msg_data=None):
        self.fan = None
        self.fat = None

        self.uid = None
        self.uuid = None
        self.nickname = None
        self.user_name = None
        self.user_gender = None

        self.parse_from_msg(msg_data)

    def parse_from_msg(self, data=None):
        if data is None:
            return
        self.fan = data['fan']
        self.fat = data['fat']
        self.uid = data['uid']
        self.uuid = data['uuid']
        self.nickname = data['fp']['nickname']
        self.user_name = data['fp']['username']
        self.user_gender = data['fp']['usergender']

    def __str__(self):
        return f'{self.uid}\t{self.uuid}\t{self.fat}\t{self.user_name}'
