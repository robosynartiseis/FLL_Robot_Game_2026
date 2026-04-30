from pybricks.parameters import Stop
from pybricks.tools import multitask, StopWatch, wait
from Setup import *
from Utils import *

async def Run_Mission():
    if not robot_state.enabled_missions[3]:
        if robot_state.game_part_debug_mode:
            print("Skipping Game Part 03")
        return

    Game_Part_Timer.reset()
    await Reset_Wheels_To_Wall("backward")
    await Arc(40, 70)

    if robot_state.enabled_missions[11]:
        await Arc(150, 33)
        await Arc(-760, 27)
        drive_base.settings(straight_speed=200)
        drive_base.settings(straight_acceleration=500)
        #await multitask(Arc(800, 5), Change_Gear(3))
        await multitask(Straight(75, Stop.BRAKE), Change_Gear(3))
    else:
        await Arc(275, 33)
        await Arc(-275, 33)
        await Straight(155, Stop.BRAKE)
        drive_base.settings(straight_speed=200)
        drive_base.settings(straight_acceleration=500)
        #await multitask(Straight(95, Stop.BRAKE), Change_Gear(3))
        await multitask(Arc(850, 5), Change_Gear(3))

    # 15 :  Το ρομπότ αφείνει ττην 1η του σημαία
    await Move_Caliper("left", 500, 80, 170)
    await Move_Caliper("right", 500, 80, 170)
    await multitask(Straight(-65, Stop.BRAKE), Change_Gear(2))
    #await Turn(-5)
    # 12 :  Το ρομπότ αφερεί την άμμο απο το πλοίο
    await Move_Caliper("right", 500, 300, 180)
    await Straight(-110, Stop.BRAKE)
    await Move_Caliper("left", 500, 300, 150)
    Initialise_Acceleration_And_Speed()
    await Arc(-550, -50, Stop.COAST)

    if robot_state.game_part_debug_mode:
        print('Game Part 03 -> Duration:', Milliseconds_To_Time(Game_Part_Timer.time())) 
