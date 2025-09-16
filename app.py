#!/usr/bin/env python3
"""
Skateboard Angle Display App

A simple pygame application that displays skateboard sprites
at a specific angle (15-degree rounded angles).
"""
import random
import pygame
import os
from typing import Tuple, Optional

class SkateboardApp:
    """Optimized skateboard game with improved performance and code organization"""
    
    def __init__(self):
        """Initialize the app"""
        pygame.init()
        pygame.mixer.init()
        
        # Create fullscreen window
        self.display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.display_width = self.display.get_width()
        self.display_height = self.display.get_height()
        print(f"Display resolution: {self.display_width}x{self.display_height}")
        
        pygame.display.set_caption("Random Skateboard Display")
        
        # Unified Color Scheme - Asphalt Focus
        self.colors = {
            # Primary colors
            'primary': (52, 73, 94),      # Dark blue-gray
            'secondary': (149, 165, 166), # Light gray
            'accent': (34, 153, 84),      # Darker Green
            'warning': (241, 196, 15),    # Yellow
            'danger': (185, 28, 28),      # Darker Red
            
            # Background colors
            'background': (44, 62, 80),   # Dark blue-gray background
            'surface': (52, 73, 94),      # Surface color
            'text': (236, 240, 241),      # Light text
            'text_secondary': (149, 165, 166), # Secondary text
            
            # UI elements
            'border': (0, 0, 0),    # Border color
            'progress_bg': (44, 62, 80),  # Progress bar background
            'progress_fill': (46, 204, 113), # Progress bar fill
            
            # Hand indicators
            'hand_left': (231, 76, 60),   # Red for left hand
            'hand_left_border': (192, 57, 43), # Darker red border
            'hand_right': (52, 152, 219), # Blue for right hand
            'hand_right_border': (41, 128, 185), # Darker blue border
            
            # Asphalt colors
            'asphalt_base': (45, 45, 45),     # Dark asphalt base color
            'asphalt_dark': (35, 35, 35),     # Darker asphalt variation
            'asphalt_light': (55, 55, 55),    # Lighter asphalt variation
            'crack_light': (65, 65, 65),      # Light crack color
            'crack_dark': (25, 25, 25),       # Dark crack color
            'patch_color': (60, 60, 60),      # Patch/repair color
        }
        
        # Fonts - scale based on screen size
        font_size = max(24, self.display_width // 40)
        title_font_size = max(36, self.display_width // 25)
        
        # Load custom fonts from fonts folder
        try:
            self.font = pygame.font.Font("fonts/ari-w9500.ttf", font_size)
            self.title_font = pygame.font.Font("fonts/ari-w9500-bold.ttf", title_font_size)
            print("Loaded custom fonts successfully")
        except pygame.error as e:
            print(f"Warning: Could not load custom fonts: {e}")
            # Fallback to default fonts
            self.font = pygame.font.Font(None, font_size)
            self.title_font = pygame.font.Font(None, title_font_size)
        
        # Load sprite resources
        self.sprite_map = None
        self.sprite_metadata = {}
        self.grid_width = 11  # New grid width for optimized spritemap
        self.grid_height = 10  # New grid height for optimized spritemap
        self.sprite_size = 64
        
        # Animation system
        self.animation_maps = {}
        self.animation_metadata = {}
        self.current_animation = None
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.05
        self.animation_completed = False  # Track if animation has completed
        
        self._load_sprite_map()
        self._load_metadata()
        self._load_animations()
        self._load_new_sprite_map()
        
        # Trick Map
        self.trick_map = {
            "BS-Shuv-It": ["down", "center"], 
            "FS-Shuv-It": ["up", "center"], 
            "Nollie BS-Shuv-It": ["center", "down"], 
            "Nollie FS-Shuv-It": ["center", "up"], 
            "Kickflip": ["left", "down"], 
            "Heelflip": ["left", "up"], 
            "Nollie Kickflip": ["down", "right"], 
            "Nollie Heelflip": ["up", "right"],
            "Varial Kickflip": ["down", "down"],
            "Varial Heelflip": ["up", "up"],
            "Inward Heelflip": ["down", "up"],
            "Hardflip": ["up", "down"]
            }
        
        # Animation behavior map - which animations should loop vs play once
        self.animation_loops = {
            # All tricks loop by default
        }
        
        # Grind Trick Map - combinations for grind tricks
        self.grind_trick_map = {
            "Nose Grind": ["left", "left"],
            "5-0 Grind": ["right", "right"],
            "Tailslide": ["up", "up"], 
            "Noseslide": ["down", "down"],
            "Crooked Grind": ["down", "right"],
            "Overcrooked Grind": ["up", "right"],
            "Smith Grind": ["left", "down"],
            "Feeble Grind": ["left", "up"], 
            "Frontside Boardslide": ["down", "up"], 
            "Backside Boardslide": ["up", "down"],
            "50-50 Grind": ["right", "left"],
            "Salad Grind": ["right", "up"],
            "Suski Grind": ["right", "down"],
            #Add willy gri
        }
        
        # Grind positions - image files for each grind
        self.grind_positions = {
            "50-50 Grind": {"image": "50-50_grind.png", "offset": (0, 0)},
            "Nose Grind": {"image": "nose_grind.png", "offset": (0, 0)},
            "Tailslide": {"image": "tailslide.png", "offset": (0, 0)},
            "Noseslide": {"image": "noseslide.png", "offset": (0, 0)},
            "Crooked Grind": {"image": "crooked_grind.png", "offset": (0, 0)},
            "Overcrooked Grind": {"image": "overcrooked_grind.png", "offset": (0, 0)},
            "Smith Grind": {"image": "smith_grind.png", "offset": (0, 0)},
            "Feeble Grind": {"image": "feeble_grind.png", "offset": (0, 0)},
            "Salad Grind": {"image": "salad_grind.png", "offset": (0, 0)},
            "Suski Grind": {"image": "suski_grind.png", "offset": (0, 0)},
            "Frontside Boardslide": {"image": "frontside_boardslide.png", "offset": (0, 0)},
            "Backside Boardslide": {"image": "backside_boardslide.png", "offset": (0, 0)},
            "5-0 Grind": {"image": "5-0_grind.png", "offset": (0, 0)}
        }
        
        # Load grind images
        self.grind_images = {}
        self._load_grind_images()

        self.airborne = False
        self.landing_angle = (0, 0)  # Default landing angle using new system
        self.last_spin_time = 0
        self.spin_interval = 0.025  # Spin every 0.1 seconds
        self.spin_speed = 1

        # Single angle setting
        # Default angle using new shuv/flip system (shuv_angle, flip_angle)
        self.default_angle = (0, 0)  # (shuv_angle, flip_angle) for new sprite system
        self.angle = self.default_angle  # (shuv_angle, flip_angle)
        
        # Scale factor for display - make it smaller for elevated camera view
        self.scale_factor = (max(self.display_width, self.display_height) / 120) * 0.2  # Reduced from 0.3 to 0.2 for more zoom out
        
        # Movement system - unified speed control
        self.move_speed = 30  # Reduced from 20 to 15 for slower movement
        self.move_update_interval = 0.15  # Update every 0.1 seconds
        self.skateboard_x_offset = 500  # Offset 300px to the left
        
        # Floor properties - zoomed out for elevated camera view
        self.floor_height = 300  # Increased from 200 to 300 for more visible floor
        self.floor_offset = 0  # Current scroll offset
        self.floor_texture_width = self.display_width  # Each segment covers full window width
        self.last_floor_update = 0  # Last time floor was updated
        
        # Floor texture system for endless map
        self.floor_texture = None  # Single repeating floor texture
        self._load_floor_texture()
        
        # Rail system
        self.rails = []  # List of active rails
        self.rail_spawn_interval = (3, 6)  # Random spawn interval in seconds
        self.last_rail_spawn = 0  # Last time a rail was spawned
        self.rail_image = None  # Rail image
        self.rail_scale = 0.4  # Scale factor to make rail smaller
        self._load_rail_image()
        
        # Keyboard control setup
        self.hands = ["center", "center"]  # [left_hand_region, right_hand_region]
        
        # Keyboard state tracking
        self.keys_pressed = {
            # Left hand controls (WASD)
            'w': False, 'a': False, 's': False, 'd': False,
            # Right hand controls (IJKL)
            'i': False, 'j': False, 'k': False, 'l': False
        }
        
        # Trick detection variables
        self.current_trick = None
        self.trick_start_time = 0
        self.trick_hold_duration = 0.2
        self.last_hand_combination = ["center", "center"]
        
        # Landing detection variables
        self.landing_detection_enabled = True
        self.landing_success = False
        self.landing_feedback_timer = 0
        self.landing_feedback_duration = 2.0  # Show feedback for 2 seconds
        
        # Catch system variables
        self.catch_required = False  # Whether current trick requires catching
        self.catch_window_start = 0  # When catch window starts
        self.catch_window_duration = 1.0  # How long catch window lasts
        self.catch_success = False  # Whether trick was caught successfully
        self.catch_attempted = False  # Whether player attempted to catch
        self.catch_feedback_timer = 0  # Timer for catch feedback display
        self.catch_feedback_duration = 1.5  # How long to show catch feedback
        self.catch_key_pressed = False  # Whether player is currently holding catch keys
        self.catch_key_released = False  # Whether player has released catch keys
        
        # Death system variables
        self.dead = False  # Whether player is dead
        self.death_timer = 0  # Timer for death effects
        self.death_duration = 0.2  # How long death effects last
        self.perfect_catch_frames = []  # List of perfect catch frame indices
        self.catch_tolerance = 5  # Frames on either side of perfect catch
        
        # Grind system variables
        self.grind_window_duration = 1  # Window to enter grind after trick (increased from 0.5)
        self.grind_window_start_time = 0  # When grind window starts
        self.in_grind_window = False  # Whether we're in the grind window
        self.grinding = False  # Whether we're currently grinding
        self.grind_trick = None  # Current grind trick being performed
        self.grind_start_time = 0  # When grinding started
        self.min_grind_duration = 0.3  # Minimum time to stay in grind.3
        
        # Grind hold mechanic
        self.grind_hold_duration = 0.15  # Time to hold grind trick to enter grind
        self.grind_hold_start_time = 0  # When grind hold started
        self.holding_grind_trick = False  # Whether currently holding a grind trick
        self.pending_grind_trick = None  # Grind trick being held
        
        # Wheels rolling sound management
        self.wheels_rolling_channel = 5
        self.wheels_sound_playing = False
        self.wheels_rolling_sound = None
        self.wheels_rolling_sound_floor = None
        
        # Trick spin speed controls
        self.shuv_spin_speed = 1      # Speed for shuv-it rotations (BS/FS Shuv-It)
        self.flip_spin_speed = 1.5     # Speed for flip rotations (Kickflip, Heelflip) - increased by 1.7x
        self.varial_spin_speed = 1.5    # Speed for varial rotations (Varial Kickflip, Varial Heelflip, Hardflip, Inward Heelflip)
        
        
        # Load sound effects
        self.sounds = {}
        self._load_sounds()
        
        # Load arrow key icons
        self.arrow_icons = {}
        self._load_arrow_icons()
        
        # Performance optimization: cache current time to avoid repeated calculations
        self._current_time = 0
        self._last_time_update = 0
        self._time_update_interval = 0.016  # Update time every ~16ms (60fps)
        
        # Performance optimization: cache scaled surfaces
        self._scaled_surfaces = {}
        self._surface_cache_max_size = 100  # Increased cache size for better performance
        
        # Automatic cache clearing
        self._last_cache_clear = 0  # Last time cache was cleared
        self._cache_clear_interval = 30  # Clear cache every 30 seconds
        
        # Performance optimization: pre-calculate common values
        self._display_center_x = self.display_width // 2
        self._display_center_y = self.display_height // 2
        self._skateboard_center_x = self._display_center_x - self.skateboard_x_offset
        
        # Performance optimization: pre-calculate key mappings
        self._key_mappings = {
            pygame.K_w: 'w', pygame.K_a: 'a', pygame.K_s: 's', pygame.K_d: 'd',
            pygame.K_i: 'i', pygame.K_j: 'j', pygame.K_k: 'k', pygame.K_l: 'l'
        }
        
        # Floor texture is loaded in _load_floor_texture()
        
        
    def _load_sprite_map(self):
        """Load the sprite map image"""
        try:
            self.sprite_map = pygame.image.load("skateboard_sprite_map_optimized.png").convert_alpha()
            print("Loaded sprite map successfully")
        except pygame.error as e:
            raise Exception(f"Failed to load sprite map: {e}")
    
    def _load_metadata(self):
        """Load sprite metadata from optimized file"""
        try:
            with open("sprite_map_metadata_optimized.txt", 'r') as f:
                content = f.read()
                
                # Parse sprite positions
                for line in content.split('\n'):
                    if " -> " in line and not line.startswith("Sprite positions"):
                        parts = line.split(" -> ")
                        if len(parts) == 2:
                            angle_key = parts[0].strip()
                            position = parts[1].strip()
                            
                            if "," in position:
                                try:
                                    row, col = position.split(",")
                                    self.sprite_metadata[angle_key] = (int(row), int(col))
                                except ValueError:
                                    continue
            
            print(f"Loaded optimized metadata: {len(self.sprite_metadata)} sprites")
            
        except FileNotFoundError:
            print("Warning: Could not load optimized sprite metadata, falling back to original")
            # Fallback to original metadata
            with open("sprite_map_metadata.txt", 'r') as f:
                content = f.read()
                
                # Extract grid size
                for line in content.split('\n'):
                    if line.startswith("Grid size:"):
                        size_part = line.split(":")[1].strip().split("x")[0]
                        self.grid_size = int(size_part)
                        break
                
                # Parse sprite positions
                for line in content.split('\n'):
                    if " -> " in line and not line.startswith("Sprite positions"):
                        parts = line.split(" -> ")
                        if len(parts) == 2:
                            angle_key = parts[0].strip()
                            position = parts[1].strip()
                            
                            if "," in position and not angle_key.startswith("Sprite positions"):
                                try:
                                    row, col = position.split(",")
                                    self.sprite_metadata[angle_key] = (int(row), int(col))
                                except ValueError:
                                    continue
            
            print(f"Loaded fallback metadata: {len(self.sprite_metadata)} sprites")
            
        except Exception as e:
            raise Exception(f"Failed to load metadata: {e}")
    
    def _load_animations(self):
        """Load animation sprite maps and metadata"""
        try:
            # Load animation index
            with open("animations/index.txt", 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if " -> " in line and not line.startswith("Available"):
                        parts = line.split(" -> ")
                        if len(parts) == 2:
                            trick_name = parts[0].strip()
                            filename = parts[1].strip()
                            
                            # Load animation sprite map
                            animation_path = f"animations/{filename}"
                            if os.path.exists(animation_path):
                                self.animation_maps[trick_name] = pygame.image.load(animation_path).convert_alpha()
                                
                                # Load animation metadata
                                metadata_path = f"animations/{filename.replace('.png', '_metadata.txt')}"
                                if os.path.exists(metadata_path):
                                    with open(metadata_path, 'r') as mf:
                                        metadata = {}
                                        for mline in mf:
                                            if "Frames:" in mline:
                                                total_frames = int(mline.split(":")[1].strip())
                                                # For shuv and flip tricks, halve the frame count since we use every other frame
                                                shuv_tricks = ["BS-Shuv-It", "FS-Shuv-It", "Nollie BS-Shuv-It", "Nollie FS-Shuv-It"]
                                                flip_tricks = ["Kickflip", "Heelflip", "Nollie Kickflip", "Nollie Heelflip"]
                                                if trick_name in shuv_tricks or trick_name in flip_tricks:
                                                    metadata['frames'] = (total_frames + 1) // 2  # Round up division
                                                else:
                                                    metadata['frames'] = total_frames
                                            elif "Frames per row:" in mline:
                                                metadata['frames_per_row'] = int(mline.split(":")[1].strip())
                                        
                                        self.animation_metadata[trick_name] = metadata
            
            print(f"Loaded {len(self.animation_maps)} animation sprite maps")
            
        except Exception as e:
            print(f"Warning: Could not load animations: {e}")
            self.animation_maps = {}
            self.animation_metadata = {}
    

    def _load_new_sprite_map(self):
        """Load the new shuv/flip sprite map"""
        try:
            # Load the new sprite map
            self.new_sprite_map = pygame.image.load("generated_sprites/shuv_flip_sprite_map.png").convert_alpha()
            self.new_sprite_size = 48
            self.new_grid_width = 24
            self.new_grid_height = 24
            
            # Load new metadata
            self.new_sprite_metadata = {}
            with open("generated_sprites/shuv_flip_sprite_map_metadata.txt", 'r') as f:
                for line in f:
                    if " -> " in line and not line.startswith("Sprite positions"):
                        parts = line.split(" -> ")
                        if len(parts) == 2:
                            angle_key = parts[0].strip()
                            position = parts[1].strip()
                            
                            if "," in position and not angle_key.startswith("Sprite positions"):
                                try:
                                    row, col = position.split(",")
                                    self.new_sprite_metadata[angle_key] = (int(row), int(col))
                                except ValueError:
                                    continue
            
            print(f"Loaded new sprite map: {self.new_grid_width}x{self.new_grid_height}")
            print(f"Loaded {len(self.new_sprite_metadata)} sprite positions")
            
        except Exception as e:
            print(f"Error loading new sprite map: {e}")
            self.new_sprite_map = None
    
    def get_new_sprite(self, shuv_angle: int, flip_angle: int) -> pygame.Surface:
        """Get sprite from new sprite map using shuv and flip angles"""
        if not self.new_sprite_map:
            return None
            
        # Create angle key
        angle_key = f"{shuv_angle}_{flip_angle}"
        
        if angle_key in self.new_sprite_metadata:
            row, col = self.new_sprite_metadata[angle_key]
            x = col * self.new_sprite_size
            y = row * self.new_sprite_size
            
            # Extract sprite
            sprite_rect = pygame.Rect(x, y, self.new_sprite_size, self.new_sprite_size)
            return self.new_sprite_map.subsurface(sprite_rect)
        
        return None

    def _load_sounds(self):
        """Load sound effects"""
        try:
            # Load success sound and modify its pitch/speed
            success_sound = pygame.mixer.Sound("SFX/Success.mp3")
            # Increase pitch and speed by 1.6x using scipy resampling
            try:
                import numpy as np
                from scipy import signal
                success_array = pygame.sndarray.array(success_sound)
                # Resample to increase speed/pitch by 1.6x
                new_length = int(len(success_array) / 3.5)
                success_array_fast = signal.resample(success_array, new_length).astype(success_array.dtype)
                success_sound_fast = pygame.sndarray.make_sound(success_array_fast)
            except ImportError:
                # Fallback if scipy not available
                print("Warning: scipy not available, using original success sound")
                success_sound_fast = success_sound
            
            # Load wheels rolling sound with different volumes/pitches
            wheels_original = pygame.mixer.Sound("SFX/WheelsRolling.wav")
            
            # Create floor version (lower volume, lower pitch)
            try:
                import numpy as np
                from scipy import signal
                wheels_array = pygame.sndarray.array(wheels_original)
                # Lower pitch by 0.7x and reduce volume
                new_length = int(len(wheels_array) / 0.7)
                wheels_array_floor = signal.resample(wheels_array, new_length).astype(wheels_array.dtype)
                wheels_floor = pygame.sndarray.make_sound(wheels_array_floor)
                wheels_floor.set_volume(0.15)  # Much quieter floor sound
            except ImportError:
                wheels_floor = wheels_original
                wheels_floor.set_volume(0.15)
            
            # Air version (normal pitch, lower volume)
            wheels_air = wheels_original
            wheels_air.set_volume(0.5)  # Lower volume for air
            
            self.wheels_rolling_sound_floor = wheels_floor
            self.wheels_rolling_sound = wheels_air
            
            self.sounds = {
                'start_trick': pygame.mixer.Sound("SFX/StartTrick.wav"),
                'cancel_trick': pygame.mixer.Sound("SFX/CancelTrick.wav"),
                'foot1': pygame.mixer.Sound("SFX/Foot1.wav"),
                'foot2': pygame.mixer.Sound("SFX/Foot2.wav"),
                'WheelsRolling.wav': wheels_air,
                'success': success_sound_fast,
                'fail': pygame.mixer.Sound("SFX/Fail.mp3"),
                'death': pygame.mixer.Sound("SFX/Death.mp3")
            }
            print("Loaded sound effects successfully")
        except pygame.error as e:
            print(f"Warning: Could not load sound effects: {e}")
            # Create empty sound objects to prevent errors
            self.wheels_rolling_sound_floor = None
            self.wheels_rolling_sound = None
            self.sounds = {
                'start_trick': None,
                'cancel_trick': None,
                'foot1': None,
                'foot2': None,
                'WheelsRolling.wav': None,
                'success': None,
                'fail': None,
                'death': None
            }
    
    def _load_arrow_icons(self):
        """Load arrow key icons (both solid and outline versions)"""
        try:
            # Load solid (always visible) icons
            self.arrow_icons_solid = {
                'up': pygame.image.load("icons/keyboard_arrow_up.png").convert_alpha(),
                'down': pygame.image.load("icons/keyboard_arrow_down.png").convert_alpha(),
                'left': pygame.image.load("icons/keyboard_arrow_left.png").convert_alpha(),
                'right': pygame.image.load("icons/keyboard_arrow_right.png").convert_alpha()
            }
            # Load outline (pressed state) icons
            self.arrow_icons_outline = {
                'up': pygame.image.load("icons/keyboard_arrow_up_outline.png").convert_alpha(),
                'down': pygame.image.load("icons/keyboard_arrow_down_outline.png").convert_alpha(),
                'left': pygame.image.load("icons/keyboard_arrow_left_outline.png").convert_alpha(),
                'right': pygame.image.load("icons/keyboard_arrow_right_outline.png").convert_alpha()
            }
            print("Loaded arrow key icons successfully")
        except pygame.error as e:
            print(f"Warning: Could not load arrow key icons: {e}")
            # Create empty icon objects to prevent errors
            self.arrow_icons_solid = {
                'up': None,
                'down': None,
                'left': None,
                'right': None
            }
            self.arrow_icons_outline = {
                'up': None,
                'down': None,
                'left': None,
                'right': None
            }
    
    def _load_grind_images(self):
        """Load grind images from the grinds folder"""
        try:
            loaded_count = 0
            for grind_name, grind_data in self.grind_positions.items():
                image_file = grind_data["image"]
                image_path = f"grinds/{image_file}"
                
                if os.path.exists(image_path):
                    self.grind_images[grind_name] = pygame.image.load(image_path).convert_alpha()
                    loaded_count += 1
                    print(f"✓ Loaded grind image: {grind_name} -> {image_file}")
                else:
                    print(f"✗ Missing grind image: {image_path}")
                    self.grind_images[grind_name] = None
            
            print(f"Grind images loaded: {loaded_count}/{len(self.grind_positions)} successfully")
            
        except Exception as e:
            print(f"Error loading grind images: {e}")
            # Create empty grind images dict to prevent errors
            self.grind_images = {}
    
    def _update_time(self):
        """Optimized time management - update time only when needed"""
        current_ticks = pygame.time.get_ticks()
        if current_ticks - self._last_time_update >= self._time_update_interval * 1000:
            self._current_time = current_ticks / 1000.0
            self._last_time_update = current_ticks
    
    def _get_cached_surface(self, surface, width, height, scale_key):
        """Cache scaled surfaces to avoid repeated transformations"""
        if scale_key in self._scaled_surfaces:
            return self._scaled_surfaces[scale_key]
        
        # Limit cache size
        if len(self._scaled_surfaces) >= self._surface_cache_max_size:
            # Remove oldest entry (simple FIFO)
            oldest_key = next(iter(self._scaled_surfaces))
            del self._scaled_surfaces[oldest_key]
        
        scaled_surface = pygame.transform.scale(surface, (width, height))
        self._scaled_surfaces[scale_key] = scaled_surface
        return scaled_surface
    
    def _clear_surface_cache(self):
        """Clear the surface cache to free memory"""
        cache_size_before = len(self._scaled_surfaces)
        self._scaled_surfaces.clear()
        self._last_cache_clear = self._current_time
        print(f"Surface cache cleared ({cache_size_before} entries freed)")
    
    def _check_auto_cache_clear(self):
        """Check if cache should be automatically cleared based on time interval"""
        if self._current_time - self._last_cache_clear >= self._cache_clear_interval:
            self._clear_surface_cache()
    
    def _load_floor_texture(self):
        """Load a random floor texture from the levels folder"""
        try:
            levels_folder = "levels"
            if not os.path.exists(levels_folder):
                print(f"Warning: {levels_folder} folder not found. Creating fallback texture.")
                self._create_fallback_floor_texture()
                return
            
            # Get all image files from levels folder
            image_extensions = ['.png', '.jpg', '.jpeg', '.bmp']
            level_files = []
            
            for file in os.listdir(levels_folder):
                if any(file.lower().endswith(ext) for ext in image_extensions):
                    level_files.append(os.path.join(levels_folder, file))
            
            if not level_files:
                print(f"Warning: No image files found in {levels_folder} folder. Creating fallback texture.")
                self._create_fallback_floor_texture()
                return
            
            # Pick a random texture
            selected_texture_path = random.choice(level_files)
            print(f"Selected random floor texture: {selected_texture_path}")
            
            # Load the selected texture
            self.floor_texture = pygame.image.load(selected_texture_path).convert()
            print(f"Loaded floor texture: {self.floor_texture.get_width()}x{self.floor_texture.get_height()}")
                
        except Exception as e:
            print(f"Error loading floor texture: {e}")
            self._create_fallback_floor_texture()
    
    def _create_fallback_floor_texture(self):
        """Create a simple fallback floor texture"""
        self.floor_texture = pygame.Surface((200, 200))  # Small repeating texture
        self.floor_texture.fill(self.colors['asphalt_base'])
        
        # Add some simple variation
        for i in range(0, 200, 50):
            for j in range(0, 200, 50):
                variation = random.randint(-10, 10)
                base_color = self.colors['asphalt_base']
                color = (
                    max(0, min(255, base_color[0] + variation)),
                    max(0, min(255, base_color[1] + variation)),
                    max(0, min(255, base_color[2] + variation))
                )
                pygame.draw.rect(self.floor_texture, color, (i, j, 50, 50), 0)
        
        print("Created fallback floor texture")
    
    def _load_rail_image(self):
        """Load and scale the rail image"""
        try:
            original_image = pygame.image.load("objects/Rail.png").convert_alpha()
            # Scale down the rail image
            original_width = original_image.get_width()
            original_height = original_image.get_height()
            new_width = int(original_width * self.rail_scale)
            new_height = int(original_height * self.rail_scale)
            self.rail_image = pygame.transform.scale(original_image, (new_width, new_height))
            print(f"Loaded and scaled rail image: {original_width}x{original_height} -> {new_width}x{new_height}")
        except pygame.error as e:
            print(f"Warning: Could not load rail image: {e}")
            self.rail_image = None
    
    def _update_floor_offset(self):
        """Update the floor scroll offset for endless scrolling"""
        current_time = self._current_time
        
        # Only update when floor is updated to match movement speed
        if current_time - self.last_floor_update >= self.move_update_interval:
            # Move floor offset to the left
            self.floor_offset -= self.move_speed
            
            # Reset offset when it goes beyond scaled texture width to create seamless loop
            if self.floor_texture:
                texture_width = self.floor_texture.get_width()
                texture_height = self.floor_texture.get_height()
                scale_factor = (self.display_height / 4) / texture_height
                scaled_width = int(texture_width * scale_factor)
                
                if self.floor_offset <= -scaled_width:
                    self.floor_offset += scaled_width
    
    def _render_floor(self):
        """Render the endless scrolling floor using repeating texture"""
        if not self.floor_texture:
            return
            
        # Update floor offset
        self._update_floor_offset()
        
        # Get texture dimensions
        texture_width = self.floor_texture.get_width()
        texture_height = self.floor_texture.get_height()
        
        # Scale texture to one-quarter frame height
        scale_factor = (self.display_height / 4) / texture_height
        scaled_width = int(texture_width * scale_factor)
        scaled_height = self.display_height // 4
        
        # Scale the texture using cached surfaces
        scale_key = f"floor_{scaled_width}_{scaled_height}"
        scaled_texture = self._get_cached_surface(self.floor_texture, scaled_width, scaled_height, scale_key)
        
        # Calculate how many times we need to repeat the scaled texture horizontally
        tiles_needed = (self.display_width // scaled_width) + 2  # +2 for seamless scrolling
        
        # Draw repeating scaled texture tiles with 4 stacked vertically
        for i in range(tiles_needed):
            x = self.floor_offset + (i * scaled_width)
            
            # Only draw if tile is visible on screen
            if x + scaled_width > 0 and x < self.display_width:
                # Draw all 4 textures stacked vertically
                for j in range(4):
                    y = j * scaled_height
                    self.display.blit(scaled_texture, (x, y))
    
    def get_sprite_position(self, shuv_angle: float, flip_angle: float) -> Optional[Tuple[int, int, int, int]]:
        """Get sprite position from shuv and flip angles using new sprite system"""
        # Normalize angles to 0-359 range
        shuv_angle = shuv_angle % 360
        flip_angle = flip_angle % 360
        
        # Round to nearest 15 degrees
        shuv_angle = round(shuv_angle / 15) * 15
        flip_angle = round(flip_angle / 15) * 15
        
        # Create angle key for new sprite system
        angle_key = f"{int(shuv_angle)}_{int(flip_angle)}"
        
        # Use new sprite map if available
        if hasattr(self, 'new_sprite_metadata') and angle_key in self.new_sprite_metadata:
            row, col = self.new_sprite_metadata[angle_key]
            x = col * 128  # New sprite size is 128x128
            y = row * 128
            return (x, y, 128, 128)
        
        # Fallback to old system for backward compatibility
        # Convert to old format for existing sprites
        x_angle = flip_angle  # Flip becomes X rotation
        y_angle = 90          # Keep Y at 90 for upright orientation
        z_angle = shuv_angle  # Shuv becomes Z rotation
        
        angle_key_old = f"{x_angle}.0_{y_angle}.0_{z_angle}.0"
        if angle_key_old in self.sprite_metadata:
            row, col = self.sprite_metadata[angle_key_old]
            x = col * self.sprite_size
            y = row * self.sprite_size
            return (x, y, self.sprite_size, self.sprite_size)
        
        return None
    
    def set_angle(self, shuv_angle: float, flip_angle: float):
        """Set the skateboard angle using new shuv/flip system"""
        # Round to nearest 15 degrees
        shuv_angle = round(shuv_angle / 15) * 15
        flip_angle = round(flip_angle / 15) * 15
        
        self.angle = (shuv_angle, flip_angle)
    
    def _update_keyboard_controls(self):
        """Optimized hand region update based on keyboard input"""
        # Reset to center
        self.hands = ["center", "center"]
        
        # Optimized key mapping for left hand (WASD)
        left_keys = [self.keys_pressed['w'], self.keys_pressed['a'], 
                    self.keys_pressed['s'], self.keys_pressed['d']]
        
        # Optimized key mapping for right hand (IJKL)
        right_keys = [self.keys_pressed['i'], self.keys_pressed['j'], 
                     self.keys_pressed['k'], self.keys_pressed['l']]
        
        # Left hand logic (WASD)
        self.hands[0] = self._get_hand_direction(left_keys)
        
        # Right hand logic (IJKL) 
        self.hands[1] = self._get_hand_direction(right_keys)
    
    def _get_hand_direction(self, keys):
        """Helper method to determine hand direction from key states"""
        # keys = [up, left, down, right]
        if keys[0] and (keys[1] or keys[3]):  # W + (A or D)
            return "up"
        elif keys[0]:  # W
            return "up"
        elif keys[2] and keys[1]:  # S + A
            return "left"
        elif keys[2] and keys[3]:  # S + D
            return "down"
        elif keys[2]:  # S
            return "down"
        elif keys[1]:  # A
            return "left"
        elif keys[3]:  # D
            return "right"
        else:
            return "center"
    
    def _check_trick_combination(self):
        """Check if current hand combination matches any trick in trick_map"""
        # Only check if hands are not both center
        if self.hands == ["center", "center"]:
            return None
        
        # Check each trick in the trick map
        for trick_name, required_hands in self.trick_map.items():
            if self.hands == required_hands:
                return trick_name
        
        return None
    
    def _update_trick_detection(self, current_time):
        """Update trick detection based on current hand combination and timing"""
        # Skip trick detection if we're grinding
        if self.grinding:
            return
            
        current_combination = self.hands.copy()
        
        # Check if we have any non-center combination (any trick attempt)
        has_combination = current_combination != ["center", "center"]
        
        # If we start a new combination (any non-center combo)
        if has_combination and current_combination != self.last_hand_combination:
            self.trick_start_time = current_time
            print(f"Trick attempt started: {current_combination}")
            # Play start trick sound
            # if self.sounds['start_trick']:
            #     self.sounds['start_trick'].play()
        
        # If we're still holding some combination
        elif has_combination and self.trick_start_time > 0:
            # Check if we've held any combination long enough
            if current_time - self.trick_start_time >= self.trick_hold_duration:
                # Check what trick the current combination matches
                detected_trick = self._check_trick_combination()
                if detected_trick:
                    self.do_trick(detected_trick, current_combination)
                else:
                    print(f"Invalid combination held: {current_combination}")
                # Reset trick detection
                self.trick_start_time = 0
        
        # If we're no longer holding any combination
        elif not has_combination and self.trick_start_time > 0:
            # Check what trick was being attempted based on last combination
            attempted_trick = None
            for trick_name, required_hands in self.trick_map.items():
                if self.last_hand_combination == required_hands:
                    attempted_trick = trick_name
                    break
            
            if attempted_trick:
                print(f"Trick attempt cancelled: {attempted_trick}")
            else:
                print(f"Trick attempt cancelled: {self.last_hand_combination}")
            # Play cancel trick sound
            if self.sounds['cancel_trick']:
                self.sounds['cancel_trick'].play()
            self.trick_start_time = 0
        
        # Check for foot movement sounds
        self._check_foot_movement_sounds(current_combination)
        
        # Update last combination
        self.last_hand_combination = current_combination
    
    def _check_foot_movement_sounds(self, current_combination):
        """Check for foot movement and play appropriate sounds"""
        # Check if left foot (hand) moved
        if current_combination[0] != self.last_hand_combination[0]:
            if self.sounds['foot1']:
                self.sounds['foot1'].play()
        
        # Check if right foot (hand) moved
        if current_combination[1] != self.last_hand_combination[1]:
            if self.sounds['foot2']:
                self.sounds['foot2'].play()
    
    def _is_landing_frame(self, animation_name, frame_index):
        """Check if the current frame is a landing frame (last 2 frames or first 2 frames if looping)"""
        if not self.landing_detection_enabled or animation_name not in self.animation_metadata:
            return False
        
        # Get total frames from metadata
        metadata = self.animation_metadata[animation_name]
        total_frames = metadata['frames']
        
        # Check if this animation should loop
        should_loop = self.animation_loops.get(animation_name, True)  # Default to looping
        
        # Determine if we're in a landing window
        is_landing_frame = False
        
        # Special tricks that can land halfway through
        halfway_landing_tricks = [
            "Varial Kickflip", 
            "Varial Heelflip", 
            "Hardflip", 
            "Inward Heelflip"
        ]
        
        if should_loop:
            # For looping animations, check last 2 frames OR first 3 frames
            # Last 2 frames: (total_frames - 2) and (total_frames - 1)
            # First 3 frames: 0, 1, and 2
            if (frame_index >= total_frames - 2) or (frame_index <= 2):
                is_landing_frame = True
            
            # For special tricks, also allow landing halfway through
            if animation_name in halfway_landing_tricks:
                halfway_point = total_frames // 2
                # Allow landing 1 frame before and 1 frame after halfway point
                if abs(frame_index - halfway_point) <= 1:
                    is_landing_frame = True
        else:
            # For non-looping animations, check last 2 frames OR first 3 frames
            if (frame_index >= total_frames - 2) or (frame_index <= 2):
                is_landing_frame = True
            
            # For special non-looping tricks, also allow landing halfway through
            if animation_name in halfway_landing_tricks:
                halfway_point = total_frames // 2
                # Allow landing 1 frame before and 1 frame after halfway point
                if abs(frame_index - halfway_point) <= 1:
                    is_landing_frame = True
        
        return is_landing_frame
    
    def _get_trick_spin_speed(self, trick_name):
        """Get the appropriate spin speed for a trick based on its type"""
        # Shuv-it tricks
        shuv_tricks = ["BS-Shuv-It", "FS-Shuv-It", "Nollie BS-Shuv-It", "Nollie FS-Shuv-It"]
        
        # Flip tricks
        flip_tricks = ["Kickflip", "Heelflip", "Nollie Kickflip", "Nollie Heelflip"]
        
        # Varial tricks (combinations of flip + shuv)
        varial_tricks = ["Varial Kickflip", "Varial Heelflip", "Hardflip", "Inward Heelflip"]
        
        if trick_name in shuv_tricks:
            return self.shuv_spin_speed
        elif trick_name in flip_tricks:
            return self.flip_spin_speed
        elif trick_name in varial_tricks:
            return self.varial_spin_speed
        else:
            # Default speed for Ollie, Nollie, etc.
            return 1.0
    
    def do_trick(self, trick_name, foot_combination):
        if self.airborne:
            return
        """Execute the completed trick"""
        # Play pop sound
        pop_sounds = [f"SFX/Pop_{i}.wav" for i in range(1, 6)]
        pop_sound_file = random.choice(pop_sounds)
        try:
            pop_sound = pygame.mixer.Sound(pop_sound_file)
            pop_sound.play()
        except Exception as e:
            print(f"Could not play pop sound: {e}")
        
        # Play random catch sound with random pitch (1.7x to 1.8x)
        catch_sounds = [f"SFX/Catch_{i}.mp3" for i in range(1, 4)]
        catch_sound_file = random.choice(catch_sounds)
        try:
            catch_sound_original = pygame.mixer.Sound(catch_sound_file)
            try:
                import numpy as np
                from scipy import signal
                catch_array = pygame.sndarray.array(catch_sound_original)
                # Random pitch between 1.7x to 1.8x
                random_pitch = random.uniform(1.7, 1.8)
                new_length = int(len(catch_array) / random_pitch)
                catch_array_fast = signal.resample(catch_array, new_length).astype(catch_array.dtype)
                catch_sound = pygame.sndarray.make_sound(catch_array_fast)
            except ImportError:
                # Fallback if scipy not available
                catch_sound = catch_sound_original
            catch_sound.play()
        except Exception as e:
            print(f"Could not play catch sound on pop: {e}")
        
        # Start animation for the trick
        if trick_name in self.animation_maps:
            self.current_animation = trick_name
            self.animation_frame = 0
            self.animation_timer = 0
            self.animation_completed = False  # Reset completion flag
            print(f"Starting animation: {trick_name}")
        
        # Set airborne state and store trick info
        self.airborne = True
        self.current_trick_name = trick_name
        self.original_flip_trick = trick_name  # Store original flip trick name for grind display
        self.trick_start_angle = self.angle
        self.landing_angle = self.angle
        
        # Reset landing detection feedback
        self.landing_success = False
        self.landing_feedback_timer = 0
        
        # Set up catch system for tricks that require catching
        self._setup_catch_system(trick_name)
        
        # Reset wheels sound state
        self.wheels_sound_playing = False
    
    def _setup_catch_system(self, trick_name):
        """Set up catch system for tricks that require catching"""
        # ALL tricks now require catching by releasing the trick keys
        self.catch_required = True
        self.catch_success = False
        self.catch_attempted = False
        self.catch_feedback_timer = 0
        self.dead = False
        self.death_timer = 0
        
        # Define perfect catch frames for each trick (middle of animation)
        self.perfect_catch_frames = self._get_perfect_catch_frames(trick_name)
        
        # Start catch window after a short delay to allow animation to start
        self.catch_window_start = self._current_time + 0.2
    
    def _get_perfect_catch_frames(self, trick_name):
        """Get the perfect catch frames for a specific trick"""
        if trick_name not in self.animation_metadata:
            return []
        
        metadata = self.animation_metadata[trick_name]
        total_frames = metadata['frames']
        
        # Perfect catch frames are the last 2 frames and first 2 frames
        perfect_frames = []
        
        # Add first 2 frames (0, 1)
        for i in range(min(5, total_frames)):
            perfect_frames.append(i)
        
        # Add last 2 frames
        for i in range(max(0, total_frames - 4), total_frames):
            if i not in perfect_frames:  # Avoid duplicates if animation is very short
                perfect_frames.append(i)
        
        print(f"Perfect catch frames for {trick_name}: {perfect_frames} (total frames: {total_frames})")
        return perfect_frames
    
    def _check_catch_input(self):
        """Check if player is attempting to catch the trick with perfect timing"""
        if not self.catch_required or not self.airborne or self.catch_attempted or self.dead:
            return
        
        current_time = self._current_time
        
        # Check if we're in the catch window
        if current_time < self.catch_window_start:
            return
        
        if current_time > self.catch_window_start + self.catch_window_duration:
            # Catch window expired - death
            print("Catch window expired - DEATH!")
            self._trigger_death()
            return
        
        # Check if player released the trick keys (both hands center = catch attempt)
        if self.hands == ["center", "center"] and not self.catch_attempted:
            # Player released trick keys - attempt catch
            self.catch_attempted = True
            self.catch_feedback_timer = current_time
            
            # Check if current frame is a perfect catch frame
            if self.animation_frame in self.perfect_catch_frames:
                self.catch_success = True
                
                # Stop animation immediately when caught
                if self.current_animation:
                    self.animation_completed = True
                    print(f"Animation stopped after catch: {self.current_animation}")
                
                # Play catch sound
                catch_sounds = [f"SFX/Catch_{i}.mp3" for i in range(1, 4)]
                catch_sound_file = random.choice(catch_sounds)
                try:
                    catch_sound_original = pygame.mixer.Sound(catch_sound_file)
                    try:
                        import numpy as np
                        from scipy import signal
                        catch_array = pygame.sndarray.array(catch_sound_original)
                        # Increase pitch by 1.2x for catch sound
                        new_length = int(len(catch_array) / 1.2)
                        catch_array_fast = signal.resample(catch_array, new_length).astype(catch_array.dtype)
                        catch_sound = pygame.sndarray.make_sound(catch_array_fast)
                    except ImportError:
                        catch_sound = catch_sound_original
                    catch_sound.play()
                except Exception as e:
                    print(f"Could not play catch sound: {e}")
            else:
                # Imperfect timing - death
                self._trigger_death()
    
    def _trigger_death(self):
        """Trigger death sequence"""
        self.dead = True
        self.catch_success = False
        self.catch_attempted = True
        self.death_timer = self._current_time
        
        # Stop movement
        self.move_speed = 0
        
        # Play death sound
        if self.sounds['death']:
            self.sounds['death'].play()
        
        print("DEATH TRIGGERED - Movement stopped")
    
    def _update_airborne_state(self):
        """Update the board's airborne state and animation"""
        # No constant wheel sound when not airborne
        if not self.airborne:
            # Stop air wheels sound if playing
            if self.wheels_sound_playing and self.wheels_rolling_sound:
                pygame.mixer.Channel(self.wheels_rolling_channel).stop()
                self.wheels_sound_playing = False
            return

        # Play air wheels sound while airborne (normal pitch, lower volume)
        if self.wheels_rolling_sound and not self.wheels_sound_playing:
            pygame.mixer.Channel(self.wheels_rolling_channel).play(self.wheels_rolling_sound, loops=-1)
            self.wheels_sound_playing = True

        # Update animation if we have one
        if self.current_animation:
            self._update_animation()

        # Check for catch input
        self._check_catch_input()

        # Check if player is dead
        if self.dead:
            # Handle death sequence
            current_time = self._current_time
            if current_time - self.death_timer >= self.death_duration:
                # Death sequence complete - land the board
                print("Death sequence complete - landing")
                self._land_board()
                return
            # Continue showing death effects during death duration
            return

        # Check if trick was caught and handle landing/grinding decision
        if self.catch_required and self.catch_attempted:
            if self.catch_success:
                # Trick was caught successfully - decide whether to land or grind
                if self._check_rail_collision():
                    # Near rail - start grind window
                    if not self.in_grind_window and not self.grinding:
                        current_time = self._current_time
                        self.grind_window_start_time = current_time
                        self.in_grind_window = True
                else:
                    # No rail nearby - land immediately
                    self._land_board()
                    return
            else:
                # Trick was not caught - land immediately with fail sound
                self._land_board()
                return

        # Handle key release logic based on current state
        if self.hands[0] == "center" and self.hands[1] == "center":
            # If we're in grind window, check if time expired
            if self.in_grind_window:
                current_time = self._current_time
                if current_time - self.grind_window_start_time >= self.grind_window_duration:
                    # Grind window expired, land the board
                    self._land_board()
                # Don't process other key release logic during grind window
            elif not self.grinding:
                # Not in grind window and not grinding - this is normal catch/landing logic
                # Stop the animation immediately
                if self.current_animation:
                    self.animation_completed = True  # Stop animation
                    print(f"Animation stopped for {self.current_animation}")
                
                # All tricks now require catching - this section is handled by catch system
        
        # If we're in grind window, check for grind trick input
        if self.in_grind_window:
            self._check_grind_trick_input()
        
        # If we're grinding, check for grind exit
        if self.grinding:
            self._update_grinding_state()
    
    
    def _check_grind_trick_input(self):
        """Check if current hand combination matches any grind trick"""
        # Only check if hands are not both center
        if self.hands == ["center", "center"]:
            # If we were holding a grind trick, stop holding it
            if self.holding_grind_trick:
                self.holding_grind_trick = False
                self.pending_grind_trick = None
            return
        
        # Check if we're still in the grind window
        current_time = self._current_time
        if current_time - self.grind_window_start_time >= self.grind_window_duration:
            # Grind window expired
            return
        
        # Check each grind trick in the grind trick map
        for grind_name, required_hands in self.grind_trick_map.items():
            if self.hands == required_hands:
                # If this is a new grind trick or we're not holding any
                if not self.holding_grind_trick or self.pending_grind_trick != grind_name:
                    self.holding_grind_trick = True
                    self.pending_grind_trick = grind_name
                    self.grind_hold_start_time = self._current_time
                
                # Check if we've held it long enough
                current_time = self._current_time
                hold_duration = current_time - self.grind_hold_start_time
                
                if hold_duration >= self.grind_hold_duration:
                    print(f"Grind hold completed for: {grind_name} (held for {hold_duration:.2f}s)")
                    self._start_grind(grind_name)
                    self.holding_grind_trick = False
                    self.pending_grind_trick = None
                
                break
    
    def _start_grind(self, grind_name):
        """Start a grind trick"""
        # Check if we're near a rail
        if not self._check_rail_collision():
            return
        
        
        # Set grind state
        self.grinding = True
        self.grind_trick = grind_name
        self.in_grind_window = False
        self.grind_start_time = self._current_time
        
        # Clear current animation when grinding
        self.current_animation = None
        self.animation_frame = 0
        self.animation_completed = False
        
        # Store grind offset for visual positioning
        if grind_name in self.grind_positions:
            grind_pos = self.grind_positions[grind_name]
            self.grind_offset = grind_pos["offset"]
        
        # Play grind sound
        try:
            grind_sound = pygame.mixer.Sound("SFX/Rail.wav")
            pygame.mixer.Channel(6).play(grind_sound, loops=-1)
        except Exception as e:
            print(f"Could not play grind sound: {e}")
    
    def _check_rail_collision(self):
        """Check if the skateboard is near a rail for grinding"""
        # Get skateboard position (matches the actual rendering position)
        skateboard_x = self._skateboard_center_x  # Use pre-calculated center
        skateboard_y = self._display_center_y
        
        for rail in self.rails:
            # Check if skateboard is close to rail (within 100 pixels vertically)
            distance_y = abs(skateboard_y - rail['y'])
            
            # Check if skateboard is within collision range of the rail
            # Rail extends from rail['x'] to rail['x'] + rail['width'] * 6 (stretched)
            rail_start_x = rail['x']
            rail_end_x = rail['x'] + rail['width'] * 6  # Account for 6x stretch (fixed inconsistency)
            
            # Check if skateboard is horizontally within rail bounds and vertically close enough
            # Add some buffer to make collision detection more forgiving
            buffer = 80  # Increased buffer from 50 to 80 pixels
            if (rail_start_x - buffer <= skateboard_x <= rail_end_x + buffer) and distance_y < 120:
                print(f"Rail collision detected: skateboard_x={skateboard_x}, rail_x={rail_start_x}-{rail_end_x}, distance_y={distance_y}")
                return True
        
        return False
    
    def _check_rail_end(self):
        """Check if the skateboard has reached the end of the current rail"""
        # Get skateboard position
        skateboard_x = self._skateboard_center_x
        skateboard_y = self._display_center_y
        
        for rail in self.rails:
            # Check if skateboard is currently on this rail
            rail_start_x = rail['x']
            rail_end_x = rail['x'] + rail['width'] * 6  # Account for 6x stretch (consistent with collision)
            distance_y = abs(skateboard_y - rail['y'])
            
            # If we're on this rail (horizontally within bounds and vertically close)
            if (rail_start_x <= skateboard_x <= rail_end_x) and distance_y < 100:
                # Check if we're at or past the end of the rail
                if skateboard_x >= rail_end_x - 50:  # 50 pixel buffer before the actual end
                    return True
        
        return False
    
    def _land_board(self):
        """Land the board and reset all states"""
        # Store catch success state before resetting it
        was_caught_successfully = self.catch_success
        
        # Reset all grind-related states
        self.in_grind_window = False
        self.grinding = False
        self.grind_trick = None
        
        # Reset hold mechanic states
        self.holding_grind_trick = False
        self.pending_grind_trick = None
        
        # Reset catch system states
        self.catch_required = False
        self.catch_success = False
        self.catch_attempted = False
        self.catch_feedback_timer = 0
        
        # Reset death system states
        self.dead = False
        self.death_timer = 0
        self.perfect_catch_frames = []
        
        # Reset trick tracking
        self.original_flip_trick = None
        
        # Restore movement speed
        self.move_speed = 30
        
        # Land the board
        self.airborne = False
        self.scale_factor = (max(self.display_width, self.display_height) / 120) * 0.2  # Made smaller
        self.current_animation = None
        self.animation_frame = 0
        self.animation_completed = False  # Reset completion flag

        # Stop air wheels rolling sound when landing
        if self.wheels_rolling_sound:
            pygame.mixer.Channel(self.wheels_rolling_channel).stop()
            self.wheels_sound_playing = False
        
        # Stop any grind sound when landing
        try:
            pygame.mixer.Channel(6).stop()
        except Exception as e:
            pass  # Ignore errors if channel is not playing

        # Play landing sound only if trick was caught successfully
        if was_caught_successfully:
            land_sounds = [f"SFX/Land_{i}.wav" for i in range(1, 5)]
            land_sound_file = random.choice(land_sounds)
            try:
                land_sound = pygame.mixer.Sound(land_sound_file)
                land_sound.play()
            except Exception as e:
                print(f"Could not play land sound: {e}")
            
            # Play success sound for caught trick
            if self.sounds['success']:
                self.sounds['success'].play()
        else:
            # Play fail sound for missed catch
            if self.sounds['fail']:
                self.sounds['fail'].play()
        
        print(f"Landed")
        self.set_angle(0, 0)  # Reset to default shuv/flip angles
    
    def _update_grinding_state(self):
        """Update grinding state - check for grind exit conditions"""
        current_time = self._current_time
        grind_duration = current_time - self.grind_start_time
        
        # Check if we've reached the end of the current rail
        if self._check_rail_end():
            self._exit_grind("rail_end")
            return
        
        # Allow manual exit by releasing all keys after minimum duration
        if self.hands == ["center", "center"] and grind_duration >= self.min_grind_duration:
            self._exit_grind("manual")
    
    def _exit_grind(self, reason):
        """Exit the current grind"""
        # Stop the grind sound
        try:
            pygame.mixer.Channel(6).stop()
        except Exception as e:
            print(f"Could not stop grind sound: {e}")
        
        # Play grind exit sound
        land_sounds = [f"SFX/Land_{i}.wav" for i in range(1, 5)]
        land_sound_file = random.choice(land_sounds)
        try:
            land_sound = pygame.mixer.Sound(land_sound_file)
            land_sound.play()
        except Exception as e:
            print(f"Could not play land sound: {e}")
        
        # Land the board
        self._land_board()
    
    def _spawn_rail(self):
        """Spawn a new rail on the right side of the screen"""
        if self.rail_image is None:
            return
            
        # Get rail image dimensions
        rail_width = self.rail_image.get_width()
        rail_height = self.rail_image.get_height()
        
        # Calculate rail position - start from right edge, align with skateboard
        rail_x = self.display_width
        rail_y = self.display_height // 2 - rail_height // 2  # Align with skateboard center
        
        # Add rail to the list
        self.rails.append({
            'x': rail_x,
            'y': rail_y,
            'width': rail_width,
            'height': rail_height
        })
    
    def _update_rails(self):
        """Update rail positions and remove off-screen rails"""
        # Only update rails when floor is updated to match concrete speed
        current_time = self._current_time
        if current_time - self.last_floor_update >= self.move_update_interval:
            # Move all rails to the left
            for rail in self.rails[:]:  # Use slice to avoid modification during iteration
                rail['x'] -= self.move_speed
                
                # Remove rails that are off-screen (account for 6x stretch)
                if rail['x'] + (rail['width'] * 6) < 0:
                    self.rails.remove(rail)
    
    def _render_rails(self):
        """Render all active rails"""
        if self.rail_image is None:
            return
            
        for rail in self.rails:
            # Stretch rail to 6x width for longer rails
            stretched_width = rail['width'] * 6
            scale_key = f"rail_{stretched_width}_{rail['height']}"
            stretched_rail = self._get_cached_surface(self.rail_image, stretched_width, rail['height'], scale_key)
            self.display.blit(stretched_rail, (rail['x'], rail['y']))
    
    def _update_animation(self):
        """Update the current animation frame"""
        if not self.current_animation or self.current_animation not in self.animation_metadata:
            return
        
        # Don't update if animation is completed and doesn't loop
        if self.animation_completed:
            return
        
        current_time = self._current_time
        
        # Get the appropriate spin speed for this trick
        trick_spin_speed = self._get_trick_spin_speed(self.current_animation)
        current_animation_speed = self.animation_speed / trick_spin_speed
        
        # Check if enough time has passed to advance frame
        if current_time - self.animation_timer >= current_animation_speed:
            metadata = self.animation_metadata[self.current_animation]
            total_frames = metadata['frames']
            
            # Check if this animation should loop
            should_loop = self.animation_loops.get(self.current_animation, True)  # Default to looping
            
            # Advance to next frame
            self.animation_frame += 1
            
            # Check if we've reached the end
            if self.animation_frame >= total_frames:
                if should_loop:
                    # Loop back to beginning
                    self.animation_frame = 0
                else:
                    # Stay on last frame and mark as completed
                    self.animation_frame = total_frames - 1
                    self.animation_completed = True
            
            self.animation_timer = current_time
    
    def render_board(self, shuv_angle: float, flip_angle: float, 
                    center_x: int = None, center_y: int = None, 
                    scale: float = None) -> bool:
        """Render the board sprite at the specified angles or animation"""
        # Use default scale if not provided
        if scale is None:
            # Make skateboard bigger when airborne
            if self.airborne:
                scale = self.scale_factor * 1.3  # 30% larger when airborne
            else:
                scale = self.scale_factor
        
        # Set default center position using pre-calculated values
        if center_x is None:
            center_x = self._skateboard_center_x
        if center_y is None:
            center_y = self._display_center_y
        
        

        # Render animation if we have one, otherwise use angle-based rendering
        if self.current_animation and self.current_animation in self.animation_maps:
            # Clear display for animations to prevent frame overlap
            self.display.fill(self.colors['background'])  # Use unified background color
            # Render the endless scrolling floor first (as the background)
            self._render_floor()
            # Render rails
            self._render_rails()
            # Render the animation
            self._render_animation(center_x, center_y, scale)
        elif self.grinding:
            # For grinding, render floor and grind image
            self.display.fill(self.colors['background'])
            # Render the endless scrolling floor first (as the background)
            self._render_floor()
            # Render rails
            self._render_rails()
            # Render the grind image
            self._render_grind_image(center_x, center_y, scale)
        else:
            # For static rendering, render floor and sprite normally
            # Render the endless scrolling floor first (as the background)
            self._render_floor()
            # Render rails
            self._render_rails()
            # Fallback to angle-based rendering using new sprite system
            sprite_pos = self.get_sprite_position(shuv_angle, flip_angle)
            if sprite_pos:
                self._render_sprite_from_position(sprite_pos, center_x, center_y, scale)
            else:
                print(f"No sprite found for angles: shuv={shuv_angle}, flip={flip_angle}")
                return False
        
        # Draw hand position indicators at preset locations (lower and smaller)
        self._draw_hand_position_indicators()
        
        # Draw trick detection feedback (lower and smaller)
        self._draw_trick_feedback()
        
        # Draw death effect (red screen flash) - keep this for visual feedback
        self._draw_death_effect()
        
        # Update display
        pygame.display.flip()
        
        return True
    
    def _render_animation(self, center_x: int, center_y: int, scale: float):
        """Render the current animation frame"""
        if not self.current_animation or self.current_animation not in self.animation_maps:
            return
        
        animation_map = self.animation_maps[self.current_animation]
        metadata = self.animation_metadata[self.current_animation]
        
        frames_per_row = metadata['frames_per_row']
        
        # Get the correct sprite size for this animation
        # Check if this is a new animation (128x128) or old animation (64x64)
        animation_sprite_size = 128 if self.current_animation in ['BS-Shuv-It', 'FS-Shuv-It', 'Kickflip', 'Heelflip', 'Varial Kickflip', 'Varial Heelflip', 'Inward Heelflip', 'Hardflip'] else self.sprite_size
        
        # For shuv and flip tricks, use every other frame to halve the animation
        shuv_tricks = ["BS-Shuv-It", "FS-Shuv-It", "Nollie BS-Shuv-It", "Nollie FS-Shuv-It"]
        flip_tricks = ["Kickflip", "Heelflip", "Nollie Kickflip", "Nollie Heelflip"]
        if self.current_animation in shuv_tricks or self.current_animation in flip_tricks:
            # Use every other frame (0, 2, 4, 6, 8, etc.) for 30-degree snaps
            actual_frame = self.animation_frame * 2
        else:
            actual_frame = self.animation_frame
        
        # Calculate which frame to render
        frame_x = (actual_frame % frames_per_row) * animation_sprite_size
        frame_y = (actual_frame // frames_per_row) * animation_sprite_size
        
        # Extract the current frame
        frame_rect = pygame.Rect(frame_x, frame_y, animation_sprite_size, animation_sprite_size)
        
        # Check if the rectangle is within the animation map bounds
        if (frame_x + animation_sprite_size <= animation_map.get_width() and 
            frame_y + animation_sprite_size <= animation_map.get_height()):
            sprite_surface = animation_map.subsurface(frame_rect)
        else:
            print(f"Error: Frame rectangle {frame_rect} is outside animation map bounds {animation_map.get_size()}")
            return
        
        # Scale the sprite using cached surfaces
        if scale != 1.0:
            new_width = int(animation_sprite_size * scale)
            new_height = int(animation_sprite_size * scale)
            scale_key = f"anim_{self.current_animation}_{self.animation_frame}_{scale}"
            sprite_surface = self._get_cached_surface(sprite_surface, new_width, new_height, scale_key)
        
        # Calculate position to center the sprite
        sprite_width, sprite_height = sprite_surface.get_size()
        draw_x = center_x - sprite_width // 2
        draw_y = center_y - sprite_height // 2
        
        # Draw the sprite
        self.display.blit(sprite_surface, (draw_x, draw_y))
    
    def _render_sprite_from_position(self, sprite_pos, center_x: int, center_y: int, scale: float):
        """Render a sprite from a position tuple"""
        sprite_x, sprite_y, sprite_w, sprite_h = sprite_pos
        
        # Use new sprite map if available and sprite size is 128x128
        if sprite_w == 128 and hasattr(self, 'new_sprite_map'):
            sprite_rect = pygame.Rect(sprite_x, sprite_y, sprite_w, sprite_h)
            sprite_surface = self.new_sprite_map.subsurface(sprite_rect)
        else:
            # Use old sprite map for backward compatibility
            sprite_rect = pygame.Rect(sprite_x, sprite_y, sprite_w, sprite_h)
            sprite_surface = self.sprite_map.subsurface(sprite_rect)
        
        # Scale the sprite using cached surfaces
        if scale != 1.0:
            new_width = int(sprite_w * scale)
            new_height = int(sprite_h * scale)
            scale_key = f"sprite_{sprite_x}_{sprite_y}_{scale}"
            sprite_surface = self._get_cached_surface(sprite_surface, new_width, new_height, scale_key)
        
        # Calculate position to center the sprite
        sprite_width, sprite_height = sprite_surface.get_size()
        draw_x = center_x - sprite_width // 2
        draw_y = center_y - sprite_height // 2
        
        # Draw the sprite
        self.display.blit(sprite_surface, (draw_x, draw_y))
    
    def _render_grind_image(self, center_x: int, center_y: int, scale: float):
        """Render the current grind image"""
        if not self.grinding or not self.grind_trick:
            return
        
        print(f"Rendering grind image: '{self.grind_trick}' at ({center_x}, {center_y})")
        
        # Get the grind image
        grind_image = self.grind_images.get(self.grind_trick)
        if not grind_image:
            print(f"Warning: No grind image found for '{self.grind_trick}' - showing placeholder")
            # Draw a placeholder rectangle to show something is happening
            placeholder_size = int(100 * scale)
            pygame.draw.rect(self.display, (255, 0, 0), 
                           (center_x - placeholder_size//2, center_y - placeholder_size//2, 
                            placeholder_size, placeholder_size))
            return
        
        # Scale the grind image using cached surfaces
        # Make grind images smaller for better proportion
        grind_scale = scale * 0.8  # 0.8x smaller than normal sprites
        if grind_scale != 1.0:
            original_width = grind_image.get_width()
            original_height = grind_image.get_height()
            new_width = int(original_width * grind_scale)
            new_height = int(original_height * grind_scale)
            scale_key = f"grind_{self.grind_trick}_{grind_scale}"
            scaled_image = self._get_cached_surface(grind_image, new_width, new_height, scale_key)
        else:
            scaled_image = grind_image
        
        # Calculate position to center the image
        image_width, image_height = scaled_image.get_size()
        draw_x = center_x - image_width // 2
        draw_y = center_y - image_height // 2
        
        # Apply grind offset if specified
        if hasattr(self, 'grind_offset'):
            draw_x += self.grind_offset[0]
            draw_y += self.grind_offset[1]
        
        # Draw the grind image
        self.display.blit(scaled_image, (draw_x, draw_y))
    
    def _draw_hand_position_indicators(self):
        """Draw hand position indicators using arrow key icons - 2 sets (WASD left, IJKL right), lower and smaller"""
        # Icon size - smaller for cleaner look
        icon_size = 60  # Reduced from 100 to 60 for smaller indicators
        
        # Position arrows lower on screen (4/5ths down)
        center_y = int(self.display_height * 4 / 5)  # Lower position - 4/5ths down the screen
        
        # Spacing between arrows in each set
        spacing = 80
        
        # Left set (WASD) - positioned closer to center (50px inward)
        left_center_x = self._display_center_x // 2 + 50  # Left quarter + 50px toward center
        left_arrow_positions = {
            'up': (left_center_x, center_y - spacing),
            'down': (left_center_x, center_y + spacing),
            'left': (left_center_x - spacing, center_y),
            'right': (left_center_x + spacing, center_y)
        }
        
        # Right set (IJKL) - positioned closer to center (50px inward)
        right_center_x = self._display_center_x + self._display_center_x // 2 - 50  # Right quarter - 50px toward center
        right_arrow_positions = {
            'up': (right_center_x, center_y - spacing),
            'down': (right_center_x, center_y + spacing),
            'left': (right_center_x - spacing, center_y),
            'right': (right_center_x + spacing, center_y)
        }
        
        # Draw left set (WASD) - always visible
        for direction, (x, y) in left_arrow_positions.items():
            # Check if this direction matches WASD keys
            is_pressed = False
            if direction == 'up' and self.keys_pressed['w']:
                is_pressed = True
            elif direction == 'down' and self.keys_pressed['s']:
                is_pressed = True
            elif direction == 'left' and self.keys_pressed['a']:
                is_pressed = True
            elif direction == 'right' and self.keys_pressed['d']:
                is_pressed = True
            
            # Choose icon based on pressed state
            icon_set = self.arrow_icons_outline if is_pressed else self.arrow_icons_solid
            
            if direction in icon_set and icon_set[direction]:
                # Scale the icon using cached surfaces
                scale_key = f"icon_{direction}_{icon_size}_{'pressed' if is_pressed else 'normal'}"
                scaled_icon = self._get_cached_surface(icon_set[direction], icon_size, icon_size, scale_key)
                # Center the icon at the position
                icon_rect = scaled_icon.get_rect(center=(x, y))
                self.display.blit(scaled_icon, icon_rect)
        
        # Draw right set (IJKL) - always visible
        for direction, (x, y) in right_arrow_positions.items():
            # Check if this direction matches IJKL keys
            is_pressed = False
            if direction == 'up' and self.keys_pressed['i']:
                is_pressed = True
            elif direction == 'down' and self.keys_pressed['k']:
                is_pressed = True
            elif direction == 'left' and self.keys_pressed['j']:
                is_pressed = True
            elif direction == 'right' and self.keys_pressed['l']:
                is_pressed = True
            
            # Choose icon based on pressed state
            icon_set = self.arrow_icons_outline if is_pressed else self.arrow_icons_solid
            
            if direction in icon_set and icon_set[direction]:
                # Scale the icon using cached surfaces
                scale_key = f"icon_{direction}_{icon_size}_{'pressed' if is_pressed else 'normal'}"
                scaled_icon = self._get_cached_surface(icon_set[direction], icon_size, icon_size, scale_key)
                # Center the icon at the position
                icon_rect = scaled_icon.get_rect(center=(x, y))
                self.display.blit(scaled_icon, icon_rect)
    
    
    
    
    def _draw_angle_info(self, shuv_angle: float, flip_angle: float):
        """Draw angle information on the display"""
        # Show animation info if playing, otherwise show angles
        if self.current_animation:
            animation_text = f"Animation: {self.current_animation} | Frame: {self.animation_frame}"
            text_surface = self.font.render(animation_text, True, self.colors['text'])
        else:
            angle_text = f"Shuv: {shuv_angle}° | Flip: {flip_angle}°"
            text_surface = self.font.render(angle_text, True, self.colors['text'])
        
        text_rect = text_surface.get_rect(center=(self._display_center_x, self.display_height - 30))
        self.display.blit(text_surface, text_rect)
    
    def _draw_trick_feedback(self):
        """Draw trick detection feedback on the display"""
        current_time = self._current_time
        
        # Show trick feedback if we're starting a trick, airborne with a trick, attempting a grind, actively grinding, or have a completed trick result
        should_show_feedback = (self.trick_start_time > 0 or 
                               (self.airborne and hasattr(self, 'current_trick_name') and self.current_trick_name) or
                               (self.in_grind_window and hasattr(self, 'pending_grind_trick') and self.pending_grind_trick) or
                               (self.grinding and hasattr(self, 'grind_trick') and self.grind_trick) or
                               (hasattr(self, 'catch_feedback_timer') and self.catch_feedback_timer > 0 and 
                                (current_time - self.catch_feedback_timer) <= 1.0))
        
        if should_show_feedback:
            # Determine what trick to show - check grind states first
            if self.grinding and hasattr(self, 'grind_trick') and self.grind_trick:
                # We're currently grinding - show the active grind trick with flip name
                if hasattr(self, 'original_flip_trick') and self.original_flip_trick:
                    combo_text = f"{self.original_flip_trick} -> {self.grind_trick}"
                else:
                    combo_text = f"{self.grind_trick}"
                text_color = self.colors['accent']  # Green while successfully grinding
            elif self.in_grind_window and hasattr(self, 'pending_grind_trick') and self.pending_grind_trick:
                # We're in grind window and attempting a grind trick - show flip -> grind format
                if hasattr(self, 'original_flip_trick') and self.original_flip_trick:
                    combo_text = f"{self.original_flip_trick} -> {self.pending_grind_trick}"
                else:
                    combo_text = f"{self.pending_grind_trick}"
                text_color = (255, 255, 255)  # White while attempting grind
            elif hasattr(self, 'current_trick_name') and self.current_trick_name:
                # We have an active flip trick
                combo_text = f"{self.current_trick_name}"
                
                # Determine text color based on catch state
                if self.catch_required and self.catch_attempted:
                    # Trick has been attempted - show result
                    if self.catch_success:
                        text_color = self.colors['accent']  # Green for success
                    else:
                        text_color = (255, 100, 100)  # Red for failure
                else:
                    # Trick is active but not yet caught - show white
                    text_color = (255, 255, 255)  # White while trick is active
            elif self.trick_start_time > 0:
                # We're starting a trick - show current combination
                detected_trick = self._check_trick_combination()
                if detected_trick:
                    combo_text = f"{detected_trick}"
                    text_color = (255, 255, 255)  # White while holding keys
                else:
                    combo_text = f"{self.hands[0]} + {self.hands[1]}"
                    text_color = self.colors['warning']  # Yellow for invalid combo
            else:
                return  # Nothing to show
            
            # Use smaller font for trick feedback
            text_surface = self.font.render(combo_text, True, text_color)
            # Position text lower on screen (3/4ths down)
            text_y = int(self.display_height * 3 / 4)
            text_rect = text_surface.get_rect(center=(self._display_center_x, text_y))
            
            # Create black drop shadow by rendering the same text in black, offset by 2 pixels
            shadow_surface = self.font.render(combo_text, True, (0, 0, 0))
            shadow_rect = shadow_surface.get_rect(center=(self._display_center_x + 2, text_y + 2))
            self.display.blit(shadow_surface, shadow_rect)
            
            # Draw the main text on top
            self.display.blit(text_surface, text_rect)
            
            # Only show progress bar during initial trick holding phase
            if self.trick_start_time > 0 and not (hasattr(self, 'current_trick_name') and self.current_trick_name):
                # Calculate progress (0.0 to 1.0)
                progress = min((current_time - self.trick_start_time) / self.trick_hold_duration, 1.0)
                
                # Draw smaller progress bar
                bar_width = 300  # Reduced from 400
                bar_height = 15  # Reduced from 20
                bar_x = (self.display_width - bar_width) // 2
                bar_y = text_y + 30  # Position below text
                
                # Background bar
                pygame.draw.rect(self.display, self.colors['progress_bg'], (bar_x, bar_y, bar_width, bar_height))
                
                # Progress bar with distinct color phases
                progress_width = int(bar_width * progress)
                
                # Determine color based on progress phases
                if progress < 0.43:
                    color = self.colors['danger']  # Red for first third
                elif progress < 0.86:
                    color = self.colors['warning']  # Yellow for second third
                else:
                    color = self.colors['accent']  # Green for final third
                
                pygame.draw.rect(self.display, color, (bar_x, bar_y, progress_width, bar_height))
                
                # Border
                pygame.draw.rect(self.display, self.colors['border'], (bar_x, bar_y, bar_width, bar_height), 5)
    
    def _draw_landing_feedback(self):
        """Draw landing detection feedback on the display"""
        current_time = self._current_time
        
        # Check if we should show landing feedback
        if self.landing_feedback_timer > 0 and (current_time - self.landing_feedback_timer) <= self.landing_feedback_duration:
            # Calculate alpha based on time remaining
            time_remaining = self.landing_feedback_duration - (current_time - self.landing_feedback_timer)
            alpha = int(255 * (time_remaining / self.landing_feedback_duration))
            
            # Choose color and text based on landing success
            if self.landing_success:
                color = self.colors['accent']  # Green for success
                text = ""  # Removed text display
            else:
                color = self.colors['danger']  # Red for failure
                text = ""  # Removed text display
            
            # Skip text rendering when text is empty
            if text:  # Only render if there's text to display
                # Create text surface
                text_surface = self.title_font.render(text, True, color)
                text_rect = text_surface.get_rect(center=(self._display_center_x, 150))
                
                # Draw background rectangle for better visibility
                bg_rect = text_rect.inflate(40, 20)
                bg_color = (*self.colors['background'], alpha)
                bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
                bg_surface.set_alpha(alpha)
                bg_surface.fill(self.colors['background'])
                self.display.blit(bg_surface, bg_rect)
                
                # Draw the text
                self.display.blit(text_surface, text_rect)
                
                # Draw border
                border_color = (*color, alpha)
                pygame.draw.rect(self.display, color, bg_rect, 3)
    
    def _draw_grind_feedback(self):
        """Draw grind detection feedback on the display"""
        current_time = self._current_time
        
        # Show grind window indicator
        if self.in_grind_window:
            # Calculate time remaining in grind window
            time_remaining = self.grind_window_duration - (current_time - self.grind_window_start_time)
            alpha = int(255 * (time_remaining / self.grind_window_duration))
            
            # Draw grind window indicator
            text = "GRIND WINDOW - Input trick!"
            color = self.colors['warning']  # Yellow for grind window
            
            # Create text surface
            text_surface = self.title_font.render(text, True, color)
            text_rect = text_surface.get_rect(center=(self._display_center_x, 200))
            
            # Draw background rectangle for better visibility
            bg_rect = text_rect.inflate(40, 20)
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
            bg_surface.set_alpha(alpha)
            bg_surface.fill(self.colors['background'])
            self.display.blit(bg_surface, bg_rect)
            
            # Draw the text
            self.display.blit(text_surface, text_rect)
            
            # Draw border
            pygame.draw.rect(self.display, color, bg_rect, 3)

            
            # Draw progress bar for grind window
            bar_width = 300
            bar_height = 15
            bar_x = (self.display_width - bar_width) // 2
            bar_y = 250
            
            # Background bar
            pygame.draw.rect(self.display, self.colors['progress_bg'], (bar_x, bar_y, bar_width, bar_height))
            
            # Progress bar
            progress = time_remaining / self.grind_window_duration
            progress_width = int(bar_width * progress)
            pygame.draw.rect(self.display, color, (bar_x, bar_y, progress_width, bar_height))
            
            # Border
            pygame.draw.rect(self.display, self.colors['border'], (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Show current grind status
        elif self.grinding:
            current_time = self._current_time
            grind_duration = current_time - self.grind_start_time
            remaining_time = max(0, self.min_grind_duration - grind_duration)
            
            text = f"GRINDING: {self.grind_trick}"
            color = self.colors['accent']  # Green for grinding
            
            # Create text surface
            text_surface = self.title_font.render(text, True, color)
            text_rect = text_surface.get_rect(center=(self._display_center_x, 200))
            
            # Draw background rectangle for better visibility
            bg_rect = text_rect.inflate(40, 20)
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
            bg_surface.set_alpha(180)
            bg_surface.fill(self.colors['background'])
            self.display.blit(bg_surface, bg_rect)
            
            # Draw the text
            self.display.blit(text_surface, text_rect)
            
            # Draw border
            pygame.draw.rect(self.display, color, bg_rect, 3)
            
            # Show remaining time
            if remaining_time > 0:
                time_text = f"Hold for {remaining_time:.1f}s more"
                time_surface = self.font.render(time_text, True, self.colors['text_secondary'])
                time_rect = time_surface.get_rect(center=(self._display_center_x, 250))
                self.display.blit(time_surface, time_rect)
        
        # Show rail proximity indicator when near rail
        elif self._check_rail_collision() and not self.grinding:
            if self.airborne:
                text = "NEAR RAIL - Release keys to grind!"
            else:
                text = "NEAR RAIL - Input grind trick!"
            color = self.colors['secondary']  # Light gray for rail proximity
            
            # Create text surface
            text_surface = self.font.render(text, True, color)
            text_rect = text_surface.get_rect(center=(self._display_center_x, 250))
            
            # Draw background rectangle for better visibility
            bg_rect = text_rect.inflate(20, 10)
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
            bg_surface.set_alpha(150)
            bg_surface.fill(self.colors['background'])
            self.display.blit(bg_surface, bg_rect)
            
            # Draw the text
            self.display.blit(text_surface, text_rect)
    
    def _draw_catch_feedback(self):
        """Draw catch detection feedback on the display"""
        current_time = self._current_time
        
        # Show catch window indicator
        if self.catch_required and self.airborne and not self.catch_attempted:
            # Check if we're in the catch window
            if current_time >= self.catch_window_start:
                time_remaining = (self.catch_window_start + self.catch_window_duration) - current_time
                if time_remaining > 0:
                    # Draw catch window indicator with different text based on state
                    if self.catch_key_pressed and not self.catch_key_released:
                        text = f"RELEASE TO CATCH! (Frame {self.animation_frame})"
                        color = self.colors['accent']  # Green when ready to release
                    else:
                        text = f"PRESS & RELEASE TO CATCH! (Perfect: {self.perfect_catch_frames})"
                        color = self.colors['warning']  # Yellow for catch window
                    
                    # Create text surface
                    text_surface = self.title_font.render(text, True, color)
                    text_rect = text_surface.get_rect(center=(self._display_center_x, 300))
                    
                    # Draw background rectangle for better visibility
                    bg_rect = text_rect.inflate(40, 20)
                    bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
                    bg_surface.set_alpha(200)
                    bg_surface.fill(self.colors['background'])
                    self.display.blit(bg_surface, bg_rect)
                    
                    # Draw the text
                    self.display.blit(text_surface, text_rect)
                    
                    # Draw border
                    pygame.draw.rect(self.display, color, bg_rect, 3)
                    
                    # Draw progress bar for catch window
                    bar_width = 300
                    bar_height = 15
                    bar_x = (self.display_width - bar_width) // 2
                    bar_y = 350
                    
                    # Background bar
                    pygame.draw.rect(self.display, self.colors['progress_bg'], (bar_x, bar_y, bar_width, bar_height))
                    
                    # Progress bar
                    progress = time_remaining / self.catch_window_duration
                    progress_width = int(bar_width * progress)
                    pygame.draw.rect(self.display, color, (bar_x, bar_y, progress_width, bar_height))
                    
                    # Border
                    pygame.draw.rect(self.display, self.colors['border'], (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Show catch feedback
        elif self.catch_feedback_timer > 0 and (current_time - self.catch_feedback_timer) <= self.catch_feedback_duration:
            # Calculate alpha based on time remaining
            time_remaining = self.catch_feedback_duration - (current_time - self.catch_feedback_timer)
            alpha = int(255 * (time_remaining / self.catch_feedback_duration))
            
            # Choose color and text based on catch success
            if self.catch_success:
                color = self.colors['accent']  # Green for success
                text = "CAUGHT!"
            else:
                color = self.colors['danger']  # Red for failure
                text = "MISSED!"
            
            # Create text surface
            text_surface = self.title_font.render(text, True, color)
            text_rect = text_surface.get_rect(center=(self._display_center_x, 300))
            
            # Draw background rectangle for better visibility
            bg_rect = text_rect.inflate(40, 20)
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
            bg_surface.set_alpha(alpha)
            bg_surface.fill(self.colors['background'])
            self.display.blit(bg_surface, bg_rect)
            
            # Draw the text
            self.display.blit(text_surface, text_rect)
            
            # Draw border
            pygame.draw.rect(self.display, color, bg_rect, 3)
        
        # Show death feedback
        elif self.dead:
            current_time = self._current_time
            time_elapsed = current_time - self.death_timer
            
            if time_elapsed <= self.death_duration:
                # Calculate alpha based on time remaining
                alpha = int(255 * (1.0 - (time_elapsed / self.death_duration)))
                
                text = "DEATH!"
                color = self.colors['danger']  # Red for death
                
                # Create text surface
                text_surface = self.title_font.render(text, True, color)
                text_rect = text_surface.get_rect(center=(self._display_center_x, 300))
                
                # Draw background rectangle for better visibility
                bg_rect = text_rect.inflate(40, 20)
                bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
                bg_surface.set_alpha(alpha)
                bg_surface.fill(self.colors['background'])
                self.display.blit(bg_surface, bg_rect)
                
                # Draw the text
                self.display.blit(text_surface, text_rect)
                
                # Draw border
                pygame.draw.rect(self.display, color, bg_rect, 3)
    
    def _draw_death_effect(self):
        """Draw death effect (red screen flash)"""
        if not self.dead:
            return
        
        current_time = self._current_time
        time_elapsed = current_time - self.death_timer
        
        if time_elapsed <= self.death_duration:
            # Calculate alpha based on time remaining (fade out)
            alpha = int(255 * (1.0 - (time_elapsed / self.death_duration)))
            
            # Create red overlay
            red_overlay = pygame.Surface((self.display_width, self.display_height))
            red_overlay.set_alpha(alpha)
            red_overlay.fill((255, 0, 0))  # Red color
            
            # Draw the overlay
            self.display.blit(red_overlay, (0, 0))
    
    def run(self):
        """Run the main application loop"""
        clock = pygame.time.Clock()
        running = True
        
        # Floor wheels sound removed - no constant background sound
        
        # Render initial frame with floor
        self.render_board(*self.angle)
        
        print("Skateboard Display App")
        print("Controls:")
        print("  Left Hand: W(up) A(left) S(down) D(right)")
        print("  Right Hand: I(up) J(left) K(down) L(right)")
        print("  ESC: Exit fullscreen")
        print("  R: Reset angle")
        print("  T: Toggle landing detection")
        print("  C: Clear surface cache")
        
        
        while running:
            # Update time once per frame
            self._update_time()
            
            # Handle events with optimized key mapping
            running = self._handle_events(running)
            
            # Update game state
            self._update_game_state()
            
            # Render current frame
            self.render_board(*self.angle)
            
            clock.tick(60)  # 60 FPS
        
        pygame.quit()
    
    def _handle_events(self, running):
        """Optimized event handling with key mapping"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_r:
                    self.set_angle(*self.default_angle)
                    print(f"Reset to default angle: {self.default_angle}")
                elif event.key == pygame.K_t:
                    self.landing_detection_enabled = not self.landing_detection_enabled
                    status = "enabled" if self.landing_detection_enabled else "disabled"
                    print(f"Landing detection {status}")
                elif event.key == pygame.K_c:
                    self._clear_surface_cache()
                elif event.key in self._key_mappings:
                    self.keys_pressed[self._key_mappings[event.key]] = True
            elif event.type == pygame.KEYUP:
                if event.key in self._key_mappings:
                    self.keys_pressed[self._key_mappings[event.key]] = False
        return running
    
    def _update_game_state(self):
        """Optimized game state update - single method for all updates"""
        # Check for automatic cache clearing
        self._check_auto_cache_clear()
        
        # Update hand regions based on keyboard input
        self._update_keyboard_controls()
        
        # Update trick detection
        self._update_trick_detection(self._current_time)
        
        # Direct grind mode removed - only allow grinding through airborne grind window
        
        # Update airborne state (spinning, landing)
        self._update_airborne_state()
        
        # Debug grinding state
        if self.grinding:
            print(f"Grinding state active: {self.grind_trick}")
        else:
            print(f"Not grinding: airborne={self.airborne}, in_grind_window={self.in_grind_window}")
        
        # Update rails
        self._update_rails()
        
        # Check for rail spawning
        if self._current_time - self.last_rail_spawn >= random.uniform(*self.rail_spawn_interval):
            self._spawn_rail()
            self.last_rail_spawn = self._current_time

def main():
    """Main function"""
    try:
        app = SkateboardApp()
        
        # Use the default angle set in __init__
        # app.set_angle(0, 0, 0)  # This was overriding the default
        
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        pygame.quit()

if __name__ == "__main__":
    main()
