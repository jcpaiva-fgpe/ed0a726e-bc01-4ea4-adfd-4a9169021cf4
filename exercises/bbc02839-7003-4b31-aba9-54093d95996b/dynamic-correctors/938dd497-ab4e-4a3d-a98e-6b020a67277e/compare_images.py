import subprocess
import os
from pathlib import Path
import sys


def check_image_exists(image_path):
    if not image_path.exists():
        print(f"Error: Image file '{image_path}' does not exist")
        return False
    if not os.access(image_path, os.R_OK):
        print(f"Error: Image file '{image_path}' is not readable")
        return False
    return True

def compare_images(base_path, test_path, output_path=None):
    # Check if input images exist
    if not check_image_exists(base_path) or not check_image_exists(test_path):
        return {'error': 'Input images not found or not readable'}
    
    # Create the compare command for metrics
    cmd = [
        'magick',
        'compare',
        '-metric', 'RMSE',
        str(base_path),
        str(test_path),
        'null:'
    ]
    
    # Run the command and capture stderr (where ImageMagick outputs the metrics)
    result = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
    
    # Parse the output
    try:
        # The output is in the format "123.45 (0.0012345)"
        difference, normalized = result.stderr.strip().split()
        difference = float(difference)
        normalized = float(normalized.strip('()'))
        
        # Create difference image if output path is provided
        if output_path:
            try:
                # Create a difference image with:
                # - Received image in background
                # - Very transparent red overlay for differences
                subprocess.run([
                    'magick',
                    str(test_path),
                    '(',
                    str(base_path),
                    str(test_path),
                    '-compose', 'difference',
                    '-composite',
                    '-threshold', '0',
                    '-fill', 'transparent',
                    '-opaque', 'black',
                    '-fill', 'rgba(255,0,0)',
                    '-opaque', 'white',
                    ')',
                    '-compose', 'over',
                    '-composite',
                    str(output_path)
                ], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Warning: Could not create difference image: {str(e)}")
        
        return {
            'difference': difference,
            'normalized_difference': normalized,
            'message': f'Images differ by {difference:.2f} ({(normalized * 100):.2f}%)'
        }
    except (ValueError, IndexError) as e:
        return {
            'error': str(e),
            'raw_output': result.stderr
        }
    except subprocess.CalledProcessError as e:
        return {
            'error': f'ImageMagick command failed: {str(e)}',
            'raw_output': e.stderr if e.stderr else str(e)
        }

def main():
    if len(sys.argv) != 3:
        print("Usage: python compare_images.py <base_image> <test_image>")
        sys.exit(1)
        
    base_image = Path(sys.argv[1])
    test_image = Path(sys.argv[2])
    diff_output = Path('difference.png')
    
    try:
        # Compare images
        metrics = compare_images(base_image, test_image, diff_output)
        
        if 'error' in metrics:
            print(f'\nError: {metrics["error"]}')
            sys.exit(1)
            
        print('\nComparison metrics:', metrics)
        
        # Exit with 0 if images are identical (difference is 0)
        if metrics['difference'] == 0:
            sys.exit(0)
        else:
            sys.exit(2)
        
    except Exception as e:
        print(f'\nError: {str(e)}')
        print("\nPlease make sure:")
        print("1. The image files exist and are readable")
        print("2. You have ImageMagick installed and available in your PATH")
        sys.exit(1)

if __name__ == '__main__':
    main()


#def read_file(filepath):
#    with open(filepath, 'r') as file:
#        return file.read().strip()

#arg1 = read_file(sys.argv[1])
#arg2 = read_file(sys.argv[2])

# Writing to standard output
#print(f"Argument 1: {arg1}", file=sys.stdout)
#print(f"Argument 2: {arg2}", file=sys.stdout)

# Writing to standard error
#print("This is an error message", file=sys.stderr)
#print( arg1, arg2)

exit(0)