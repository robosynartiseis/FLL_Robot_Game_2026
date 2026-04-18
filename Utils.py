# Εισάγουμε το Stop για να μπορούμε να ορίζουμε τον τρόπο σταματήματος του ρομπότ
from pybricks.parameters import Stop

# Εισάγουμε την wait για μικρές καθυστερήσεις
# και το StopWatch για χρήση χρονόμετρου
from pybricks.tools import wait, StopWatch

# Εισάγουμε ΟΛΑ τα αντικείμενα και τις σταθερές από το Setup
# (prime_hub, drive_base, sensors, robot_state κλπ)
from Setup import *

# ============================================================
# HUB INITIALIZATION
# ============================================================


def Initialise_Hub():
    # Ρυθμίζουμε τον προσανατολισμό της οθόνης του hub
    # ώστε η αριστερή πλευρά να θεωρείται "πάνω"
    prime_hub.display.orientation(up=Side.LEFT)

    # Ορίζουμε ποια κουμπιά θα σταματούν το πρόγραμμα
    # Εδώ: CENTER + BLUETOOTH μαζί
    prime_hub.system.set_stop_button((Button.CENTER, Button.BLUETOOTH))

    # Ενεργοποιούμε το γυροσκόπιο για πιο ακριβείς στροφές
    drive_base.use_gyro(True)


def Check_IMU():
    # Ελέγχουμε αν το γυροσκόπιο είναι έτοιμο
    if not prime_hub.imu.ready():

        # Αν είναι ενεργό το debug mode των utils
        if robot_state.utils_debug_mode:
            # Εμφανίζουμε μήνυμα
            print("IMU not ready!")

        # Επιστρέφουμε False για να σταματήσει το πρόγραμμα
        return False

    # Αν είναι έτοιμο επιστρέφουμε True
    return True


def Wait_For_Start(color=Color.GREEN):
    # Όσο το κουμπί CENTER δεν έχει πατηθεί
    while Button.CENTER not in prime_hub.buttons.pressed():

        # Ανάβουμε το LED για ένδειξη αναμονής
        prime_hub.light.on(color)

        # Μικρή καθυστέρηση για να μην καταναλώνει CPU
        wait(1)

    # Όταν πατηθεί, σβήνουμε το LED
    prime_hub.light.off()


# ============================================================
# DRIVE SETTINGS
# ============================================================

def Initialise_Acceleration_And_Speed():
    # Ορίζουμε την προεπιλεγμένη ταχύτητα ευθείας κίνησης
    drive_base.settings(straight_speed=DEFAULT_DRIVE_SPEED)

    # Ορίζουμε την επιτάχυνση ευθείας
    drive_base.settings(straight_acceleration=DEFAULT_DRIVE_ACCELERATION)

    # Ορίζουμε την ταχύτητα περιστροφής
    drive_base.settings(turn_rate=DEFAULT_TURN_SPEED)

    # Ορίζουμε την επιτάχυνση περιστροφής
    drive_base.settings(turn_acceleration=DEFAULT_TURN_ACCELERATION)

    # Αν είναι ενεργό το debug mode
    if robot_state.utils_debug_mode:
        print(
            "Initialise acceleration and speed ->",
            "Drive speed:", DEFAULT_DRIVE_SPEED,
            "Drive acceleration:", DEFAULT_DRIVE_ACCELERATION,
            "Turn speed:", DEFAULT_TURN_SPEED,
            "Turn acceleration:", DEFAULT_TURN_ACCELERATION
        )


# ============================================================
# TIME FORMATTER
# ============================================================

def Milliseconds_To_Time(ms):
    # Μετατρέπουμε τα ms σε δευτερόλεπτα
    seconds = ms // 1000

    # Υπολογίζουμε τα λεπτά
    minutes = (seconds % 3600) // 60

    # Υπολογίζουμε τα υπόλοιπα δευτερόλεπτα
    remaining_seconds = seconds % 60

    # Υπολογίζουμε τα υπόλοιπα ms
    milliseconds = ms % 1000

    # Επιστρέφουμε μορφοποιημένο χρόνο
    return f"{minutes:02}:{remaining_seconds:02}.{milliseconds:03}"


