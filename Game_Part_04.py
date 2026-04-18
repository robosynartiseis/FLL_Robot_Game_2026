from pybricks.parameters import Stop
from pybricks.tools import multitask, StopWatch, wait
from Setup import *
from Utils import *

async def Run_Mission():
    if not robot_state.enabled_missions[4]:
        if robot_state.game_part_debug_mode:
            print("Skipping Game Part 04")
        return

    Game_Part_Timer.reset()
    await Reset_Wheels_To_Wall("backward")
    # 14.1 : Το ρομπότ αφείνει τα μισά artifacts στο κέντρο
    #await Arc(1050, 25)
    await Arc(1150, 26)
    await Arc(850, -35, Stop.COAST)

    if robot_state.game_part_debug_mode:
        print('Game Part 04 -> Duration:', Milliseconds_To_Time(Game_Part_Timer.time())) 
