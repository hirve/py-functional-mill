import functions

X_AREA = (-1, 61)
Y_AREA = (-1, 61)
SIDE_DZ = 0.1
MILL_DY = 0.1
MILL_DX = 0.1
PATH_TOLERANCE = 0.01
OUT_TOP_Z = 30
SAFE_TOP_Z = 10
TOP_Z = 0
BOTTOM_Z = -14.0
FEED = 1000
SPEED = 15000
NUM_FORMAT = '{:.4f}'
OUTPUT_CODE_FILENAME = "function.ngc"
OUTPUT_IMAGE_FILENAME = "function.jpg"
(W, H) = (
    int((X_AREA[1] - X_AREA[0]) / MILL_DX + 1),
    int((Y_AREA[1] - Y_AREA[0]) / MILL_DY + 1),
)
BG_COLOR = (255, 255, 255)
OUTPUT_IMAGE_QUALITY = 98

F = functions.wood