# ============================================================
# ANGLE DELTA
# ============================================================

def Angle_Delta(start, end):
    # Υπολογίζουμε τη διαφορά γωνίας
    delta = end - start

    # Αν η διαφορά είναι μεγαλύτερη από 180
    while delta > 180:
        # Αφαιρούμε 360 για διόρθωση wrap
        delta -= 360

    # Αν η διαφορά είναι μικρότερη από -180
    while delta < -180:
        # Προσθέτουμε 360 για διόρθωση wrap
        delta += 360

    # Επιστρέφουμε τη διορθωμένη διαφορά
    return delta


# ============================================================
# MONITOR REFLECTION
# ============================================================

def Monitor_Reflection():
    # Η συνάρτηση αυτή χρησιμοποιείται μόνο για debugging.
    # Διαβάζει συνεχώς τις τιμές αντανάκλασης (reflection)
    # από τους δύο αισθητήρες χρώματος
    # και τις εμφανίζει στην κονσόλα.
    # Δεν σταματά ποτέ μόνη της (τρέχει σε άπειρο βρόχο).

    while True:
        # Διαβάζουμε την αντανάκλαση από τον αριστερό αισθητήρα.
        # Η τιμή είναι από 0 έως 100.
        # 0 = πολύ σκοτεινό (μαύρο)
        # 100 = πολύ φωτεινό (λευκό)
        left_reflection = left_colour_sensor.reflection()

        # Διαβάζουμε την αντανάκλαση από τον δεξιό αισθητήρα.
        right_reflection = right_colour_sensor.reflection()

        # Αν είναι ενεργό το debug mode,
        # εμφανίζουμε τις τιμές στην κονσόλα.
        if robot_state.utils_debug_mode:
            print(
                "Monitor reflection ->",
                "Left reflection:", left_reflection,
                "Right reflection:", right_reflection
            )

        # Μικρή καθυστέρηση 1 millisecond.
        # Αυτό αποτρέπει υπερβολική κατανάλωση CPU
        # και επιτρέπει στο σύστημα να λειτουργεί ομαλά.
        wait(1)


# ============================================================
# RESET WHEELS TO WALL
# ============================================================

async def Reset_Wheels_To_Wall(direction):
    # Η συνάρτηση αυτή χρησιμοποιείται για μηχανική ευθυγράμμιση.
    # Το ρομπότ κινείται για συγκεκριμένο χρόνο προς έναν τοίχο
    # ώστε οι τροχοί να "πατήσουν" σωστά και να μηδενιστεί
    # τυχόν μικρή απόκλιση θέσης.
    #
    # direction μπορεί να είναι:
    # "forward"  -> κινείται μπροστά
    # "backward" -> κινείται πίσω

    # Αυξάνουμε προσωρινά την ταχύτητα ευθείας κίνησης.
    # Θέλουμε σταθερή και δυναμική επαφή με τον τοίχο.
    drive_base.settings(straight_speed=750)

    # Αυξάνουμε και την επιτάχυνση,
    # ώστε να φτάσει γρήγορα στη μικρή ταχύτητα που θα δώσουμε.
    drive_base.settings(straight_acceleration=1000)

    # Μηδενίζουμε το χρονόμετρο που χρησιμοποιούμε
    # για να ελέγξουμε πόσο θα διαρκέσει η κίνηση.
    Function_Timer.reset()

    # Όσο ο χρόνος είναι μικρότερος από
    # τη σταθερά RESET_WHELLS_TO_WALL_DURATION
    while Function_Timer.time() < RESET_WHELLS_TO_WALL_DURATION:

        # Αν ζητήθηκε κίνηση μπροστά
        if direction == "forward":

            # Δίνουμε μικρή ταχύτητα μπροστά (100 mm/s)
            # 0 σημαίνει καμία περιστροφή
            drive_base.drive(100, 0)

        # Αν ζητήθηκε κίνηση πίσω
        elif direction == "backward":

            # Δίνουμε μικρή ταχύτητα πίσω (-100 mm/s)
            drive_base.drive(-100, 0)

        # Αν δοθεί λάθος τιμή direction
        else:

            # Δεν κάνουμε τίποτα
            # (κρατάμε το ρομπότ ακίνητο)
            pass

    # Μόλις τελειώσει ο χρόνος,
    # σταματάμε πλήρως τη βάση κίνησης.
    drive_base.stop()

    # Επαναφέρουμε τις προκαθορισμένες τιμές
    # ταχύτητας και επιτάχυνσης.
    drive_base.settings(straight_speed=DEFAULT_DRIVE_SPEED)
    drive_base.settings(straight_acceleration=DEFAULT_DRIVE_ACCELERATION)

    # Αν είναι ενεργό το debug mode των utils,
    # εμφανίζουμε επιβεβαίωση στην κονσόλα.
    if robot_state.utils_debug_mode:
        print(
            'Reset wheels to wall ->',
            'Drive speed:', DEFAULT_DRIVE_SPEED,
            'Drive acceleration:', DEFAULT_DRIVE_ACCELERATION
        )

