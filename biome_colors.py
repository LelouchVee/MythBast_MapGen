import random

class BiomeColors:
    def __init__(self, randomness=0.2, map_style='Random'):
        self.randomness = randomness
        self.map_style = map_style

        # Define biome groups based on hue
        self.water_colors = [
            "#607D8B",  # Blue Grey - Misty Moors
            "#03A9F4",  # Light Blue - Azure Lakes
            "#2196F3",  # Blue - Cerulean Sea (main for Island, Archipelago, and Shore)
            "#009688",  # Teal - Verdant Marshes
        ]

        self.forest_colors = [
            "#4CAF50",  # Green - Emerald Forest
            "#8BC34A",  # Light Green - Verdant Plains
            "#2E7D32",  # Dark Green - Pine Forest
            "#1B5E20",  # Darker Green - Deep Woods
            "#388E3C",  # Medium Dark Green - Woodland
            "#CDDC39",  # Lime - Savanna Grasslands
        ]

        self.plain_colors = [
            "#FFEB3B",  # Yellow - Golden Dunes
            "#FFC107",  # Amber - Sunlit Meadows
        ]

        self.mountain_colors = [
            "#8D6E63",  # Brown - Sierra Brown
            "#795548",  # Brown - Umberwood
            "#6D4C41",  # Dark Brown - Rocky Earth
            "#A1887F",  # Light Brown - Dusty Peaks
            "#FF9800",  # Orange - Terracotta Highlands
            "#FF5722",  # Deep Orange - Cinder Wastes
        ]

        # Pre-select sides for water in the Shore style
        self.water_sides = self._select_water_sides()

    # ... remaining code ...


    def _select_water_sides(self):
        """Randomly select one or two sides to be predominantly water."""
        sides = ['top', 'bottom', 'left', 'right']
        selected_sides = random.sample(sides, random.choice([1, 2]))
        return selected_sides

    def get_biome_color(self, color_grid, row, col, total_rows, total_cols):
        """Generate a color for a hex, considering the map style and biome clumping."""
        if self.map_style == 'Continental':
            return self._continental_biome(row, col, total_rows, total_cols)
        elif self.map_style == 'Shore':
            return self._shore_biome(row, col, total_rows, total_cols)
        elif self.map_style == 'Island':
            return self._island_biome(row, col, total_rows, total_cols)
        elif self.map_style == 'Archipelago':
            return self._archipelago_biome(row, col, total_rows, total_cols)
        elif self.map_style == 'Valleys':
            return self._valleys_biome(row, col, total_rows, total_cols)
        else:
            return self._random_biome(color_grid, row, col)

    def _random_biome(self, color_grid, row, col):
        """Default random biome generation with clumping."""
        neighbors = self.get_neighbors_colors(color_grid, row, col)
        if neighbors and random.random() > self.randomness:
            return random.choice(neighbors)
        else:
            return random.choice(
                self.water_colors + self.forest_colors + self.plain_colors + self.mountain_colors
            )

    def _continental_biome(self, row, col, total_rows, total_cols):
        """Small clumps of water biomes around the map."""
        if random.random() < 0.1:
            return random.choice(self.water_colors)
        else:
            return random.choice(self.forest_colors + self.plain_colors + self.mountain_colors)

    def _shore_biome(self, row, col, total_rows, total_cols):
        """Waters along one or two sides of the map with a predominantly Cerulean Sea color."""
        shore_margin = random.uniform(0.1, 0.3)  # Randomize the width of the shore

        if 'top' in self.water_sides and row < total_rows * shore_margin:
            return "#2196F3"  # Cerulean Sea
        elif 'bottom' in self.water_sides and row > total_rows * (1 - shore_margin):
            return "#2196F3"  # Cerulean Sea
        elif 'left' in self.water_sides and col < total_cols * shore_margin:
            return "#2196F3"  # Cerulean Sea
        elif 'right' in self.water_sides and col > total_cols * (1 - shore_margin):
            return "#2196F3"  # Cerulean Sea
        else:
            return random.choice(self.forest_colors + self.plain_colors + self.mountain_colors)

    def _island_biome(self, row, col, total_rows, total_cols):
        """Waters along all sides of the map, with scaled margins that are never narrower than 1 hex."""
        # Scale margins based on the total number of rows and columns
        margin_factor = 0.1  # Base factor for the margins
        row_margin = max(int(total_rows * margin_factor), 1)  # Ensure at least 1 hex wide
        col_margin = max(int(total_cols * margin_factor), 1)  # Ensure at least 1 hex wide
    
        # Introduce a slight random shift to break up uniformity
        random_shift_row = random.randint(-1, 1)
        random_shift_col = random.randint(-1, 1)
    
        # Calculate the dynamic margins based on the row and column positions
        top_margin = row_margin + random_shift_row
        bottom_margin = total_rows - row_margin + random_shift_row
        left_margin = col_margin + random_shift_col
        right_margin = total_cols - col_margin + random_shift_col
    
        # Determine if the current hex should be water
        if (row < top_margin or row > bottom_margin or
            col < left_margin or col > right_margin):
            return "#2196F3"  # Cerulean Sea
        else:
            return random.choice(self.forest_colors + self.plain_colors + self.mountain_colors)


    def _archipelago_biome(self, row, col, total_rows, total_cols):
        """Small clumps of different biomes across the map, with more random water coverage."""
        water_probability = random.uniform(0.4, 0.6)  # Randomize the likelihood of water
        if random.random() < water_probability:
            return "#2196F3"  # Cerulean Sea
        else:
            return random.choice(self.forest_colors + self.plain_colors + self.mountain_colors)

    def _valleys_biome(self, row, col, total_rows, total_cols):
        """More mountains, especially along the sides of the map."""
        if row < total_rows * 0.2 or row > total_rows * 0.8 or random.random() < 0.2:
            return random.choice(self.mountain_colors)
        else:
            return random.choice(self.forest_colors + self.plain_colors)

    def get_neighbors_colors(self, color_grid, row, col):
        """Return a list of colors from neighboring hexes."""
        neighbors = []
        offsets = [
            (-1, 0), (-1, 1), (0, -1), (0, 1), (1, 0), (1, -1)
        ] if col % 2 == 0 else [
            (-1, -1), (-1, 0), (0, -1), (0, 1), (1, 0), (1, 1)
        ]
        
        for dy, dx in offsets:
            nr, nc = row + dy, col + dx
            if 0 <= nr < len(color_grid) and 0 <= nc < len(color_grid[0]):
                neighbor_color = color_grid[nr][nc]
                if neighbor_color:
                    neighbors.append(neighbor_color)
        
        return neighbors
