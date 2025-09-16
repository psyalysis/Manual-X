#!/usr/bin/env python3
"""
Create animations using the new shuv/flip sprite map
"""

import pygame
import os
from typing import Dict, List, Tuple

class ShuvFlipAnimationGenerator:
    def __init__(self):
        """Initialize the animation generator"""
        pygame.init()
        pygame.display.set_mode((1, 1))  # Minimal display for image processing
        
        # Load the new sprite map
        self.sprite_map = pygame.image.load("generated_sprites/shuv_flip_sprite_map.png").convert_alpha()
        self.sprite_size = 128
        self.grid_width = 24
        self.grid_height = 24
        
        # Load metadata
        self.sprite_metadata = self._load_metadata()
        
        # Define trick animations with shuv/flip angle sequences
        self.trick_animations = self._define_trick_animations()
        
        # Create animations directory
        if not os.path.exists("animations"):
            os.makedirs("animations")
    
    def _load_metadata(self) -> Dict[str, Tuple[int, int]]:
        """Load sprite metadata from file"""
        metadata = {}
        try:
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
                                    metadata[angle_key] = (int(row), int(col))
                                except ValueError:
                                    continue
        except Exception as e:
            print(f"Error loading metadata: {e}")
        
        return metadata
    
    def _define_trick_animations(self) -> Dict[str, List[str]]:
        """Define the sprite sequences for each trick animation using shuv/flip angles"""
        return {
            "Ollie": [
                "0_0",      # Start position
                "0_15",     # Pop up
                "0_30",     # Peak
                "0_15",     # Coming down
                "0_0"       # Landing
            ],
            "Nollie": [
                "0_0",      # Start position
                "345_0",    # Pop up (fakie)
                "330_0",    # Peak (fakie)
                "345_0",    # Coming down (fakie)
                "0_0"       # Landing
            ],
            "BS-Shuv-It": [
                "0_0",      # Start
                "15_0",     # Begin shuv
                "30_0",     # Mid shuv
                "45_0",     # Continue shuv
                "60_0",     # More shuv
                "75_0",     # Almost complete
                "90_0",     # Complete shuv
                "105_0",    # Continue
                "120_0",    # Continue
                "135_0",    # Continue
                "150_0",    # Continue
                "165_0",    # Continue
                "180_0",    # Half rotation
                "195_0",    # Continue
                "210_0",    # Continue
                "225_0",    # Continue
                "240_0",    # Continue
                "255_0",    # Continue
                "270_0",    # Continue
                "285_0",    # Continue
                "300_0",    # Continue
                "315_0",    # Continue
                "330_0",    # Continue
                "345_0",    # Almost back
                "0_0"       # Complete rotation
            ],
            "FS-Shuv-It": [
                "0_0",      # Start
                "345_0",    # Begin shuv (reverse)
                "330_0",    # Mid shuv
                "315_0",    # Continue shuv
                "300_0",    # More shuv
                "285_0",    # Almost complete
                "270_0",    # Complete shuv
                "255_0",    # Continue
                "240_0",    # Continue
                "225_0",    # Continue
                "210_0",    # Continue
                "195_0",    # Continue
                "180_0",    # Half rotation
                "165_0",    # Continue
                "150_0",    # Continue
                "135_0",    # Continue
                "120_0",    # Continue
                "105_0",    # Continue
                "90_0",     # Continue
                "75_0",     # Continue
                "60_0",     # Continue
                "45_0",     # Continue
                "30_0",     # Continue
                "15_0",     # Almost back
                "0_0"       # Complete rotation
            ],
            "Kickflip": [
                "0_0",      # Start
                "0_345",    # Begin flip (backside - heelflip direction)
                "0_330",    # Quarter flip
                "0_315",    # Half flip
                "0_300",    # Three quarter flip
                "0_285",    # Almost complete
                "0_270",    # Complete flip
                "0_255",    # Continue
                "0_240",    # Continue
                "0_225",    # Continue
                "0_210",    # Continue
                "0_195",    # Continue
                "0_180",    # Continue
                "0_165",    # Continue
                "0_150",    # Continue
                "0_135",    # Continue
                "0_120",    # Continue
                "0_105",    # Continue
                "0_90",     # Continue
                "0_75",     # Continue
                "0_60",     # Continue
                "0_45",     # Continue
                "0_30",     # Continue
                "0_15",     # Almost back
                "0_0"       # Back to start
            ],
            "Heelflip": [
                "0_0",      # Start
                "0_15",     # Begin flip (frontside - kickflip direction)
                "0_30",     # Quarter flip
                "0_45",     # Half flip
                "0_60",     # Three quarter flip
                "0_75",     # Almost complete
                "0_90",     # Complete flip
                "0_105",    # Continue
                "0_120",    # Continue
                "0_135",    # Continue
                "0_150",    # Continue
                "0_165",    # Continue
                "0_180",    # Continue
                "0_195",    # Continue
                "0_210",    # Continue
                "0_225",    # Continue
                "0_240",    # Continue
                "0_255",    # Continue
                "0_270",    # Continue
                "0_285",    # Continue
                "0_300",    # Continue
                "0_315",    # Continue
                "0_330",    # Continue
                "0_345",    # Almost back
                "0_0"       # Back to start
            ],
            "Varial Heelflip": [
                "0_0",      # Start
                "345_30",   # Begin flip + shuv (frontside flip, double speed)
                "330_60",   # Quarter flip + shuv
                "315_90",   # Half flip + shuv
                "300_120",  # Three quarter flip + shuv
                "285_150",  # Almost complete
                "270_180",  # Complete flip + shuv (180° shuv, 360° flip)
                "255_210",  # Continue
                "240_240",  # Continue
                "225_270",  # Continue
                "210_300",  # Continue
                "195_330",  # Continue
                "180_0"     # Complete 180° shuv, back to start flip
            ],
            "Hardflip": [
                "0_0",      # Start
                "345_330",  # Begin flip + shuv (frontside flip, double speed)
                "330_300",  # Quarter flip + shuv
                "315_270",  # Half flip + shuv
                "300_240",  # Three quarter flip + shuv
                "285_210",  # Almost complete
                "270_180",  # Complete flip + shuv (180° shuv, 360° flip)
                "255_150",  # Continue
                "240_120",  # Continue
                "225_90",   # Continue
                "210_60",   # Continue
                "195_30",   # Continue
                "180_0"     # Complete 180° shuv, back to start flip
            ],
            "Varial Kickflip": [
                "0_0",      # Start
                "15_330",   # Begin flip + shuv (backside flip, double speed)
                "30_300",   # Quarter flip + shuv
                "45_270",   # Half flip + shuv
                "60_240",   # Three quarter flip + shuv
                "75_210",   # Almost complete
                "90_180",   # Complete flip + shuv (180° shuv, 360° flip)
                "105_150",  # Continue
                "120_120",  # Continue
                "135_90",   # Continue
                "150_60",   # Continue
                "165_30",   # Continue
                "180_0"     # Complete 180° shuv, back to start flip
            ],
            "Inward Heelflip": [
                "0_0",      # Start
                "15_30",    # Begin flip + shuv (backside flip, double speed)
                "30_60",    # Quarter flip + shuv
                "45_90",    # Half flip + shuv
                "60_120",   # Three quarter flip + shuv
                "75_150",   # Almost complete
                "90_180",   # Complete flip + shuv (180° shuv, 360° flip)
                "105_210",  # Continue
                "120_240",  # Continue
                "135_270",  # Continue
                "150_300",  # Continue
                "165_330",  # Continue
                "180_0"     # Complete 180° shuv, back to start flip
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
            f.write("Frame sequence (shuv_flip):\n")
            f.write("-" * 20 + "\n")
            for i, angle_key in enumerate(sprite_sequence):
                f.write(f"Frame {i:2d}: {angle_key}\n")
        
        return filename
    
    def generate_all_animations(self):
        """Generate sprite maps for all trick animations"""
        print("Generating shuv/flip animations...")
        
        for trick_name, sprite_sequence in self.trick_animations.items():
            print(f"Creating animation for: {trick_name}")
            filename = self.create_animation_sprite_map(trick_name, sprite_sequence)
            print(f"  Saved: {filename}")
        
        print(f"\nGenerated {len(self.trick_animations)} animation sprite maps in 'animations' folder")
        
        # Create a master index file
        index_filename = "animations/index.txt"
        with open(index_filename, 'w') as f:
            f.write("Shuv-Flip Animation Sprite Maps Index\n")
            f.write("=" * 40 + "\n\n")
            f.write("Available animations:\n")
            f.write("-" * 20 + "\n")
            for trick_name in self.trick_animations.keys():
                filename = f"{trick_name.replace(' ', '_').replace('-', '_')}.png"
                f.write(f"{trick_name:20s} -> {filename}\n")
        
        print(f"Created index file: {index_filename}")

def main():
    """Main function"""
    try:
        generator = ShuvFlipAnimationGenerator()
        generator.generate_all_animations()
        print("\nAnimation generation complete!")
    except Exception as e:
        print(f"Error: {e}")
        pygame.quit()

if __name__ == "__main__":
    main()
