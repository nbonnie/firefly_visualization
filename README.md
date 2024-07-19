# Firefly Swarm Visualization and Export

This repository contains Python scripts for visualizing and exporting an animation of firefly swarm data from CSV files to an MP4 video format.

## Key Features:
* **KDE-Based Bounding Box**: Dynamically calculates a bounding box that contains a statistically significant amount of data.
* **Frame Exporting**: Saves individual frames as PNG files.
* **Video Creation**: Combines saved frames into an MP4 video using FFmpeg.
* **Frame Skipping**: Allows exporting frames starting from a specific frame number.
* **Auto Cleanup**: Automatically cleans up all the temporary files created by the script.

## Usage

### Prerequisites:
* Python 3.8+
* Required Python libraries: pandas, numpy, pygame, scipy, progressbar2
* FFmpeg (ensure it's installed and accessible in your system's PATH)
* Firefly datafile csv with x, y, z, t variables being the first 4 columns.

### Instructions:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/firefly_swarm_visualization.git
    cd firefly_swarm_visualization
    ```

2. **Install Required Libraries**:
    ```bash
    pip install pandas numpy pygame scipy progressbar2
    ```

3. **Run the Script**:
    * Modify the script to point to your CSV file by updating the `FNAME` variable.
    * Adjust the `START_FRAME` variable to set the starting frame for exporting.
    * Run the script:
    ```bash
    python replay_ff.py
    ```

4. **Video Creation**:
    The script will automatically call FFmpeg to create an MP4 video from the exported frames. Ensure FFmpeg is installed and available in your system's PATH.

## Output
The script generates:
* Temporary PNG frames saved in a `frames` directory.
* An MP4 video file named `output.mp4` in the same directory as the script.

## License
This project is licensed under the MIT License - see the LICENSE file for details.