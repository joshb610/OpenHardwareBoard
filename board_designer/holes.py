import cadquery as cq # type: ignore
def create_bolt_slip_fit(model, x, y, diameter, block_depth):
    return model.faces(">Z").workplane().move(x, y).hole(diameter, block_depth)

def add_hex_holes(model, x, y, fit, depth, bolt_slip_fit, block_depth):
    model = model.faces(">Z").workplane().move(x, y).polygon(6, fit).cutBlind(-depth)

    return create_bolt_slip_fit(model, x, y, bolt_slip_fit, block_depth)


def add_counter_bore_holes(model, x, y, diameter, depth, bolt_slip_fit, block_depth):
    model = model.faces(">Z").workplane().move(x, y).hole(diameter, depth)
    #model = add_text(model, x+diameter+3, y, text_content)

    return create_bolt_slip_fit(model, x, y, bolt_slip_fit, block_depth)

def add_counter_sink_holes(model, x, y, inputs, bolt_slip_fit, block_depth):
    depth = inputs["counter_sunk_chamfer_depth"]
    # Position cylinder so its top sits 0.2mm above the board surface.
    # board top (before final translate) is at +block_depth/2.
    z_offset = block_depth / 2 - depth / 2 + 0.2
    chamfer = cq.Workplane("XY").cylinder(depth, inputs["counter_sunk_diameter"] / 2)
    chamfer = chamfer.faces("<Z").chamfer(inputs["counter_sunk_chamfer"])
    chamfer = chamfer.translate((x, y, z_offset))
    model = model.cut(chamfer)
    return create_bolt_slip_fit(model, x, y, bolt_slip_fit, block_depth)


def add_square_hole(model, x, y, size, depth, bolt_slip_fit, block_depth):
    model = model.faces(">Z").workplane().move(x, y).rect(size, size).cutBlind(-depth)
    #model = add_text(model, x+size+3, y, text_content)

    return create_bolt_slip_fit(model, x, y, bolt_slip_fit, block_depth)

def add_vertical_square_slot(model, x, y, depth, length, width, bolt_slip_fit, block_depth, height):
    # Create the rectangular slot on top surface
    model = model.faces(">Z").workplane().move(x, y).rect(length, width).cutBlind(-depth)

    # Calculate depth for bottom through hole
    bottom_hole_depth = block_depth - depth

    # Add bottom through hole - use original function that was working
    model = add_bottom_hole(model, x, y, bolt_slip_fit, bottom_hole_depth+1)

    # Add side hole - keep original Y positioning but fix Z to be centered with slot
    # Original calculation for hole depth in Y direction
    hole_depth_side = (height/2) + y  # Distance from front face to the center

    # Box is centered at Z=0, so top face is at +block_depth/2.
    # Slot is cut from top face downward, so its Z center is at block_depth/2 - depth/2.
    hole_z_position = block_depth / 2 - depth / 2

    # XZ workplane normal is -Y, so offset=+height/2 places the plane at Y=-height/2 (slot side).
    # extrude(-hole_depth_side) then goes in +Y toward the slot center.
    side_hole = (cq.Workplane("XZ")
                .workplane(offset=height/2)  # Slot-side face (Y = -height/2)
                .center(x, hole_z_position)
                .circle(bolt_slip_fit/2)
                .extrude(-hole_depth_side))  # Drill inward toward slot
    model = model.cut(side_hole)

    return model

def add_bottom_hole(model, x, y, bolt_slip_fit, depth):
    return model.faces("<Z").workplane().move(x, y).hole(bolt_slip_fit, depth)
