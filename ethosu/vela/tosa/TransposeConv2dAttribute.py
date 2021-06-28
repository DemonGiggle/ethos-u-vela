# automatically generated by the FlatBuffers compiler, do not modify

# namespace: tosa

import flatbuffers

class TransposeConv2dAttribute(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsTransposeConv2dAttribute(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = TransposeConv2dAttribute()
        x.Init(buf, n + offset)
        return x

    # TransposeConv2dAttribute
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # TransposeConv2dAttribute
    def Outpad(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Int32Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 4))
        return 0

    # TransposeConv2dAttribute
    def OutpadAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Int32Flags, o)
        return 0

    # TransposeConv2dAttribute
    def OutpadLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # TransposeConv2dAttribute
    def Stride(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Int32Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 4))
        return 0

    # TransposeConv2dAttribute
    def StrideAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Int32Flags, o)
        return 0

    # TransposeConv2dAttribute
    def StrideLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # TransposeConv2dAttribute
    def Dilation(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Int32Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 4))
        return 0

    # TransposeConv2dAttribute
    def DilationAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Int32Flags, o)
        return 0

    # TransposeConv2dAttribute
    def DilationLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # TransposeConv2dAttribute
    def OutputShape(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            a = self._tab.Vector(o)
            return self._tab.Get(flatbuffers.number_types.Int32Flags, a + flatbuffers.number_types.UOffsetTFlags.py_type(j * 4))
        return 0

    # TransposeConv2dAttribute
    def OutputShapeAsNumpy(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return self._tab.GetVectorAsNumpy(flatbuffers.number_types.Int32Flags, o)
        return 0

    # TransposeConv2dAttribute
    def OutputShapeLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

def TransposeConv2dAttributeStart(builder): builder.StartObject(4)
def TransposeConv2dAttributeAddOutpad(builder, outpad): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(outpad), 0)
def TransposeConv2dAttributeStartOutpadVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def TransposeConv2dAttributeAddStride(builder, stride): builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(stride), 0)
def TransposeConv2dAttributeStartStrideVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def TransposeConv2dAttributeAddDilation(builder, dilation): builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(dilation), 0)
def TransposeConv2dAttributeStartDilationVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def TransposeConv2dAttributeAddOutputShape(builder, outputShape): builder.PrependUOffsetTRelativeSlot(3, flatbuffers.number_types.UOffsetTFlags.py_type(outputShape), 0)
def TransposeConv2dAttributeStartOutputShapeVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def TransposeConv2dAttributeEnd(builder): return builder.EndObject()
