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
    """Simple app that displays skateboard at a specific angle"""
    
    def __init__(self):
        """Initialize the app"""
        pygame.init()
        pygame.mixer.init()
        
        # Create a simple 1000x800 window
        self.display = pygame.display.set_mode((1000, 800))
        self.display_width = 1000
        self.display_height = 800
        print(f"Display resolution: {self.display_width}x{self.display_height}")
        
        pygame.display.set_caption("Random Skateboard Display")
        
        # Unified Color Scheme
        self.colors = {
            # Primary colors
            'primary': (52, 73, 94),      # Dark blue-gray
            'secondary': (149, 165, 166), # Light gray
            'accent': (46, 204, 113),     # Green
            'warning': (241, 196, 15),    # Yellow
            'danger': (231, 76, 60),      # Red
            
            # Background colors
            'background': (44, 62, 80),   # Dark blue-gray background
            'surface': (52, 73, 94),      # Surface color
            'text': (236, 240, 241),      # Light text
            'text_secondary': (149, 165, 166), # Secondary text
            
            # UI elements
            'border': (127, 140, 141),    # Border color
            'progress_bg': (44, 62, 80),  # Progress bar background
            'progress_fill': (46, 204, 113), # Progress bar fill
            
            # Hand indicators
            'hand_left': (231, 76, 60),   # Red for left hand
            'hand_left_border': (192, 57, 43), # Darker red border
            'hand_right': (52, 152, 219), # Blue for right hand
            'hand_right_border': (41, 128, 185), # Darker blue border
            
            # Floor colors
            'concrete_base': (149, 165, 166), # Concrete base color
            'concrete_dark': (127, 140, 141), # Concrete dark variation
            'concrete_crack': (108, 122, 137), # Concrete crack color
        }
        
        # Fonts - scale based on screen size
        font_size = max(24, self.display_width // 40)
        title_font_size = max(36, self.display_width // 25)
        self.font = pygame.font.Font(None, font_size)
        self.title_font = pygame.font.Font(None, title_font_size)
        
        # Load sprite resources
        self.sprite_map = None
        self.sprite_metadata = {}
        self.grid_size = 118
        self.sprite_size = 64
        
        # Animation system
        self.animation_maps = {}
        self.animation_metadata = {}
        self.current_animation = None
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.025
        
        self._load_sprite_map()
        self._load_metadata()
        self._load_animations()
        
        # Trick Map
        self.trick_map = {
            "Ollie": ["left", "center"],
            "Nollie": ["center", "right"], 
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

        self.airborne = False
        self.landing_angle = (0, 90, 0)
        self.last_spin_time = 0
        self.spin_interval = 0.025  # Spin every 0.1 seconds
        self.spin_speed = 2

        # Single angle setting
        self.default_angle = (0, 90, 0)
        self.angle = self.default_angle  # (x_angle, y_angle, z_angle)
        
        # Scale factor for display - make it smaller for elevated camera view
        self.scale_factor = max(self.display_width, self.display_height) / 120  # Smaller scale for elevated view
        
        # Movement system - unified speed control
        self.move_speed = 30  # Pixels per update for all moving objects
        self.move_update_interval = 0.1  # Update every 0.1 seconds
        
        # Floor properties - zoomed out for elevated camera view
        self.floor_height = 200  # Increased height for more visible floor
        self.floor_offset = 0  # Current scroll offset
        self.floor_texture_width = 300  # Wider texture segments for zoomed out view
        self.last_floor_update = 0  # Last time floor was updated
        
        # Rail system
        self.rails = []  # List of active rails
        self.rail_spawn_interval = (3, 6)  # Random spawn interval in seconds
        self.last_rail_spawn = 0  # Last time a rail was spawned
        self.rail_image = None  # Rail image
        self.rail_scale = 0.5  # Scale factor to make rail smaller
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
        self.trick_hold_duration = 0.3
        self.last_hand_combination = ["center", "center"]
        
        
        # Load sound effects
        self.sounds = {}
        self._load_sounds()
        
        # Initialize floor texture to prevent flickering
        self.floor_texture = self._create_floor_texture()
        
        
    def _load_sprite_map(self):
        """Load the sprite map image"""
        try:
            self.sprite_map = pygame.image.load("skateboard_sprite_map.png").convert_alpha()
            print("Loaded sprite map successfully")
        except pygame.error as e:
            raise Exception(f"Failed to load sprite map: {e}")
    
    def _load_metadata(self):
        """Load sprite metadata from file"""
        try:
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
            
            print(f"Loaded metadata: {len(self.sprite_metadata)} sprites")
            
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
                                                metadata['frames'] = int(mline.split(":")[1].strip())
                                            elif "Frames per row:" in mline:
                                                metadata['frames_per_row'] = int(mline.split(":")[1].strip())
                                        
                                        self.animation_metadata[trick_name] = metadata
            
            print(f"Loaded {len(self.animation_maps)} animation sprite maps")
            
        except Exception as e:
            print(f"Warning: Could not load animations: {e}")
            self.animation_maps = {}
            self.animation_metadata = {}
    
    def _load_sounds(self):
        """Load sound effects"""
        try:
            self.sounds = {
                'start_trick': pygame.mixer.Sound("SFX/StartTrick.wav"),
                'cancel_trick': pygame.mixer.Sound("SFX/CancelTrick.wav"),
                'foot1': pygame.mixer.Sound("SFX/Foot1.wav"),
                'foot2': pygame.mixer.Sound("SFX/Foot2.wav"),
                'WheelsRolling.wav': pygame.mixer.Sound("SFX/WheelsRolling.wav")
            }
            print("Loaded sound effects successfully")
        except pygame.error as e:
            print(f"Warning: Could not load sound effects: {e}")
            # Create empty sound objects to prevent errors
            self.sounds = {
                'start_trick': None,
                'cancel_trick': None,
                'foot1': None,
                'foot2': None,
                'WheelsRolling.wav': None
            }
    
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
    
    def _create_floor_texture(self):
        """Create a concrete floor texture pattern"""
        # Create a surface for the floor texture
        floor_surface = pygame.Surface((self.floor_texture_width, self.floor_height))
        
        # Base concrete color from unified scheme
        floor_surface.fill(self.colors['concrete_base'])
        
        # Add concrete texture details with seamless tiling - larger patterns for zoomed out view
        for i in range(0, self.floor_texture_width, 30):
            for j in range(0, self.floor_height, 25):
                # Random variation in color for texture using unified colors
                variation = random.randint(-20, 20)
                base_color = self.colors['concrete_base']
                color = (
                    max(0, min(255, base_color[0] + variation)),
                    max(0, min(255, base_color[1] + variation)),
                    max(0, min(255, base_color[2] + variation))
                )
                # Draw without borders to avoid seams - ensure no gaps
                pygame.draw.rect(floor_surface, color, (i, j, 30, 25), 0)
        
        # Add some subtle cracks and lines using unified colors
        for i in range(15, self.floor_texture_width - 15, 75):
            pygame.draw.line(floor_surface, self.colors['concrete_crack'], (i, 0), (i, self.floor_height), 1)
        
        # Ensure the texture is seamless by making sure the edges match
        # Copy edge pixels to create seamless tiling
        for j in range(self.floor_height):
            # Copy right edge to left edge
            floor_surface.set_at((0, j), floor_surface.get_at((self.floor_texture_width - 1, j)))
            # Copy left edge to right edge  
            floor_surface.set_at((self.floor_texture_width - 1, j), floor_surface.get_at((0, j)))
        
        return floor_surface
    
    def _render_floor(self):
        """Render the scrolling concrete floor"""
        # Always render floor - don't skip when airborne
        
        # Update floor scroll offset every 0.1 seconds for stylized effect
        current_time = pygame.time.get_ticks() / 1000.0
        if current_time - self.last_floor_update >= self.move_update_interval:
            self.floor_offset = (self.floor_offset + self.move_speed) % self.floor_texture_width
            self.last_floor_update = current_time
        
        # Ensure floor texture exists
        if not hasattr(self, 'floor_texture') or self.floor_texture is None:
            self.floor_texture = self._create_floor_texture()
        
        # Calculate floor position - start higher for elevated camera view
        floor_y = self.display_height - self.floor_height + 50  # Start higher up
        
        # Draw multiple floor segments to cover the entire width with seamless tiling
        # Start from -texture_width to ensure seamless scrolling
        start_x = -self.floor_texture_width - (self.floor_offset % self.floor_texture_width)
        for x in range(start_x, self.display_width + self.floor_texture_width, self.floor_texture_width):
            # Draw the floor texture
            self.display.blit(self.floor_texture, (x, floor_y))
            
            # Extend the floor upward to cover the entire screen height
            # Create a vertical extension of the floor pattern for elevated view
            for y in range(floor_y - self.floor_height, -self.floor_height, -self.floor_height):
                self.display.blit(self.floor_texture, (x, y))
    
    def get_sprite_position(self, x_angle: float, y_angle: float, z_angle: float) -> Optional[Tuple[int, int, int, int]]:
        """Get sprite position from 3D rotation angles"""
        # Normalize angles to 0-359 range
        x_angle = x_angle % 360
        y_angle = y_angle % 360
        z_angle = z_angle % 360
        
        # Round to nearest 15 degrees
        x_angle = round(x_angle / 15) * 15
        y_angle = round(y_angle / 15) * 15
        z_angle = round(z_angle / 15) * 15
        
        # No coordinate transformation needed - axes are correctly mapped
        
        # Create angle key
        angle_key = f"{x_angle}.0_{y_angle}.0_{z_angle}.0"
        
        # Look up position in metadata
        if angle_key in self.sprite_metadata:
            row, col = self.sprite_metadata[angle_key]
            x = col * self.sprite_size
            y = row * self.sprite_size
            return (x, y, self.sprite_size, self.sprite_size)
        
        return None
    
    def set_angle(self, x_angle: float, y_angle: float, z_angle: float):
        """Set the skateboard angle"""
        # Round to nearest 15 degrees
        x_angle = round(x_angle / 15) * 15
        y_angle = round(y_angle / 15) * 15
        z_angle = round(z_angle / 15) * 15
        
        # No coordinate transformation needed - axes are correctly mapped
        
        self.angle = (x_angle, y_angle, z_angle)
    
    def _update_keyboard_controls(self):
        """Update hand regions based on keyboard input"""
        # Reset to center
        self.hands = ["center", "center"]
        
        # Left hand controls (WASD) - controls left side
        if self.keys_pressed['w'] and self.keys_pressed['a']:
            self.hands[0] = "up"
        elif self.keys_pressed['w'] and self.keys_pressed['d']:
            self.hands[0] = "up"
        elif self.keys_pressed['s'] and self.keys_pressed['a']:
            self.hands[0] = "left"
        elif self.keys_pressed['s'] and self.keys_pressed['d']:
            self.hands[0] = "down"
        elif self.keys_pressed['w']:
            self.hands[0] = "up"
        elif self.keys_pressed['a']:
            self.hands[0] = "left"
        elif self.keys_pressed['s']:
            self.hands[0] = "down"
        elif self.keys_pressed['d']:
            self.hands[0] = "right"
        
        # Right hand controls (IJKL) - controls right side
        if self.keys_pressed['i'] and self.keys_pressed['j']:
            self.hands[1] = "up"
        elif self.keys_pressed['i'] and self.keys_pressed['l']:
            self.hands[1] = "up"
        elif self.keys_pressed['k'] and self.keys_pressed['j']:
            self.hands[1] = "left"
        elif self.keys_pressed['k'] and self.keys_pressed['l']:
            self.hands[1] = "down"
        elif self.keys_pressed['i']:
            self.hands[1] = "up"
        elif self.keys_pressed['j']:
            self.hands[1] = "left"
        elif self.keys_pressed['k']:
            self.hands[1] = "down"
        elif self.keys_pressed['l']:
            self.hands[1] = "right"
    
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
        current_combination = self.hands.copy()
        
        # Check if we have any non-center combination (any trick attempt)
        has_combination = current_combination != ["center", "center"]
        
        # If we start a new combination (any non-center combo)
        if has_combination and current_combination != self.last_hand_combination:
            self.trick_start_time = current_time
            print(f"Trick attempt started: {current_combination}")
            # Play start trick sound
            if self.sounds['start_trick']:
                self.sounds['start_trick'].play()
        
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
        
        # Start animation for the trick
        if trick_name in self.animation_maps:
            self.current_animation = trick_name
            self.animation_frame = 0
            self.animation_timer = 0
            print(f"Starting animation: {trick_name}")
        
        # Set airborne state and store trick info
        self.scale_factor *= 1.2
        self.airborne = True
        self.current_trick_name = trick_name
        self.trick_start_angle = self.angle
        self.landing_angle = self.angle
    
    def _update_airborne_state(self):
        """Update the board's airborne state and animation"""
        if not self.airborne:
            return

        # Play wheels rolling sound while airborne
        if self.sounds['WheelsRolling.wav']:
            if not pygame.mixer.Channel(5).get_busy():
                pygame.mixer.Channel(5).play(self.sounds['WheelsRolling.wav'], loops=-1)

        # Update animation if we have one
        if self.current_animation:
            self._update_animation()

        # Check if keys are still held (not both center)
        if self.hands[0] == "center" and self.hands[1] == "center":
            # Keys released - land the board
            self.airborne = False
            self.scale_factor = max(self.display_width, self.display_height) / 120
            self.current_animation = None
            self.animation_frame = 0

            # Stop wheels rolling sound when landing
            if self.sounds['WheelsRolling.wav']:
                pygame.mixer.Channel(5).stop()

            # Play landing sound
            land_sounds = [f"SFX/Land_{i}.wav" for i in range(1, 5)]
            land_sound_file = random.choice(land_sounds)
            try:
                land_sound = pygame.mixer.Sound(land_sound_file)
                land_sound.play()
            except Exception as e:
                print(f"Could not play land sound: {e}")
            
            print(f"Landed")
            self.set_angle(0, 90, 0)
    
    def _spawn_rail(self):
        """Spawn a new rail on the right side of the screen"""
        if self.rail_image is None:
            return
            
        # Get rail image dimensions
        rail_width = self.rail_image.get_width()
        rail_height = self.rail_image.get_height()
        
        # Calculate rail position - start from right edge
        rail_x = self.display_width
        rail_y = self.display_height - self.floor_height + 50 - rail_height  # Position on floor
        
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
        current_time = pygame.time.get_ticks() / 1000.0
        if current_time - self.last_floor_update >= self.move_update_interval:
            # Move all rails to the left
            for rail in self.rails[:]:  # Use slice to avoid modification during iteration
                rail['x'] -= self.move_speed
                
                # Remove rails that are off-screen
                if rail['x'] + rail['width'] < 0:
                    self.rails.remove(rail)
    
    def _render_rails(self):
        """Render all active rails"""
        if self.rail_image is None:
            return
            
        for rail in self.rails:
            self.display.blit(self.rail_image, (rail['x'], rail['y']))
    
    def _update_animation(self):
        """Update the current animation frame"""
        if not self.current_animation or self.current_animation not in self.animation_metadata:
            return
        
        current_time = pygame.time.get_ticks() / 1000.0
        
        # Check if enough time has passed to advance frame
        if current_time - self.animation_timer >= self.animation_speed:
            metadata = self.animation_metadata[self.current_animation]
            total_frames = metadata['frames']
            
            # Advance to next frame
            self.animation_frame = (self.animation_frame + 1) % total_frames
            self.animation_timer = current_time
    
    def render_board(self, x_angle: float, y_angle: float, z_angle: float, 
                    center_x: int = None, center_y: int = None, 
                    scale: float = None) -> bool:
        """Render the board sprite at the specified angles or animation"""
        # Use default scale if not provided
        if scale is None:
            scale = self.scale_factor
        
        # Set default center position
        if center_x is None:
            center_x = self.display_width // 2
        if center_y is None:
            center_y = self.display_height // 2
        
        # Render animation if we have one, otherwise use angle-based rendering
        if self.current_animation and self.current_animation in self.animation_maps:
            # Clear display for animations to prevent frame overlap
            self.display.fill(self.colors['background'])  # Use unified background color
            # Render the scrolling floor first (as the background)
            self._render_floor()
            # Render rails
            self._render_rails()
            # Render the animation
            self._render_animation(center_x, center_y, scale)
        else:
            # For static rendering, render floor and sprite normally
            # Render the scrolling floor first (as the background)
            self._render_floor()
            # Render rails
            self._render_rails()
            # Fallback to angle-based rendering
            sprite_pos = self.get_sprite_position(x_angle, y_angle, z_angle)
            if sprite_pos:
                self._render_sprite_from_position(sprite_pos, center_x, center_y, scale)
            else:
                print(f"No sprite found for angles: x={x_angle}, y={y_angle}, z={z_angle}")
                return False
        
        # Draw hand position indicators at preset locations
        self._draw_hand_position_indicators()
        
        # Draw angle information
        self._draw_angle_info(x_angle, y_angle, z_angle)
        
        # Draw trick detection feedback
        self._draw_trick_feedback()
        
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
        
        # Calculate which frame to render
        frame_x = (self.animation_frame % frames_per_row) * self.sprite_size
        frame_y = (self.animation_frame // frames_per_row) * self.sprite_size
        
        # Extract the current frame
        frame_rect = pygame.Rect(frame_x, frame_y, self.sprite_size, self.sprite_size)
        sprite_surface = animation_map.subsurface(frame_rect)
        
        # Scale the sprite
        if scale != 1.0:
            new_width = int(self.sprite_size * scale)
            new_height = int(self.sprite_size * scale)
            sprite_surface = pygame.transform.scale(sprite_surface, (new_width, new_height))
        
        # Calculate position to center the sprite
        sprite_width, sprite_height = sprite_surface.get_size()
        draw_x = center_x - sprite_width // 2
        draw_y = center_y - sprite_height // 2
        
        # Draw the sprite
        self.display.blit(sprite_surface, (draw_x, draw_y))
    
    def _render_sprite_from_position(self, sprite_pos, center_x: int, center_y: int, scale: float):
        """Render a sprite from a position tuple"""
        sprite_x, sprite_y, sprite_w, sprite_h = sprite_pos
        sprite_rect = pygame.Rect(sprite_x, sprite_y, sprite_w, sprite_h)
        sprite_surface = self.sprite_map.subsurface(sprite_rect)
        
        # Scale the sprite
        if scale != 1.0:
            new_width = int(sprite_w * scale)
            new_height = int(sprite_h * scale)
            sprite_surface = pygame.transform.scale(sprite_surface, (new_width, new_height))
        
        # Calculate position to center the sprite
        sprite_width, sprite_height = sprite_surface.get_size()
        draw_x = center_x - sprite_width // 2
        draw_y = center_y - sprite_height // 2
        
        # Draw the sprite
        self.display.blit(sprite_surface, (draw_x, draw_y))
    
    def _draw_hand_position_indicators(self):
        """Draw hand position indicators"""
        # Circle properties - smaller radius to match skateboard scale
        circle_radius = 25
        
        # Scale factor for circle positioning to match skateboard scale
        position_scale = 120 / 75  # Same ratio as skateboard scale reduction
        
        # Move center position 65px toward center and set all positions 50px away
        center_offset = int(40 * position_scale) + 65  # Move 65px toward center (inward)
        position_distance = 50  # All positions 50px away from center
        
        # Left hand positions (left side of screen) - moved toward center with 50px spacing
        left_hand_positions = {
            "center": (self.display_width // 4 + center_offset, self.display_height // 2),
            "up": (self.display_width // 4 + center_offset, self.display_height // 2 - position_distance),
            "down": (self.display_width // 4 + center_offset, self.display_height // 2 + position_distance),
            "left": (self.display_width // 4 + center_offset - position_distance, self.display_height // 2),
            "right": (self.display_width // 4 + center_offset + position_distance, self.display_height // 2)
        }
        
        # Right hand positions (right side of screen) - moved toward center with 50px spacing
        right_hand_positions = {
            "center": (3 * self.display_width // 4 - center_offset, self.display_height // 2),
            "up": (3 * self.display_width // 4 - center_offset, self.display_height // 2 - position_distance),
            "down": (3 * self.display_width // 4 - center_offset, self.display_height // 2 + position_distance),
            "left": (3 * self.display_width // 4 - center_offset - position_distance, self.display_height // 2),
            "right": (3 * self.display_width // 4 - center_offset + position_distance, self.display_height // 2)
        }
        
        # Draw left hand indicator (red) on left side
        if self.hands[0] in left_hand_positions:
            screen_x, screen_y = left_hand_positions[self.hands[0]]
            pygame.draw.circle(self.display, self.colors['hand_left'], (screen_x, screen_y), circle_radius)
            pygame.draw.circle(self.display, self.colors['hand_left_border'], (screen_x, screen_y), circle_radius, 5)
        
        # Draw right hand indicator (blue) on right side
        if self.hands[1] in right_hand_positions:
            screen_x, screen_y = right_hand_positions[self.hands[1]]
            pygame.draw.circle(self.display, self.colors['hand_right'], (screen_x, screen_y), circle_radius)
            pygame.draw.circle(self.display, self.colors['hand_right_border'], (screen_x, screen_y), circle_radius, 5)
    
    
    
    
    def _draw_angle_info(self, x_angle: float, y_angle: float, z_angle: float):
        """Draw angle information on the display"""
        # Show animation info if playing, otherwise show angles
        if self.current_animation:
            animation_text = f"Animation: {self.current_animation} | Frame: {self.animation_frame}"
            text_surface = self.font.render(animation_text, True, self.colors['text'])
        else:
            angle_text = f"X: {x_angle}° | Y: {y_angle}° | Z: {z_angle}°"
            text_surface = self.font.render(angle_text, True, self.colors['text'])
        
        text_rect = text_surface.get_rect(center=(self.display_width // 2, self.display_height - 30))
        self.display.blit(text_surface, text_rect)
    
    def _draw_trick_feedback(self):
        """Draw trick detection feedback on the display"""
        current_time = pygame.time.get_ticks() / 1000.0
        
        if self.trick_start_time > 0:
            # Calculate progress (0.0 to 1.0)
            progress = min((current_time - self.trick_start_time) / self.trick_hold_duration, 1.0)
            
            # Check what trick the current combination would be
            detected_trick = self._check_trick_combination()
            
            # Draw combination info at top center
            if detected_trick:
                combo_text = f"Trick: {detected_trick}"
                text_color = self.colors['accent']  # Green for valid trick
            else:
                combo_text = f"Combo: {self.hands[0]} + {self.hands[1]}"
                text_color = self.colors['warning']  # Yellow for invalid combo
            
            text_surface = self.title_font.render(combo_text, True, text_color)
            text_rect = text_surface.get_rect(center=(self.display_width // 2, 50))
            self.display.blit(text_surface, text_rect)
            
            # Draw progress bar
            bar_width = 400
            bar_height = 20
            bar_x = (self.display_width - bar_width) // 2
            bar_y = 100
            
            # Background bar
            pygame.draw.rect(self.display, self.colors['progress_bg'], (bar_x, bar_y, bar_width, bar_height))
            
            # Progress bar
            progress_width = int(bar_width * progress)
            color = self.colors['accent'] if progress >= 1.0 else self.colors['warning']  # Green when complete, yellow when in progress
            pygame.draw.rect(self.display, color, (bar_x, bar_y, progress_width, bar_height))
            
            # Border
            pygame.draw.rect(self.display, self.colors['border'], (bar_x, bar_y, bar_width, bar_height), 2)
    
    def run(self):
        """Run the main application loop"""
        clock = pygame.time.Clock()
        running = True
        
        # Render initial frame with floor
        self.render_board(*self.angle)
        
        print("Skateboard Display App")
        print("Controls:")
        print("  Left Hand: W(up) A(left) S(down) D(right)")
        print("  Right Hand: I(up) J(left) K(down) L(right)")
        print("  ESC: Exit")
        print("  R: Reset angle")
        
        while running:
            # Check for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_r:
                        self.set_angle(*self.default_angle)
                        print(f"Reset to default angle: {self.default_angle}")
                    # Left hand controls
                    elif event.key == pygame.K_w:
                        self.keys_pressed['w'] = True
                    elif event.key == pygame.K_a:
                        self.keys_pressed['a'] = True
                    elif event.key == pygame.K_s:
                        self.keys_pressed['s'] = True
                    elif event.key == pygame.K_d:
                        self.keys_pressed['d'] = True
                    # Right hand controls
                    elif event.key == pygame.K_i:
                        self.keys_pressed['i'] = True
                    elif event.key == pygame.K_j:
                        self.keys_pressed['j'] = True
                    elif event.key == pygame.K_k:
                        self.keys_pressed['k'] = True
                    elif event.key == pygame.K_l:
                        self.keys_pressed['l'] = True
                elif event.type == pygame.KEYUP:
                    # Left hand controls
                    if event.key == pygame.K_w:
                        self.keys_pressed['w'] = False
                    elif event.key == pygame.K_a:
                        self.keys_pressed['a'] = False
                    elif event.key == pygame.K_s:
                        self.keys_pressed['s'] = False
                    elif event.key == pygame.K_d:
                        self.keys_pressed['d'] = False
                    # Right hand controls
                    elif event.key == pygame.K_i:
                        self.keys_pressed['i'] = False
                    elif event.key == pygame.K_j:
                        self.keys_pressed['j'] = False
                    elif event.key == pygame.K_k:
                        self.keys_pressed['k'] = False
                    elif event.key == pygame.K_l:
                        self.keys_pressed['l'] = False
            
            # Update hand regions based on keyboard input
            self._update_keyboard_controls()
            
            # Update trick detection
            current_time = pygame.time.get_ticks() / 1000.0  # Convert to seconds
            self._update_trick_detection(current_time)
            
            # Update airborne state (spinning, landing)
            self._update_airborne_state()
            
            # Update rails
            self._update_rails()
            
            # Check for rail spawning
            current_time = pygame.time.get_ticks() / 1000.0
            if current_time - self.last_rail_spawn >= random.uniform(*self.rail_spawn_interval):
                self._spawn_rail()
                self.last_rail_spawn = current_time
            
            # Render current angle
            self.render_board(*self.angle)
            
            clock.tick(60)  # 60 FPS
        
        pygame.quit()

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
