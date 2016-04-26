from base import Serializer
import msgpack


def get_default_serializer():
    return MsgpackSerializer


class MsgpackSerializer(Serializer):

    @staticmethod
    def serialize(obj):
        return msgpack.dumps(obj)

    @staticmethod
    def deserialize(serialized):
        return msgpack.loads(serialized)
