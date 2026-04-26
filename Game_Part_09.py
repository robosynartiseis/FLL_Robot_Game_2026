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
    await multitask(Reset_Wheels_To_Wall("backward"), Change_Gear(4))
    await Straight(30, Stop.BRAKE)
    await Arc(-80, 55)
    await multitask(Straight(450, Stop.BRAKE), Move_Caliper("left", 500, 200, 150))
    await Arc(870, 35)
    # 14.2 : Το ρομπότ αφείνει τα άλλα μισά artifacts
    await Straight(-140, Stop.BRAKE)
    await Turn(45)
    # 15 : Το ρομπότ παραδήδει την τελευταία σημαία
    await Arc(860, angle=25)
    await multitask(Arc(-460, angle=25), Change_Gear(2))
    await Move_Caliper("right", 600, 500, 120)
    
    if robot_state.enabled_missions[10]:
        await Move_Caliper("left", 600, 5, 120)
        await Change_Gear(1)
        await Move_Caliper("right", 650, 550, 200)
        await Straight(-80, Stop.BRAKE)
        drive_base.settings(turn_rate=250)
        drive_base.settings(turn_acceleration=375)
        await Turn(90)
        await multitask(Straight(-370, Stop.BRAKE), Change_Gear(4))
        await Move_Caliper("left", 1000, 1000, 200)
        await Move_Caliper("left", 1000, 10, 170)
        # 14.3 : Το ρομπότ αφείνει τον explorer
        await Change_Gear(1)
        await Move_Caliper("left", 500, 650, 200)
    else:
        await Straight(-70, Stop.COAST)

    if robot_state.game_part_debug_mode:
        print('Game Part 09 -> Duration:', Milliseconds_To_Time(Game_Part_Timer.time())) 
