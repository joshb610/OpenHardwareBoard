import cadquery as cq # type: ignore

def create_triangle(line_width=0.4, size_multiplier=1.0, extrusion_height=0.4):
    """
    Create a solid triangle (arrow) with parametric sizing.

    Args:
        line_width: Not used for solid triangles, kept for compatibility
        size_multiplier: Scale factor for triangle size (default 1.0x)
        extrusion_height: Height/depth of extrusion in z-axis (default 0.4mm)
    """

    # Triangle dimensions (scaled by multiplier)
    base_size = 2.2  # Base side length
    side_length = base_size * size_multiplier

    # Compute the height of the equilateral triangle
    height = (side_length * (3 ** 0.5)) / 2

    # Create solid triangle
    triangle = (
        cq.Workplane("XY")
        .polyline([
            (-side_length / 2, 0),
            (side_length / 2, 0),
            (0, height),
            (-side_length / 2, 0)
        ])
        .close()
        .extrude(extrusion_height)
    )

    # Add small fillets to smooth the edges
    # Fillet radius scales with triangle size (0.15mm base * size_multiplier)
    fillet_radius = 0.15 * size_multiplier

    # Only apply fillet if it's reasonable (not too large for the triangle)
    if fillet_radius > 0.05 and fillet_radius < side_length * 0.2:
        try:
            triangle = triangle.edges("|Z").fillet(fillet_radius)
        except:
            # If filleting fails, return triangle without fillets
            pass

    return triangle

def create_lines(x, y, length, between, side, line_width=0.4, size_multiplier=1.0, extrusion_height=0.4):
    """
    Create dimension lines with arrows.

    Args:
        x, y: Position
        length: Length of horizontal lines
        between: Distance between the two parallel lines (diameter value)
        side: "left" or "right" for triangle positioning
        line_width: Width of the lines (default 0.4mm)
        size_multiplier: Scale factor for triangles (default 1.0x)
    """
    if(side == "left"):
        offset = 1.5 * size_multiplier
    else:
        offset = -1.5 * size_multiplier

    # Store original diameter value for digit check
    diameter_value = between
    between = between - line_width

    right_line = cq.Workplane("XY").box(length, line_width, extrusion_height).translate((0, 0, extrusion_height/2))
    left_line = cq.Workplane("XY").box(length, line_width, extrusion_height).translate((0, 0, extrusion_height/2))

    right_line = right_line.translate((x,y+(between/2),0))
    left_line = left_line.translate((x,y-(between/2),0))

    left_triangle = create_triangle(line_width, size_multiplier, extrusion_height)
    right_triangle = create_triangle(line_width, size_multiplier, extrusion_height)

    # Calculate triangle spacing based on size multiplier
    base_triangle_height = 2.2 * 0.866  # Height of base triangle (2.2 * sqrt(3)/2)
    triangle_height = base_triangle_height * size_multiplier
    triangle_spacing = triangle_height + 0.6

    # Check if diameter has 3+ digits before decimal
    diameter_str = str(diameter_value)
    if '.' in diameter_str:
        digits_before_decimal = len(diameter_str.split('.')[0])
    else:
        digits_before_decimal = len(diameter_str)

    # Estimate text width (assuming dimension_text_size = 5mm)
    # Rough estimate: each character is ~0.65 * font_size wide
    dimension_text_size = 5
    text_chars = len(diameter_str)
    estimated_text_width = text_chars * 0.65 * dimension_text_size

    # Add small buffer for text margins
    text_with_buffer = estimated_text_width + 2

    # Minimum gap needed for inward arrows with middle line
    min_gap_for_inward = (2 * triangle_spacing) + (line_width * 2)

    # Decide arrow direction based on new logic
    if (between <= 6 * size_multiplier):
        # Gap too small - always point outward
        arrows_outward = True
    elif (between < text_with_buffer):
        # Gap exists but text won't fit - point outward
        arrows_outward = True
    elif (digits_before_decimal >= 3):
        # 3+ digit number (like 10.2, 100.3) - point outward
        arrows_outward = True
    else:
        # Gap is big enough and <3 digits - point inward
        arrows_outward = False

    if arrows_outward:
        # Arrows pointing outward (for small gaps or large numbers)
        left_triangle = left_triangle.translate((x-offset, y-(between/2)-triangle_spacing, 0))
        right_triangle = right_triangle.rotate((0,0,0), (0,0,1), 180)
        right_triangle = right_triangle.translate((x-offset, y+(between/2)+triangle_spacing, 0))
        model = right_line+left_line+left_triangle+right_triangle
    else:
        # Arrows pointing inward with middle line (gap is big enough and number is small)
        left_triangle = right_triangle.rotate((0,0,0), (0,0,1), 180)
        left_triangle = left_triangle.translate((x-offset, y-(between/2)+triangle_spacing, 0))
        right_triangle = right_triangle.translate((x-offset, y+(between/2)-triangle_spacing, 0))

        # Middle line between triangles
        middle_line_length = between - (2 * triangle_spacing) - (line_width * 2)
        middle_line = cq.Workplane("XY").box(line_width, middle_line_length, extrusion_height).translate((0, 0, extrusion_height/2))
        middle_line = middle_line.translate((x-offset, y, 0))

        model = right_line+left_line+left_triangle+right_triangle+middle_line

    return model