# ============================================================
# TURN
# ============================================================

async def Turn(angle, stop_mode=Stop.HOLD):
    # Αποθηκεύουμε τη γωνία πριν τη στροφή
    start_angle = drive_base.angle()

    # Εκτελούμε τη στροφή
    await drive_base.turn(angle, then=stop_mode)

    # Μικρό async yield
    await wait(1)

    # Διαβάζουμε τη γωνία μετά
    end_angle = drive_base.angle()

    # Υπολογίζουμε πόσο στρίψαμε πραγματικά
    real_angle = Angle_Delta(start_angle, end_angle)

    # Υπολογίζουμε το σφάλμα
    error = real_angle - angle

    # Καταγράφουμε το σφάλμα στο robot_state
    robot_state.last_turn_error = error

    # Αν είναι ενεργό το debug mode
    if robot_state.track_debug_mode:
        print(
            "Turn ->",
            "Target:", angle,
            "Real:", real_angle,
            "Error:", error
        )


# ============================================================
# TURN WITH TIMEOUT
# ============================================================

async def Turn_With_Timeout(angle, timeout_ms=100, turn_rate=DEFAULT_TURN_SPEED):
    # Η συνάρτηση αυτή στρίβει το ρομπότ με γυροσκόπιο
    # αλλά έχει χρονικό όριο (timeout),
    # ώστε να μην κολλήσει αν κάτι εμποδίσει τη στροφή.

    # Δημιουργούμε ένα χρονόμετρο
    Function_Timer = StopWatch()

    # Μηδενίζουμε το χρονόμετρο
    Function_Timer.reset()

    # Διαβάζουμε τη γωνία πριν ξεκινήσει η περιστροφή
    previous_angle = drive_base.angle()

    # Δημιουργούμε μεταβλητή που θα κρατά
    # πόσες μοίρες στρίψαμε συνολικά
    real_angle = 0

    # Αν το angle είναι θετικό → στρίβουμε δεξιά
    # Αν είναι αρνητικό → στρίβουμε αριστερά
    direction = 1 if angle >= 0 else -1

    # Ξεκινάμε συνεχή περιστροφή
    # 0 σημαίνει δεν κινείται μπροστά/πίσω
    # direction * turn_rate είναι η ταχύτητα στροφής
    drive_base.drive(0, direction * abs(turn_rate))

    # Μεταβλητή για να ξέρουμε γιατί σταματήσαμε
    reached_mode = "Unknown"

    # Ξεκινάμε βρόχο ελέγχου
    while True:

        # Διαβάζουμε τη νέα γωνία
        current_angle = drive_base.angle()

        # Υπολογίζουμε τη μικρή διαφορά γωνίας
        step_delta = Angle_Delta(previous_angle, current_angle)

        # Προσθέτουμε τη διαφορά στη συνολική περιστροφή
        real_angle += step_delta

        # Ενημερώνουμε την προηγούμενη γωνία
        previous_angle = current_angle

        # Αν φτάσαμε τον στόχο
        if abs(real_angle) >= abs(angle):
            reached_mode = "Target reached"
            break

        # Αν πέρασε ο χρόνος timeout
        if Function_Timer.time() >= timeout_ms:
            reached_mode = "Timeout reached"
            break

        # Μικρή καθυστέρηση για async σταθερότητα
        await wait(1)

    # Σταματάμε την περιστροφή
    drive_base.brake()

    # Υπολογίζουμε το σφάλμα
    error = real_angle - angle

    # Καταγράφουμε το σφάλμα
    robot_state.last_turn_error = error

    # Αν είναι ενεργό το debug
    if robot_state.track_debug_mode:
        print(
            "Turn with timeout ->",
            "Target:", angle,
            "Real:", real_angle,
            "Error:", error,
            "Mode:", reached_mode
        )

    # Επιστρέφουμε πόσο στρίψαμε
    return real_angle


