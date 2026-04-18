from pybricks.parameters import Stop
from pybricks.tools import multitask, StopWatch, wait
from Setup import *
from Utils import *

async def Run_Mission():
    if not robot_state.enabled_missions[7]:
        if robot_state.game_part_debug_mode:
            print("Skipping Game Part 07")
        return

    Game_Part_Timer.reset()
    await Reset_Wheels_To_Wall("backward")
    await Straight(640, Stop.BRAKE)
    await Turn(68)
    await multitask(Straight(210, Stop.BRAKE), Change_Gear(4))
    # 07 :  Το ρομπότ πέρνει το artifact,
    await Move_Caliper("left", 2000, 1500, 200)
    await Change_Gear(1)
    # 06 : Το ρομπότ μαζέυει τις πέτρες
    await Move_Caliper("left", 3000, 500, 200)
    await Change_Gear(3)
    # 05 : Το ρομπότ αποκαλύφτει το κρυφό μέρος
    await Move_Caliper("right", 750, 750, 200)
    await Move_Caliper("left", 500, 800, 150)
    await Straight(-130, Stop.BRAKE)
    drive_base.settings(straight_speed=200)
    drive_base.settings(straight_acceleration=500)
    await Arc(100, -65, Stop.NONE)
    Initialise_Acceleration_And_Speed()
    await Straight(-400, Stop.NONE)
    await Arc(150, -70, Stop.COAST)

    if robot_state.game_part_debug_mode:
        print('Game Part 07 -> Duration:', Milliseconds_To_Time(Game_Part_Timer.time())) 