def diameter_lines(inputs, coordinates, line_width=0.4, size_multiplier=1.0, extrusion_height=0.4, scale=1.0):
    """Create diameter dimension lines for all holes with parametric positioning."""
    offset = 4 * scale
    line_length = 5 * scale

    # Left Side
    slip_hex = create_lines(-coordinates["x"]-(inputs["slip_fit_hex"]/2)-offset, coordinates["row1_y"], line_length, inputs["slip_fit_hex"], "left", line_width, size_multiplier, extrusion_height)
    press_hex = create_lines(-coordinates["x"]-(inputs["press_fit_hex"]/2)-offset, coordinates["row2_y"], line_length, inputs["press_fit_hex"], "left", line_width, size_multiplier, extrusion_height)
    counter_bore = create_lines(-coordinates["x"]-(inputs["counter_bore_diameter"]/2)-offset, coordinates["row3_y"], line_length, inputs["counter_bore_diameter"], "left", line_width, size_multiplier, extrusion_height)
    counter_sunk = create_lines(-coordinates["x"]-(inputs["counter_sunk_diameter"]/2)-offset, coordinates["row4_y"], line_length, inputs["counter_sunk_diameter"], "left", line_width, size_multiplier, extrusion_height)
    heat_insert = create_lines(-coordinates["x"]-(inputs["heat_insert"]/2)-offset, coordinates["heat_insert_y"], line_length, inputs["heat_insert"], "left", line_width, size_multiplier, extrusion_height)

    # Right Side
    slip_square = create_lines(coordinates["x"]+(inputs["square_slip_fit"]/2)+offset, coordinates["row1_y"], line_length, inputs["square_slip_fit"], "right", line_width, size_multiplier, extrusion_height)
    press_square = create_lines(coordinates["x"]+(inputs["square_press_fit"]/2)+offset, coordinates["row2_y"], line_length, inputs["square_press_fit"], "right", line_width, size_multiplier, extrusion_height)
    counter_bore_washer = create_lines(coordinates["x"]+(inputs["counter_bore_washer_diameter"]/2)+offset, coordinates["row3_y"], line_length, inputs["counter_bore_washer_diameter"], "right", line_width, size_multiplier, extrusion_height)
    hole_y = coordinates["row3_y"] - (inputs["counter_bore_washer_diameter"]/2)-(14*scale/2)-(inputs["bolt_slip_fit"]/2)
    hole_y1 = coordinates["vert_square_y"] + (inputs["square_slip_fit_vertical_width"]/2)+(15*scale/2)+(4*scale)
    center = ((hole_y+hole_y1)/2)
    bolt_slip_fit = create_lines(coordinates["x"]+(inputs["bolt_slip_fit"]/2)+offset, center, line_length, inputs["bolt_slip_fit"], "right", line_width, size_multiplier, extrusion_height)
    vertical_square = create_lines(coordinates["x"]+(inputs["square_slip_fit_vertical_length"]/2)+offset, coordinates["vert_square_y"], line_length, inputs["square_slip_fit_vertical_width"], "right", line_width, size_multiplier, extrusion_height)

    model = slip_hex+press_hex+counter_bore+counter_sunk+slip_square+press_square+counter_bore_washer+vertical_square+bolt_slip_fit+heat_insert
    return model

