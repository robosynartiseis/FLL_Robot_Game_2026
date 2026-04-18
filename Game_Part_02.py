from pybricks.parameters import Stop
from pybricks.tools import multitask, StopWatch, wait
from Setup import *
from Utils import *

async def Run_Mission():
    if not robot_state.enabled_missions[2]:
        if robot_state.game_part_debug_mode:
            print("Skipping Game Part 02")
        return

    Game_Part_Timer.reset()
    await multitask(Reset_Wheels_To_Wall("backward"), Change_Gear(4))
    await multitask(Move_Caliper("right", 1000, 800, 200), Straight(700, Stop.BRAKE))
    await Turn(73)
    Initialise_Acceleration_And_Speed()
    #await Straight(355, Stop.BRAKE)
    await Straight(365, Stop.BRAKE)
    drive_base.settings(straight_speed=500)
    drive_base.settings(straight_acceleration=750)
    # await  multitask(Arc(30, -90), Change_Gear(2))
    await  multitask(Arc(30, -91), Change_Gear(2))
    # 03 : Το ρομπότ σπρώχνει τον explorer
    await Move_Caliper("left", 1000, 1400, 200)
    await Change_Gear(1)
    await Move_Caliper("left", 500, 700, 150)
    await Straight(200, Stop.BRAKE)
    # 04 : Και το ρομπότ πέρνει το artifact
    await Move_Caliper("right", 500, 700, 170)
    await Move_Caliper("left", 500, 700, 150)
    await Straight(-100, Stop.BRAKE)
    drive_base.settings(turn_rate=325)
    drive_base.settings(turn_acceleration=250)
    await Turn(132)
    await multitask(Straight(-30, Stop.BRAKE), Change_Gear(4))
    await Move_Caliper("left", 1000, 1000, 200)
    await Straight(75, Stop.BRAKE)
    # 13 : Το ρομπότ κατεβάζει την δαγκάνα του και σηκώνει την ουρά του statue
    await Move_Caliper("right", 2000, 1000, 250)
    Initialise_Acceleration_And_Speed()
    await Turn(-25)
    await Arc(350, -90, Stop.NONE)
    await Straight(-550, Stop.COAST)

    if robot_state.game_part_debug_mode:
        print('Game Part 02 -> Duration:', Milliseconds_To_Time(Game_Part_Timer.time()))
