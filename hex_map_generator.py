import svgutils.transform as sg
from svgutils.compose import Unit
import math
import string
from cairosvg import svg2png
from biome_colors import BiomeColors
from icon_placer import IconPlacer


class HexMapGenerator:
    def __init__(self, rows, cols, hex_size=50, show_labels=True, randomness=0.2, dpi=300, map_style='Random', num_holdings=None, place_seat=True):
        self.rows = rows
        self.cols = cols
        self.hex_size = hex_size
        self.show_labels = show_labels
        self.randomness = randomness
        self.dpi = dpi  # Set the DPI for the output PNG
        self.map_style = map_style  # Set the map style
        self.biome_colors = BiomeColors(randomness=randomness, map_style=map_style)  # Initialize biome color generator
        self.hex_width = hex_size * 2
        self.hex_height = math.sqrt(3) * hex_size

        # Calculate the size of the entire grid including the labels
        self.grid_width = self.cols * self.hex_width * 0.75 + self.hex_size
        self.grid_height = self.rows * self.hex_height + self.hex_height * 0.5
        
        self.canvas_width = self.grid_width + self.hex_size * 1.5
        self.canvas_height = self.grid_height + self.hex_size * 1.5
        
        self.icon_placer = IconPlacer()
        self.num_holdings = num_holdings  # Store the number of holdings, can be None
        self.place_seat = place_seat
        

    def generate_svg(self):
        fig = sg.SVGFigure(Unit(self.canvas_width), Unit(self.canvas_height))

        # Calculate the offsets to center the grid and labels on the canvas
        x_offset = (self.canvas_width - self.grid_width) / 2
        y_offset = (self.canvas_height - self.grid_height) / 2

        # Initialize a grid to store the color of each hex
        color_grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]

        # Generate colors for the hexagons based on the map style and clumping
        for row in range(self.rows):
            for col in range(self.cols):
                color = self.biome_colors.get_biome_color(color_grid, row, col, self.rows, self.cols)
                color_grid[row][col] = color

                x = col * self.hex_width * 0.75 + self.hex_size + x_offset
                y = row * self.hex_height + (col % 2) * (self.hex_height / 2) + self.hex_size + y_offset
                
                hex_element = self.create_hex(x, y, color)
                fig.append(hex_element)
 
        self.icon_placer.place_holdings(fig, color_grid, self.rows, self.cols, self.hex_size, x_offset, y_offset, self.num_holdings)

        # Add row and column labels if enabled
        if self.show_labels:
            self.add_labels(fig, x_offset, y_offset)
        
        return fig

    def add_labels(self, fig, x_offset, y_offset):
        # Add row labels on the left side
        for row in range(self.rows):
            y = row * self.hex_height + self.hex_size + (self.hex_height / 2) + y_offset
            label = string.ascii_uppercase[row]
            label_element = self.create_side_label(x=x_offset, y=y, text=label)
            fig.append(label_element)
        
        # Add column labels on the top
        for col in range(self.cols):
            x = col * self.hex_width * 0.75 + self.hex_size + x_offset
            label = f"{col + 1}"
            label_element = self.create_side_label(x=x, y=y_offset, text=label)
            fig.append(label_element)

    def create_hex(self, x, y, color):
        hex_points = [
            (x + self.hex_size * math.cos(math.radians(angle)),
             y + self.hex_size * math.sin(math.radians(angle)))
            for angle in range(0, 360, 60)
        ]
        points_str = " ".join(f"{p[0]},{p[1]}" for p in hex_points)
        hex_element = sg.fromstring(f'<polygon points="{points_str}" fill="{color}" stroke="black"/>')
        return hex_element

    def create_side_label(self, x, y, text):
        label_element = sg.fromstring(f'<text x="{x}" y="{y}" font-size="18" text-anchor="middle" fill="black">{text}</text>')
        return label_element

    def save_map(self, filename):
        svg_map = self.generate_svg()
        
        # Save the SVG file
        svg_map.save(f"output/{filename}.svg")
        
        # Calculate the scale factor based on DPI
        scale_factor = self.dpi / 96  # Default DPI for SVG is 96
        
        # Convert to PNG with a white background and the specified DPI resolution
        svg2png(
            url=f"output/{filename}.svg",
            write_to=f"output/{filename}.png",
            background_color="white",
            scale=scale_factor
        )
