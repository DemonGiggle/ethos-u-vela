# automatically generated by the FlatBuffers compiler, do not modify

# namespace: tflite

import flatbuffers

class FillOptions(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsFillOptions(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = FillOptions()
        x.Init(buf, n + offset)
        return x

    # FillOptions
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

def FillOptionsStart(builder): builder.StartObject(0)
def FillOptionsEnd(builder): return builder.EndObject()
