class State:
    def __init__(self, cfg=None):

        if cfg:
            self.__dict__.update(cfg)

        for k, v in self.__dict__.items():
            if isinstance(v, dict):
                self.__dict__.update({k: State(v)})
            if isinstance(v, State):
                self.__dict__.update({k: State(v.__dict__)})

    def __iter__(self):
        for k, v in self.items():
            yield k

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, v):
        if isinstance(v, dict):
            v = State(v)
        self.__dict__[key] = v

    def __delitem__(self, key):
        del self.__dict__[key]

    def update(self, dict_):
        self.__dict__.update(dict_)
        return self

    def items(self):
        return self.__dict__.items()

    def __repr__(self):
        d = self._dismantle(self.__dict__)
        return str(d)

    def _dismantle(self, dic):
        d = {}
        for k, v in dic.items():
            if isinstance(v, State):
                d[k] = self._dismantle(v.__dict__)
            elif type(v) == dict:
                d[k] = self._dismantle(v)
            elif type(v) == list:
                a = []
                for o in v:
                    if isinstance(o, State):
                        a.append(self._dismantle(o.__dict__))
                    elif type(o) == dict:
                        a.append(self._dismantle(o))
                    else:
                        a.append(o)
                d[k] = a
            else:
                d[k] = v
        return d

    def get(self, key, default_val=None):
        if key in self.__dict__:
            return self.__dict__[key]
        return default_val

    def setdefault(self, key, default_val=None):
        if key not in self.__dict__:
            if type(default_val) == dict:
                self.__dict__[key] = self._dismantle(default_val)
            elif type(default_val) == list:
                a = []
                for o in default_val:
                    if type(o) == dict:
                        a.append(State(self._dismantle(o)))
                    else:
                        a.append(o)
                self.__dict__[key] = a
            else:
                self.__dict__[key] = default_val
        return self.__dict__[key]
