"""
Input validation for hardware board parameters
"""

from typing import Dict, List, Tuple


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


class HardwareValidator:
    """Validates hardware parameters before board generation"""

    # Standard bolt sizes and typical values
    BOLT_SIZES = ['M2', 'M3', 'M4', 'M5', 'M6', 'M8', 'M10', 'M12']

    # Typical bolt slip fit diameters (mm)
    BOLT_SLIP_FIT_RANGES = {
        'M2': (2.1, 2.4),
        'M3': (3.1, 3.4),
        'M4': (4.1, 4.5),
        'M5': (5.1, 5.5),
        'M6': (6.1, 6.6),
        'M8': (8.2, 8.6),
        'M10': (10.2, 10.6),
        'M12': (12.2, 12.8),
    }

    @staticmethod
    def validate_positive(value: float, name: str) -> None:
        """Validate that a value is positive"""
        if value <= 0:
            raise ValidationError(f"{name} must be greater than 0")

    @staticmethod
    def validate_range(value: float, name: str, min_val: float, max_val: float) -> None:
        """Validate that a value is within a range"""
        if value < min_val or value > max_val:
            raise ValidationError(f"{name} must be between {min_val} and {max_val}")

    @staticmethod
    def validate_bolt_size(bolt_size: str) -> None:
        """Validate bolt size"""
        if bolt_size not in HardwareValidator.BOLT_SIZES:
            raise ValidationError(f"Bolt size must be one of: {', '.join(HardwareValidator.BOLT_SIZES)}")

    @staticmethod
    def validate_bolt_slip_fit(bolt_size: str, slip_fit: float) -> List[str]:
        """
        Validate bolt slip fit diameter

        Returns:
            List of warnings (not errors)
        """
        warnings = []

        if bolt_size in HardwareValidator.BOLT_SLIP_FIT_RANGES:
            min_val, max_val = HardwareValidator.BOLT_SLIP_FIT_RANGES[bolt_size]
            if slip_fit < min_val or slip_fit > max_val:
                warnings.append(
                    f"Bolt slip fit {slip_fit}mm is outside typical range "
                    f"for {bolt_size} ({min_val}-{max_val}mm)"
                )

        return warnings

    @staticmethod
    def validate_press_fit_smaller_than_slip(press_fit: float, slip_fit: float, name: str) -> None:
        """Validate that press fit is smaller than slip fit"""
        if press_fit >= slip_fit:
            raise ValidationError(
                f"Press fit {name} ({press_fit}mm) should be smaller than "
                f"slip fit {name} ({slip_fit}mm) for proper interference fit"
            )

    @staticmethod
    def validate_depth_reasonable(depth: float, name: str, max_depth: float = 50) -> None:
        """Validate that depth is reasonable"""
        HardwareValidator.validate_positive(depth, name)
        if depth > max_depth:
            raise ValidationError(f"{name} depth of {depth}mm seems too deep (max {max_depth}mm)")

    @staticmethod
    def validate_counter_sunk(diameter: float, chamfer_depth: float, bolt_slip_fit: float) -> None:
        """Validate countersunk parameters"""
        if diameter <= bolt_slip_fit:
            raise ValidationError(
                f"Counter sunk diameter ({diameter}mm) must be larger than "
                f"bolt slip fit ({bolt_slip_fit}mm)"
            )

        HardwareValidator.validate_depth_reasonable(chamfer_depth, "Counter sunk chamfer depth", 10)

    @staticmethod
    def validate_all_parameters(params: Dict) -> Tuple[bool, List[str], List[str]]:
        """
        Validate all hardware parameters

        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        errors = []
        warnings = []

        try:
            # Validate bolt size
            HardwareValidator.validate_bolt_size(params['bolt_size'])

            # Validate bolt slip fit
            HardwareValidator.validate_positive(params['bolt_slip_fit'], "Bolt slip fit")
            bolt_warnings = HardwareValidator.validate_bolt_slip_fit(
                params['bolt_size'],
                params['bolt_slip_fit']
            )
            warnings.extend(bolt_warnings)

            # Validate hex dimensions
            HardwareValidator.validate_positive(params['press_fit_hex'], "Press fit hex")
            HardwareValidator.validate_positive(params['slip_fit_hex'], "Slip fit hex")
            HardwareValidator.validate_depth_reasonable(params['hex_depth'], "Hex depth")

            try:
                HardwareValidator.validate_press_fit_smaller_than_slip(
                    params['press_fit_hex'],
                    params['slip_fit_hex'],
                    "hex nut"
                )
            except ValidationError as e:
                warnings.append(str(e))  # Press/slip fit order is a warning, not error

            # Validate square dimensions
            HardwareValidator.validate_positive(params['square_press_fit'], "Square press fit")
            HardwareValidator.validate_positive(params['square_slip_fit'], "Square slip fit")
            HardwareValidator.validate_depth_reasonable(params['square_depth'], "Square depth")

            try:
                HardwareValidator.validate_press_fit_smaller_than_slip(
                    params['square_press_fit'],
                    params['square_slip_fit'],
                    "square nut"
                )
            except ValidationError as e:
                warnings.append(str(e))

            # Validate vertical square dimensions
            HardwareValidator.validate_positive(params['square_slip_fit_vertical_width'], "Vertical square width")
            HardwareValidator.validate_positive(params['square_slip_fit_vertical_length'], "Vertical square length")
            HardwareValidator.validate_positive(params['square_slip_fit_vertical_depth'], "Vertical square depth")

            # Validate counter bore
            HardwareValidator.validate_positive(params['counter_bore_diameter'], "Counter bore diameter")
            HardwareValidator.validate_depth_reasonable(params['counter_bore_depth'], "Counter bore depth")

            # Validate counter bore + washer
            HardwareValidator.validate_positive(params['counter_bore_washer_diameter'], "Counter bore washer diameter")
            HardwareValidator.validate_depth_reasonable(params['counter_bore_washer_depth'], "Counter bore washer depth")

            if params['counter_bore_washer_diameter'] <= params['counter_bore_diameter']:
                warnings.append(
                    "Counter bore washer diameter should typically be larger than standard counter bore"
                )

            # Validate countersunk
            HardwareValidator.validate_counter_sunk(
                params['counter_sunk_diameter'],
                params['counter_sunk_chamfer_depth'],
                params['bolt_slip_fit']
            )
            HardwareValidator.validate_positive(params['counter_sunk_chamfer'], "Counter sunk chamfer")

            # Validate heat insert
            HardwareValidator.validate_positive(params['heat_insert_diameter'], "Heat insert diameter")
            if params['heat_insert_diameter'] <= params['bolt_slip_fit']:
                warnings.append(
                    f"Heat insert diameter ({params['heat_insert_diameter']}mm) should typically be "
                    f"larger than bolt slip fit ({params['bolt_slip_fit']}mm)"
                )

            # Validate optional heat insert depth
            if params.get('heat_insert_depth') is not None:
                HardwareValidator.validate_positive(params['heat_insert_depth'], "Heat insert depth")

            # Validate export parameters
            if params.get('text_height'):
                HardwareValidator.validate_range(params['text_height'], "Text height", 0.1, 2.0)

            if params.get('line_width'):
                HardwareValidator.validate_range(params['line_width'], "Line width", 0.2, 2.0)

        except ValidationError as e:
            errors.append(str(e))
        except KeyError as e:
            errors.append(f"Missing required parameter: {e}")
        except (TypeError, ValueError) as e:
            errors.append(f"Invalid parameter value: {e}")

        is_valid = len(errors) == 0
        return is_valid, errors, warnings

    @staticmethod
    def get_suggested_values(bolt_size: str, measured_hex: float = None,
                            measured_square: float = None,
                            slip_fit_offset: float = 0.2,
                            press_fit_offset: float = -0.1) -> Dict:
        """
        Generate suggested values for simplified mode

        Args:
            bolt_size: The metric bolt size (e.g., 'M3')
            measured_hex: Measured hex nut size (flat-to-flat)
            measured_square: Measured square nut size
            slip_fit_offset: Offset for slip fits (default +0.2mm)
            press_fit_offset: Offset for press fits (default -0.1mm)

        Returns:
            Dictionary of suggested values
        """
        # Standard values based on ISO/DIN standards
        standard_values = {
            'M2': {
                'bolt_slip_fit': 2.2,
                'hex_size': 4.0,
                'square_size': 4.0,
                'heat_insert': 3.2,
            },
            'M3': {
                'bolt_slip_fit': 3.3,
                'hex_size': 5.5,
                'square_size': 5.5,
                'heat_insert': 4.4,
            },
            'M4': {
                'bolt_slip_fit': 4.3,
                'hex_size': 7.0,
                'square_size': 7.0,
                'heat_insert': 5.6,
            },
            'M5': {
                'bolt_slip_fit': 5.3,
                'hex_size': 8.0,
                'square_size': 8.0,
                'heat_insert': 6.8,
            },
            'M6': {
                'bolt_slip_fit': 6.4,
                'hex_size': 10.0,
                'square_size': 10.0,
                'heat_insert': 8.0,
            },
            'M8': {
                'bolt_slip_fit': 8.4,
                'hex_size': 13.0,
                'square_size': 13.0,
                'heat_insert': 10.4,
            },
            'M10': {
                'bolt_slip_fit': 10.5,
                'hex_size': 17.0,
                'square_size': 17.0,
                'heat_insert': 12.6,
            },
            'M12': {
                'bolt_slip_fit': 12.6,
                'hex_size': 19.0,
                'square_size': 19.0,
                'heat_insert': 14.8,
            },
        }

        if bolt_size not in standard_values:
            raise ValidationError(f"Unsupported bolt size: {bolt_size}")

        std = standard_values[bolt_size]

        # Use measured values if provided, otherwise use standard
        hex_size = measured_hex if measured_hex else std['hex_size']
        square_size = measured_square if measured_square else std['square_size']

        # Calculate slip and press fits with offsets
        suggestions = {
            'bolt_slip_fit': std['bolt_slip_fit'],
            'press_fit_hex': hex_size + press_fit_offset,
            'slip_fit_hex': hex_size + slip_fit_offset,
            'hex_depth': std['bolt_slip_fit'] + 0.5,  # Slightly deeper than bolt
            'counter_bore_diameter': hex_size + 1.0,
            'counter_bore_depth': std['bolt_slip_fit'] + 1.0,
            'counter_sunk_diameter': std['bolt_slip_fit'] * 2,
            'counter_sunk_chamfer_depth': std['bolt_slip_fit'] * 0.7,
            'counter_sunk_chamfer': std['bolt_slip_fit'] * 0.5,
            'counter_bore_washer_diameter': hex_size + 2.5,
            'counter_bore_washer_depth': std['bolt_slip_fit'] + 1.5,
            'square_press_fit': square_size + press_fit_offset,
            'square_slip_fit': square_size + slip_fit_offset,
            'square_depth': std['bolt_slip_fit'] + 0.5,
            'square_slip_fit_vertical_width': square_size * 0.4,  # Nut thickness ~40% of size
            'square_slip_fit_vertical_length': square_size + slip_fit_offset,
            'square_slip_fit_vertical_depth': square_size + slip_fit_offset,
            'heat_insert_diameter': std['heat_insert'],
        }

        return suggestions
