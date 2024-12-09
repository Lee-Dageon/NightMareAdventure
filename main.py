from pico2d import *

import enter_stage1
import enter_stage2
import game_framework
import base_stage
import lose_mode_stage1
import lose_mode_stage2
import stage1_mode
import stage2_mode
import start_mode
import win_mode

open_canvas()
game_framework.run(stage2_mode)
close_canvas()