def depth_lines(x, y, line_width=0.4, size_multiplier=1.0, extrusion_height=0.4):
    """
    Create depth indicator lines with arrow.

    Args:
        x, y: Position
        line_width: Width of the lines (default 0.4mm)
        size_multiplier: Scale factor for triangles (default 1.0x)
    """
    # Scale line lengths with size multiplier
    long_line_length = 4 * size_multiplier
    short_line_length = 2 * size_multiplier

    long_line = cq.Workplane("XY").box(line_width, long_line_length, extrusion_height).translate((0, 0, extrusion_height/2))
    short_line = cq.Workplane("XY").box(short_line_length, line_width, extrusion_height).translate((0, 0, extrusion_height/2))

    long_line = long_line.translate((x, y, 0))
    short_line = short_line.translate((x, y + long_line_length/2, 0))

    arrow = create_triangle(line_width, size_multiplier, extrusion_height)
    arrow = arrow.rotate((0,0,0), (0,0,1), 180)
    arrow = arrow.translate((x, y - long_line_length/2, 0))

    return long_line+short_line+arrow

def depth_info(inputs, coordinates, line_width=0.4, size_multiplier=1.0, extrusion_height=0.4, scale=1.0):
    """Create depth indicator lines for all features with parametric positioning."""
    model = cq.Workplane("XY")

    # Hex Depth
    hex_depth = depth_lines(-coordinates["x"]+(1*scale), coordinates["row1_y"]-(inputs["slip_fit_hex"]/2)-(6*scale), line_width, size_multiplier, extrusion_height)

    # Counter Bore Depth
    counter_bore_depth = depth_lines(-coordinates["x"]+(1*scale), coordinates["row3_y"]-(inputs["counter_bore_diameter"]/2)-(4*scale), line_width, size_multiplier, extrusion_height)

    # Square Depth
    square_depth = depth_lines(coordinates["x"]-(1*scale), coordinates["row1_y"]-(inputs["square_slip_fit"]/2)-(6*scale), line_width, size_multiplier, extrusion_height)

    # Counter Bore Washer Depth
    counter_bore_washer_depth = depth_lines(coordinates["x"]-(1*scale), coordinates["row3_y"]-(inputs["counter_bore_washer_diameter"]/2)-(4*scale), line_width, size_multiplier, extrusion_height)

    # Vertical Square Info
    vertical_square_depth = depth_lines(coordinates["x"]-(2.5*scale), coordinates["vert_square_y"]+(inputs["square_slip_fit_vertical_width"]/2)+(13*scale), line_width, size_multiplier, extrusion_height)
    right_triangle = create_triangle(line_width, size_multiplier, extrusion_height)
    right_triangle = right_triangle.rotate((0,0,0), (0,0,1), 270)
    left_triangle = right_triangle.rotate((0,0,0),(0,0,1), 180)
    right_triangle = right_triangle.translate((coordinates["x"]-(2*scale), coordinates["vert_square_y"]+(inputs["square_slip_fit_vertical_width"]/2)+(5*scale)))
    left_triangle = left_triangle.translate((coordinates["x"]-(3*scale), coordinates["vert_square_y"]+(inputs["square_slip_fit_vertical_width"]/2)+(5*scale)))

    return hex_depth+counter_bore_depth+square_depth+counter_bore_washer_depth+vertical_square_depth+right_triangle+left_triangle

