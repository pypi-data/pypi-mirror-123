from classiq_interface.generator import segments


class Wire:
    def __init__(self, start_segment: segments.FunctionCall, output_name: str):
        self._start_seg = start_segment
        self._start_name: str = output_name
        self._wire_name = f"{self._start_seg.name}_{self._start_name}"

    def connect_wire(self, end_segment: segments.FunctionCall, input_name: str):
        self._start_seg.outputs[self._start_name] = self._wire_name
        end_segment.inputs[input_name] = self._wire_name
