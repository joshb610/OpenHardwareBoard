import cadquery as cq # type: ignore
import os

dimension_text_size = 3.5
depth_text_size = 3.5
hardware_text_size = 4
title_text_size = 5
def create_text(model, x, y, text_content, size, text_height=0.4):
   # Create text at the specified x, y, z position
    current_directory = os.getcwd()
    #font_path = current_directory + "/Titillium_Web/TitilliumWeb-SemiBold.ttf"
    text_model = (model.faces("XY")
                  .workplane()  # Set the correct reference for text placement
                  .text(text_content, size, text_height,
                        halign='center', valign='center',
                        cut=False, combine=True,
                        font="Arial Black")
                  .clean())
    
    #text_model = text_model.rotate((0,0,0), (0,0,1), 90)
    text_model = text_model.translate((x,y,0))

    return text_model


def diameter_text(model, inputs, coordinates, scale=1.0, text_height=0.4):
    """Create diameter text with parametric positioning - adjusted to avoid overlaps"""
    scaled_text_size = dimension_text_size * scale
    # Offset to position text next to dimension lines (reduced text size from 5 to 3.5)
    offset = 11 * scale

    # Left Side
    slip_hex = create_text(model, -coordinates["x"]-(inputs["slip_fit_hex"]/2)-offset, coordinates["row1_y"],str(inputs["slip_fit_hex"]), scaled_text_size, text_height)
    press_hex = create_text(model, -coordinates["x"]-(inputs["press_fit_hex"]/2)-offset, coordinates["row2_y"],str(inputs["press_fit_hex"]), scaled_text_size, text_height)
    counter_bore = create_text(model, -coordinates["x"]-(inputs["counter_bore_diameter"]/2)-offset, coordinates["row3_y"],str(inputs["counter_bore_diameter"]), scaled_text_size, text_height)
    counter_sunk = create_text(model, -coordinates["x"]-(inputs["counter_sunk_diameter"]/2)-offset, coordinates["row4_y"],str(inputs["counter_sunk_diameter"]), scaled_text_size, text_height)
    heat_insert = create_text(model, -coordinates["x"]-(inputs["heat_insert"]/2)-offset, coordinates["heat_insert_y"],str(inputs["heat_insert"]), scaled_text_size, text_height)

    # Right Side
    slip_square = create_text(model, coordinates["x"]+(inputs["square_slip_fit"]/2)+offset, coordinates["row1_y"],str(inputs["square_slip_fit"]), scaled_text_size, text_height)
    press_square = create_text(model, coordinates["x"]+(inputs["square_press_fit"]/2)+offset, coordinates["row2_y"],str(inputs["square_press_fit"]), scaled_text_size, text_height)
    counter_bore_washer = create_text(model, coordinates["x"]+(inputs["counter_bore_washer_diameter"]/2)+offset, coordinates["row3_y"],str(inputs["counter_bore_washer_diameter"]), scaled_text_size, text_height)
    hole_y = coordinates["row3_y"] - (inputs["counter_bore_washer_diameter"]/2)-(14*scale/2)-(inputs["bolt_slip_fit"]/2)
    hole_y1 = coordinates["vert_square_y"] + (inputs["square_slip_fit_vertical_width"]/2)+(15*scale/2)+(4*scale)
    center = ((hole_y+hole_y1)/2)
    bolt_slip_fit = create_text(model, coordinates["x"]+(inputs["bolt_slip_fit"]/2)+offset, center, str(inputs["bolt_slip_fit"]), scaled_text_size, text_height)
    vert_square = create_text(model, coordinates["x"]+(inputs["square_slip_fit_vertical_length"]/2)+offset, coordinates["vert_square_y"],str(inputs["square_slip_fit_vertical_width"]), scaled_text_size, text_height)
    model = slip_hex+press_hex+counter_bore+counter_sunk+slip_square+press_square+counter_bore_washer+vert_square+bolt_slip_fit+heat_insert
    return model

