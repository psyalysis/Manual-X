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
        
        # Get display info for multi-monitor support
        pygame.display.init()
        display_info = pygame.display.Info()
        
        # Try to use second monitor with proper resolution detection
        try:
            # First, try to get the second monitor's resolution by creating a temporary display
            temp_display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, display=1)
            temp_width = temp_display.get_width()
            temp_height = temp_display.get_height()
            pygame.display.quit()
            pygame.init()
            
            # Now create the actual display with the detected resolution
            self.display = pygame.display.set_mode((temp_width, temp_height), pygame.NOFRAME, display=1)
            print(f"Using second monitor (display=1) with detected resolution: {temp_width}x{temp_height}")
            self.fullscreen = False
        except:
            try:
                # Fallback to fullscreen on second monitor
                self.display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, display=1)
                print("Using second monitor (display=1) with full resolution")
                self.fullscreen = True
            except:
                try:
                    # Fallback to primary monitor with full resolution
                    self.display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    print("Using primary monitor with full resolution")
                    self.fullscreen = True
                except:
                    # Final fallback with high resolution
                    self.display = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
                    print("Using fallback resolution (1920x1080)")
                    self.fullscreen = True
        
        # Get actual screen dimensions
        self.display_width = self.display.get_width()
        self.display_height = self.display.get_height()
        print(f"Display resolution: {self.display_width}x{self.display_height}")
        
        pygame.display.set_caption("Random Skateboard Display")
        
        # Colors
        self.colors = {
            'background': (0, 0, 0, 0),  # Transparent background
            'text': (255, 255, 255),
            'border': (100, 100, 100)
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
        
        self._load_sprite_map()
        self._load_metadata()
        
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
        self.spin_interval = 0.05  # Spin every 0.1 seconds
        self.spin_speed = 1

        # Single angle setting
        self.default_angle = (0, 90, 0)
        self.angle = self.default_angle  # (x_angle, y_angle, z_angle)
        
        # Scale factor for fullscreen display - make it much bigger
        self.scale_factor = max(self.display_width, self.display_height) / 75  # Much larger scale
        
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
                    if detected_trick == "Ollie":
                        self.set_angle(30, 90, 0)
                    elif detected_trick == "Nollie":
                        self.set_angle(-30, 90, 0)
                        
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
        
        # Set airborne state and store trick info
        self.scale_factor *= 1.2
        self.airborne = True
        self.current_trick_name = trick_name
        self.trick_start_angle = self.angle
        self.landing_angle = self.angle
    
    def _update_airborne_state(self):
        """Update the board's airborne state and spinning"""
        if not self.airborne:
            return

        # Play wheels rolling sound while airborne
        if self.sounds['WheelsRolling.wav']:
            if not pygame.mixer.Channel(5).get_busy():
                pygame.mixer.Channel(5).play(self.sounds['WheelsRolling.wav'], loops=-1)

        # Check if keys are still held (not both center)
        if self.hands[0] == "center" and self.hands[1] == "center":
            # Keys released - land the board
            self.airborne = False
            self.scale_factor = max(self.display_width, self.display_height) / 75
            self.angle = self.landing_angle

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
            
            print(f"Landed: {self.angle}")
            self.landing_angle = self.angle

            self.set_angle(0, 90, 0)
        else:
            # Keys still held - continue spinning
            self._spin_board_in_air()
    
    def _spin_board_in_air(self):
        """Spin the board according to the current trick every 0.05 seconds"""
        if not hasattr(self, 'current_trick_name'):
            return
        
        current_time = pygame.time.get_ticks() / 1000.0
        
        # Check if enough time has passed since last spin
        if current_time - self.last_spin_time < self.spin_interval:
            return
        
        trick_name = self.current_trick_name
        
        # Define spin rates for different tricks (degrees per 0.1 seconds)
        # At (0, 90, 0): tail left, nose right, griptape facing camera
        # Y axis = kickflipping (vertical flips), Z axis = shuv-its (horizontal spins)
        spin_rates = {
            "Ollie": (5, 0, 0),  # No spin
            "Nollie": (-5, 0, 0),  # No spin
            "BS-Shuv-It": (-15, 15, 0),  # Backside shuv - X rotation (horizontal spin)
            "FS-Shuv-It": (15, 15, 0),  # Frontside shuv - X rotation (opposite direction)
            "Nollie BS-Shuv-It": (15, 0, 0),  # Nollie backside shuv
            "Nollie FS-Shuv-It": (-15, 0, 0),  # Nollie frontside shuv
            "Kickflip": (0, 30, 0),  # Kickflip - Y rotation (vertical flip)
            "Heelflip": (0, -30, 0),  # Heelflip - Y rotation (opposite direction)
            "Nollie Kickflip": (0, 30, 0),  # Nollie kickflip
            "Nollie Heelflip": (0, 30, 0),  # Nollie heelflip
            "Varial Kickflip": (0, 15, 15),  # Varial kickflip - both Y and Z
            "Varial Heelflip": (0, -15, -15),  # Varial heelflip - both Y and Z
            "Inward Heelflip": (0, -15, 15),  # Inward heelflip
            "Hardflip": (0, 15, -15)  # Hardflip
        }
        
        if trick_name in spin_rates:
            
            x_spin, y_spin, z_spin = spin_rates[trick_name]
            # Apply rotation to current angle
            new_x = (self.angle[0] + (x_spin * self.spin_speed)) % 360
            new_y = (self.angle[1] + (y_spin * self.spin_speed)) % 360
            new_z = (self.angle[2] + (z_spin * self.spin_speed)) % 360
            if trick_name == "Ollie":
                self.set_angle(self.angle[0] + 5, 90, 0)
            elif trick_name == "Nollie":
                self.set_angle(self.angle[0] - 5, 90, 0)
            else:
                self.set_angle(new_x, new_y, new_z)
            
            # Update last spin time
            self.last_spin_time = current_time
    
    def render_board(self, x_angle: float, y_angle: float, z_angle: float, 
                    center_x: int = None, center_y: int = None, 
                    scale: float = None) -> bool:
        """Render the board sprite at the specified angles"""
        # Use default scale if not provided
        if scale is None:
            scale = self.scale_factor
            
        # Get sprite position from sprite map
        sprite_pos = self.get_sprite_position(x_angle, y_angle, z_angle)
        
        if sprite_pos is None:
            print(f"No sprite found for angles: x={x_angle}, y={y_angle}, z={z_angle}")
            return False
        
        # Clear display - try to make it transparent for projector
        if not self.fullscreen:
            # For windowed mode, try to make background transparent
            self.display.fill((0, 0, 0, 0))  # Transparent background
        else:
            # For fullscreen, we can't have true transparency
            self.display.fill((0, 0, 0))  # Black background
        
        # Set default center position
        if center_x is None:
            center_x = self.display_width // 2
        if center_y is None:
            center_y = self.display_height // 2
        
        # Extract sprite from sprite map
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
        
        # Draw hand position indicators at preset locations
        self._draw_hand_position_indicators()
        
        # Draw angle information
        self._draw_angle_info(x_angle, y_angle, z_angle)
        
        # Draw trick detection feedback
        self._draw_trick_feedback()
        
        # Update display
        pygame.display.flip()
        
        return True
    
    def _draw_hand_position_indicators(self):
        """Draw hand position indicators"""
        # Circle properties
        circle_radius = 40
        
        # Left hand positions (left side of screen)
        left_hand_positions = {
            "center": (self.display_width // 4 + 40, self.display_height // 2),
            "up": (self.display_width // 4 + 40, self.display_height // 4),
            "down": (self.display_width // 4 + 40, 3 * self.display_height // 4),
            "left": (self.display_width // 8 + 40, self.display_height // 2),
            "right": (3 * self.display_width // 8 + 40, self.display_height // 2)
        }
        
        # Right hand positions (right side of screen)
        right_hand_positions = {
            "center": (3 * self.display_width // 4 - 40, self.display_height // 2),
            "up": (3 * self.display_width // 4 - 40, self.display_height // 4),
            "down": (3 * self.display_width // 4 - 40, 3 * self.display_height // 4),
            "left": (5 * self.display_width // 8 - 40, self.display_height // 2),
            "right": (7 * self.display_width // 8 - 40, self.display_height // 2)
        }
        
        # Draw left hand indicator (red) on left side
        if self.hands[0] in left_hand_positions:
            screen_x, screen_y = left_hand_positions[self.hands[0]]
            pygame.draw.circle(self.display, (255, 0, 0), (screen_x, screen_y), circle_radius)
            pygame.draw.circle(self.display, (200, 0, 0), (screen_x, screen_y), circle_radius, 5)
        
        # Draw right hand indicator (cyan) on right side
        if self.hands[1] in right_hand_positions:
            screen_x, screen_y = right_hand_positions[self.hands[1]]
            pygame.draw.circle(self.display, (0, 255, 255), (screen_x, screen_y), circle_radius)
            pygame.draw.circle(self.display, (0, 200, 200), (screen_x, screen_y), circle_radius, 5)
    
    
    
    
    def _draw_angle_info(self, x_angle: float, y_angle: float, z_angle: float):
        """Draw angle information on the display"""
        # Only show angle information at bottom
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
                text_color = (0, 255, 0)  # Green for valid trick
            else:
                combo_text = f"Combo: {self.hands[0]} + {self.hands[1]}"
                text_color = (255, 255, 0)  # Yellow for invalid combo
            
            text_surface = self.title_font.render(combo_text, True, text_color)
            text_rect = text_surface.get_rect(center=(self.display_width // 2, 50))
            self.display.blit(text_surface, text_rect)
            
            # Draw progress bar
            bar_width = 400
            bar_height = 20
            bar_x = (self.display_width - bar_width) // 2
            bar_y = 100
            
            # Background bar
            pygame.draw.rect(self.display, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
            
            # Progress bar
            progress_width = int(bar_width * progress)
            color = (0, 255, 0) if progress >= 1.0 else (255, 255, 0)  # Green when complete, yellow when in progress
            pygame.draw.rect(self.display, color, (bar_x, bar_y, progress_width, bar_height))
            
            # Border
            pygame.draw.rect(self.display, (200, 200, 200), (bar_x, bar_y, bar_width, bar_height), 2)
    
    def run(self):
        """Run the main application loop"""
        clock = pygame.time.Clock()
        running = True
        
        # Render initial angle
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
