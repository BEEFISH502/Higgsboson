from build_godot import get_root
import json
import math
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_PATH = BASE_DIR / "data" / "processed" / "godot_vfx_events.json"

'''1. particle config variable
2. get_root()
3. get_value()
4. calculate_momentum()
5. normalize_vector()
6. map_particle_to_godot()
7. create_godot_json()
8. main()'''

'''
calculate_intensity()
calculate_focus()
calculate_transparency()
calculate_curvature()
build_tags()
map_particle_to_godot()
map_event_to_godot()
create_godot_json()
'''