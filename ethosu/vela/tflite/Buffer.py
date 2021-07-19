# automatically generated by the FlatBuffers compiler, do not modify

# namespace: tflite

import flatbuffers

class Buffer(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsBuffer(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Buffer()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def BufferBufferHasIdentifier(cls, buf, offset, size_prefixed=False):
        return flatbuffers.util.BufferHasIdentifier(buf, offset, b"\x54\x46\x4C\x33", size_prefixed=size_prefixed)

    # Buffer
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Buffer
    def Data(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 1))
        return 0

    # Buffer
    def DataAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Uint8Flags, o)
        return 0

    # Buffer
    def DataLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Buffer
    def DataIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        return o == 0

def BufferStart(builder): builder.StartObject(1)
def BufferAddData(builder, data): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(data), 0)
def BufferStartDataVector(builder, numElems): return builder.StartVector(1, numElems, 1)
def BufferEnd(builder): return builder.EndObject()
