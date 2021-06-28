# automatically generated by the FlatBuffers compiler, do not modify

# namespace: tosa

import flatbuffers

class Pool2dAttribute(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsPool2dAttribute(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Pool2dAttribute()
        x.Init(buf, n + offset)
        return x

    # Pool2dAttribute
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Pool2dAttribute
    def Padding(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Int32Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 4))
        return 0

    # Pool2dAttribute
    def PaddingAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Int32Flags, o)
        return 0

    # Pool2dAttribute
    def PaddingLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Pool2dAttribute
    def Kernel(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Int32Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 4))
        return 0

    # Pool2dAttribute
    def KernelAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Int32Flags, o)
        return 0

    # Pool2dAttribute
    def KernelLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # Pool2dAttribute
    def Stride(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Int32Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 4))
        return 0

    # Pool2dAttribute
    def StrideAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Int32Flags, o)
        return 0

    # Pool2dAttribute
    def StrideLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

def Pool2dAttributeStart(builder): builder.StartObject(3)
def Pool2dAttributeAddPadding(builder, padding): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(padding), 0)
def Pool2dAttributeStartPaddingVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def Pool2dAttributeAddKernel(builder, kernel): builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(kernel), 0)
def Pool2dAttributeStartKernelVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def Pool2dAttributeAddStride(builder, stride): builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(stride), 0)
def Pool2dAttributeStartStrideVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def Pool2dAttributeEnd(builder): return builder.EndObject()
