import sys, numpy, inspect
from PIL import Image
from config import *

output_code = []
output_image = Image.new('RGB', (W, H), BG_COLOR)
output_image_pixels = output_image.load()

def code (line):
    global output_code
    output_code.append(line)

def pixel (x, y, z):
    output_image_pixels[
        int((x - X_AREA[0]) / MILL_DX), int(W - (y - Y_AREA[0]) / MILL_DY - 1)
    ] = (int(96 + z * 16), int(128 + z * 32), 128)

code('%')
code('(AREA X ' + str(X_AREA[0]) + '..' + str(X_AREA[1]) + ')')
code('(AREA Y ' + str(Y_AREA[0]) + '..' + str(Y_AREA[1]) + ')')
code('(OUT TOP Z ' + str(OUT_TOP_Z) + ')')
code('(SAFE TOP Z ' + str(SAFE_TOP_Z) + ')')
code('(TOP Z ' + str(TOP_Z) + ')')
code('(BOTTOM Z ' + str(BOTTOM_Z) + ')')
code('(F ' + str(FEED) + ')')
code('(S ' + str(SPEED) + ')')
code('(MILL DX ' + str(MILL_DX) + ')')
code('(MILL DY ' + str(MILL_DY) + ')')
code('(SIDE DZ ' + str(SIDE_DZ) + ')')
code('(PATH TOLERANCE ' + str(PATH_TOLERANCE) + ')')
code('')

function_text = inspect.getsource(F)

code('(FUNCTION:)')
code('(' + function_text.replace('(', '[').replace(')', ']').replace('\n', ')\n(')[:-2])
code('')
code('(INIT)')
code('G64 P' + str(PATH_TOLERANCE))
code('G0 Z' + str(OUT_TOP_Z))
code('X' + str(X_AREA[0]) + ' Y' + str(Y_AREA[0]))
code('Z' + str(SAFE_TOP_Z))
code('')

code('(SIDE)')
y = Y_AREA[0]
z_min = 0
for x in numpy.arange(X_AREA[0], X_AREA[1], MILL_DX):
  z_min = min(F(x, y), z_min)
z_min = max(BOTTOM_Z, z_min)
code('(Z min: ' + str(z_min) + ')')
x_dir = +1
for z_min_current_step in numpy.arange(0, z_min - SIDE_DZ * 0.1, -SIDE_DZ):
  code('(Z' + str(z_min_current_step) + ', X' + ('+' if x_dir > 0 else '-') + ')')
  code('G1 F' + str(FEED))
  y = Y_AREA[0]
  (x_begin, x_end) = (X_AREA[0], X_AREA[1]) if x_dir > 0 else (X_AREA[1], X_AREA[0])
  for x in numpy.arange(x_begin, x_end + MILL_DX * x_dir * 0.1, MILL_DX * x_dir):
    z = max(z_min_current_step, F(x, y), BOTTOM_Z)
    code('X' + NUM_FORMAT.format(x) + ' Z' + NUM_FORMAT.format(z))
  x_dir = -x_dir;
code('')

code('(MOVE TO MILL)')
code('Z' + str(SAFE_TOP_Z))
code('G0 Z' + str(OUT_TOP_Z))
code('X' + str(X_AREA[0]) + ' Y' + str(Y_AREA[0]))
code('Z' + str(SAFE_TOP_Z))
code('')

code('(MILL)')
z_min = float("inf")
z_max = float("-inf")
x_dir = +1
for y in numpy.arange(Y_AREA[0], Y_AREA[1] + MILL_DY * 0.1, MILL_DY):
  code('(Y ' + str(y) + ', X' + ('+' if x_dir > 0 else '-') + ')')
  code('G1 Y' + NUM_FORMAT.format(y) + ' F' + str(FEED))
  (x_begin, x_end) = (X_AREA[0], X_AREA[1]) if x_dir > 0 else (X_AREA[1], X_AREA[0])
  for x in numpy.arange(x_begin, x_end + MILL_DX * x_dir * 0.1, MILL_DX * x_dir):
    z = F(x, y)
    z_min = min(z, z_min)
    z_max = max(z, z_max)
    z = max(z, BOTTOM_Z)
    code('X' + NUM_FORMAT.format(x) + ' Z' + NUM_FORMAT.format(z))
    pixel(x, y, z)
  x_dir = -x_dir;
code('(Z_AREA: ' + NUM_FORMAT.format(z_min) + ' ... ' + NUM_FORMAT.format(z_max) + ')')
code('')

code('(MOVE OUT)')
code('Z' + str(SAFE_TOP_Z))
code('G0 Z' + str(OUT_TOP_Z))
code('X' + str(X_AREA[0]) + ' Y' + str(Y_AREA[0]))
code('%')

output_image.save(OUTPUT_IMAGE_FILENAME, 'JPEG', quality = OUTPUT_IMAGE_QUALITY)
with open(OUTPUT_CODE_FILENAME, "w") as output:
    output.write("\n".join(output_code))
