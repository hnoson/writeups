#!/usr/bin/env python
import angr

p = angr.Project('./yakisoba')
st = p.factory.blank_state()
simgr = p.factory.simulation_manager(st)
simgr.explore(find=0x4006d9, avoid=0x400700)
print(simgr.one_found.posix.dumps(0))
