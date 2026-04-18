from django.shortcuts import render, redirect
from django.http import JsonResponse, FileResponse, Http404
from django.views.decorators.http import require_http_methods
from django.conf import settings
from .forms import HardwareBoardForm, TestPieceForm
from .board_generator import HardwareBoardGenerator
from .test_piece_generator import TestPieceGenerator
from .validation import HardwareValidator
import os
import shutil
import json


def home(request):
    """Home page with standard mode and test pieces forms"""
    standard_form = HardwareBoardForm()
    test_piece_form = TestPieceForm()

    context = {
        'standard_form': standard_form,
        'test_piece_form': test_piece_form,
    }

    return render(request, 'board_designer/home.html', context)


@require_http_methods(["POST"])
def generate_board(request):
    """Generate hardware board and return download links"""

    # Standard mode - get all parameters from form
    standard_form = HardwareBoardForm(request.POST)
    if not standard_form.is_valid():
        return JsonResponse({
            'success': False,
            'errors': standard_form.errors
        })

    # Convert form to parameters dictionary
    params = {}
    for field in standard_form.cleaned_data:
        params[field] = standard_form.cleaned_data[field]

    # Handle bolt head type
    if params.get('bolt_head_type') == 'custom':
        params['bolt_head_type'] = params.get('custom_bolt_head_type', '')
    elif params.get('bolt_head_type') == '':
        params['bolt_head_type'] = ''

    # Validate parameters
    is_valid, errors, warnings = HardwareValidator.validate_all_parameters(params)

    if not is_valid:
        return JsonResponse({
            'success': False,
            'errors': errors,
            'warnings': warnings
        })

    try:
        # Generate the board
        generator = HardwareBoardGenerator(params)
        base_path, graphics_path = generator.generate()

        # Copy files to media directory for serving
        media_dir = settings.MEDIA_ROOT
        os.makedirs(media_dir, exist_ok=True)

        bolt_size = params['bolt_size']
        bolt_head = params.get('bolt_head_type', '').replace(' ', '_')
        base_filename = f"{bolt_size}_{bolt_head}_hardware_board_base.stl".replace('__', '_')

        # Copy base file
        base_dest = os.path.join(media_dir, base_filename)
        shutil.copy(base_path, base_dest)

        response_data = {
            'success': True,
            'base_file': base_filename,
            'warnings': warnings
        }

        # Copy graphics file if multi-color
        if graphics_path:
            graphics_filename = f"{bolt_size}_{bolt_head}_hardware_board_graphics.stl".replace('__', '_')
            graphics_dest = os.path.join(media_dir, graphics_filename)
            shutil.copy(graphics_path, graphics_dest)
            response_data['graphics_file'] = graphics_filename

        # Clean up temp files
        if os.path.exists(base_path):
            os.remove(base_path)
        if graphics_path and os.path.exists(graphics_path):
            os.remove(graphics_path)

        return JsonResponse(response_data)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'errors': [f"Error generating board: {str(e)}"]
        })


def download_stl(request, filename):
    """Download STL file"""
    file_path = os.path.join(settings.MEDIA_ROOT, filename)

    if not os.path.exists(file_path):
        raise Http404("File not found")

    # Security check - ensure filename doesn't contain path traversal
    if '..' in filename or '/' in filename or '\\' in filename:
        raise Http404("Invalid filename")

    # Ensure it's an STL file
    if not filename.endswith('.stl'):
        raise Http404("Invalid file type")

    response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
    response['Content-Type'] = 'application/octet-stream'
    response['X-Content-Type-Options'] = 'nosniff'

    return response


@require_http_methods(["POST"])
def generate_test_piece(request):
    """Generate test piece and return download link"""

    test_piece_form = TestPieceForm(request.POST)

    if not test_piece_form.is_valid():
        return JsonResponse({
            'success': False,
            'errors': test_piece_form.errors
        })

    try:
        # Build params dict for test piece generator
        params = {
            'piece_type': test_piece_form.cleaned_data['piece_type'],
            'bolt_slip_fit': test_piece_form.cleaned_data['bolt_slip_fit'],
            'base_size': test_piece_form.cleaned_data['base_size'],
        }

        # Add optional fields based on piece type
        piece_type = params['piece_type']

        # For bolt_slip_fit test piece, use base_size as the bolt_slip_fit value
        if piece_type == 'bolt_slip_fit':
            params['bolt_slip_fit'] = params['base_size']

        if piece_type == 'hex_nut':
            params['hex_depth'] = test_piece_form.cleaned_data.get('hex_depth')
        elif piece_type == 'square_nut':
            params['square_depth'] = test_piece_form.cleaned_data.get('square_depth')
        elif piece_type == 'counter_bore':
            params['counter_bore_depth'] = test_piece_form.cleaned_data.get('counter_bore_depth')
        elif piece_type == 'counter_bore_washer':
            params['counter_bore_washer_depth'] = test_piece_form.cleaned_data.get('counter_bore_washer_depth')
        elif piece_type == 'counter_sunk':
            params['counter_sunk_chamfer_depth'] = test_piece_form.cleaned_data.get('counter_sunk_chamfer_depth')
            params['counter_sunk_chamfer'] = test_piece_form.cleaned_data.get('counter_sunk_chamfer')
        elif piece_type == 'heat_insert':
            params['heat_insert_depth'] = test_piece_form.cleaned_data.get('heat_insert_depth')
        elif piece_type == 'vertical_square':
            params['square_slip_fit_vertical_width'] = test_piece_form.cleaned_data.get('square_slip_fit_vertical_width')
            params['square_slip_fit_vertical_depth'] = test_piece_form.cleaned_data.get('square_slip_fit_vertical_depth')

        # Generate the test piece
        generator = TestPieceGenerator(params)
        test_piece_path = generator.generate()

        # Copy file to media directory for serving
        media_dir = settings.MEDIA_ROOT
        os.makedirs(media_dir, exist_ok=True)

        base_size = params['base_size']
        filename = f"test_{piece_type}_{base_size}.stl"

        dest_path = os.path.join(media_dir, filename)
        shutil.copy(test_piece_path, dest_path)

        # Clean up temp file
        if os.path.exists(test_piece_path):
            os.remove(test_piece_path)

        return JsonResponse({
            'success': True,
            'file': filename
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'errors': [f"Error generating test piece: {str(e)}"]
        })