# ============================================================
# STRAIGHT
# ============================================================

async def Straight(distance, stop_mode=Stop.BRAKE):
    # Η συνάρτηση αυτή κινεί το ρομπότ ευθεία
    # για συγκεκριμένη απόσταση (σε mm).

    # Διαβάζουμε την απόσταση πριν την κίνηση
    start_distance = drive_base.distance()

    # Εκτελούμε την κίνηση
    await drive_base.straight(distance, then=stop_mode)

    # Μικρή καθυστέρηση
    await wait(1)

    # Διαβάζουμε την απόσταση μετά
    end_distance = drive_base.distance()

    # Υπολογίζουμε πόσα mm κινήθηκε
    real_distance = end_distance - start_distance

    # Υπολογίζουμε το σφάλμα
    error = real_distance - distance

    # Καταγράφουμε το σφάλμα
    robot_state.last_straight_error = error

    # Αν είναι ενεργό το debug
    if robot_state.track_debug_mode:
        print(
            "Straight ->",
            "Target:", distance,
            "Real:", real_distance,
            "Error:", error
        )

# ============================================================
# STRAIGHT WITH TIMEOUT
# ============================================================

async def Straight_With_Timeout(distance, timeout_ms=100, speed=DEFAULT_DRIVE_SPEED):
    # Εκτελεί ευθεία κίνηση αλλά με χρονικό όριο.

    # Δημιουργούμε χρονόμετρο
    Function_Timer = StopWatch()

    # Μηδενίζουμε χρονόμετρο
    Function_Timer.reset()

    # Διαβάζουμε την απόσταση πριν ξεκινήσει
    previous_distance = drive_base.distance()

    # Μεταβλητή για συνολική μετακίνηση
    real_distance = 0

    # Καθορίζουμε κατεύθυνση
    direction = 1 if distance >= 0 else -1

    # Ξεκινάμε συνεχή κίνηση
    drive_base.drive(direction * abs(speed), 0)

    reached_mode = "Unknown"

    # Βρόχος ελέγχου
    while True:

        # Διαβάζουμε τρέχουσα απόσταση
        current_distance = drive_base.distance()

        # Υπολογίζουμε μικρή διαφορά
        step_delta = current_distance - previous_distance

        # Προσθέτουμε στη συνολική μετακίνηση
        real_distance += step_delta

        # Ενημερώνουμε προηγούμενη τιμή
        previous_distance = current_distance

        # Αν φτάσαμε τον στόχο
        if abs(real_distance) >= abs(distance):
            reached_mode = "Target reached"
            break

        # Αν περάσει timeout
        if Function_Timer.time() >= timeout_ms:
            reached_mode = "Timeout reached"
            break

        await wait(1)

    # Σταματάμε το ρομπότ
    drive_base.brake()

    # Υπολογίζουμε σφάλμα
    error = real_distance - distance

    # Καταγράφουμε σφάλμα
    robot_state.last_straight_error = error

    # Αν debug ενεργό
    if robot_state.track_debug_mode:
        print(
            "Straight with timeout ->",
            "Target:", distance,
            "Real:", real_distance,
            "Error:", error,
            "Mode:", reached_mode
        )

    return real_distance


# ============================================================
# ARC
# ============================================================

