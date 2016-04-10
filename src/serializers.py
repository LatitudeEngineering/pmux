import msgpack


class MsgpackSerializer(Serializer):

    def serialize(self, obj):
        return msgpack.dumps(obj)

    def deserialize(self, serialized):
        return msgpack.loads(serialized)
