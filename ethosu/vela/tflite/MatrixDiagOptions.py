# automatically generated by the FlatBuffers compiler, do not modify

# namespace: tflite

import flatbuffers

class MatrixDiagOptions(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsMatrixDiagOptions(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = MatrixDiagOptions()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def MatrixDiagOptionsBufferHasIdentifier(cls, buf, offset, size_prefixed=False):
        return flatbuffers.util.BufferHasIdentifier(buf, offset, b"\x54\x46\x4C\x33", size_prefixed=size_prefixed)

    # MatrixDiagOptions
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

def MatrixDiagOptionsStart(builder): builder.StartObject(0)
def MatrixDiagOptionsEnd(builder): return builder.EndObject()
