"""
Test Piece Generator - Creates small test pieces with 5 holes in 0.1mm increments
For testing hole sizes before printing the full hardware board
"""

import cadquery as cq
from typing import Dict, Tuple
from . import holes


class TestPieceGenerator:
    """Generates test pieces with 5 holes in 0.1mm increments"""

    def __init__(self, params: Dict):
        """Initialize test piece generator with parameters"""
        self.params = params
        self.piece_type = params['piece_type']
        self.bolt_slip_fit = params['bolt_slip_fit']

        # Base size for the piece being tested
        self.base_size = params['base_size']

        # Generate 5 sizes: base, base+0.1, base+0.2, base+0.3, base+0.4
        self.test_sizes = [round(self.base_size + (i * 0.1), 1) for i in range(5)]

        # Spacing between holes
        self.hole_spacing = 15  # mm between hole centers

    def calculate_dimensions(self) -> Tuple[float, float, float]:
        """Calculate test piece dimensions based on hole type"""
        # Width: 5 holes with spacing + margins
        width = (self.hole_spacing * 4) + 20  # 20mm total margins

        # Height: based on largest hole + margins
        max_hole_size = max(self.test_sizes)
        height = max_hole_size + 20  # 10mm margin on each side

        # Depth: based on hole type
        if self.piece_type == 'bolt_slip_fit':
            depth = 6.0  # Simple through hole, standard depth
        elif self.piece_type == 'hex_nut':
            depth = self.params.get('hex_depth', 3.0) + 1.0
        elif self.piece_type == 'square_nut':
            depth = self.params.get('square_depth', 3.0) + 1.0
        elif self.piece_type == 'counter_bore':
            depth = self.params.get('counter_bore_depth', 3.0) + 1.0
        elif self.piece_type == 'counter_bore_washer':
            depth = self.params.get('counter_bore_washer_depth', 3.0) + 1.0
        elif self.piece_type == 'counter_sunk':
            depth = self.params.get('counter_sunk_chamfer_depth', 2.0) + 2.0
        elif self.piece_type == 'heat_insert':
            depth = self.params.get('heat_insert_depth', 6.0) + 1.0
        elif self.piece_type == 'vertical_square':
            depth = self.params.get('square_slip_fit_vertical_depth', 6.0) + 1.0
        else:
            depth = 6.0

        return width, height, depth

    def create_base_piece(self) -> cq.Workplane:
        """Create the base rectangular piece"""
        width, height, depth = self.calculate_dimensions()

        piece = cq.Workplane("XY").box(width, height, depth)
        piece = piece.edges("|Z").fillet(2.0)  # Round corners
        piece = piece.edges("|X").fillet(0.5)

        return piece

    def add_size_labels(self, piece: cq.Workplane) -> cq.Workplane:
        """Add size labels above each hole (cut into the piece)"""
        width, height, depth = self.calculate_dimensions()

        # Starting X position (leftmost hole)
        start_x = -(self.hole_spacing * 2)
        label_y = height/2 - 5  # 5mm from top edge

        for i, size in enumerate(self.test_sizes):
            x = start_x + (i * self.hole_spacing)
            label_text = str(size)

            # Create text at top of piece
            text_piece = (cq.Workplane("XY")
                         .workplane(offset=depth/2)
                         .text(label_text, 8, -0.5,  # Cut 0.5mm into surface, 8mm text size
                               halign='center', valign='center',
                               cut=False, combine=True,
                               font="Arial Black")
                         .translate((x, label_y, 0)))

            piece = piece.cut(text_piece)

        return piece

    def create_holes(self, piece: cq.Workplane) -> cq.Workplane:
        """Create the test holes based on piece type"""
        width, height, depth = self.calculate_dimensions()

        # Starting X position (leftmost hole)
        start_x = -(self.hole_spacing * 2)
        y = -3  # Position holes lower (not centered)

        for i, size in enumerate(self.test_sizes):
            x = start_x + (i * self.hole_spacing)

            if self.piece_type == 'bolt_slip_fit':
                # Simple through hole
                piece = holes.create_bolt_slip_fit(piece, x, y, size, depth)

            elif self.piece_type == 'hex_nut':
                # Hex nut pocket + bolt through hole
                hex_depth = self.params.get('hex_depth', 3.0)
                piece = holes.add_hex_holes(piece, x, y, size, hex_depth,
                                           self.bolt_slip_fit, depth)

            elif self.piece_type == 'square_nut':
                # Square nut pocket + bolt through hole
                square_depth = self.params.get('square_depth', 3.0)
                piece = holes.add_square_hole(piece, x, y, size, square_depth,
                                             self.bolt_slip_fit, depth)

            elif self.piece_type == 'counter_bore':
                # Counter bore + bolt through hole
                cb_depth = self.params.get('counter_bore_depth', 3.0)
                piece = holes.add_counter_bore_holes(piece, x, y, size, cb_depth,
                                                     self.bolt_slip_fit, depth)

            elif self.piece_type == 'counter_bore_washer':
                # Counter bore + washer + bolt through hole
                cbw_depth = self.params.get('counter_bore_washer_depth', 3.0)
                piece = holes.add_counter_bore_holes(piece, x, y, size, cbw_depth,
                                                     self.bolt_slip_fit, depth)

            elif self.piece_type == 'counter_sunk':
                # Counter sunk + bolt through hole
                inputs = {
                    'counter_sunk_diameter': size,
                    'counter_sunk_chamfer_depth': self.params.get('counter_sunk_chamfer_depth', 2.0),
                    'counter_sunk_chamfer': self.params.get('counter_sunk_chamfer', 1.5),
                }
                piece = holes.add_counter_sink_holes(piece, x, y, inputs,
                                                     self.bolt_slip_fit, depth)

            elif self.piece_type == 'heat_insert':
                # Heat insert pocket + bolt through hole
                insert_depth = self.params.get('heat_insert_depth', 6.0)
                piece = holes.add_counter_bore_holes(piece, x, y, size, insert_depth,
                                                     self.bolt_slip_fit, depth)

            elif self.piece_type == 'vertical_square':
                # Vertical square slot (rotated 90 degrees)
                # Position 5mm from bottom edge instead of below center
                slot_y = -(height/2) + 5
                slot_width = self.params.get('square_slip_fit_vertical_width', 2.1)
                slot_length = size  # Testing the length dimension
                slot_depth = self.params.get('square_slip_fit_vertical_depth', 6.0)
                piece = holes.add_vertical_square_slot(piece, x, slot_y, slot_depth,
                                                       slot_length, slot_width,
                                                       self.bolt_slip_fit, depth, height)

        return piece

    def generate(self) -> str:
        """Generate test piece and return file path"""
        import tempfile
        import os

        # Create base piece
        piece = self.create_base_piece()

        # Add holes
        piece = self.create_holes(piece)

        # Add size labels
        piece = self.add_size_labels(piece)

        # Translate so bottom is at Z=0
        _, _, depth = self.calculate_dimensions()
        piece = piece.translate((0, 0, depth / 2))

        # Export to STL
        temp_dir = tempfile.mkdtemp()
        filename = f"test_{self.piece_type}_{self.base_size}.stl"
        file_path = os.path.join(temp_dir, filename)

        cq.exporters.export(piece, file_path)

        return file_path
