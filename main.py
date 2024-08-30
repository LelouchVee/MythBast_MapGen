import argparse
from hex_map_generator import HexMapGenerator

def main():
    parser = argparse.ArgumentParser(
        description="Generate a hex map with optional labels, biome clumping, and map styles."
    )

    parser.add_argument("rows", type=int, nargs='?', default=12, help="Number of rows in the hex grid (default: 12)")
    parser.add_argument("cols", type=int, nargs='?', default=12, help="Number of columns in the hex grid (default: 12)")
    parser.add_argument("--size", type=int, default=50, help="Size of each hexagon (default: 50)")
    parser.add_argument("--labels", type=bool, default=True, help="Show row and column labels (default: True)")
    parser.add_argument("--randomness", type=float, default=0.2, help="Control the randomness of biome clumping (0-1, default: 0.2)")
    parser.add_argument("--dpi", type=int, default=300, help="Set the DPI for the output PNG (default: 300)")
    parser.add_argument("--map_style", type=str, default="Random", choices=["Random", "Continental", "Shore", "Island", "Archipelago", "Valleys"], help="Control the general look of the map (default: Random)")
    parser.add_argument("--holdings", type=int, default=None, help="Number of Holding icons to place on the map (default: calculated based on map size)")
    parser.add_argument("--place_seat", type=bool, default=True, help="Whether to replace one holding with a Seat of Power (default: True)")
    parser.add_argument("--filename", type=str, default="hex_map_example", help="Output filename without extension (default: hex_map_example)")

    args = parser.parse_args()

    generator = HexMapGenerator(
        rows=args.rows,
        cols=args.cols,
        hex_size=args.size,
        show_labels=args.labels,
        randomness=args.randomness,
        dpi=args.dpi,
        map_style=args.map_style,
        num_holdings=args.holdings,
        place_seat=args.place_seat
    )
    generator.save_map(args.filename)
    print(f"Map generated: output/{args.filename}.svg and output/{args.filename}.png")

if __name__ == "__main__":
    main()
