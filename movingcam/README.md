**Code for photogrammetry exhibit in the Jerusalem Science Museum**

Directory **"main"**: python code for generating the object and texture files using Meshroom batch and viewing it localy via OpenGL.
- **photogrammetry.py** - main code handling everything, run this.
- **settings_override.json** - settings configuration for Meshroom.
- **consts.py** - consts file.
- **run_camera.py** - code for handling camera operations.
- **run_meshroom.py** - code for handling Meshroom processes.
- **objloader.py** - code for handling object and texture files.
- **pictures** - sub directory containing all screen pictures for every state.
- **pictures_consts.py** - consts for pictures 

Directory **"outside_screen"**: python code for viewing the object files from the shared directory.
- **main.py** - main code for viewing the models via OpenGL.
- **consts.py** - consts file.

Directory **"arduino"**: arduino code for running the moving camera about 70 degrees around the person.
- **Spinning-Arm-Photogrammetry.ino** - main code for arduino.
- **Consts.h** - consts header.
- **Basic_Routines.h** - basic routines for moving arm.
