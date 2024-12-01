#!/usr/bin/env python3
import angr
import claripy

flag = claripy.BVS('flag', 0x31*8, explicit_name=True)
p = angr.Project('./a.out')
state = p.factory.entry_state(stdin=flag)
simgr = p.factory.simulation_manager(state)
simgr.explore(find=0x44eeaa, avoid=[0x44eeda, 0x44eec3])
print(simgr.found[0].solver.eval(flag, cast_to=bytes))
