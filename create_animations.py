#!/usr/bin/env python3
"""
Animation Sprite Map Generator

Creates individual sprite maps for each trick animation by extracting
relevant sprites from the main sprite map and organizing them into
looping animations.
"""

import pygame
import os
from typing import Dict, List, Tuple

class AnimationGenerator:
    def __init__(self):
        """Initialize the animation generator"""
        pygame.init()
        pygame.display.set_mode((1, 1))  # Minimal display for image processing
        
        # Load the main sprite map
        self.sprite_map = pygame.image.load("skateboard_sprite_map.png").convert_alpha()
        self.sprite_size = 64
        self.grid_size = 118
        
        # Load metadata
        self.sprite_metadata = self._load_metadata()
        
        # Define trick animations with their sprite sequences
        self.trick_animations = self._define_trick_animations()
        
        # Create animations directory
        if not os.path.exists("animations"):
            os.makedirs("animations")
    
    def _load_metadata(self) -> Dict[str, Tuple[int, int]]:
        """Load sprite metadata from file"""
        metadata = {}
        try:
            with open("sprite_map_metadata.txt", 'r') as f:
                for line in f:
                    if " -> " in line and not line.startswith("Sprite positions"):
                        parts = line.split(" -> ")
                        if len(parts) == 2:
                            angle_key = parts[0].strip()
                            position = parts[1].strip()
                            
                            if "," in position and not angle_key.startswith("Sprite positions"):
                                try:
                                    row, col = position.split(",")
                                    metadata[angle_key] = (int(row), int(col))
                                except ValueError:
                                    continue
        except Exception as e:
            print(f"Error loading metadata: {e}")
        
        return metadata
    
    def _define_trick_animations(self) -> Dict[str, List[str]]:
        """Define the sprite sequences for each trick animation"""
        return {
            "Ollie": [
                "0.0_90.0_0.0",    # Start position
                "15.0_90.0_0.0",   # Pop up
                "30.0_90.0_0.0",   # Peak
                "15.0_90.0_0.0",   # Coming down
                "0.0_90.0_0.0"     # Landing
            ],
            "Nollie": [
                "0.0_90.0_0.0",    # Start position
                "-15.0_90.0_0.0",  # Pop up
                "-30.0_90.0_0.0",  # Peak
                "-15.0_90.0_0.0",  # Coming down
                "0.0_90.0_0.0"     # Landing
            ],
            "BS-Shuv-It": [
                "0.0_90.0_0.0",    # Start
                "0.0_90.0_15.0",   # Begin shuv
                "0.0_90.0_30.0",   # Mid shuv
                "0.0_90.0_45.0",   # Continue shuv
                "0.0_90.0_60.0",   # More shuv
                "0.0_90.0_75.0",   # Almost complete
                "0.0_90.0_90.0",   # Complete shuv
                "0.0_90.0_105.0",  # Continue
                "0.0_90.0_120.0",  # Continue
                "0.0_90.0_135.0",  # Continue
                "0.0_90.0_150.0",  # Continue
                "0.0_90.0_165.0",  # Continue
                "0.0_90.0_180.0",  # Half rotation
                "0.0_90.0_195.0",  # Continue
                "0.0_90.0_210.0",  # Continue
                "0.0_90.0_225.0",  # Continue
                "0.0_90.0_240.0",  # Continue
                "0.0_90.0_255.0",  # Continue
                "0.0_90.0_270.0",  # Continue
                "0.0_90.0_285.0",  # Continue
                "0.0_90.0_300.0",  # Continue
                "0.0_90.0_315.0",  # Continue
                "0.0_90.0_330.0",  # Continue
                "0.0_90.0_345.0",  # Almost back
                "0.0_90.0_0.0"     # Complete rotation
            ],
            "FS-Shuv-It": [
                "0.0_90.0_0.0",    # Start
                "0.0_90.0_345.0",  # Begin shuv (reverse)
                "0.0_90.0_330.0",  # Mid shuv
                "0.0_90.0_315.0",  # Continue shuv
                "0.0_90.0_300.0",  # More shuv
                "0.0_90.0_285.0",  # Almost complete
                "0.0_90.0_270.0",  # Complete shuv
                "0.0_90.0_255.0",  # Continue
                "0.0_90.0_240.0",  # Continue
                "0.0_90.0_225.0",  # Continue
                "0.0_90.0_210.0",  # Continue
                "0.0_90.0_195.0",  # Continue
                "0.0_90.0_180.0",  # Half rotation
                "0.0_90.0_165.0",  # Continue
                "0.0_90.0_150.0",  # Continue
                "0.0_90.0_135.0",  # Continue
                "0.0_90.0_120.0",  # Continue
                "0.0_90.0_105.0",  # Continue
                "0.0_90.0_90.0",   # Continue
                "0.0_90.0_75.0",   # Continue
                "0.0_90.0_60.0",   # Continue
                "0.0_90.0_45.0",   # Continue
                "0.0_90.0_30.0",   # Continue
                "0.0_90.0_15.0",   # Almost back
                "0.0_90.0_0.0"     # Complete rotation
            ],
            "Kickflip": [
                "0.0_90.0_0.0",    # Start
                "0.0_105.0_0.0",   # Begin flip
                "0.0_120.0_0.0",   # Quarter flip
                "0.0_135.0_0.0",   # Half flip
                "0.0_150.0_0.0",   # Three quarter flip
                "0.0_165.0_0.0",   # Almost complete
                "0.0_180.0_0.0",   # Complete flip
                "0.0_195.0_0.0",   # Continue
                "0.0_210.0_0.0",   # Continue
                "0.0_225.0_0.0",   # Continue
                "0.0_240.0_0.0",   # Continue
                "0.0_255.0_0.0",   # Continue
                "0.0_270.0_0.0",   # Continue
                "0.0_285.0_0.0",   # Continue
                "0.0_300.0_0.0",   # Continue
                "0.0_315.0_0.0",   # Continue
                "0.0_330.0_0.0",   # Continue
                "0.0_345.0_0.0",   # Almost back
                "0.0_0.0_0.0",     # Complete rotation
                "0.0_15.0_0.0",    # Continue
                "0.0_30.0_0.0",    # Continue
                "0.0_45.0_0.0",    # Continue
                "0.0_60.0_0.0",    # Continue
                "0.0_75.0_0.0",    # Continue
                "0.0_90.0_0.0"     # Back to start
            ],
            "Heelflip": [
                "0.0_90.0_0.0",    # Start
                "0.0_75.0_0.0",    # Begin flip (reverse)
                "0.0_60.0_0.0",    # Quarter flip
                "0.0_45.0_0.0",    # Half flip
                "0.0_30.0_0.0",    # Three quarter flip
                "0.0_15.0_0.0",    # Almost complete
                "0.0_0.0_0.0",     # Complete flip
                "0.0_345.0_0.0",   # Continue
                "0.0_330.0_0.0",   # Continue
                "0.0_315.0_0.0",   # Continue
                "0.0_300.0_0.0",   # Continue
                "0.0_285.0_0.0",   # Continue
                "0.0_270.0_0.0",   # Continue
                "0.0_255.0_0.0",   # Continue
                "0.0_240.0_0.0",   # Continue
                "0.0_225.0_0.0",   # Continue
                "0.0_210.0_0.0",   # Continue
                "0.0_195.0_0.0",   # Continue
                "0.0_180.0_0.0",   # Half rotation
                "0.0_165.0_0.0",   # Continue
                "0.0_150.0_0.0",   # Continue
                "0.0_135.0_0.0",   # Continue
                "0.0_120.0_0.0",   # Continue
                "0.0_105.0_0.0",   # Continue
                "0.0_90.0_0.0"     # Back to start
            ],
            "Nollie Kickflip": [
                "0.0_90.0_0.0",    # Start
                "-15.0_90.0_0.0",  # Nollie pop
                "-15.0_105.0_0.0", # Begin flip
                "-15.0_120.0_0.0", # Quarter flip
                "-15.0_135.0_0.0", # Half flip
                "-15.0_150.0_0.0", # Three quarter flip
                "-15.0_165.0_0.0", # Almost complete
                "-15.0_180.0_0.0", # Complete flip
                "-15.0_195.0_0.0", # Continue
                "-15.0_210.0_0.0", # Continue
                "-15.0_225.0_0.0", # Continue
                "-15.0_240.0_0.0", # Continue
                "-15.0_255.0_0.0", # Continue
                "-15.0_270.0_0.0", # Continue
                "-15.0_285.0_0.0", # Continue
                "-15.0_300.0_0.0", # Continue
                "-15.0_315.0_0.0", # Continue
                "-15.0_330.0_0.0", # Continue
                "-15.0_345.0_0.0", # Almost back
                "-15.0_0.0_0.0",   # Complete rotation
                "-15.0_15.0_0.0",  # Continue
                "-15.0_30.0_0.0",  # Continue
                "-15.0_45.0_0.0",  # Continue
                "-15.0_60.0_0.0",  # Continue
                "-15.0_75.0_0.0",  # Continue
                "0.0_90.0_0.0"     # Back to start
            ],
            "Nollie Heelflip": [
                "0.0_90.0_0.0",    # Start
                "-15.0_90.0_0.0",  # Nollie pop
                "-15.0_75.0_0.0",  # Begin flip (reverse)
                "-15.0_60.0_0.0",  # Quarter flip
                "-15.0_45.0_0.0",  # Half flip
                "-15.0_30.0_0.0",  # Three quarter flip
                "-15.0_15.0_0.0",  # Almost complete
                "-15.0_0.0_0.0",   # Complete flip
                "-15.0_345.0_0.0", # Continue
                "-15.0_330.0_0.0", # Continue
                "-15.0_315.0_0.0", # Continue
                "-15.0_300.0_0.0", # Continue
                "-15.0_285.0_0.0", # Continue
                "-15.0_270.0_0.0", # Continue
                "-15.0_255.0_0.0", # Continue
                "-15.0_240.0_0.0", # Continue
                "-15.0_225.0_0.0", # Continue
                "-15.0_210.0_0.0", # Continue
                "-15.0_195.0_0.0", # Continue
                "-15.0_180.0_0.0", # Half rotation
                "-15.0_165.0_0.0", # Continue
                "-15.0_150.0_0.0", # Continue
                "-15.0_135.0_0.0", # Continue
                "-15.0_120.0_0.0", # Continue
                "-15.0_105.0_0.0", # Continue
                "0.0_90.0_0.0"     # Back to start
            ],
            "Varial Kickflip": [
                "0.0_90.0_0.0",    # Start
                "0.0_105.0_15.0",  # Begin flip + shuv
                "0.0_120.0_30.0",  # Quarter flip + shuv
                "0.0_135.0_45.0",  # Half flip + shuv
                "0.0_150.0_60.0",  # Three quarter flip + shuv
                "0.0_165.0_75.0",  # Almost complete
                "0.0_180.0_90.0",  # Complete flip + shuv
                "0.0_195.0_105.0", # Continue
                "0.0_210.0_120.0", # Continue
                "0.0_225.0_135.0", # Continue
                "0.0_240.0_150.0", # Continue
                "0.0_255.0_165.0", # Continue
                "0.0_270.0_180.0", # Continue
                "0.0_285.0_195.0", # Continue
                "0.0_300.0_210.0", # Continue
                "0.0_315.0_225.0", # Continue
                "0.0_330.0_240.0", # Continue
                "0.0_345.0_255.0", # Almost back
                "0.0_0.0_270.0",   # Complete rotation
                "0.0_15.0_285.0",  # Continue
                "0.0_30.0_300.0",  # Continue
                "0.0_45.0_315.0",  # Continue
                "0.0_60.0_330.0",  # Continue
                "0.0_75.0_345.0",  # Continue
                "0.0_90.0_0.0"     # Back to start
            ],
            "Varial Heelflip": [
                "0.0_90.0_0.0",    # Start
                "0.0_75.0_345.0",  # Begin flip + shuv (reverse)
                "0.0_60.0_330.0",  # Quarter flip + shuv
                "0.0_45.0_315.0",  # Half flip + shuv
                "0.0_30.0_300.0",  # Three quarter flip + shuv
                "0.0_15.0_285.0",  # Almost complete
                "0.0_0.0_270.0",   # Complete flip + shuv
                "0.0_345.0_255.0", # Continue
                "0.0_330.0_240.0", # Continue
                "0.0_315.0_225.0", # Continue
                "0.0_300.0_210.0", # Continue
                "0.0_285.0_195.0", # Continue
                "0.0_270.0_180.0", # Continue
                "0.0_255.0_165.0", # Continue
                "0.0_240.0_150.0", # Continue
                "0.0_225.0_135.0", # Continue
                "0.0_210.0_120.0", # Continue
                "0.0_195.0_105.0", # Continue
                "0.0_180.0_90.0",  # Half rotation
                "0.0_165.0_75.0",  # Continue
                "0.0_150.0_60.0",  # Continue
                "0.0_135.0_45.0",  # Continue
                "0.0_120.0_30.0",  # Continue
                "0.0_105.0_15.0",  # Continue
                "0.0_90.0_0.0"     # Back to start
            ],
            "Inward Heelflip": [
                "0.0_90.0_0.0",    # Start
                "0.0_75.0_15.0",   # Begin flip + shuv
                "0.0_60.0_30.0",   # Quarter flip + shuv
                "0.0_45.0_45.0",   # Half flip + shuv
                "0.0_30.0_60.0",   # Three quarter flip + shuv
                "0.0_15.0_75.0",   # Almost complete
                "0.0_0.0_90.0",    # Complete flip + shuv
                "0.0_345.0_105.0", # Continue
                "0.0_330.0_120.0", # Continue
                "0.0_315.0_135.0", # Continue
                "0.0_300.0_150.0", # Continue
                "0.0_285.0_165.0", # Continue
                "0.0_270.0_180.0", # Continue
                "0.0_255.0_195.0", # Continue
                "0.0_240.0_210.0", # Continue
                "0.0_225.0_225.0", # Continue
                "0.0_210.0_240.0", # Continue
                "0.0_195.0_255.0", # Continue
                "0.0_180.0_270.0", # Half rotation
                "0.0_165.0_285.0", # Continue
                "0.0_150.0_300.0", # Continue
                "0.0_135.0_315.0", # Continue
                "0.0_120.0_330.0", # Continue
                "0.0_105.0_345.0", # Continue
                "0.0_90.0_0.0"     # Back to start
            ],
            "Hardflip": [
                "0.0_90.0_0.0",    # Start
                "0.0_105.0_345.0", # Begin flip + shuv (reverse)
                "0.0_120.0_330.0", # Quarter flip + shuv
                "0.0_135.0_315.0", # Half flip + shuv
                "0.0_150.0_300.0", # Three quarter flip + shuv
                "0.0_165.0_285.0", # Almost complete
                "0.0_180.0_270.0", # Complete flip + shuv
                "0.0_195.0_255.0", # Continue
                "0.0_210.0_240.0", # Continue
                "0.0_225.0_225.0", # Continue
                "0.0_240.0_210.0", # Continue
                "0.0_255.0_195.0", # Continue
                "0.0_270.0_180.0", # Continue
                "0.0_285.0_165.0", # Continue
                "0.0_300.0_150.0", # Continue
                "0.0_315.0_135.0", # Continue
                "0.0_330.0_120.0", # Continue
                "0.0_345.0_105.0", # Almost back
                "0.0_0.0_90.0",    # Complete rotation
                "0.0_15.0_75.0",   # Continue
                "0.0_30.0_60.0",   # Continue
                "0.0_45.0_45.0",   # Continue
                "0.0_60.0_30.0",   # Continue
                "0.0_75.0_15.0",   # Continue
                "0.0_90.0_0.0"     # Back to start
            ]
        }
    
    def get_sprite_position(self, angle_key: str) -> Tuple[int, int, int, int]:
        """Get sprite position from angle key"""
        if angle_key in self.sprite_metadata:
            row, col = self.sprite_metadata[angle_key]
            x = col * self.sprite_size
            y = row * self.sprite_size
            return (x, y, self.sprite_size, self.sprite_size)
        return None
    
    def create_animation_sprite_map(self, trick_name: str, sprite_sequence: List[str]) -> str:
        """Create a sprite map for a specific trick animation"""
        # Calculate dimensions for the sprite map
        num_frames = len(sprite_sequence)
        frames_per_row = min(8, num_frames)  # Max 8 frames per row
        rows = (num_frames + frames_per_row - 1) // frames_per_row
        
        # Create the animation sprite map surface
        map_width = frames_per_row * self.sprite_size
        map_height = rows * self.sprite_size
        animation_map = pygame.Surface((map_width, map_height), pygame.SRCALPHA)
        
        # Extract and place each sprite
        for i, angle_key in enumerate(sprite_sequence):
            sprite_pos = self.get_sprite_position(angle_key)
            if sprite_pos:
                x, y, w, h = sprite_pos
                sprite_rect = pygame.Rect(x, y, w, h)
                sprite_surface = self.sprite_map.subsurface(sprite_rect)
                
                # Calculate position in the animation map
                frame_x = (i % frames_per_row) * self.sprite_size
                frame_y = (i // frames_per_row) * self.sprite_size
                
                # Blit the sprite to the animation map
                animation_map.blit(sprite_surface, (frame_x, frame_y))
            else:
                print(f"Warning: No sprite found for angle {angle_key} in {trick_name}")
        
        # Save the animation sprite map
        filename = f"animations/{trick_name.replace(' ', '_').replace('-', '_')}.png"
        pygame.image.save(animation_map, filename)
        
        # Create metadata file for the animation
        metadata_filename = f"animations/{trick_name.replace(' ', '_').replace('-', '_')}_metadata.txt"
        with open(metadata_filename, 'w') as f:
            f.write(f"{trick_name} Animation Metadata\n")
            f.write("=" * 40 + "\n\n")
            f.write(f"Frames: {num_frames}\n")
            f.write(f"Frames per row: {frames_per_row}\n")
            f.write(f"Rows: {rows}\n")
            f.write(f"Sprite size: {self.sprite_size}x{self.sprite_size}\n\n")
            f.write("Frame sequence:\n")
            f.write("-" * 20 + "\n")
            for i, angle_key in enumerate(sprite_sequence):
                f.write(f"Frame {i:2d}: {angle_key}\n")
        
        return filename
    
    def generate_all_animations(self):
        """Generate sprite maps for all trick animations"""
        print("Generating animation sprite maps...")
        
        for trick_name, sprite_sequence in self.trick_animations.items():
            print(f"Creating animation for: {trick_name}")
            filename = self.create_animation_sprite_map(trick_name, sprite_sequence)
            print(f"  Saved: {filename}")
        
        print(f"\nGenerated {len(self.trick_animations)} animation sprite maps in 'animations' folder")
        
        # Create a master index file
        index_filename = "animations/index.txt"
        with open(index_filename, 'w') as f:
            f.write("Animation Sprite Maps Index\n")
            f.write("=" * 30 + "\n\n")
            f.write("Available animations:\n")
            f.write("-" * 20 + "\n")
            for trick_name in self.trick_animations.keys():
                filename = f"{trick_name.replace(' ', '_').replace('-', '_')}.png"
                f.write(f"{trick_name:20s} -> {filename}\n")
        
        print(f"Created index file: {index_filename}")

def main():
    """Main function"""
    try:
        generator = AnimationGenerator()
        generator.generate_all_animations()
        print("\nAnimation generation complete!")
    except Exception as e:
        print(f"Error: {e}")
        pygame.quit()

if __name__ == "__main__":
    main()
