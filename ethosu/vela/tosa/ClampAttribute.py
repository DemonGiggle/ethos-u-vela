# automatically generated by the FlatBuffers compiler, do not modify

# namespace: tosa

import flatbuffers

class ClampAttribute(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsClampAttribute(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = ClampAttribute()
        x.Init(buf, n + offset)
        return x

    # ClampAttribute
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # ClampAttribute
    def MinInt(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # ClampAttribute
    def MaxInt(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

    # ClampAttribute
    def MinFp(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return 0.0

    # ClampAttribute
    def MaxFp(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return 0.0

def ClampAttributeStart(builder): builder.StartObject(4)
def ClampAttributeAddMinInt(builder, minInt): builder.PrependInt32Slot(0, minInt, 0)
def ClampAttributeAddMaxInt(builder, maxInt): builder.PrependInt32Slot(1, maxInt, 0)
def ClampAttributeAddMinFp(builder, minFp): builder.PrependFloat32Slot(2, minFp, 0.0)
def ClampAttributeAddMaxFp(builder, maxFp): builder.PrependFloat32Slot(3, maxFp, 0.0)
def ClampAttributeEnd(builder): return builder.EndObject()