def depth_text(model, inputs, coordinates, scale=1.0, text_height=0.4):
    """Create depth text with parametric positioning"""
    scaled_text_size = depth_text_size * scale

    # Left Side
    slip_hex_dimension = create_text(model, -coordinates["x"]-(5*scale), coordinates["row1_y"]-(inputs["slip_fit_hex"]/2)-(5*scale),str(inputs["hex_depth"]), scaled_text_size, text_height)
    slip_hex_text = create_text(model, -coordinates["x"]-(6*scale), coordinates["row1_y"]-(inputs["slip_fit_hex"]/2)-(9.5*scale), "Hex", scaled_text_size, text_height)

    counter_bore_dimension = create_text(model, -coordinates["x"]-(4.5*scale), coordinates["row3_y"]-(inputs["counter_bore_diameter"]/2)-(5*scale),str(inputs["counter_bore_depth"]), scaled_text_size, text_height)
    counter_bore_text = create_text(model, -coordinates["x"]-(4*scale), coordinates["row3_y"]-(inputs["counter_bore_diameter"]/2)-(9.5*scale),"CB", scaled_text_size*0.8, text_height)

    # Right Side
    slip_square_dimension = create_text(model, coordinates["x"]+(5*scale), coordinates["row1_y"]-(inputs["square_slip_fit"]/2)-(5*scale),str(inputs["square_depth"]), scaled_text_size, text_height)
    slip_square_text = create_text(model, coordinates["x"]+(5.5*scale), coordinates["row1_y"]-(inputs["square_slip_fit"]/2)-(9.5*scale), "Sqr", scaled_text_size, text_height)

    counter_bore_washer_dimension = create_text(model, coordinates["x"]+(4.5*scale), coordinates["row3_y"]-(inputs["counter_bore_washer_diameter"]/2)-(5*scale),str(inputs["counter_bore_washer_depth"]), scaled_text_size, text_height)
    counter_bore_washer_text = create_text(model, coordinates["x"]+(9*scale), coordinates["row3_y"]-(inputs["counter_bore_washer_diameter"]/2)-(9.5*scale), "CB+Wsr", scaled_text_size*0.8, text_height)

    vertical_square_depth_dimension = create_text(model, coordinates["x"]+(4.5*scale), coordinates["vert_square_y"]+(inputs["square_slip_fit_vertical_width"]/2)+(12*scale), str(inputs["square_slip_fit_vertical_depth"]), scaled_text_size, text_height)
    vertical_square_length_dimension = create_text(model, coordinates["x"]+(5.5*scale), coordinates["vert_square_y"]+(inputs["square_slip_fit_vertical_width"]/2)+(5.5*scale), str(inputs["square_slip_fit_vertical_length"]), scaled_text_size, text_height)

    model = slip_hex_dimension+slip_hex_text+counter_bore_dimension+counter_bore_text+slip_square_dimension+slip_square_text+counter_bore_washer_dimension+counter_bore_washer_text+vertical_square_depth_dimension+vertical_square_length_dimension
    return model

