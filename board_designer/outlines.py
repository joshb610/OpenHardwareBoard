import cadquery as cq # type: ignore

def create_square(length, height, outer_radius, x, y, line_width=0.8, extrusion_height=0.4):
    # FIX RADIUS STUFF MORE
    inner_radius = outer_radius - line_width
    outer = cq.Workplane("XY").box(length, height, extrusion_height).translate((0, 0, extrusion_height/2))
    outer = outer.edges("|Z").fillet(outer_radius)
    inner = cq.Workplane("XY").box(length-(line_width*2), height-(line_width*2), extrusion_height).translate((0, 0, extrusion_height/2))
    inner = inner.edges("|Z").fillet(inner_radius)
    outer = outer.cut(inner)
    # move o
    outer = outer.translate((x,y,0))
    return outer

def create_polygon(length, height, outer_radius, outer_chamfer, x, y, line_width=0.8, extrusion_height=0.4):
    inner_radius = outer_radius - line_width
    inner_chamfer = outer_chamfer - (line_width/2)
    outer = cq.Workplane("XY").box(length, height, extrusion_height).translate((0, 0, extrusion_height/2))
    outer = outer.edges("|Z").chamfer(outer_chamfer)
    outer = outer.edges("|Z").fillet(outer_radius)

    inner = cq.Workplane("XY").box(length-(line_width*2), height-(line_width*2), extrusion_height).translate((0, 0, extrusion_height/2))
    inner = inner.edges("|Z").chamfer(inner_chamfer)
    inner = inner.edges("|Z").fillet(inner_radius)
    outer = outer.cut(inner)

    outer = outer.translate((x,y,0))
    return outer

def chamfer_outline(length1, height1, length2, height2, outer_radius, x, y, line_width=0.8, extrusion_height=0.4):
    inner_radius = outer_radius - line_width

    # Calculate overlap to ensure boxes combine properly
    # Box2 should overlap with box1 by at least line_width to avoid gap
    overlap = max(line_width * 2, 2)

    # Create outer L-shape
    box1_outer = cq.Workplane("XY").box(length1, height1, extrusion_height).translate((0, 0, extrusion_height/2))
    box2_outer = cq.Workplane("XY").box(length2, height2, extrusion_height).translate((0, 0, extrusion_height/2))
    # Position box2 to properly overlap with box1
    box2_outer = box2_outer.translate((x+(length1/2)+(length2/2)-overlap, y-((height1/2)-(height2/2))))
    box1_outer = box1_outer.translate((x,y,0))
    box_outer = box1_outer + box2_outer

    # Create inner L-shape
    box1_inner = cq.Workplane("XY").box(length1-(line_width*2), height1-(line_width*2), extrusion_height).translate((0, 0, extrusion_height/2))
    box2_inner = cq.Workplane("XY").box(length2-(line_width*2), height2-(line_width*2), extrusion_height).translate((0, 0, extrusion_height/2))
    box2_inner = box2_inner.translate((x+(length1/2)+(length2/2)-overlap, y-((height1/2)-(height2/2))))
    box1_inner = box1_inner.translate((x,y,0))
    box_inner = box1_inner + box2_inner

    # Cut to create the outline FIRST, before filleting
    outline = box_outer.cut(box_inner)

    # Now fillet only the actual outline edges (this avoids double-filleting the interior corner)
    outline = outline.edges("|Z").fillet(outer_radius)

    return outline


def add_outlines(inputs, coordinates, height, line_width=0.8, extrusion_height=0.4, scale=1.0):
    """Add all outlines with parametric scaling"""
    board_depth = inputs["square_slip_fit_vertical_depth"] + 0.6

    # Parametric outline dimensions
    outline_padding = 22 * scale
    title_width = 80 * scale
    title_height = 8 * scale
    title_radius = 3.9 * scale

    title_outline = create_square(title_width, title_height, title_radius, 0, (height/2)-(5*scale), line_width, extrusion_height)

    hex_outline = create_polygon(inputs["slip_fit_hex"]+outline_padding, (inputs["slip_fit_hex"]+inputs["press_fit_hex"])+(24*scale), 1*scale, 4*scale, -coordinates["x"]-(7*scale), (coordinates["row1_y"]+coordinates["row2_y"])/2, line_width, extrusion_height)
    square_outline = create_square(inputs["square_slip_fit"]+outline_padding, (inputs["square_slip_fit"]+inputs["square_press_fit"])+(24*scale), 2*scale, coordinates["x"]+(7*scale), (coordinates["row1_y"]+coordinates["row2_y"])/2, line_width, extrusion_height)

    counter_bore_outline = create_square(inputs["counter_bore_diameter"]+outline_padding, inputs["counter_bore_diameter"]+(18*scale), 2*scale, -coordinates["x"]-(7*scale), coordinates["row3_y"]-(4*scale), line_width, extrusion_height)
    counter_bore_washer_outline = create_square(inputs["counter_bore_washer_diameter"]+outline_padding, inputs["counter_bore_washer_diameter"]+(17*scale), 2*scale, coordinates["x"]+(7*scale), coordinates["row3_y"]-(4*scale), line_width, extrusion_height)

    hole_y = coordinates["row3_y"] - (inputs["counter_bore_washer_diameter"]/2)-(14*scale/2)-(inputs["bolt_slip_fit"]/2)
    hole_y1 = coordinates["vert_square_y"] + (inputs["square_slip_fit_vertical_width"]/2)+(15*scale/2)+(4*scale)
    center = ((hole_y+hole_y1)/2)
    bolt_slip_fit_outline = create_square(inputs["bolt_slip_fit"]+outline_padding, inputs["bolt_slip_fit"]+(10*scale), 2*scale, coordinates["x"]+(7*scale), center, line_width, extrusion_height)

    counter_sink_outline = chamfer_outline(inputs["counter_sunk_diameter"]+(21*scale), inputs["counter_sunk_diameter"]+(23*scale), 18*scale, 14*scale, 2*scale, -coordinates["x"]-(7*scale), coordinates["row4_y"]-(7*scale), line_width, extrusion_height)

    vertical_square_outline = create_square(inputs["square_slip_fit_vertical_length"]+outline_padding, inputs["square_slip_fit_vertical_width"]+(23*scale), 2*scale, coordinates["x"]+(7*scale), coordinates["vert_square_y"]+(7*scale), line_width, extrusion_height)

    heat_insert_outline = create_square(inputs["heat_insert"]+outline_padding, inputs["heat_insert"]+(13*scale), 2*scale, -coordinates["x"]-(7*scale), coordinates["heat_insert_y"], line_width, extrusion_height)

    model = hex_outline+square_outline+title_outline+counter_bore_outline+counter_bore_washer_outline+vertical_square_outline+counter_sink_outline+bolt_slip_fit_outline+heat_insert_outline

    # Position outlines on top surface of the board (box is centered at origin)
    return model.translate((0, 0, board_depth / 2))