async def Arc(radius, angle, stop_mode=Stop.HOLD):
    # Η συνάρτηση αυτή εκτελεί καμπύλη κίνηση (arc).
    # Το ρομπότ κινείται σε κύκλο με συγκεκριμένη ακτίνα (radius)
    # και στρίβει συνολικά συγκεκριμένες μοίρες (angle).

    # Διαβάζουμε τη γωνία πριν την κίνηση
    start_angle = drive_base.angle()

    # Διαβάζουμε την απόσταση πριν την κίνηση
    start_distance = drive_base.distance()

    # Εκτελούμε την καμπύλη κίνηση
    await drive_base.arc(radius, angle=angle, then=stop_mode)

    # Μικρή καθυστέρηση για σταθεροποίηση
    await wait(1)

    # Διαβάζουμε τη γωνία μετά την κίνηση
    end_angle = drive_base.angle()

    # Διαβάζουμε την απόσταση μετά την κίνηση
    end_distance = drive_base.distance()

    # Υπολογίζουμε την πραγματική μεταβολή γωνίας
    real_heading_change = Angle_Delta(start_angle, end_angle)

    # Υπολογίζουμε την πραγματική απόσταση
    real_distance = end_distance - start_distance

    # Υπολογίζουμε ποια θα έπρεπε να είναι η μεταβολή γωνίας
    # Αν η ακτίνα είναι αρνητική αλλάζει η φορά
    expected_heading_change = -angle if radius < 0 else angle

    # Υπολογίζουμε το σφάλμα γωνίας
    error = real_heading_change - expected_heading_change

    # Καταγράφουμε το σφάλμα στο robot_state
    robot_state.last_arc_heading_error = error

    # Αν είναι ενεργό το debug mode
    if robot_state.track_debug_mode:
        print(
            "Arc ->",
            "Radius:", radius,
            "Target angle:", angle,
            "Real heading:", real_heading_change,
            "Error:", error,
            "Distance:", real_distance
        )


# ============================================================
# DRIVE UNTIL REFLECTION THRESHOLD
# ============================================================

async def Drive_Until_Reflection_Threshold(speed=DEFAULT_DRIVE_SPEED, reflection_threshold=50):
    # Η συνάρτηση αυτή κινεί το ρομπότ μπροστά
    # μέχρι ένας από τους δύο αισθητήρες
    # να φτάσει ένα συγκεκριμένο όριο φωτεινότητας.

    # Ξεκινάμε συνεχή κίνηση μπροστά
    drive_base.drive(speed, 0)

    # Μεταβλητή για να ξέρουμε ποιος αισθητήρας σταμάτησε την κίνηση
    reached_mode = "Unknown"

    # Συνεχής έλεγχος αισθητήρων
    while True:

        # Διαβάζουμε την αντανάκλαση από τον αριστερό αισθητήρα
        left_reflection = await left_colour_sensor.reflection()

        # Διαβάζουμε την αντανάκλαση από τον δεξιό αισθητήρα
        right_reflection = await right_colour_sensor.reflection()

        # Αν ο αριστερός φτάσει το όριο
        if left_reflection >= reflection_threshold:
            reached_mode = "Left threshold"
            break

        # Αν ο δεξιός φτάσει το όριο
        if right_reflection >= reflection_threshold:
            reached_mode = "Right threshold"
            break

        # Μικρή καθυστέρηση για async σταθερότητα
        await wait(1)

    # Σταματάμε το ρομπότ
    drive_base.brake()

    # Αν είναι ενεργό το debug mode
    if robot_state.track_debug_mode:
        print(
            "Drive until reflectionm threshold ->",
            "Left:", left_reflection,
            "Right:", right_reflection,
            "Mode:", reached_mode
        )


# ============================================================
# RESET CALLIPERS
# ============================================================

async def Reset_Callipers():
    # Η συνάρτηση αυτή επαναφέρει και τις δύο δαγκάνες στη θέση 0 μοιρών.

    # Θέτουμε στόχο 0 μοίρες για τη δεξιά δαγκάνα
    right_calliper.track_target(0)

    # Θέτουμε στόχο 0 μοίρες για την αριστερή δαγκάνα
    left_calliper.track_target(0)

    # Διαβάζουμε την τρέχουσα γωνία του δεξιού calliper.
    # Η angle() επιστρέφει πόσες μοίρες έχει περιστραφεί το μοτέρ
    # από την τελευταία φορά που έγινε reset_angle().
    right_calliper_angle = right_calliper.angle()

    # Διαβάζουμε την τρέχουσα γωνία του αριστερού calliper.
    # Έτσι μπορούμε να γνωρίζουμε τη θέση και των δύο δαγκανών.
    left_calliper_angle = left_calliper.angle()

    # Αν είναι ενεργό το debug
    if robot_state.utils_debug_mode:
        print(
            "Reset callipers ->",
            "Right:", right_calliper_angle,
            "Left:", left_calliper_angle
        )


