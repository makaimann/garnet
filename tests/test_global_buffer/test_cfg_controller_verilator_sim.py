import glob
import pytest
import os
from gemstone.common.run_genesis import run_genesis
from verilator_sim import run_verilator, verilator_available


def run_verilator_regression(top, test_driver, genesis_params={},
                             verilog_params={}):
    # Genesis version of global_controller
    run_genesis(f"{top}",
                ["global_buffer/genesis/cfg_address_generator.svp",
                 "global_buffer/genesis/cfg_controller.svp"],
                genesis_params)
    files = []
    files.extend(glob.glob('genesis_verif/cfg_address_generator.sv'))
    files.extend(glob.glob('genesis_verif/cfg_controller.sv'))
    return run_verilator(verilog_params, top, files, test_driver)


@pytest.mark.skipif(not verilator_available(),
                    reason="verilator not available")
@pytest.mark.parametrize('verilog_params', [
    {
        "BANK_DATA_WIDTH": 64,
        "GLB_ADDR_WIDTH": 22
    }
])
def test_cfg_controller_verilator(verilog_params):
    test_driver = f"tests/test_global_buffer/verilator/"\
                  f"test_cfg_controller.cpp"
    res = run_verilator_regression("cfg_controller", test_driver,
                                   {}, verilog_params)
    assert res == 1
