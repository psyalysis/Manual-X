#!/usr/bin/env python3
"""
Create organized sprite map from shuv/flip angle sprites
Generates a sprite map with shuv angles (Z-axis) and flip angles (X-axis)
"""

import pygame
import os
import glob
from typing import Dict, Tuple, List

class ShuvFlipSpriteMapGenerator:
    def __init__(self, sprites_dir="sprites"):
        """Initialize the sprite map generator"""
        pygame.init()
        pygame.display.set_mode((1, 1))  # Minimal display for image processing
        
        self.sprites_dir = sprites_dir
        self.sprite_size = 128  # Size of individual sprites
        self.sprites_per_row = 24  # 24 shuv angles per row
        self.sprites_per_col = 24  # 24 flip angles per column
        
        # Create output directory
        if not os.path.exists("generated_sprites"):
            os.makedirs("generated_sprites")
    
    def parse_filename(self, filename: str) -> Tuple[int, int]:
        """Parse filename to extract shuv and flip angles"""
        # Expected format: shuv000_barrel000.png
        try:
            name = filename.replace('.png', '')
            if '_' in name:
                parts = name.split('_')
                if len(parts) == 2:
                    shuv_part = parts[0].replace('shuv', '')
                    flip_part = parts[1].replace('barrel', '')
                    shuv_angle = int(shuv_part)
                    flip_angle = int(flip_part)
                    return shuv_angle, flip_angle
        except (ValueError, IndexError):
            pass
        return None, None
    
    def load_sprites(self) -> Dict[Tuple[int, int], pygame.Surface]:
        """Load all sprites and organize by shuv/flip angles"""
        sprites = {}
        
        if not os.path.exists(self.sprites_dir):
            print(f"Error: Sprites directory '{self.sprites_dir}' not found!")
            return sprites
        
        # Get all PNG files in the sprites directory
        pattern = os.path.join(self.sprites_dir, "*.png")
        sprite_files = glob.glob(pattern)
        
        print(f"Found {len(sprite_files)} sprite files")
        
        for sprite_file in sprite_files:
            filename = os.path.basename(sprite_file)
            shuv_angle, flip_angle = self.parse_filename(filename)
            
            if shuv_angle is not None and flip_angle is not None:
                try:
                    sprite = pygame.image.load(sprite_file).convert_alpha()
                    # Ensure the sprite has proper alpha channel
                    if sprite.get_flags() & pygame.SRCALPHA:
                        sprites[(shuv_angle, flip_angle)] = sprite
                        print(f"Loaded: {filename} -> Shuv:{shuv_angle}°, Flip:{flip_angle}°")
                    else:
                        # Convert to surface with alpha if needed
                        sprite_with_alpha = pygame.Surface(sprite.get_size(), pygame.SRCALPHA, 32)
                        sprite_with_alpha.blit(sprite, (0, 0))
                        sprites[(shuv_angle, flip_angle)] = sprite_with_alpha
                        print(f"Loaded (converted): {filename} -> Shuv:{shuv_angle}°, Flip:{flip_angle}°")
                except pygame.error as e:
                    print(f"Error loading {filename}: {e}")
        
        return sprites
    
    def create_sprite_map(self, sprites: Dict[Tuple[int, int], pygame.Surface]) -> pygame.Surface:
        """Create the organized sprite map"""
        # Calculate map dimensions
        map_width = self.sprites_per_row * self.sprite_size
        map_height = self.sprites_per_col * self.sprite_size
        
        # Create the sprite map surface with alpha channel
        sprite_map = pygame.Surface((map_width, map_height), pygame.SRCALPHA, 32)
        
        # Fill with transparent background
        sprite_map.fill((0, 0, 0, 0))
        
        # Place sprites in organized grid
        for (shuv_angle, flip_angle), sprite in sprites.items():
            # Calculate grid position
            # Shuv angles: 0, 15, 30, ..., 345 (24 angles)
            # Flip angles: 0, 15, 30, ..., 345 (24 angles)
            
            shuv_index = shuv_angle // 15
            flip_index = flip_angle // 15
            
            # Ensure indices are within bounds
            if 0 <= shuv_index < self.sprites_per_row and 0 <= flip_index < self.sprites_per_col:
                x = shuv_index * self.sprite_size
                y = flip_index * self.sprite_size
                
                # Resize sprite if needed
                if sprite.get_size() != (self.sprite_size, self.sprite_size):
                    sprite = pygame.transform.scale(sprite, (self.sprite_size, self.sprite_size))
                
                # Blit sprite to map
                sprite_map.blit(sprite, (x, y))
        
        return sprite_map
    
    def create_metadata(self, sprites: Dict[Tuple[int, int], pygame.Surface]) -> str:
        """Create metadata file for the sprite map"""
        metadata_content = []
        metadata_content.append("Shuv-Flip Sprite Map Metadata")
        metadata_content.append("=" * 40)
        metadata_content.append("")
        metadata_content.append(f"Grid dimensions: {self.sprites_per_row}x{self.sprites_per_col}")
        metadata_content.append(f"Sprite size: {self.sprite_size}x{self.sprite_size}")
        metadata_content.append(f"Total sprites: {len(sprites)}")
        metadata_content.append("")
        metadata_content.append("Sprite positions (shuv_angle,flip_angle -> row,col):")
        metadata_content.append("-" * 50)
        
        # Create mapping for each sprite
        for (shuv_angle, flip_angle) in sorted(sprites.keys()):
            shuv_index = shuv_angle // 15
            flip_index = flip_angle // 15
            
            if 0 <= shuv_index < self.sprites_per_row and 0 <= flip_index < self.sprites_per_col:
                metadata_content.append(f"{shuv_angle}_{flip_angle} -> {flip_index},{shuv_index}")
        
        return "\n".join(metadata_content)
    
    def generate_sprite_map(self):
        """Generate the complete sprite map and metadata"""
        print("Loading sprites...")
        sprites = self.load_sprites()
        
        if not sprites:
            print("No sprites found! Make sure the sprites directory exists and contains PNG files.")
            return
        
        print(f"Creating sprite map with {len(sprites)} sprites...")
        sprite_map = self.create_sprite_map(sprites)
        
        # Save sprite map
        sprite_map_path = "generated_sprites/shuv_flip_sprite_map.png"
        pygame.image.save(sprite_map, sprite_map_path)
        print(f"Saved sprite map: {sprite_map_path}")
        
        # Create and save metadata
        metadata_content = self.create_metadata(sprites)
        metadata_path = "generated_sprites/shuv_flip_sprite_map_metadata.txt"
        with open(metadata_path, 'w') as f:
            f.write(metadata_content)
        print(f"Saved metadata: {metadata_path}")
        
        # Create angle mapping for easy lookup
        self.create_angle_mapping(sprites)
        
        print(f"\nSprite map generation complete!")
        print(f"Map size: {sprite_map.get_width()}x{sprite_map.get_height()}")
        print(f"Sprites: {len(sprites)}/{self.sprites_per_row * self.sprites_per_col}")
    
    def create_angle_mapping(self, sprites: Dict[Tuple[int, int], pygame.Surface]):
        """Create a mapping file for easy angle lookup"""
        mapping_content = []
        mapping_content.append("Shuv-Flip Angle Mapping")
        mapping_content.append("=" * 30)
        mapping_content.append("")
        mapping_content.append("Format: shuv_angle,flip_angle -> row,col")
        mapping_content.append("")
        
        for (shuv_angle, flip_angle) in sorted(sprites.keys()):
            shuv_index = shuv_angle // 15
            flip_index = flip_angle // 15
            
            if 0 <= shuv_index < self.sprites_per_row and 0 <= flip_index < self.sprites_per_col:
                mapping_content.append(f"{shuv_angle},{flip_angle} -> {flip_index},{shuv_index}")
        
        mapping_path = "generated_sprites/angle_mapping.txt"
        with open(mapping_path, 'w') as f:
            f.write("\n".join(mapping_content))
        print(f"Saved angle mapping: {mapping_path}")

def main():
    """Main function"""
    generator = ShuvFlipSpriteMapGenerator()
    generator.generate_sprite_map()

if __name__ == "__main__":
    main()
