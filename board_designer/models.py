from django.db import models


class HardwareBoard(models.Model):
    """Model to store hardware board configurations"""

    BOLT_SIZES = [
        ('M2', 'M2'),
        ('M3', 'M3'),
        ('M4', 'M4'),
        ('M5', 'M5'),
        ('M6', 'M6'),
        ('M8', 'M8'),
        ('M10', 'M10'),
        ('M12', 'M12'),
    ]

    BOLT_HEAD_TYPES = [
        ('', 'None'),
        ('Button Head', 'Button Head'),
        ('Socket Head', 'Socket Head'),
        ('Flat Head', 'Flat Head'),
        ('Pan Head', 'Pan Head'),
        ('Hex Head', 'Hex Head'),
        ('Truss Head', 'Truss Head'),
        ('custom', 'Custom'),
    ]

    # Basic info
    bolt_size = models.CharField(max_length=10, choices=BOLT_SIZES, default='M3')
    bolt_head_type = models.CharField(max_length=20, choices=BOLT_HEAD_TYPES, blank=True, default='')
    custom_bolt_head_type = models.CharField(max_length=20, blank=True, null=True)

    # Bolt parameters
    bolt_slip_fit = models.FloatField()

    # Hex nut parameters
    press_fit_hex = models.FloatField()
    slip_fit_hex = models.FloatField()
    hex_depth = models.FloatField()

    # Counter bore parameters
    counter_bore_diameter = models.FloatField()
    counter_bore_depth = models.FloatField()

    # Counter sunk parameters
    counter_sunk_diameter = models.FloatField()
    counter_sunk_chamfer_depth = models.FloatField()
    counter_sunk_chamfer = models.FloatField()

    # Counter bore + washer parameters
    counter_bore_washer_diameter = models.FloatField()
    counter_bore_washer_depth = models.FloatField()

    # Square nut parameters
    square_press_fit = models.FloatField()
    square_slip_fit = models.FloatField()
    square_depth = models.FloatField()

    # Vertical square nut parameters
    square_slip_fit_vertical_width = models.FloatField()
    square_slip_fit_vertical_length = models.FloatField()
    square_slip_fit_vertical_depth = models.FloatField()

    # Heat insert parameters
    heat_insert_diameter = models.FloatField()
    heat_insert_depth = models.FloatField(null=True, blank=True)

    # Export options
    EXPORT_MODE_CHOICES = [
        ('multi_recessed', 'Multi-Color - Recessed (flush with surface, for multi-material printers)'),
        ('multi_raised', 'Multi-Color - Raised (above surface)'),
        ('single_cutout', 'Single Color - Cutout (cut into surface)'),
        ('single_raised', 'Single Color - Raised (above surface)'),
    ]
    export_mode = models.CharField(
        max_length=20,
        choices=EXPORT_MODE_CHOICES,
        default='single_raised'
    )
    text_height = models.FloatField(default=0.4)
    line_width = models.FloatField(default=0.8)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        head_type = self.custom_bolt_head_type if self.bolt_head_type == 'custom' else self.bolt_head_type
        return f"{self.bolt_size} {head_type} Board"

    def get_bolt_head_display_value(self):
        """Get the display value for bolt head type"""
        if self.bolt_head_type == 'custom':
            return self.custom_bolt_head_type or 'Custom'
        return self.bolt_head_type or ''

    def to_dict(self):
        """Convert model to dictionary for board generator"""
        return {
            'bolt_size': self.bolt_size,
            'bolt_head_type': self.get_bolt_head_display_value(),
            'bolt_slip_fit': self.bolt_slip_fit,
            'press_fit_hex': self.press_fit_hex,
            'slip_fit_hex': self.slip_fit_hex,
            'hex_depth': self.hex_depth,
            'counter_bore_diameter': self.counter_bore_diameter,
            'counter_bore_depth': self.counter_bore_depth,
            'counter_sunk_diameter': self.counter_sunk_diameter,
            'counter_sunk_chamfer_depth': self.counter_sunk_chamfer_depth,
            'counter_sunk_chamfer': self.counter_sunk_chamfer,
            'counter_bore_washer_diameter': self.counter_bore_washer_diameter,
            'counter_bore_washer_depth': self.counter_bore_washer_depth,
            'square_press_fit': self.square_press_fit,
            'square_slip_fit': self.square_slip_fit,
            'square_depth': self.square_depth,
            'square_slip_fit_vertical_width': self.square_slip_fit_vertical_width,
            'square_slip_fit_vertical_length': self.square_slip_fit_vertical_length,
            'square_slip_fit_vertical_depth': self.square_slip_fit_vertical_depth,
            'heat_insert_diameter': self.heat_insert_diameter,
            'heat_insert_depth': self.heat_insert_depth,
            'export_mode': self.export_mode,
            'text_height': self.text_height,
            'line_width': self.line_width,
        }