def hardware_text(model, inputs, coordinates, scale=1.0, text_height=0.4):
    """Create hardware labels with parametric positioning - adjusted to avoid overlaps"""
    scaled_text_size = hardware_text_size * scale

    slip_fit = create_text(model, 0, coordinates["row1_y"], "Slip Fit", scaled_text_size, text_height)
    press_fit = create_text(model, 0, coordinates["row2_y"], "Press Fit", scaled_text_size, text_height)
    cb = create_text(model, -coordinates["x"]+(inputs["counter_bore_diameter"]/2)+(12*scale), coordinates["row3_y"], "CB", scaled_text_size, text_height)
    cbw = create_text(model, coordinates["x"]-(inputs["counter_bore_washer_diameter"]/2)-(16*scale), coordinates["row3_y"], "CB+W", scaled_text_size, text_height)
    cs = create_text(model, -coordinates["x"]+(inputs["counter_sunk_diameter"]/2)+(8*scale), coordinates["row4_y"], "CS", scaled_text_size, text_height)

    # Position Slip/Fit text to the right of the dimension numbers in the vertical square slot
    v_slip = create_text(model, coordinates["x"]+(13*scale), coordinates["vert_square_y"]+(inputs["square_slip_fit_vertical_width"]/2)+(11*scale), "Slip", scaled_text_size, text_height)
    v_fit = create_text(model, coordinates["x"]+(13*scale), coordinates["vert_square_y"]+(inputs["square_slip_fit_vertical_width"]/2)+(6*scale), "Fit", scaled_text_size, text_height)

    hole_y = coordinates["row3_y"] - (inputs["counter_bore_washer_diameter"]/2)-(14*scale/2)-(inputs["bolt_slip_fit"]/2)
    hole_y1 = coordinates["vert_square_y"] + (inputs["square_slip_fit_vertical_width"]/2)+(15*scale/2)+(4*scale)
    center = ((hole_y+hole_y1)/2)
    bolt = create_text(model, coordinates["x"]-(inputs["bolt_slip_fit"]/2)-(15*scale), center+(2.25*scale), "Bolt", scaled_text_size, text_height)
    slip = create_text(model, coordinates["x"]-(inputs["bolt_slip_fit"]/2)-(16*scale), center-(2.25*scale), "Slip Fit", scaled_text_size, text_height)

    # Move Square/Slot text further left to avoid overlap
    square_slot = create_text(model, coordinates["x"]-(inputs["square_slip_fit_vertical_length"]/2)-(16*scale), coordinates["vert_square_y"]+(9*scale), "Square", scaled_text_size, text_height)
    slot_slot = create_text(model, coordinates["x"]-(inputs["square_slip_fit_vertical_length"]/2)-(13*scale), coordinates["vert_square_y"]+(4*scale), "Slot", scaled_text_size, text_height)

    heat = create_text(model, -coordinates["x"]+(inputs["heat_insert"]/2)+(12*scale), coordinates["heat_insert_y"], "Heat", scaled_text_size, text_height)
    set_insert = create_text(model, -coordinates["x"]+(inputs["heat_insert"]/2)+(19*scale), coordinates["heat_insert_y"]-(5*scale), "Set Insert", scaled_text_size, text_height)

    model = slip_fit+press_fit+cb+cbw+cs+bolt+slip+slot_slot+square_slot+v_slip+v_fit+heat+set_insert
    return model

def chamfer_text(model, coordinates, inputs, scale=1.0, text_height=0.4):
    """Create chamfer text with parametric positioning"""
    scaled_text_size = depth_text_size * scale

    bore_depth = create_text(model, -coordinates["x"]-(15.5*scale), coordinates["row4_y"]-(inputs["counter_sunk_diameter"]/2)-(8.5*scale), str(inputs["counter_sunk_chamfer_depth"]), scaled_text_size*0.9, text_height)
    chamfer_depth = create_text(model, -coordinates["x"]+(14.5*scale), coordinates["row4_y"]-(inputs["counter_sunk_diameter"]/2)-(9.5*scale), str(inputs["counter_sunk_chamfer"]), scaled_text_size*0.9, text_height)
    chamfer_text = create_text(model, -coordinates["x"]+(15.5*scale), coordinates["row4_y"]-(inputs["counter_sunk_diameter"]/2)-(14*scale), "Cmfr", scaled_text_size*0.9, text_height)
    model = bore_depth+chamfer_depth+chamfer_text
    return model

def add_text(inputs, coordinates, height, scale=1.0, text_height=0.4):
    """Add all text with parametric scaling"""
    block_depth = inputs["square_slip_fit_vertical_depth"]+0.6
    model = cq.Workplane("XY")

    # Extract just the bolt size (M2, M3, etc.) without bolt head type
    bolt_size = inputs.get("bolt_size", inputs.get("bolt_type", "M3"))
    if " " in bolt_size:
        bolt_size = bolt_size.split()[0]  # Get just "M3" from "M3 Hex" if present

    # Scale text sizes
    scaled_title_size = title_text_size * scale

    # Title without bolt head type (will add drawing later)
    title = create_text(model, 0, (height/2)-(5*scale), f"{bolt_size} Hardware Design Board", scaled_title_size, text_height)
    diameter = diameter_text(model, inputs, coordinates, scale, text_height)
    depth = depth_text(model, inputs, coordinates, scale, text_height)
    hardware = hardware_text(model, inputs, coordinates, scale, text_height)
    chamfer_drawing = chamfer_text(model, coordinates, inputs, scale, text_height)

    model = title+diameter+depth+hardware+chamfer_drawing

    # Position text on top surface of the board (box is centered at origin)
    return model.translate((0, 0, block_depth / 2))