# ============================================================
# CHANGE GEAR
# ============================================================

async def Change_Gear(gear):
    # Η συνάρτηση αυτή αλλάζει τη "μηχανική ταχύτητα"
    # μέσω του δεξιού calliper.

    # Αν επιλέξουμε gear 1
    if gear == 1:
        right_calliper.track_target(270)

    # Αν επιλέξουμε gear 2
    elif gear == 2:
        right_calliper.track_target(90)

    # Αν επιλέξουμε gear 3
    elif gear == 3:
        right_calliper.track_target(0)

    # Για οποιαδήποτε άλλη τιμή
    else:
        right_calliper.track_target(180)

    # Δηλώνουμε ότι έγινε αλλαγή gear
    robot_state.gear_change = 1

    # Κρατάμε τη θέση
    right_calliper.hold()

    # Περιμένουμε 250ms για μηχανική σταθεροποίηση
    await wait(250)

    # Διαβάζουμε την τρέχουσα γωνία του δεξιού calliper.
    # Η angle() επιστρέφει πόσες μοίρες έχει περιστραφεί το μοτέρ
    right_calliper_angle = right_calliper.angle()

    # Αν είναι ενεργό το debug
    if robot_state.utils_debug_mode:
        print(
            "Change gear ->",
            "Gear:", gear,
            "Angle:", right_calliper_angle
        )


# ============================================================
# MOVE CALIPER
# ============================================================

async def Move_Caliper(direction, speed, target_angle, load, check_stalled=True):
    # Η συνάρτηση αυτή κινεί την αριστερή δαγκάνα.
    # Σταματά όταν:
    # - φτάσει γωνία
    # - φτάσει load
    # - μπλοκάρει (stalled)

    # Μηδενίζουμε τη γωνία πριν ξεκινήσει
    left_calliper.reset_angle(0)

    # Αν αλλάξει κατεύθυνση από την προηγούμενη φορά
    if (direction == "right" and robot_state.previous_caliper_direction != "right") or \
       (direction == "left" and robot_state.previous_caliper_direction != "left"):
        target_angle += 90

    # Αν είχε προηγηθεί αλλαγή gear
    if robot_state.gear_change == 1:
        target_angle += 90
        robot_state.gear_change = 0

    # Αν η κατεύθυνση είναι δεξιά
    if direction == "right":
        robot_state.previous_caliper_direction = "right"
        left_calliper.run(speed)

    # Αν η κατεύθυνση είναι αριστερά
    else:
        robot_state.previous_caliper_direction = "left"
        left_calliper.run(-speed)

    reached_mode = "Unknown"

    # Βρόχος ελέγχου
    while True:

        # Διαβάζουμε γωνία
        angle_now = left_calliper.angle()

        # Διαβάζουμε φορτίο
        load_now = left_calliper.load()

        # Αν φτάσει τη γωνία
        if abs(angle_now) >= target_angle:
            reached_mode = "Angle reached"
            break

        # Αν φτάσει το load
        if abs(load_now) >= load:
            reached_mode = "Load reached"
            break

        # Ελέγχουμε stalled ΜΟΝΟ αν επιτρέπεται
        if check_stalled:
            if left_calliper.stalled():
                reached_mode = "Stalled"
                break

        # Μικρή καθυστέρηση
        await wait(1)

    # Κρατάμε τη θέση
    left_calliper.hold()

    # Αν είναι ενεργό το debug
    if robot_state.utils_debug_mode:
        print(
            "Move caliper ->",
            "Direction:", direction,
            "Target:", target_angle,
            "Angle:", angle_now,
            "Load:", load_now,
            "Mode:", reached_mode
        )
#===============================================================================
