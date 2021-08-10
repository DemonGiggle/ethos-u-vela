# automatically generated by the FlatBuffers compiler, do not modify

# namespace: tosa

import flatbuffers

class AxisAttribute(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsAxisAttribute(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = AxisAttribute()
        x.Init(buf, n + offset)
        return x

    # AxisAttribute
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # AxisAttribute
    def Axis(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int32Flags, o + self._tab.Pos)
        return 0

def AxisAttributeStart(builder): builder.StartObject(1)
def AxisAttributeAddAxis(builder, axis): builder.PrependInt32Slot(0, axis, 0)
def AxisAttributeEnd(builder): return builder.EndObject()