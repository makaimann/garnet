import magma as m
from gemstone.common.genesis_wrapper import GenesisWrapper, default_type_map
from gemstone.common.generator_interface import GeneratorInterface


"""
Defines the memory_core using genesis2.

`data_width`: width of an entry in the memory
`data_depth`: number of entries in the memory

Example usage:
    >>> memory_core = memory_core_wrapper.generator()(
            data_width=16, data_depth=1024)
"""
interface = GeneratorInterface()\
    .register("data_width", int, 64)\
    .register("word_width", int, 16)\
    .register("data_depth", int, 128)\
    .register("num_banks", int, 2)

memory_core_wrapper = GenesisWrapper(
    interface, "memory_core", ["memory_core/genesis/input_sr.vp",
                               "memory_core/genesis/output_sr.vp",
                               "memory_core/genesis/linebuffer_control.vp",
                               "memory_core/genesis_new/fifo_control.vp",
                               "memory_core/genesis_new/mem.vp",
                               "memory_core/genesis_new/sram_control.vp",
                               "memory_core/genesis_new/memory_core.vp"],
    type_map={"clk_in": m.In(m.Clock),
              "reset": m.In(m.AsyncReset),
              "config_en": m.In(m.Enable)})

param_mapping = {"data_width": "dwidth", "data_depth": "ddepth", "word_width": "wwidth", "num_banks": "bbanks"}

if __name__ == "__main__":
    """
    This program generates the verilog for the memory core and parses it into a
    Magma circuit. The circuit declaration is printed at the end of the
    program.
    """
    # These functions are unit tested directly, so no need to cover them
    memory_core_wrapper.main(param_mapping=param_mapping)  # pragma: no cover
