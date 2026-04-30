from pybricks.parameters import Stop
from pybricks.tools import multitask, StopWatch, wait
from Setup import *
from Utils import *

async def Run_Mission():
    if not robot_state.enabled_missions[8]:
        if robot_state.game_part_debug_mode:
            print("Skipping Game Part 08")
        return

    Game_Part_Timer.reset()
    await Reset_Wheels_To_Wall("backward")
    await multitask(Arc(-280, 20), Change_Gear(1))
    await multitask(Straight(420, Stop.BRAKE), Move_Caliper("left", 2000, 120, 200))
    await Move_Caliper("left", 2000, 400, 200)
    # 09 :  Το ρομπότ σηκώνει το σκεπή
    await Straight(-70, Stop.BRAKE)
    await multitask(Straight(15, Stop.BRAKE), Move_Caliper("right", 2000, 900, 200))
    await Straight(-65, Stop.BRAKE)
    await Move_Caliper("left", 2000, 700, 200)
    # 09 :  Το ρομπότ σηκώνει το ware
    await Turn(-20)
    await Straight(-35, Stop.BRAKE)
    await Turn(-25)
    await multitask(Straight(-110, Stop.BRAKE), Change_Gear(4))
    await Turn(90)
    await Straight(75, Stop.BRAKE)

    if not robot_state.enabled_missions[12]:
        # 08 :  Το ρομπότ χτυπάει το σιλό 4 φορές και βγάζει τα γρανάζια
        await Move_Caliper("right", 3000, 7000, 200)
    else:
        # 08 :  Το ρομπότ χτυπάει το σιλό 3 φορές και βγάζει τα γρανάζια
        await Move_Caliper("right", 3000, 5000, 200)

    await Arc(230, -90, Stop.COAST)
    
    if robot_state.game_part_debug_mode:
        print('Game Part 08 -> Duration:', Milliseconds_To_Time(Game_Part_Timer.time())) 
