import abc
import msgpack


class Serializer(object):
    """Boundary for serialization

    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def serialize(self, obj):
        pass

    @abc.abstractmethod
    def deserialize(self, serialized):
        pass


class MsgpackSerializer(Serializer):

    def serialize(self, obj):
        return msgpack.dumps(obj)

    def deserialize(self, serialized):
        return msgpack.loads(serialized)
