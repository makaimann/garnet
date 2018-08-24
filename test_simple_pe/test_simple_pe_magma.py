from simple_pe.simple_pe_magma import define_pe
import fault.random
import operator
import magma as m
import mantle
import os


def test_simple_pe():
    ops = [operator.add, operator.sub, operator.and_, operator.or_]
    pe = define_pe(ops, T=m.UInt, data_width=16)

    tester = fault.Tester(pe)

    m.compile("test_simple_pe/build/pe", pe, output="coreir",
              coreir_args={"passes": ["rungenerators", "flatten",
                                      "cullgraph"]})

    # Sanity check each op with random value
    for i, op in enumerate(ops):
        tester.poke(pe.opcode, i)
        I0 = fault.random.random_bv(16)
        I1 = fault.random.random_bv(16)
        tester.poke(pe.I0, I0)
        tester.poke(pe.I1, I1)
        tester.eval()
        tester.expect(pe.O, op(I0, I1))
    tester.compile_and_run(target="coreir")
    opcode_width = m.bitutils.clog2(len(ops))
    op_strs = {
        operator.add: "+",
        operator.sub: "-",
        operator.and_: "&",
        operator.or_: "|"
    }

    problem = """\
[GENERAL]
model_file: pe.json

[DEFAULT]
bmc_length: 30
verification: safety

"""
    for i, op in enumerate(ops):
        problem += f"""\
[PE check {op.__name__}]
description: "Check opcode={i} corresponds to {op.__name__}"
formula: (self.opcode = {i}_{opcode_width}) -> ((self.I0 {op_strs[op]} self.I1) = self.O)
prove: TRUE
expected: TRUE

[PE check {op.__name__} is possible]
description: "Avoid vacuosly true version of above property"
formula: (self.opcode != {i}_{opcode_width})
prove: TRUE
expected: FALSE


"""  # noqa
    with open("test_simple_pe/build/problem.txt", "w") as f:
        f.write(problem)
    assert not os.system(
        "CoSA --problem test_simple_pe/build/problem.txt")