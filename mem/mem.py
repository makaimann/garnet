from common.configurable_model import ConfigurableModel
import functools
from bit_vector import BitVector
from enum import Enum


class Mode(Enum):
    LINE_BUFFER = 0
    FIFO = 1
    SRAM = 2


def check_addr(fn):
    @functools.wraps(fn)
    def wrapped(self, addr, *args):
        if not (0 <= addr < self.data_depth):
            raise ValueError(f"Invalid address ({addr}),"
                             f" must be within range(0, {self.data_depth})")
        return fn(self, addr, *args)
    return wrapped


def gen_mem(data_width: int,
            data_depth: int):
    class Mem(ConfigurableModel(32, 32)):
        def __init__(self):
            super().__init__()
            self.memory = {}
            # store self.data_depth so the decorator `check_addr` can reference
            # it without having to be defined within the scope of the closure
            self.data_depth = data_depth
            self.config_addr = BitVector(0, 32)

        def __call__(self):
            # TODO: Should this define a __call__? What should the semantics
            # be?
            raise NotImplementedError()

        @property
        def mode(self):
            """
            The mode is stored in the lowest 2 (least significant) bits of the
            configuration data.
            """
            return Mode((self.config[self.config_addr] & 0x3).unsigned_value)

        @mode.setter
        def mode(self, mode):
            """
            Expose an interface to set the mode

            Example:
                `mem_inst.mode = Mode.SRAM`
            """
            if not isinstance(mode, Mode):
                raise ValueError(
                    "Expected `mode` to be an instance of `mem.Mode`")
            # Clear lower 2 bits
            self.config[self.config_addr] &= ~0x3
            # set new mode
            self.config[self.config_addr] |= BitVector(mode.value, 2)

        @check_addr
        def read(self, addr):
            if self.mode == Mode.SRAM:
                return self.memory[addr]
            else:
                raise NotImplementedError(self.mode)

        @check_addr
        def write(self, addr, value):
            if isinstance(value, BitVector) and value.num_bits > data_width:
                raise ValueError(f"value.num_bits must be <= {data_width}")
            elif isinstance(value, int) and value.bit_length() > data_width:
                raise ValueError(f"value.bit_length() must be <= {data_width}")
            if self.mode == Mode.SRAM:
                self.memory[addr] = value
            else:
                raise NotImplementedError(self.mode)
    return Mem
