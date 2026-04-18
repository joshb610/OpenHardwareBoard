from django import forms
from .models import HardwareBoard
from .validation import HardwareValidator


class HardwareBoardForm(forms.ModelForm):
    """Form for standard mode - all parameters"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-fill with M3 example values from overview.md for testing
        if not self.instance.pk and not self.data:
            self.initial = {
                'bolt_size': 'M3',
                'bolt_slip_fit': 3.3,
                'press_fit_hex': 5.4,
                'slip_fit_hex': 5.7,
                'hex_depth': 6.6,
                'counter_bore_diameter': 5.7,
                'counter_bore_depth': 8.2,
                'counter_bore_washer_diameter': 7.4,
                'counter_bore_washer_depth': 9.9,
                'counter_sunk_diameter': 6.4,
                'counter_sunk_chamfer_depth': 2.2,
                'counter_sunk_chamfer': 1.5,
                'square_press_fit': 5.4,
                'square_slip_fit': 5.8,
                'square_depth': 2.1,
                'square_slip_fit_vertical_width': 2.1,
                'square_slip_fit_vertical_length': 6.1,
                'square_slip_fit_vertical_depth': 6.1,
                'heat_insert_diameter': 4.5,
                'multi_color': False,
                'text_style': 'raised',
                'text_height': 0.4,
                'line_width': 0.8,
            }

    class Meta:
        model = HardwareBoard
        fields = '__all__'
        exclude = ['created_at', 'updated_at']
        widgets = {
            'bolt_size': forms.Select(attrs={'class': 'form-control'}),
            'bolt_head_type': forms.Select(attrs={'class': 'form-control'}),
            'custom_bolt_head_type': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '20',
                'placeholder': 'Custom bolt head type'
            }),
            'bolt_slip_fit': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0.1'
            }),
            'press_fit_hex': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0.1'
            }),
            'slip_fit_hex': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0.1'
            }),
            'hex_depth': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0.1'
            }),
            'counter_bore_diameter': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0.1'
            }),
            'counter_bore_depth': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0.1'
            }),
            'counter_sunk_diameter': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0.1'
            }),
            'counter_sunk_chamfer_depth': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0.1'
            }),
            'counter_sunk_chamfer': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0.1'
            }),
            'counter_bore_washer_diameter': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0.1'
            }),
            'counter_bore_washer_depth': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0.1'
            }),
            'square_press_fit': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0.1'
            }),
            'square_slip_fit': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0.1'
            }),
            'square_depth': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0.1'
            }),
            'square_slip_fit_vertical_width': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0.1'
            }),
            'square_slip_fit_vertical_length': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0.1'
            }),
            'square_slip_fit_vertical_depth': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0.1'
            }),
            'heat_insert_diameter': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0.1'
            }),
            'heat_insert_depth': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0.1',
                'placeholder': 'Optional - defaults to board depth - 1mm'
            }),
            'export_mode': forms.Select(attrs={'class': 'form-control'}),
            'text_height': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0.1',
                'max': '2.0'
            }),
            'line_width': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0.2',
                'max': '2.0'
            }),
        }
        labels = {
            'bolt_slip_fit': 'Bolt Slip Fit (mm)',
            'press_fit_hex': 'Hex Press Fit (mm)',
            'slip_fit_hex': 'Hex Slip Fit (mm)',
            'hex_depth': 'Hex Depth (mm)',
            'counter_bore_diameter': 'Counter Bore Diameter (mm)',
            'counter_bore_depth': 'Counter Bore Depth (mm)',
            'counter_sunk_diameter': 'Counter Sunk Diameter (mm)',
            'counter_sunk_chamfer_depth': 'Counter Sunk Chamfer Depth (mm)',
            'counter_sunk_chamfer': 'Counter Sunk Chamfer (mm)',
            'counter_bore_washer_diameter': 'Counter Bore + Washer Diameter (mm)',
            'counter_bore_washer_depth': 'Counter Bore + Washer Depth (mm)',
            'square_press_fit': 'Square Press Fit (mm)',
            'square_slip_fit': 'Square Slip Fit (mm)',
            'square_depth': 'Square Depth (mm)',
            'square_slip_fit_vertical_width': 'Vertical Square Width (mm)',
            'square_slip_fit_vertical_length': 'Vertical Square Length (mm)',
            'square_slip_fit_vertical_depth': 'Vertical Square Depth (mm)',
            'heat_insert_diameter': 'Heat Insert Diameter (mm)',
            'heat_insert_depth': 'Heat Insert Depth (mm) - Optional',
            'export_mode': 'Export Mode',
            'text_height': 'Text/Line Height (mm)',
            'line_width': 'Line Width (mm)',
        }
        help_texts = {
            'heat_insert_depth': 'For permanent inserts. Depth will not be shown on the board. Leave empty to default to board depth - 1mm.',
            'export_mode': 'Choose how graphics/text are exported: Multi-color modes create 2 separate STL files, single color modes create 1 STL file.',
        }

    def clean(self):
        cleaned_data = super().clean()

        # Validate all float fields have 1 decimal place max
        for field_name, value in cleaned_data.items():
            if isinstance(value, float):
                # Check decimal places
                str_value = str(value)
                if '.' in str_value:
                    decimal_places = len(str_value.split('.')[1])
                    if decimal_places > 1:
                        self.add_error(field_name, f'Maximum 1 decimal place allowed. Got {decimal_places}.')

        # Validate all parameters
        is_valid, errors, warnings = HardwareValidator.validate_all_parameters(cleaned_data)

        if not is_valid:
            for error in errors:
                self.add_error(None, error)

        # Store warnings for display (non-field errors)
        if warnings:
            for warning in warnings:
                self.add_error(None, f"Warning: {warning}")

        return cleaned_data


class TestPieceForm(forms.Form):
    """Form for generating test pieces with 5 holes in 0.1mm increments"""

    PIECE_TYPES = [
        ('bolt_slip_fit', 'Bolt Slip Fit'),
        ('hex_nut', 'Hex Nut (works for both press and slip fit)'),
        ('square_nut', 'Square Nut (works for both press and slip fit)'),
        ('counter_bore', 'Counter Bore'),
        ('counter_bore_washer', 'Counter Bore + Washer'),
        ('counter_sunk', 'Counter Sunk'),
        ('heat_insert', 'Heat Insert'),
        ('vertical_square', 'Vertical Square Nut'),
    ]

    piece_type = forms.ChoiceField(
        choices=PIECE_TYPES,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'piece_type'}),
        label='Test Piece Type'
    )

    # Common field - required for all piece types except bolt_slip_fit
    bolt_slip_fit = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'min': '0.1',
            'id': 'bolt_slip_fit'
        }),
        label='Bolt Slip Fit (mm)',
    )

    # Base size being tested (generates +0.1, +0.2, +0.3, +0.4)
    base_size = forms.FloatField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'min': '0.1',
            'id': 'base_size'
        }),
        label='Base Size (mm)',
        help_text='Will generate 5 holes: this size, +0.1, +0.2, +0.3, +0.4mm'
    )

    # Hex nut specific
    hex_depth = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'min': '0.1'
        }),
        label='Hex Depth (mm)',
    )

    # Square nut specific
    square_depth = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'min': '0.1'
        }),
        label='Square Depth (mm)',
    )

    # Counter bore specific
    counter_bore_depth = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'min': '0.1'
        }),
        label='Counter Bore Depth (mm)',
    )

    # Counter bore + washer specific
    counter_bore_washer_depth = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'min': '0.1'
        }),
        label='Counter Bore + Washer Depth (mm)',
    )

    # Counter sunk specific
    counter_sunk_chamfer_depth = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'min': '0.1'
        }),
        label='Counter Sunk Chamfer Depth (mm)',
    )

    counter_sunk_chamfer = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'min': '0.1'
        }),
        label='Counter Sunk Chamfer (mm)',
    )

    # Heat insert specific
    heat_insert_depth = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'min': '0.1'
        }),
        label='Heat Insert Depth (mm)',
    )

    # Vertical square specific
    square_slip_fit_vertical_width = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'min': '0.1'
        }),
        label='Vertical Square Width (mm)',
    )

    square_slip_fit_vertical_depth = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'min': '0.1'
        }),
        label='Vertical Square Depth (mm)',
    )

    def clean(self):
        """Validate that required fields for selected piece type are present"""
        cleaned_data = super().clean()
        piece_type = cleaned_data.get('piece_type')

        # Validate all float fields have 1 decimal place max
        for field_name, value in cleaned_data.items():
            if isinstance(value, float):
                # Check decimal places
                str_value = str(value)
                if '.' in str_value:
                    decimal_places = len(str_value.split('.')[1])
                    if decimal_places > 1:
                        self.add_error(field_name, f'Maximum 1 decimal place allowed. Got {decimal_places}.')

        # Bolt slip fit is required for all piece types except bolt_slip_fit
        if piece_type != 'bolt_slip_fit' and not cleaned_data.get('bolt_slip_fit'):
            self.add_error('bolt_slip_fit', 'This field is required.')

        # Validate required fields based on piece type
        if piece_type == 'hex_nut' and not cleaned_data.get('hex_depth'):
            self.add_error('hex_depth', 'This field is required for Hex Nut test pieces.')

        if piece_type == 'square_nut' and not cleaned_data.get('square_depth'):
            self.add_error('square_depth', 'This field is required for Square Nut test pieces.')

        if piece_type == 'counter_bore' and not cleaned_data.get('counter_bore_depth'):
            self.add_error('counter_bore_depth', 'This field is required for Counter Bore test pieces.')

        if piece_type == 'counter_bore_washer' and not cleaned_data.get('counter_bore_washer_depth'):
            self.add_error('counter_bore_washer_depth', 'This field is required for Counter Bore + Washer test pieces.')

        if piece_type == 'counter_sunk':
            if not cleaned_data.get('counter_sunk_chamfer_depth'):
                self.add_error('counter_sunk_chamfer_depth', 'This field is required for Counter Sunk test pieces.')
            if not cleaned_data.get('counter_sunk_chamfer'):
                self.add_error('counter_sunk_chamfer', 'This field is required for Counter Sunk test pieces.')

        if piece_type == 'heat_insert' and not cleaned_data.get('heat_insert_depth'):
            self.add_error('heat_insert_depth', 'This field is required for Heat Insert test pieces.')

        if piece_type == 'vertical_square':
            if not cleaned_data.get('square_slip_fit_vertical_width'):
                self.add_error('square_slip_fit_vertical_width', 'This field is required for Vertical Square Nut test pieces.')
            if not cleaned_data.get('square_slip_fit_vertical_depth'):
                self.add_error('square_slip_fit_vertical_depth', 'This field is required for Vertical Square Nut test pieces.')

        return cleaned_data
