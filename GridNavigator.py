from pybricks.tools import wait


class GridNavigator:
    # --------------------------------------------------------
    # Grid Navigator (Chessboard Localization System)
    # --------------------------------------------------------
    # Η κλάση αυτή υλοποιεί ένα σύστημα εντοπισμού θέσης
    # βασισμένο σε grid (σαν σκακιέρα).
    #
    # Στόχος:
    # Το ρομπότ να γνωρίζει σε ποιο "τετράγωνο" βρίσκεται
    # και να μην κινείται τυφλά.
    #
    # Χρησιμοποιεί:
    # - 2 αισθητήρες χρώματος
    # - grid συντεταγμένες (x, y)
    # - checkpoints για διόρθωση θέσης
    #
    # Λογική:
    # - Το grid είναι η "απόλυτη" θέση
    # - Οι αισθητήρες δίνουν "διορθώσεις"
    #
    # --------------------------------------------------------

    # --------------------------------------------------------
    # Constructor
    # --------------------------------------------------------
    def __init__(self, left_sensor, right_sensor, robot_state):
        # Αρχικοποίηση του συστήματος

        # Αισθητήρες χρώματος
        self.left_sensor = left_sensor
        self.right_sensor = right_sensor

        # Robot state για debug
        self.robot_state = robot_state

        # ----------------------------------------------------
        # Grid Dimensions
        # ----------------------------------------------------
        # Πίστα: 200 x 114 cm
        # Ρομπότ: 20 x 13.5 cm

        self.grid_width = 10   # στήλες (X)
        self.grid_height = 8   # γραμμές (Y)

        # ----------------------------------------------------
        # Current Position
        # ----------------------------------------------------
        # Ξεκινάμε από A1 → (1,1)
        self.current_position = (1, 1)

        # ----------------------------------------------------
        # Grid Coordinates Map
        # ----------------------------------------------------
        # Μετατροπή (x,y) → "A1"
        self.grid_coordinates = {}

        for y in range(1, self.grid_height + 1):
            for x in range(1, self.grid_width + 1):

                row_letter = chr(ord('A') + y - 1)
                cell_name = f"{row_letter}{x}"

                self.grid_coordinates[(x, y)] = cell_name

        # Reverse lookup: "A1" → (1,1)
        self.grid_reverse = {v: k for k, v in self.grid_coordinates.items()}

        # ----------------------------------------------------
        # Checkpoints (Sensor-based correction)
        # ----------------------------------------------------
        # Εδώ βάζουμε πραγματικά σημεία της πίστας
        # που έχουν μοναδικά patterns

        self.checkpoints = {
            # Row A
            ("green", "brown", "A1"): (1, 1),
            ("brown", "green", "A2"): (2, 1),
            ("green", "green", "A3"): (3, 1),
            ("brown", "brown", "A4"): (4, 1),
            ("green", "brown", "A5"): (5, 1),
            ("brown", "green", "A6"): (6, 1),
            ("green", "green", "A7"): (7, 1),
            ("brown", "brown", "A8"): (8, 1),
            ("green", "brown", "A9"): (9, 1),
            ("brown", "green", "A10"): (10, 1),

            # Row B
            ("brown", "green", "B1"): (1, 2),
            ("green", "brown", "B2"): (2, 2),
            ("brown", "brown", "B3"): (3, 2),
            ("green", "green", "B4"): (4, 2),
            ("brown", "green", "B5"): (5, 2),
            ("green", "brown", "B6"): (6, 2),
            ("brown", "brown", "B7"): (7, 2),
            ("green", "green", "B8"): (8, 2),
            ("brown", "green", "B9"): (9, 2),
            ("green", "brown", "B10"): (10, 2),

            # Row C
            ("green", "green", "C1"): (1, 3),
            ("brown", "brown", "C2"): (2, 3),
            ("green", "brown", "C3"): (3, 3),
            ("brown", "green", "C4"): (4, 3),
            ("green", "green", "C5"): (5, 3),
            ("brown", "brown", "C6"): (6, 3),
            ("green", "brown", "C7"): (7, 3),
            ("brown", "green", "C8"): (8, 3),
            ("green", "green", "C9"): (9, 3),
            ("brown", "brown", "C10"): (10, 3),

            # Row D
            ("green", "brown", "D1"): (1, 4),
            ("brown", "green", "D2"): (2, 4),
            ("green", "green", "D3"): (3, 4),
            ("brown", "brown", "D4"): (4, 4),
            ("green", "brown", "D5"): (5, 4),
            ("brown", "green", "D6"): (6, 4),
            ("green", "green", "D7"): (7, 4),
            ("brown", "brown", "D8"): (8, 4),
            ("green", "brown", "D9"): (9, 4),
            ("brown", "green", "D10"): (10, 4),

            # Row E
            ("brown", "green", "E1"): (1, 5),
            ("green", "brown", "E2"): (2, 5),
            ("brown", "brown", "E3"): (3, 5),
            ("green", "green", "E4"): (4, 5),
            ("brown", "green", "E5"): (5, 5),
            ("green", "brown", "E6"): (6, 5),
            ("brown", "brown", "E7"): (7, 5),
            ("green", "green", "E8"): (8, 5),
            ("brown", "green", "E9"): (9, 5),
            ("green", "brown", "E10"): (10, 5),

            # Row F
            ("green", "green", "F1"): (1, 6),
            ("brown", "brown", "F2"): (2, 6),
            ("green", "brown", "F3"): (3, 6),
            ("brown", "green", "F4"): (4, 6),
            ("green", "green", "F5"): (5, 6),
            ("brown", "brown", "F6"): (6, 6),
            ("green", "brown", "F7"): (7, 6),
            ("brown", "green", "F8"): (8, 6),
            ("green", "green", "F9"): (9, 6),
            ("brown", "brown", "F10"): (10, 6),

            # Row G
            ("green", "brown", "G1"): (1, 7),
            ("brown", "green", "G2"): (2, 7),
            ("green", "green", "G3"): (3, 7),
            ("brown", "brown", "G4"): (4, 7),
            ("green", "brown", "G5"): (5, 7),
            ("brown", "green", "G6"): (6, 7),
            ("green", "green", "G7"): (7, 7),
            ("brown", "brown", "G8"): (8, 7),
            ("green", "brown", "G9"): (9, 7),
            ("brown", "green", "G10"): (10, 7),

            # Row H
            ("brown", "green", "H1"): (1, 8),
            ("green", "brown", "H2"): (2, 8),
            ("brown", "brown", "H3"): (3, 8),
            ("green", "green", "H4"): (4, 8),
            ("brown", "green", "H5"): (5, 8),
            ("green", "brown", "H6"): (6, 8),
            ("brown", "brown", "H7"): (7, 8),
            ("green", "green", "H8"): (8, 8),
            ("brown", "green", "H9"): (9, 8),
            ("green", "brown", "H10"): (10, 8),
        }

    # --------------------------------------------------------
    # Color Classification
    # --------------------------------------------------------
    def classify_color(self, reflection):
        # Μετατροπή reflection → color

        if reflection < 20:
            return "black"
        elif reflection < 45:
            return "brown"
        else:
            return "green"

    # --------------------------------------------------------
    # Read Sensors
    # --------------------------------------------------------
    async def read_sensors(self):
        # Διαβάζει τους αισθητήρες

        left = await self.left_sensor.reflection()
        right = await self.right_sensor.reflection()

        return (
            self.classify_color(left),
            self.classify_color(right)
        )

    # --------------------------------------------------------
    # Update Position (with correction)
    # --------------------------------------------------------
    async def update_position(self):
        # Ενημερώνει τη θέση με βάση sensors

        left_color, right_color = await self.read_sensors()

        key = (left_color, right_color)

        # Αν είναι checkpoint → διορθώνουμε θέση
        if key in self.checkpoints:
            self.current_position = self.checkpoints[key]

            if self.robot_state.track_debug_mode:
                print("Grid -> Corrected to:", self.get_cell_name())

        return self.current_position

    # --------------------------------------------------------
    # Get Cell Name
    # --------------------------------------------------------
    def get_cell_name(self):
        # Επιστρέφει "A1"

        return self.grid_coordinates.get(self.current_position, "Unknown")

    # --------------------------------------------------------
    # Move Simulation (Chess-like)
    # --------------------------------------------------------
    def move(self, dx, dy):
        # Μετακινεί το ρομπότ στο grid

        x, y = self.current_position

        new_x = x + dx
        new_y = y + dy

        # Έλεγχος ορίων
        if 1 <= new_x <= self.grid_width and 1 <= new_y <= self.grid_height:
            self.current_position = (new_x, new_y)

            if self.robot_state.track_debug_mode:
                print("Grid -> Moved to:", self.get_cell_name())

    # --------------------------------------------------------
    # Check Position
    # --------------------------------------------------------
    async def is_in_cell(self, cell):
        # Ελέγχει αν είμαστε σε συγκεκριμένο κελί

        await self.update_position()
        return self.get_cell_name() == cell

    # --------------------------------------------------------
    # Wait Until Cell
    # --------------------------------------------------------
    async def wait_until_cell(self, target_cell):
        # Περιμένει μέχρι να φτάσουμε σε κελί

        while True:
            await self.update_position()

            if self.get_cell_name() == target_cell:
                if self.robot_state.track_debug_mode:
                    print("Reached:", target_cell)
                break

            await wait(10)