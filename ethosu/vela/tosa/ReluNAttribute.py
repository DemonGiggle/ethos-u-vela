# automatically generated by the FlatBuffers compiler, do not modify

# namespace: tosa

import flatbuffers

class ReluNAttribute(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsReluNAttribute(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = ReluNAttribute()
        x.Init(buf, n + offset)
        return x

    # ReluNAttribute
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # ReluNAttribute
    def MaxInt(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # ReluNAttribute
    def MaxFp(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return 0.0

def ReluNAttributeStart(builder): builder.StartObject(2)
def ReluNAttributeAddMaxInt(builder, maxInt): builder.PrependInt32Slot(0, maxInt, 0)
def ReluNAttributeAddMaxFp(builder, maxFp): builder.PrependFloat32Slot(1, maxFp, 0.0)
def ReluNAttributeEnd(builder): return builder.EndObject()
