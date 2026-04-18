"""
Hardware Design Test Board Generator using CadQuery
Fully parametric version using modular architecture
"""

import cadquery as cq
import math
from typing import Dict, Tuple, Optional
from . import holes, lines, outlines, text


class HardwareBoardGenerator:
    """Generates fully parametric hardware test boards for any bolt size"""

    # Constants for parametric scaling
    DIMENSION_LINE_WIDTH = 0.6
    OUTLINE_LINE_WIDTH = 0.8
    EXTRUSION_HEIGHT = 0.3
    BASE_TEXT_SIZE = 5  # Base size for M3, will scale
    TRIANGLE_SIZE_MULTIPLIER = 1.2

    def __init__(self, params: Dict):
        """Initialize board generator with hardware parameters"""
        self.params = params
        self.bolt_size = params.get('bolt_size', 'M3')
        self.bolt_head_type = params.get('bolt_head_type', '')

        # Extract all dimensions
        self.bolt_slip_fit = params['bolt_slip_fit']
        self.press_fit_hex = params['press_fit_hex']
        self.slip_fit_hex = params['slip_fit_hex']
        self.hex_depth = params['hex_depth']
        self.counter_bore_diameter = params['counter_bore_diameter']
        self.counter_bore_depth = params['counter_bore_depth']
        self.counter_sunk_diameter = params['counter_sunk_diameter']
        self.counter_sunk_chamfer_depth = params['counter_sunk_chamfer_depth']
        self.counter_sunk_chamfer = params['counter_sunk_chamfer']
        self.counter_bore_washer_diameter = params['counter_bore_washer_diameter']
        self.counter_bore_washer_depth = params['counter_bore_washer_depth']
        self.square_press_fit = params['square_press_fit']
        self.square_slip_fit = params['square_slip_fit']
        self.square_depth = params['square_depth']
        self.square_slip_fit_vertical_width = params['square_slip_fit_vertical_width']
        self.square_slip_fit_vertical_length = params['square_slip_fit_vertical_length']
        self.square_slip_fit_vertical_depth = params['square_slip_fit_vertical_depth']
        self.heat_insert_diameter = params.get('heat_insert_diameter', params['bolt_slip_fit'] * 1.3)
        self.heat_insert_depth = params.get('heat_insert_depth')  # Optional, defaults to None

        # Export parameters
        self.export_mode = params.get('export_mode', 'single_raised')
        self.text_height = params.get('text_height', 0.4)
        self.line_width = params.get('line_width', 0.8)

        # Parse export mode
        self.is_multi_color = self.export_mode.startswith('multi_')
        self.is_raised = 'raised' in self.export_mode
        self.is_cutout = 'cutout' in self.export_mode
        self.is_recessed = 'recessed' in self.export_mode

        # Calculate scale factor (M3 = 1.0)
        base_scale = self.bolt_slip_fit / 3.3

        # Limit scale to keep board under 170mm max dimension
        # M3 board is ~123mm tall, so max scale is 170/123 = 1.38
        MAX_SCALE = 1.38
        self.scale = min(base_scale, MAX_SCALE)

        # If scale was limited, adjust margins to compensate
        self.scale_limited = base_scale > MAX_SCALE
        self.original_scale = base_scale

        # Calculate board dimensions and coordinates
        self.height, self.width, self.coordinates = self.get_coordinates()
        self.block_depth = self.square_slip_fit_vertical_depth + 0.6

    def get_coordinates(self) -> Tuple[float, float, Dict]:
        """Calculate parametric board dimensions and feature coordinates"""

        # Calculate total hardware dimensions
        max_hardware_height = (self.press_fit_hex + self.slip_fit_hex +
                               self.counter_bore_diameter + self.counter_sunk_diameter +
                               self.heat_insert_diameter)
        max_hardware_width = self.counter_bore_diameter + self.counter_bore_washer_diameter

        # Parametric spacing that scales with hardware size
        vertical_gap = 10 * self.scale

        # Total height with scaled spacing
        height = max_hardware_height + (vertical_gap * 3) + (70 * self.scale)

        # Width calculation with parametric margins
        base_margin = 85 * self.scale
        width = max_hardware_width + base_margin

        # Calculate row positions from top to bottom (parametric)
        row1_y = height/2 - max(self.slip_fit_hex/2, self.square_slip_fit/2) - (15 * self.scale)
        row2_y = row1_y - max(self.slip_fit_hex, self.square_slip_fit) - (15.5 * self.scale)
        row3_y = row2_y - max(self.press_fit_hex, self.square_press_fit) - (12 * self.scale)
        row4_y = row3_y - max(self.counter_bore_diameter, self.counter_bore_washer_diameter) - (17 * self.scale)

        vert_square_y = -((height/2) - (self.square_slip_fit_vertical_width/2)) + (7 * self.scale)

        # X-coordinate (parametric)
        x = (width/2) - (self.counter_sunk_diameter/2) - (20 * self.scale)
        heat_insert_y = vert_square_y + (3 * self.scale)

        coordinates = {
            "row1_y": row1_y,
            "row2_y": row2_y,
            "row3_y": row3_y,
            "row4_y": row4_y,
            "x": x,
            "vert_square_y": vert_square_y,
            "heat_insert_y": heat_insert_y
        }

        return height, width, coordinates

    def create_case_block(self) -> cq.Workplane:
        """Create the base board with filleted edges"""
        model = cq.Workplane("XY").box(self.width, self.height, self.block_depth)
        model = model.edges("|Z").fillet(5 * self.scale)
        model = model.edges("|X").fillet(0.5 * self.scale)
        return model

    def create_model(self) -> cq.Workplane:
        """Create the board with all holes using modular hole functions"""
        model = self.create_case_block()

        # Convert to inputs dict for original function signatures
        inputs = {
            "bolt_slip_fit": self.bolt_slip_fit,
            "slip_fit_hex": self.slip_fit_hex,
            "press_fit_hex": self.press_fit_hex,
            "hex_depth": self.hex_depth,
            "counter_bore_diameter": self.counter_bore_diameter,
            "counter_bore_depth": self.counter_bore_depth,
            "counter_sunk_diameter": self.counter_sunk_diameter,
            "counter_sunk_chamfer_depth": self.counter_sunk_chamfer_depth,
            "counter_sunk_chamfer": self.counter_sunk_chamfer,
            "counter_bore_washer_diameter": self.counter_bore_washer_diameter,
            "counter_bore_washer_depth": self.counter_bore_washer_depth,
            "square_press_fit": self.square_press_fit,
            "square_slip_fit": self.square_slip_fit,
            "square_depth": self.square_depth,
            "square_slip_fit_vertical_width": self.square_slip_fit_vertical_width,
            "square_slip_fit_vertical_length": self.square_slip_fit_vertical_length,
            "square_slip_fit_vertical_depth": self.square_slip_fit_vertical_depth,
            "heat_insert": self.heat_insert_diameter,
        }

        # LEFT SIDE HOLES
        model = holes.add_hex_holes(model, -self.coordinates["x"], self.coordinates["row1_y"],
                                    inputs["slip_fit_hex"], inputs["hex_depth"],
                                    inputs["bolt_slip_fit"], self.block_depth)
        model = holes.add_hex_holes(model, -self.coordinates["x"], self.coordinates["row2_y"],
                                    inputs["press_fit_hex"], inputs["hex_depth"],
                                    inputs["bolt_slip_fit"], self.block_depth)
        model = holes.add_counter_bore_holes(model, -self.coordinates["x"], self.coordinates["row3_y"],
                                             inputs["counter_bore_diameter"], inputs["counter_bore_depth"],
                                             inputs["bolt_slip_fit"], self.block_depth)
        model = holes.add_counter_sink_holes(model, -self.coordinates["x"], self.coordinates["row4_y"],
                                             inputs, inputs["bolt_slip_fit"], self.block_depth)

        # Use custom heat insert depth if provided, otherwise default to block_depth - 1
        heat_insert_depth_value = self.heat_insert_depth if self.heat_insert_depth is not None else self.block_depth - 1
        model = holes.add_counter_bore_holes(model, -self.coordinates["x"], self.coordinates["heat_insert_y"],
                                             inputs["heat_insert"], heat_insert_depth_value,
                                             inputs["bolt_slip_fit"], self.block_depth)

        # RIGHT SIDE HOLES
        model = holes.add_square_hole(model, self.coordinates["x"], self.coordinates["row1_y"],
                                     inputs["square_slip_fit"], inputs["square_depth"],
                                     inputs["bolt_slip_fit"], self.block_depth)
        model = holes.add_square_hole(model, self.coordinates["x"], self.coordinates["row2_y"],
                                     inputs["square_press_fit"], inputs["square_depth"],
                                     inputs["bolt_slip_fit"], self.block_depth)
        model = holes.add_counter_bore_holes(model, self.coordinates["x"], self.coordinates["row3_y"],
                                             inputs["counter_bore_washer_diameter"],
                                             inputs["counter_bore_washer_depth"],
                                             inputs["bolt_slip_fit"], self.block_depth)

        # Bolt slip fit hole
        hole_y = self.coordinates["row3_y"] - (inputs["counter_bore_washer_diameter"]/2) - (14 * self.scale/2) - (inputs["bolt_slip_fit"]/2)
        hole_y1 = self.coordinates["vert_square_y"] + (inputs["square_slip_fit_vertical_width"]/2) + (15 * self.scale/2) + (4 * self.scale)
        center = ((hole_y + hole_y1) / 2)
        model = holes.create_bolt_slip_fit(model, self.coordinates["x"], center,
                                          inputs["bolt_slip_fit"], self.block_depth)

        # Vertical Square Slot with side and bottom holes
        model = holes.add_vertical_square_slot(model, self.coordinates["x"], self.coordinates["vert_square_y"],
                                               inputs["square_slip_fit_vertical_depth"],
                                               inputs["square_slip_fit_vertical_length"],
                                               inputs["square_slip_fit_vertical_width"],
                                               inputs["bolt_slip_fit"], self.block_depth, self.height)

        return model

    def generate_graphics_layer(self) -> Optional[cq.Workplane]:
        """Generate all text, outlines, and dimension lines using modular functions"""

        # Convert to inputs dict with bolt_type for text generation
        inputs = {
            "bolt_type": f"{self.bolt_size} {self.bolt_head_type}".strip(),
            "bolt_slip_fit": self.bolt_slip_fit,
            "slip_fit_hex": self.slip_fit_hex,
            "press_fit_hex": self.press_fit_hex,
            "hex_depth": self.hex_depth,
            "counter_bore_diameter": self.counter_bore_diameter,
            "counter_bore_depth": self.counter_bore_depth,
            "counter_sunk_diameter": self.counter_sunk_diameter,
            "counter_sunk_chamfer_depth": self.counter_sunk_chamfer_depth,
            "counter_sunk_chamfer": self.counter_sunk_chamfer,
            "counter_bore_washer_diameter": self.counter_bore_washer_diameter,
            "counter_bore_washer_depth": self.counter_bore_washer_depth,
            "square_press_fit": self.square_press_fit,
            "square_slip_fit": self.square_slip_fit,
            "square_depth": self.square_depth,
            "square_slip_fit_vertical_width": self.square_slip_fit_vertical_width,
            "square_slip_fit_vertical_length": self.square_slip_fit_vertical_length,
            "square_slip_fit_vertical_depth": self.square_slip_fit_vertical_depth,
            "heat_insert": self.heat_insert_diameter,
        }

        # Generate all graphics components with parametric scaling
        text_layer = text.add_text(inputs, self.coordinates, self.height, self.scale, self.text_height)

        # Scale triangle size proportionally with board
        triangle_multiplier = self.TRIANGLE_SIZE_MULTIPLIER * self.scale

        lines_layer = lines.add_lines(inputs, self.coordinates,
                                      self.line_width * self.scale,
                                      triangle_multiplier,
                                      self.text_height,
                                      self.scale)
        outlines_layer = outlines.add_outlines(inputs, self.coordinates, self.height,
                                               self.line_width,
                                               self.text_height,
                                               self.scale)

        # Combine all graphics
        graphics = text_layer + lines_layer + outlines_layer
        return graphics

    def generate_base_board(self) -> cq.Workplane:
        """Generate base board with all holes"""
        board = self.create_model()

        # Handle single color modes - graphics are part of the board
        if not self.is_multi_color:
            graphics = self.generate_graphics_layer()
            if graphics:
                if self.is_cutout:
                    # single_cutout: subtract graphics from board surface
                    board = board.cut(graphics)
                else:
                    # single_raised: union graphics with board
                    board = board.union(graphics)

        return board

    def export_stl(self, board: cq.Workplane, filename: str):
        """Export to STL"""
        cq.exporters.export(board, filename)

    def generate(self) -> Tuple[str, Optional[str]]:
        """Generate board and return file paths"""
        import tempfile
        import os

        base_board = self.generate_base_board()

        # Translate board so bottom is at Z=0 (board is centered, so translate up by half its thickness)
        base_board = base_board.translate((0, 0, self.block_depth / 2))

        temp_dir = tempfile.mkdtemp()

        base_filename = f"{self.bolt_size}_hardware_board_base.stl"
        base_path = os.path.join(temp_dir, base_filename)
        self.export_stl(base_board, base_path)

        graphics_path = None
        if self.is_multi_color:
            graphics_layer = self.generate_graphics_layer()
            if graphics_layer:
                # Position graphics based on export mode
                if self.is_recessed:
                    # multi_recessed: graphics flush with top surface (translate down into board by text_height)
                    z_offset = self.block_depth / 2 - self.text_height
                else:
                    # multi_raised: graphics raised above top surface
                    z_offset = self.block_depth / 2

                graphics_layer = graphics_layer.translate((0, 0, z_offset))

                graphics_filename = f"{self.bolt_size}_hardware_board_graphics.stl"
                graphics_path = os.path.join(temp_dir, graphics_filename)
                self.export_stl(graphics_layer, graphics_path)

        return base_path, graphics_path
