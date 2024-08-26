from time import sleep
from testmodel import WagoPLC
import sys


def setupWAGO():
    wago = WagoPLC("192.168.1.8", 16, True, virtual=False)
    wago.connection()
    if wago.modbus == None:
        sys.exit(1)
    print("WAGO connected")
    wago.resetValves()
    return wago


wago = setupWAGO()


pre_solution_delay = 1
solution_delay = 1
pos_solution_delay = 2
between_rep_delay = 0.5

solution_valve = 5
air_valve = 6

wago = setupWAGO()

wago.toggleValve(air_valve)
sleep(pre_solution_delay)

wago.toggleValve(solution_valve)
sleep(solution_delay)
wago.toggleValve(solution_valve)
sleep(pos_solution_delay)

wago.toggleValve(air_valve)

sleep(between_rep_delay)

wago.resetValvesN()
