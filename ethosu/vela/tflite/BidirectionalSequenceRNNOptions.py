# automatically generated by the FlatBuffers compiler, do not modify

# namespace: tflite

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class BidirectionalSequenceRNNOptions(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAs(cls, buf, offset=0):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = BidirectionalSequenceRNNOptions()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def GetRootAsBidirectionalSequenceRNNOptions(cls, buf, offset=0):
        """This method is deprecated. Please switch to GetRootAs."""
        return cls.GetRootAs(buf, offset)
    @classmethod
    def BidirectionalSequenceRNNOptionsBufferHasIdentifier(cls, buf, offset, size_prefixed=False):
        return flatbuffers.util.BufferHasIdentifier(buf, offset, b"\x54\x46\x4C\x33", size_prefixed=size_prefixed)

    # BidirectionalSequenceRNNOptions
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # BidirectionalSequenceRNNOptions
    def TimeMajor(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return bool(self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos))
        return False

    # BidirectionalSequenceRNNOptions
    def FusedActivationFunction(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Int8Flags, o + self._tab.Pos)
        return 0

    # BidirectionalSequenceRNNOptions
    def MergeOutputs(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return bool(self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos))
        return False

    # BidirectionalSequenceRNNOptions
    def AsymmetricQuantizeInputs(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return bool(self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos))
        return False

def Start(builder): builder.StartObject(4)
def BidirectionalSequenceRNNOptionsStart(builder):
    """This method is deprecated. Please switch to Start."""
    return Start(builder)
def AddTimeMajor(builder, timeMajor): builder.PrependBoolSlot(0, timeMajor, 0)
def BidirectionalSequenceRNNOptionsAddTimeMajor(builder, timeMajor):
    """This method is deprecated. Please switch to AddTimeMajor."""
    return AddTimeMajor(builder, timeMajor)
def AddFusedActivationFunction(builder, fusedActivationFunction): builder.PrependInt8Slot(1, fusedActivationFunction, 0)
def BidirectionalSequenceRNNOptionsAddFusedActivationFunction(builder, fusedActivationFunction):
    """This method is deprecated. Please switch to AddFusedActivationFunction."""
    return AddFusedActivationFunction(builder, fusedActivationFunction)
def AddMergeOutputs(builder, mergeOutputs): builder.PrependBoolSlot(2, mergeOutputs, 0)
def BidirectionalSequenceRNNOptionsAddMergeOutputs(builder, mergeOutputs):
    """This method is deprecated. Please switch to AddMergeOutputs."""
    return AddMergeOutputs(builder, mergeOutputs)
def AddAsymmetricQuantizeInputs(builder, asymmetricQuantizeInputs): builder.PrependBoolSlot(3, asymmetricQuantizeInputs, 0)
def BidirectionalSequenceRNNOptionsAddAsymmetricQuantizeInputs(builder, asymmetricQuantizeInputs):
    """This method is deprecated. Please switch to AddAsymmetricQuantizeInputs."""
    return AddAsymmetricQuantizeInputs(builder, asymmetricQuantizeInputs)
def End(builder): return builder.EndObject()
def BidirectionalSequenceRNNOptionsEnd(builder):
    """This method is deprecated. Please switch to End."""
    return End(builder)