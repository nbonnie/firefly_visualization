#--------------------------------------------------------------------------------
# Script Name: replay_ff.py
# Description: Visualizes firefly swarm xyzt data from a CSV file, exports individual 
#              frames as PNG images, and combines them into an MP4 video using FFmpeg.
#
# Usage:       python replay_ff.py
#
# Author:      Nolan R. Bonnie
# Contact:     nolan.bonnie@colorado.edu
# Created:     07/2024
#--------------------------------------------------------------------------------

import pandas as pd
import numpy as np
import pygame
import sys
from scipy.stats import gaussian_kde
import os
import progressbar
import subprocess
import shutil

# Check for ffmpeg installation
if shutil.which("ffmpeg") is None:
    print("FFmpeg is not installed. Please install FFmpeg to proceed.")
    sys.exit(1)

# Constants
FPS = 30
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)
POINT_COLOR = (255, 255, 0)
POINT_SIZE = 5
FNAME = '/Users/nbonnie/Desktop/xyztkj_tc_20240518_crit_a.csv'
START_FRAME = 108000  # Start exporting frames from this frame number

# Load CSV data with specified column names
try:
    df = pd.read_csv(FNAME, header=None, usecols=[0, 1, 2, 3], names=['x', 'y', 'z', 't'])
except FileNotFoundError:
    print("CSV file not found. Please make sure the path is correct.")
    sys.exit()

# Function to find the bounding box
def find_significant_bounding_box(df, threshold=0.95):
    xy = np.vstack([df['x'], df['y']])
    kde = gaussian_kde(xy)
    density = kde(xy)
    sorted_density = np.sort(density)
    cutoff_index = int((1 - threshold) * len(sorted_density))
    density_threshold = sorted_density[cutoff_index]
    significant_points = xy[:, density > density_threshold]
    x_min, y_min = significant_points.min(axis=1)
    x_max, y_max = significant_points.max(axis=1)
    return x_min, x_max, y_min, y_max

# Calculate the bounding box
x_min, x_max, y_min, y_max = find_significant_bounding_box(df)

# Normalize positions for visualization within bounding box
df['x'] = (df['x'] - x_min) / (x_max - x_min) * WIDTH
df['y'] = (df['y'] - y_min) / (y_max - y_min) * HEIGHT

# Calculate frame numbers based on FPS
df['frame'] = ((df['t'] - df['t'].min()) * FPS).astype(int)
min_frame = int(df['frame'].min())
max_frame = int(df['frame'].max())

# Print total number of frames before skipping
total_frames_before_skip = max_frame - min_frame + 1
print(f"Total number of frames before skipping: {total_frames_before_skip}")

# Filter dataframe based on start frame
df = df[df['frame'] >= START_FRAME]
min_frame = START_FRAME

# Print the total number of frames to be exported
total_frames = max_frame - min_frame + 1
print(f"Total number of frames to be exported: {total_frames}")

# Initialize Pygame without displaying the window
pygame.display.init()
screen = pygame.Surface((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Directory to save frames
output_dir = 'frames'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def get_frame(frame_number):
    frame_data = df[df['frame'] == frame_number]
    positions = frame_data[['x', 'y']].values
    return positions

def draw_frame(screen, positions):
    screen.fill(BACKGROUND_COLOR)
    for pos in positions:
        pygame.draw.circle(screen, POINT_COLOR, (int(pos[0]), int(pos[1])), POINT_SIZE)

def save_frame(screen, export_frame_number):
    pygame.image.save(screen, os.path.join(output_dir, f'frame_{export_frame_number:06d}.png'))

# Main loop to save frames
export_frame_number = 0
with progressbar.ProgressBar(max_value=total_frames) as bar:
    for current_frame in range(min_frame, max_frame + 1):
        positions = get_frame(current_frame)
        draw_frame(screen, positions)
        save_frame(screen, export_frame_number)
        clock.tick(FPS)
        bar.update(export_frame_number + 1)
        export_frame_number += 1

pygame.quit()

# Create the video using FFmpeg
video_filename = 'output.mp4'
ffmpeg_command = [
    'ffmpeg', '-framerate', str(FPS), '-i', os.path.join(output_dir, 'frame_%06d.png'),
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', video_filename
]
try:
    subprocess.run(ffmpeg_command, check=True)
    print(f"Video created successfully: {video_filename}")

    # Remove the frames directory after successful video creation
    for file_name in os.listdir(output_dir):
        file_path = os.path.join(output_dir, file_name)
        if os.path.isfile(file_path):
            os.unlink(file_path)
    os.rmdir(output_dir)
    print("Frames directory removed.")
except subprocess.CalledProcessError as e:
    print(f"FFmpeg command failed: {e}")
    sys.exit(1)

print("Frames saved. Use FFmpeg to combine them into a video.")