#!/usr/bin/env python3
"""
Update the app to use the new shuv/flip sprite map system
"""

import re

def update_app_sprite_system():
    """Update the app.py file to use the new sprite system"""
    
    # Read the current app.py
    with open('app.py', 'r') as f:
        content = f.read()
    
    # Add new sprite map loading method
    new_sprite_loading = '''
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
'''
    
    # Find the _load_animations method and add the new sprite loading after it
    pattern = r'(def _load_animations\(self\):.*?)(\n    def )'
    replacement = r'\1\n' + new_sprite_loading + r'\2'
    
    updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # Add new sprite map loading to __init__
    init_pattern = r'(self\._load_animations\(\))'
    init_replacement = r'\1\n        self._load_new_sprite_map()'
    
    updated_content = re.sub(init_pattern, init_replacement, updated_content)
    
    # Write the updated content
    with open('app.py', 'w') as f:
        f.write(updated_content)
    
    print("Updated app.py with new sprite map system!")

if __name__ == "__main__":
    update_app_sprite_system()
