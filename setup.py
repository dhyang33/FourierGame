import sys
import cx_Freeze

build_exe_options = {"packages":
                        ["pygame",
                         "argparse",
                         "librosa",
                         "time",
                         "numpy",
                         "soundfile",
                         "random",
                         "os",
                         "sys",
                         "matplotlib",
                         "scipy",
                         "pylab",
                         "llvmlite"],
                     "includes":
                        ["pitchgame1",
                         "pitchgame2",
                         "pitchgame3",
                         "pitchgame4",
                         "scoreScreen",
                         "sprite",
                         "startScreen",
                         "textBox",
                         "tutorial"],
                     "include_files":
                        ["downarrow-removebg.png",
                         "downarrow.PNG",
                         "Mary.mp3",
                         "orig_sound.wav",
                         "sound.png",
                         "uparrow-removebg.png",
                         "uparrow.PNG"],
                     "silent": True}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

cx_Freeze.setup(
    name = "Fourier Game",
    version = "1.0",
    options={"build_exe": build_exe_options},
    executables = [cx_Freeze.Executable("game.py", base=base)]

)