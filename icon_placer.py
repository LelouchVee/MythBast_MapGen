import random
import svgutils.transform as sg
import math

class IconPlacer:
    def __init__(self):
        pass

    def place_holdings(self, fig, color_grid, rows, cols, hex_size, x_offset, y_offset, num_holdings=None, place_seat=True):
        """Place 'Holding' icons inside randomly chosen non-water hexes with sufficient spacing."""
        if num_holdings is None:
            num_holdings = min(rows, cols) // 3  # Default limit for Holdings

        non_water_hexes = [(row, col) for row in range(rows) for col in range(cols)
                           if not self.is_water(color_grid[row][col])]

        chosen_hexes = []
        min_distance = 2  # Minimum distance in hexes

        while len(chosen_hexes) < num_holdings and non_water_hexes:
            row, col = random.choice(non_water_hexes)

            # Check if this hex is far enough from existing chosen hexes
            if all(self.distance_between_hexes(row, col, r, c) >= min_distance for r, c in chosen_hexes):
                chosen_hexes.append((row, col))
                non_water_hexes.remove((row, col))

        # Place icons
        for i, (row, col) in enumerate(chosen_hexes):
            x, y = self.get_hex_center(row, col, hex_size, x_offset, y_offset)
            icon_path = 'icons/holding.svg'
            if i == 0 and place_seat:
                icon_path = 'icons/seat.svg'  # Replace one with Seat of Power
            icon_element = self.load_icon(icon_path, x, y, hex_size)
            fig.append(icon_element)

    def distance_between_hexes(self, row1, col1, row2, col2):
        """Calculate the distance between two hexes."""
        return math.sqrt((row2 - row1) ** 2 + (col2 - col1) ** 2)

    def is_water(self, biome_color):
        """Determine if a hex is a water biome."""
        water_colors = [
            "#607D8B",  # Blue Grey - Misty Moors
            "#03A9F4",  # Light Blue - Azure Lakes
            "#2196F3",  # Blue - Cerulean Sea
            "#009688",  # Teal - Verdant Marshes
        ]
        return biome_color in water_colors

    def get_hex_center(self, row, col, hex_size, x_offset, y_offset):
        """Calculate the center of a hex based on its row and column."""
        hex_width = hex_size * 2
        hex_height = (3**0.5) * hex_size  # Height of a regular hexagon

        x = col * hex_width * 0.75 + x_offset + hex_size
        y = row * hex_height + (col % 2) * (hex_height / 2) + y_offset + hex_size / 2
        return x, y

    def load_icon(self, icon_path, x, y, hex_size):
        """Load and center the SVG icon inside the hex, assuming icons are 255x255 units."""
        icon = sg.fromfile(icon_path)
        icon_root = icon.getroot()

        # The size of the SVG file is fixed at 255x255 units
        default_size = 255.0
        scale = hex_size / default_size

        # Apply the scaling to the icon
        icon_root.scale(scale)

        # Calculate the translation to center the icon at (x, y)
        translate_x = x - (default_size / 2) * scale
        translate_y = y  # No need to adjust y; keep it centered vertically

        # Apply the translation to center the icon within the hex
        icon_root.moveto(translate_x, translate_y)

        return icon_root