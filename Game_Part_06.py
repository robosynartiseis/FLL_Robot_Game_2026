from pybricks.parameters import Stop
from pybricks.tools import multitask, StopWatch, wait
from Setup import *
from Utils import *

async def Run_Mission():
    if not robot_state.enabled_missions[6]:
        if robot_state.game_part_debug_mode:
            print("Skipping Game Part 06")
        return

    Game_Part_Timer.reset()
    await Reset_Wheels_To_Wall("backward")
    await Straight(78, Stop.BRAKE)
    await multitask(Arc(-80, 55), Change_Gear(4))
    await multitask(Straight(610, Stop.BRAKE), Move_Caliper("right", 1000, 1400, 200))
    await Arc(55, -100)
    # 10 : το Ρομπότ κατεβάζει το scale και πέρνει το artifact
    await Move_Caliper("right", 1100, 1200, 250, False)
    await Move_Caliper("left", 1000, 1400, 200)
    await Change_Gear(3)
    await Move_Caliper("left", 500, 200, 120)
    await Straight(90, Stop.BRAKE)
    await Turn(-80, Stop.NONE)
    await Straight(700, Stop.COAST)

    if robot_state.game_part_debug_mode:
        print('Game Part 06 -> Duration:', Milliseconds_To_Time(Game_Part_Timer.time())) 