def create_chamfer_drawing(x, y, line_width=0.4, size_multiplier=1.0, extrusion_height=0.4, scale=1.0):
    """
    Create chamfer detail drawing with parametric scaling.

    Args:
        x, y: Position
        line_width: Width of the lines (default 0.4mm)
        size_multiplier: Scale factor for triangles (default 1.0x)
        extrusion_height: Height of extrusion (default 0.2mm)
        scale: Overall scale factor
    """
    # Scale all dimensions proportionally
    outer_box = cq.Workplane("XY").box(17*scale, 8*scale, extrusion_height).translate((0, 0, extrusion_height/2))

    rotated_box = cq.Workplane("XY").box(6*scale, 6*scale, extrusion_height).translate((0, 0, extrusion_height/2)).rotate((0,0,0), (0,0,1), 45).translate((0, 3.5*scale))
    top_box = cq.Workplane("XY").box(8.49*scale, 8*scale, extrusion_height).translate((0, 0, extrusion_height/2)).translate((0, 7.5*scale))
    thread_box = cq.Workplane("XY").box(3*scale, 8*scale, extrusion_height).translate((0, 0, extrusion_height/2))

    # Cutouts for dimension lines (slightly larger than line width for clearance)
    cutout_width = line_width + (0.6*scale)
    chamfer_line_cutout1 = cq.Workplane("XY").box(cutout_width, 4*scale, extrusion_height).translate((0, 0, extrusion_height/2)).rotate((0,0,0), (0,0,1), 45).translate((4.7*scale, 0.5*scale))
    chamfer_line_cutout2 = cq.Workplane("XY").box(4*scale, cutout_width, extrusion_height).translate((0, 0, extrusion_height/2)).translate((7.75*scale, -0.76*scale))
    chamfer_height_cutout = cq.Workplane("XY").box(7*scale, cutout_width, extrusion_height).translate((0, 0, extrusion_height/2)).translate((-6*scale, 0.75*scale))

    # Dimension lines
    chamfer_line1 = cq.Workplane("XY").box(line_width, 3.5*scale, extrusion_height).translate((0, 0, extrusion_height/2)).rotate((0,0,0), (0,0,1), 45).translate((4.7*scale, 0.5*scale))
    chamfer_line2 = cq.Workplane("XY").box(4*scale, line_width, extrusion_height).translate((0, 0, extrusion_height/2)).translate((7.8*scale, -0.76*scale))
    chamfer_height_lower = cq.Workplane("XY").box(9*scale, line_width, extrusion_height).translate((0, 0, extrusion_height/2)).translate((-7.5*scale, 0.75*scale))
    chamfer_height_upper = cq.Workplane("XY").box(3*scale, line_width, extrusion_height).translate((0, 0, extrusion_height/2)).translate((-10.5*scale, 4*scale-(line_width/2)))

    # Triangular arrows
    upper_triangle = create_triangle(line_width, size_multiplier, extrusion_height)
    upper_triangle = upper_triangle.rotate((0,0,0), (0,0,1), 180).translate((-10.5*scale, 7*scale-(line_width/2)))
    lower_triangle = create_triangle(line_width, size_multiplier, extrusion_height)
    lower_triangle = lower_triangle.translate((-10.5*scale, -2*scale-(line_width/2)))

    outer_box = outer_box.cut(rotated_box)
    outer_box = outer_box.cut(top_box)
    outer_box = outer_box.cut(thread_box)
    outer_box = outer_box.cut(chamfer_line_cutout1)
    outer_box = outer_box.cut(chamfer_line_cutout2)
    outer_box = outer_box.cut(chamfer_height_cutout)
    outer_box = outer_box+chamfer_line1+chamfer_line2+chamfer_height_lower+chamfer_height_upper+upper_triangle+lower_triangle
    outer_box = outer_box.translate((x, y))

    return outer_box

def add_lines(inputs, coordinates, line_width=0.4, size_multiplier=1.0, extrusion_height=0.4, scale=1.0):
    """
    Add all dimension lines to the model with parametric scaling.

    Args:
        inputs: Hardware specifications dictionary
        coordinates: Position coordinates dictionary
        line_width: Width of dimension lines (default 0.4mm)
        size_multiplier: Scale factor for triangle arrows (default 1.0x)
        extrusion_height: Height of extrusions (default 0.4mm)
        scale: Overall parametric scale factor
    """
    board_depth = inputs["square_slip_fit_vertical_depth"] + 0.6
    diameter_lines_model = diameter_lines(inputs, coordinates, line_width, size_multiplier, extrusion_height, scale)
    depth_lines_model = depth_info(inputs, coordinates, line_width, size_multiplier, extrusion_height, scale)
    chamfer_drawing = create_chamfer_drawing(-coordinates["x"], coordinates["row4_y"]-(inputs["counter_sunk_diameter"]/2)-(11*scale), line_width, size_multiplier, extrusion_height, scale)
    model = diameter_lines_model+depth_lines_model+chamfer_drawing

    # Position lines on top surface of the board (box is centered at origin)
    return model.translate((0, 0, board_depth / 2))
