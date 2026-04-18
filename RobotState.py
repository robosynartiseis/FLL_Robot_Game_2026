class RobotState:
    # Κρατάει όλη την κατάσταση του ρομπότ κατά την εκτέλεση.

    # Χρησιμοποιείται για:
    # - Debug control
    # - Gear system state
    # - Μηχανική παρακολούθηση
    # - Drift tracking
    # - Runtime πληροφορίες
    # - Mission strategy control

    # --------------------------------------------------------
    # Constructor
    # --------------------------------------------------------
    def __init__(self, main_debug=False, track_debug=False, game_part_debug=False, utils_debug=False):

        # Αρχικοποίηση της κατάστασης του ρομπότ.

        # Παράμετροι debug:
        # - main_debug: Debug μηνύματα από main
        # - track_debug: Debug για κινήσεις (Turn, Straight, Arc)
        # - game_part_debug: Debug για κάθε mission
        # - utils_debug: Debug για μηχανισμούς (π.χ. caliper)

        # -------------------------
        # Debug Modes
        # -------------------------

        # Debug για main program
        self.main_debug_mode = main_debug

        # Debug για κινήσεις drive base
        self.track_debug_mode = track_debug

        # Debug για κάθε Game Part
        self.game_part_debug_mode = game_part_debug

        # Debug για βοηθητικές συναρτήσεις
        self.utils_debug_mode = utils_debug


        # --------------------------------------------------------
        # Mission Enable Table
        # --------------------------------------------------------
        # Το dictionary αυτό καθορίζει ποια missions θα εκτελεστούν.
        #
        # True  -> Το mission εκτελείται
        # False -> Το mission παραλείπεται
        #
        # Χρησιμοποιείται για:
        # - αλλαγή στρατηγικής στον αγώνα
        # - testing συγκεκριμένων missions
        # - debugging
        #
        # Παράδειγμα χρήσης μέσα σε Game Part:
        #
        # if not robot_state.enabled_missions[1]:
        #     return

        self.enabled_missions = {
            1: True,
            2: True,
            3: True,
            4: True,
            5: True,
            6: False,
            7: True,
            8: True,
            9: True,
            10: True
        }


        # --------------------------------------------------------
        # Gear System State
        # --------------------------------------------------------
        # Δείχνει αν έχει προηγηθεί αλλαγή gear.
        #
        # Χρησιμοποιείται για compensation
        # στη συνάρτηση Move_Caliper.
        #
        # Όταν αλλάζει gear:
        # gear_change = 1
        #
        # Μετά τη χρήση επανέρχεται σε:
        # gear_change = 0

        self.gear_change = 0


        # --------------------------------------------------------
        # Caliper Direction Tracking
        # --------------------------------------------------------
        # Αποθηκεύει την τελευταία κατεύθυνση
        # περιστροφής της δαγκάνας.
        #
        # Χρησιμοποιείται ώστε να γίνεται
        # σωστό angle compensation όταν αλλάζει κατεύθυνση.

        self.previous_caliper_direction = None


        # --------------------------------------------------------
        # Heading Drift Tracking
        # --------------------------------------------------------
        # Συνολική απόκλιση heading κατά τη διάρκεια του run.
        #
        # Χρησιμοποιείται για μελλοντικό
        # adaptive correction system.

        self.total_heading_drift = 0


        # --------------------------------------------------------
        # Runtime Statistics
        # --------------------------------------------------------
        # Καταγραφή πραγματικών σφαλμάτων κίνησης.

        # Πόσο διέφερε η πραγματική στροφή
        # από την επιθυμητή γωνία.
        self.last_turn_error = 0

        # Πόσο διέφερε η πραγματική απόσταση
        # από την επιθυμητή απόσταση.
        self.last_straight_error = 0

        # Λόγος τερματισμού τελευταίας κίνησης.
        #
        # Πιθανές τιμές:
        # - "Target reached"
        # - "Timeout reached"
        # - "Load reached"
        # - "Stalled"

        self.last_reached_reason = None


    # --------------------------------------------------------
    # Mission Control Helpers
    # --------------------------------------------------------

    def enable_mission(self, mission_number):
        # Ενεργοποιεί ένα συγκεκριμένο mission.

        if mission_number in self.enabled_missions:
            self.enabled_missions[mission_number] = True


    def disable_mission(self, mission_number):
        # Απενεργοποιεί ένα συγκεκριμένο mission.

        if mission_number in self.enabled_missions:
            self.enabled_missions[mission_number] = False


    # --------------------------------------------------------
    # Reset Dynamic State
    # --------------------------------------------------------

    def reset_dynamic_state(self):
        # Κάνει reset μόνο των δυναμικών μεταβλητών.
        #
        # Δεν επηρεάζει:
        # - Debug modes
        # - Mission strategy

        self.gear_change = 0
        self.previous_caliper_direction = None
        self.total_heading_drift = 0
        self.last_turn_error = 0
        self.last_straight_error = 0
        self.last_reached_reason = None


    # --------------------------------------------------------
    # Debug Helper
    # --------------------------------------------------------

    def print_state(self):
        # Εκτυπώνει ολόκληρη την κατάσταση του ρομπότ.
        # Χρήσιμο για debugging.

        print("------ ROBOT STATE ------")
        print("Main Debug:", self.main_debug_mode)
        print("Track Debug:", self.track_debug_mode)
        print("Game Part Debug:", self.game_part_debug_mode)
        print("Utils Debug:", self.utils_debug_mode)
        print("Gear Change:", self.gear_change)
        print("Previous Caliper Direction:", self.previous_caliper_direction)
        print("Total Heading Drift:", self.total_heading_drift)
        print("Last Turn Error:", self.last_turn_error)
        print("Last Straight Error:", self.last_straight_error)
        print("Last Reached Reason:", self.last_reached_reason)
        print("Enabled Missions:", self.enabled_missions)
        print("--------------------------")
#===============================================================================
