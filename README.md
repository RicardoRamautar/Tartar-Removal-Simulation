# Running the script
The file structure of this directory is as follows:
```bash
.
├── dependencies
│   ├── pantograph.py
│   ├── pshape.py
│   └── pyhapi.py
├── images
│   ├── front_sprite_rounded_rotated.png
│   ├── lower_jaw_rotated2.png
│   ├── realistic_tartar_rotated.png
│   ├── rotated_teeth_contour.png
│   └── tartar_detection_rotated_2.png
├── main.py
├── modules
│   ├── config.py
│   ├── end_loop.py
│   ├── game_loop.py
│   ├── gradient_field.py
│   ├── haptic_port.py
│   ├── initial_screen.py
│   ├── settings_screen.py
│   └── ui_logic.py
└── README.md

```
`dependencies` Contains the python files  that are necessary to run the code with the haply board, which were also provided in assignments 1 and 2. `modules` contains our own files that are necessary to run the game. `modules/initial_screen.py`, `modules/settings_screen.py`, `modules/game_loop.py`, and `modules/end_loop.py`, contain the code for the different simulation screens denoted in **The simulation** section. These files use the classes for writing text and rectangles onto the pygame screen that are stored in `modules/ui_logic.py`. `modules/haptic_port.py` contains some logic for the serial port. The main logic that implements the force feedback is stored in `main.py`, which makes use of some variables that are stored inside `config.py`. The logic for creating the gradient fields is stored inside `modules/gradient_field.py`, which is also used by `main.py`.

To run the simulation, simply run `main.py`. However, note that the code uses relative paths, so make sure that you are working inside this directory (so the file strucutre should look the same as the tree shown above). Otherwise, you will need to change the paths inside the code.

# The simulation
### 1. Settings screen
This is the first screen you see when running `main.py`. Here you need to fill in the name of the participant and the assistanc level.  You do this by clicking the rectangles with your mouse (maybe you have to click twice) and then simply typing the name/assistance level. 

You need to do this for every trial. Make sure that you write the same name at every trial for the same participant, since it is used as key to store the results of this trial for that specific participant. Additionally, ensure that each participant uses a different name here. Otherwise, results will get mixed up. Alternatively, you can simply rename the .json files after a participant has finished all trials.

Assign haptic assitance levels as follows:
- **Group 1: Shared control** - Assistance level is always `0.2`.
- **Group 2: Degrading control** - First two runs, assistance level is `0.2`. The two runs after that, it should be `0.175`. The final two trials should have an assistance level of `0.15`.
- **Group 3: No shared control** - Assistance level is `0`.

However, during the baseline runs and evaluation runs, the assistance level should be `0`.

Press `continue` to move on to the next screen.

### 2. Start screen
As shown on the screen, press the `e`-key on your keyboard to move onto the next screen.

### 3. Positioning screen
You now need to let go of your mouse and move the end of the Haply board towards the turquoise circle. 

Once the haptic handle is on the circle, a timer will count down from 5 and the game will start after the countdown ends. Make sure you hold the end of the Haply board tightly, since the Haply board might exert a small force at the start of the game.

### 4. Game screen
You need to remove the tartar on the front teeth. You only get 30 seconds to do this. `Time remaining` denotes how much time you have left. `tartar removed` denotes the percentage of the total amount of tartar you have currently removed. 

You get negative points every time you touch the gums. The `gum hits` denotes how many times you have touched the gums. You get penalized as follows: Once you hit the gums you get -1 point. This position at which you touched the gum is then stored. The next time you hit the gums, you will only get penalized if this position is at least 10 pixels away from the previous position you hit the gums to ensure you don't get penalized every iteration at which you are positioned on the gums. 

Note that some of the tartar is positioned over the gums. You are free to remove this tartar and will not be penalized for this. However, even if you only slightly hit the gum region without tartar, you will get penalized.

### 5. End screen
`Your score` denotes how well you did. The maximum score is 100. We get this score by subtracting the gum damage from the amount of tartar removed. `Tartar removed` denotes the fraction of the total tartar that you removed and `Gum damage` denotes how often you hit the gums.

This result will be stored in a dictionary inside the `data_storage.json` file with the following structure:
```python
{
"Participant1": 
    {
        "1": {"total_score": 73, "tartar_fraction": 84, "gum_score": -11}, 
        "2": {"total_score": 75, "tartar_fraction": 92, "gum_score": -17}
    }, 
"Participant2": 
    {
        "1": {"total_score": -9, "tartar_fraction": 15, "gum_score": -24}, 
        "2": {"total_score": -1, "tartar_fraction": 0, "gum_score": -1}
    }
}
```
`Participant1` and `Participant2` are the names of the two participants. In this example, each participant did two trials which are indexed by `1` and `2` with the corresponding scores of each trial.
