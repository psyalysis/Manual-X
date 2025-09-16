#!/usr/bin/env python3
"""
Level Texture Generator
Creates multiple asphalt texture variations for the skateboard game
"""

import pygame
import random
import os
import math

def create_asphalt_texture(width, height, pattern_type):
    """Create an asphalt texture with specified pattern and noise"""
    surface = pygame.Surface((width, height))
    
    # Base asphalt color (dark gray)
    base_color = (45, 45, 45)
    surface.fill(base_color)
    
    if pattern_type == "smooth":
        # Smooth asphalt with minimal variation
        for i in range(0, width, 50):
            for j in range(0, height, 50):
                variation = random.randint(-8, 8)
                color = (
                    max(0, min(255, base_color[0] + variation)),
                    max(0, min(255, base_color[1] + variation)),
                    max(0, min(255, base_color[2] + variation))
                )
                pygame.draw.rect(surface, color, (i, j, 50, 50), 0)
    
    elif pattern_type == "spider_cracks":
        # Smooth asphalt with medium variation
        for i in range(0, width, 50):
            for j in range(0, height, 50):
                variation = random.randint(-12, 12)
                color = (
                    max(0, min(255, base_color[0] + variation)),
                    max(0, min(255, base_color[1] + variation)),
                    max(0, min(255, base_color[2] + variation))
                )
                pygame.draw.rect(surface, color, (i, j, 50, 50), 0)
    
    elif pattern_type == "linear_cracks":
        # Smooth asphalt with high variation
        for i in range(0, width, 50):
            for j in range(0, height, 50):
                variation = random.randint(-15, 15)
                color = (
                    max(0, min(255, base_color[0] + variation)),
                    max(0, min(255, base_color[1] + variation)),
                    max(0, min(255, base_color[2] + variation))
                )
                pygame.draw.rect(surface, color, (i, j, 50, 50), 0)
    
    elif pattern_type == "alligator_cracks":
        # Smooth asphalt with small tile variation
        for i in range(0, width, 50):
            for j in range(0, height, 50):
                variation = random.randint(-10, 10)
                color = (
                    max(0, min(255, base_color[0] + variation)),
                    max(0, min(255, base_color[1] + variation)),
                    max(0, min(255, base_color[2] + variation))
                )
                pygame.draw.rect(surface, color, (i, j, 50, 50), 0)
    
    elif pattern_type == "patched_cracks":
        # Smooth asphalt with patch-like variations
        for i in range(0, width, 50):
            for j in range(0, height, 50):
                variation = random.randint(-12, 12)
                color = (
                    max(0, min(255, base_color[0] + variation)),
                    max(0, min(255, base_color[1] + variation)),
                    max(0, min(255, base_color[2] + variation))
                )
                pygame.draw.rect(surface, color, (i, j, 50, 50), 0)
        
        # Add patch-like areas with different shades
        for _ in range(5):
            x = random.randint(0, width - 70)
            y = random.randint(0, height - 50)
            patch_color = (55, 55, 55)
            pygame.draw.rect(surface, patch_color, (x, y, 70, 50), 0)
    
    elif pattern_type == "weathered_cracks":
        # Smooth asphalt with weathered texture variation
        for i in range(0, width, 50):
            for j in range(0, height, 50):
                variation = random.randint(-18, 18)
                color = (
                    max(0, min(255, base_color[0] + variation)),
                    max(0, min(255, base_color[1] + variation)),
                    max(0, min(255, base_color[2] + variation))
                )
                pygame.draw.rect(surface, color, (i, j, 50, 50), 0)
    
    elif pattern_type == "stress_cracks":
        # Smooth asphalt with stress pattern variation
        for i in range(0, width, 50):
            for j in range(0, height, 50):
                variation = random.randint(-14, 14)
                color = (
                    max(0, min(255, base_color[0] + variation)),
                    max(0, min(255, base_color[1] + variation)),
                    max(0, min(255, base_color[2] + variation))
                )
                pygame.draw.rect(surface, color, (i, j, 50, 50), 0)
    
    elif pattern_type == "random_cracks":
        # Smooth asphalt with random texture variation
        for i in range(0, width, 50):
            for j in range(0, height, 50):
                variation = random.randint(-16, 16)
                color = (
                    max(0, min(255, base_color[0] + variation)),
                    max(0, min(255, base_color[1] + variation)),
                    max(0, min(255, base_color[2] + variation))
                )
                pygame.draw.rect(surface, color, (i, j, 50, 50), 0)
    
    # No speckle noise - clean smooth textures
    
    return surface

def generate_levels():
    """Generate all level textures"""
    pygame.init()
    
    # Create levels directory if it doesn't exist
    if not os.path.exists("levels"):
        os.makedirs("levels")
        print("Created 'levels' directory")
    
    # Define patterns to generate
    patterns = [
        "smooth", "spider_cracks", "linear_cracks", "alligator_cracks",
        "patched_cracks", "weathered_cracks", "stress_cracks", "random_cracks"
    ]
    
    # Standard segment dimensions (will be scaled by the game)
    width = 1200  # Slightly wider than typical screen
    height = 200  # Floor height
    
    print(f"Generating {len(patterns)} asphalt texture patterns...")
    
    for i, pattern in enumerate(patterns):
        print(f"Generating {pattern}...")
        
        # Create texture with this pattern
        texture = create_asphalt_texture(width, height, pattern)
        
        # Save as PNG
        filename = f"levels/sprite_{i+1:03d}.png"
        pygame.image.save(texture, filename)
        print(f"Saved: {filename}")
    
    # Generate additional variations for more variety
    print("\nGenerating additional variations...")
    
    # Create 4 more variations
    for i in range(4):
        pattern = random.choice(patterns)
        
        texture = create_asphalt_texture(width, height, pattern)
        
        filename = f"levels/sprite_{len(patterns) + i + 1:03d}.png"
        pygame.image.save(texture, filename)
        print(f"Saved variation: {filename}")
    
    pygame.quit()
    print(f"\nGenerated {len(patterns) + 4} asphalt textures in 'levels' folder!")
    print("Textures are ready to use in your skateboard game.")

if __name__ == "__main__":
    generate_levels()
