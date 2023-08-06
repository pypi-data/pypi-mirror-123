import copy


class Tracking(object):
    CHANGE = 0
    ADD = 1
    DELETE = 2

    def __init__(self, node, tracker=None, getter=None):
        self.node = node
        self.tracker = tracker
        self.getter = getter

        self.attached = {}
        self.records = {}
        self.objects = {}

    def save_initial_value(self):
        self.track(initial=True)

    def track(self, element=None, initial=False):
        element = element if element else (self.getter() if self.getter else None)
        if element is not None:
            self.event(Tracking.CHANGE, element, initial=initial)

    def event(self, event_type, element=None, key=None, initial=False):
        if not self.counter:
            return

        index = self.counter.t + (0 if initial else 1)
        if index not in self.records or event_type == Tracking.CHANGE:
            self.records[index] = []
        self.records[index].append((event_type, key, id(element)))
    
    def attach_object(self, object_):
        if object_ is None:
            return
        
        object_ = self.track_object(object_)

        id_ = id(object_)
        self.objects[id_] = None
        self.attached[id_] = object_
        return object_

    def detach_object(self, object_):
        if object_ is None:
            return

        id_ = id(object_)
        self.objects[id_] = self.node.serializer.serialize_data(object_)
        del self.attached[id_]
        return id_
    
    # def attached(self):
    #     if self.save_initial_value:
    #         self.track(initial=True)
    #         self.save_initial_value = False

    def attach(self, new_tracker):
        t = copy.copy(self)
        t.tracker = new_tracker
        return t

    @property
    def root(self):
        root = self.node
        while root.parent:
            root = root.parent
        return root

    @property
    def counter(self):
        return self.node.counter
    
    def track_object(self, object_):
        if isinstance(object_, list):
            return ListTracker(object_, self.node)
        else:
            return object_


class AttributeTracker(object):
    def __init__(self, node, name, object_):
        self.node = node
        self.name = name
        self.object = None

        self._tracking = Tracking(self.node, getter=self.getter)

        self.setter(self, object_, no_event=True)

        self._tracking.save_initial_value()

    def getter(self, instance=None):
        return self.object

    def setter(self, instance, value, no_event=False):
        self._tracking.detach_object(self.object)
        self.object = self._tracking.attach_object(value)

        if not no_event:
            self._tracking.event(Tracking.CHANGE, self.object)

    # def attached(self):
    #     self._tracking.attached()


class GenericTracker(object):
    def __init__(self, node, tracking=None, save_initial_value=True):
        if tracking:
            self._tracking = tracking.attach(self)
            self._tracking.track()
        else:
            self._tracking = Tracking(node)


# class Tracker(GenericTracker):
#     def __init__(self, obj, host, tracking=None, save_initial_value=False):
#         super().__init__(obj, host, tracking=tracking,
#                          save_initial_value=save_initial_value)
    
#     @property
#     def object(self):
#         return self._object
    
#     @object.setter
#     def object(self, obj):
#         self.update(obj)

#     def update(self, obj):
#         self._object = obj
    
#     def updated(self):
#         pass
    
#     def track(self):
#         self._tracking.track()


# class AutoTracker(Tracker):
#     def __init__(self, obj, host, tracking=None, save_initial_value=True):
#         super().__init__(obj, host, tracking=tracking,
#                          save_initial_value=save_initial_value)

#     def update(self, obj):
#         self._object = obj
#         self._tracking.track()

#     def updated(self):
#         self._tracking.track()


class ListTracker(list, GenericTracker):
    def __init__(self, list_, node, tracking=None, save_initial_value=True):
        list.__init__(self, list_)
        GenericTracker.__init__(self, node, tracking=tracking, save_initial_value=save_initial_value)

    def append(self, x):
        x = self._tracking.attach_object(x)

        list.append(self, x)
        self._tracking.event(Tracking.ADD, x, key=len(self) - 1)

    def insert(self, i, x):
        x = self._tracking.attach_object(x)

        list.insert(self, i, x)
        self._tracking.event(Tracking.ADD, x, key=i)

    def remove(self, x):
        i = list.index(self, x)
        self._tracking.detach_object(x)

        list.remove(self, x)
        self._tracking.event(Tracking.DELETE, key=i)
    
    def pop(self, i=0):
        x = list.pop(self, i)
        self._tracking.detach_object(x)
        self._tracking.event(Tracking.DELETE, key=i)


def get_tracking(obj):
    return obj._tracking



# class WrapperAutoTracker(GenericTracker):
#     def __init__(self, obj, host, tracking=None):
#         super().__init__(obj, host, tracking=tracking)
#         # self.tracker = Tracking()
    
#     def __getattr__(self, name):
#         return getattr(self._obj, name)
    
#     def __deepcopy__(self, m):
#         pass

#     def __repr__(self):
#         return self._object.__repr__()

#     def __add__(self, o):
#         return self.__class__(self._tracking.host, self._object.__add__(o), tracking=self._tracking)


# class TrackList(list):
#     def __init__(self, *args):
#         super().__init__(*args)
#         self.tracking
