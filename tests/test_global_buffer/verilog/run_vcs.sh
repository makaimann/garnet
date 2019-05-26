#!/bin/tcsh
vcs +vcs+lic+wait +define+VCS_BUILD -full64 -LDFLAGS -Wl,--no-as-needed +v2k -debug -sverilog genesis_verif/*.sv clocker.sv global_buffer_tb.sv
