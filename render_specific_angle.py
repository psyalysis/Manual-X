import bpy
import math
import os

# === SETTINGS ===
output_dir = bpy.path.abspath("C:/Users/DREAD/Desktop/Sidequests/manual-x/Manual-X/sprites")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# === SPECIFY YOUR ANGLE HERE ===
# Set these values to the angles you want to capture
TARGET_SHUV_ANGLE = 90    # Z-axis rotation (horizontal spin) in degrees
TARGET_BARREL_ANGLE = 45  # X-axis rotation (front-to-back flip) in degrees

# Select your actual object by name
if "Skateboard" not in bpy.data.objects:
    print("Error: 'Skateboard' object not found in scene!")
    print("Available objects:", [obj.name for obj in bpy.data.objects])
    exit()

obj = bpy.data.objects["Skateboard"]  # Change to your object name

# === RENDER SETTINGS ===
# Note: Make sure to set these manually in Blender before running the script:
# - File Format: PNG
# - Color Mode: RGBA
# - Film Transparent: ON
# - Resolution: 48x48
# - Camera Type: Orthographic

scene = bpy.context.scene

# === MAIN RENDERING ===
# Clear any existing animation data
obj.animation_data_clear()

# Store original rotation
original_rotation = obj.rotation_euler.copy()

# Set the specific rotation angles
obj.rotation_euler = (
    math.radians(TARGET_BARREL_ANGLE),  # X-axis barrel roll (front-to-back flip)
    math.radians(180),                  # Y-axis
    math.radians(TARGET_SHUV_ANGLE)     # Z-axis shuv rotation (horizontal spin)
)

# Insert keyframe to force update
obj.keyframe_insert(data_path="rotation_euler", frame=1)

# Update the scene
bpy.context.view_layer.update()

# Render the image
filename = f"angle_{TARGET_SHUV_ANGLE:03d}_{TARGET_BARREL_ANGLE:03d}.png"
scene.render.filepath = os.path.join(output_dir, filename)
bpy.ops.render.render(write_still=True)

print(f"Rendered {filename} with angles:")
print(f"  Shuv (Z-axis): {TARGET_SHUV_ANGLE}°")
print(f"  Barrel (X-axis): {TARGET_BARREL_ANGLE}°")
print(f"Saved to: {output_dir}")
