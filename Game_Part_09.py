from pybricks.parameters import Stop
from pybricks.tools import multitask, StopWatch, wait
from Setup import *
from Utils import *

async def Run_Mission():
    if not robot_state.enabled_missions[9]:
        if robot_state.game_part_debug_mode:
            print("Skipping Game Part 09")
        return

    Game_Part_Timer.reset()
    await multitask(Reset_Wheels_To_Wall("backward"), Change_Gear(2))
    await Straight(30, Stop.BRAKE)
    await Arc(-80, 55)
    await Straight(450, Stop.BRAKE)
    await Arc(850, 35)
    # 14.2 : Το ρομπότ αφείνει τα άλλα μισά artifacts
    await Straight(-140, Stop.BRAKE)
    await Turn(45)
    # 15 : Το ρομπότ παραδήδει την τελευταία σημαία
    await Arc(865, angle=25)
    await Arc(-465, angle=25)
    await Move_Caliper("right", 600, 500, 120)
    
    if robot_state.enabled_missions[10]:
        await Change_Gear(1)
        await Move_Caliper("right", 800, 350, 200)
        await Straight(-100, Stop.BRAKE)
        await Turn(20)
        await multitask(Straight(-335, Stop.BRAKE), Move_Caliper("left", 600, 625, 200))
        await Arc(-280, angle=-70)
        # 14.3 : Το ρομπότ αφείνει τον explorer
        await Move_Caliper("left", 500, 720, 200)
        await Straight(-130, Stop.COAST)
    else:
        await Straight(-70, Stop.COAST)

    if robot_state.game_part_debug_mode:
        print('Game Part 09 -> Duration:', Milliseconds_To_Time(Game_Part_Timer.time())) 
