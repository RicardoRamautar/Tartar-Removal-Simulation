from modules.ui_logic import create_transparent_rect, Text
from modules.config import *
from modules.gradient_field import gradientField
from modules.haptic_port import serial_ports
from modules.settings_screen import display_settings
from modules.initial_screen import display_initial_screen
from modules.game_loop import game
from modules.end_loop import display_end

# Calculate the amount of pixels per milimeter (dpmm)
app = QApplication(sys.argv)
screen = app.screens()[0]
dpi = screen.physicalDotsPerInch()
dpmm = dpi/25.4
dpm = dpmm * 1000
app.quit()

## Game setup
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True

# Center of screen coordinates
xc,yc = screen.get_rect().center

# Position of top-left corner of images
x_image = int(xc - 0.5 * jaw_image.get_width())
y_image = int( yc - 0.5 * jaw_image.get_height())
pos_image = np.array([x_image, y_image])


## Generate gradient fields around teeth
teeth_heightmaps = [gradientField(tooth, x_image=x_image, y_image=y_image, A=500, screen_dimensions=screen_dimensions) for tooth in teeth_ellipsoids]

total_gradients = np.zeros((screen_dimensions[1], screen_dimensions[0]))
for tooth in teeth_heightmaps:
    total_gradients += tooth.height_map

y_gradient, x_gradient = np.gradient(total_gradients)

## Haptic device setup
port = serial_ports()
if port:
    print("Board found on port %s"%port[0])
    haplyBoard = Board("test", port[0], 0)
    device = Device(5, haplyBoard)
    pantograph = Pantograph()
    device.set_mechanism(pantograph)
    
    device.add_actuator(1, CCW, 2)
    device.add_actuator(2, CW, 1)
    
    device.add_encoder(1, CCW, 241, 10752, 2)
    device.add_encoder(2, CW, -61, 10752, 1)
    
    device.device_set_parameters()
else:
    print("No compatible device found. Running virtual environnement...")


## Settings screen
participant_name, assistance_level = display_settings(xc, yc, screen)

## Determine current trial
if os.path.exists(file_name):
    with open(file_name, 'r') as json_file:
        loaded_dict = json.load(json_file)
else:
    loaded_dict = {}

try:
    print("loaded dict: \n", loaded_dict)
    print("loaded_dict[participant_name]: ", loaded_dict[participant_name])
    vals = list(loaded_dict[participant_name].keys())
    last_trial = max([int(i) for i in vals])
    current_trial = last_trial + 1
except:
    current_trial = 1

## Display initial screen                     
display_initial_screen(xc, yc, screen, port, x_image, y_image, haplyBoard, device)

# Display game
tartar_score, gum_score, tartar_fraction = game(xc, yc, current_trial, port, pos_image, x_gradient, y_gradient, assistance_level, x_image, y_image, screen, clock, dpm, device, haplyBoard)

total_score = tartar_fraction + gum_score

## Display ending scenelo
display_end(xc, yc, screen, tartar_fraction, gum_score, total_score)

print("Amount of tartar removed: ", tartar_fraction)
print("Number of times gum was touched: ", gum_score)
print("Total score: ", total_score)
    
if current_trial == 1:
    loaded_dict[participant_name] = {str(current_trial): {"total_score": total_score,
                                            "tartar_fraction": tartar_fraction,
                                            "gum_score": gum_score}}

loaded_dict[participant_name][str(current_trial)] = {"total_score": total_score,
                                                     "tartar_fraction": tartar_fraction,
                                                     "gum_score": gum_score}

with open(file_name, 'w') as json_file:
    json.dump(loaded_dict, json_file)