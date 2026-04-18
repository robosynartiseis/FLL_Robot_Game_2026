from pybricks.parameters import Stop
from pybricks.tools import multitask, StopWatch, wait
from Setup import *
from Utils import *

async def Run_Mission():
    if not robot_state.enabled_missions[1]:
        if robot_state.game_part_debug_mode:
            print("Skipping Game Part 01")
        return

    Game_Part_Timer.reset()
    await multitask(Reset_Wheels_To_Wall("backward"), Change_Gear(1))
    await multitask(Move_Caliper("left", 500, 100, 190), Straight(710, Stop.BRAKE))
    await Turn(-65)
    await Straight(200, Stop.BRAKE)
    # 01 : Το ρομπότ σηκώνει το top soil και τερματίζει το map reveal
    await Move_Caliper("right", 500, 400, 180)
    await Change_Gear(2)
    await Move_Caliper("left", 500, 650, 150)
    drive_base.settings(straight_speed=200)
    drive_base.settings(straight_acceleration=500)
    await Change_Gear(3)
    await multitask(Move_Caliper("right", 500, 700, 150), Straight(-50, Stop.BRAKE))
    await Arc(-92, -140)
    await Straight(-50, Stop.BRAKE)
    # 02 : Το ρομπότ ρίχνει τα soil deposits και σηκώνει το πινέλο
    await Move_Caliper("left", 750, 700, 200)
    await Move_Caliper("right", 600, 790, 170)
    Initialise_Acceleration_And_Speed()
    await Arc(140, 80, Stop.NONE)
    await Straight(400, Stop.COAST)
    
    if robot_state.game_part_debug_mode:
        print('Game Part 01 -> Duration:', Milliseconds_To_Time(Game_Part_Timer.time()))
