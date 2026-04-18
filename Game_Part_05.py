from pybricks.parameters import Stop
from pybricks.tools import multitask, StopWatch, wait
from Setup import *
from Utils import *

async def Run_Mission():
    if not robot_state.enabled_missions[5]:
        if robot_state.game_part_debug_mode:
            print("Skipping Game Part 05")
        return

    Game_Part_Timer.reset()
    await multitask(Reset_Wheels_To_Wall("backward"), Change_Gear(4))
    await Arc(320, 73)

    if not robot_state.enabled_missions[6]:
        await multitask(Straight(685, Stop.BRAKE), Move_Caliper("right", 1000, 1400, 200))
    else:
        #await Straight(670, Stop.BRAKE)
        await Straight(680, Stop.BRAKE)

    await Turn(90)
    #await multitask(Straight(145, Stop.BRAKE), Change_Gear(2))
    await multitask(Straight(150, Stop.BRAKE), Change_Gear(2))
    real_turn = await Turn_With_Timeout(angle=-10, timeout_ms=500, turn_rate=150)
    # 11 : Το ρομπότ σηκώνει το artifact μέχρι πάνω
    await Move_Caliper("left", 1000, 1200, 200)
    await Turn(-real_turn)

    if not robot_state.enabled_missions[6]:
        await Arc(-75, -90)
        await Arc(75, -90)
        await multitask(Straight(-20, Stop.BRAKE), Change_Gear(4))
        # 10 : το Ρομπότ κατεβάζει το scale και πέρνει το artifact
        await Move_Caliper("right", 1000, 1200, 220)
        await Move_Caliper("left", 1000, 1200, 200)
        await Change_Gear(3)
        await Move_Caliper("left", 500, 200, 120)
        await Straight(90, Stop.BRAKE)
    else:
        await Straight(-110, Stop.BRAKE)
        
    await Turn(-80)
    #await Straight(700, Stop.COAST)
    await Straight(750, Stop.BRAKE)

    if robot_state.game_part_debug_mode:
        print('Game Part 05 -> Duration:', Milliseconds_To_Time(Game_Part_Timer.time())) 
