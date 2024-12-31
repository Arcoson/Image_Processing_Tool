# Image Processing Tool 🖼️

A powerful command-line tool for batch image processing with AI enhancement capabilities. This tool provides an intuitive, colorful interface for various image processing operations including AI-powered upscaling and enhancement.

## Features ✨

- **AI Image Enhancement**: 2x upscaling with detail preservation
- **Batch Processing**: Process multiple images at once
- **Format Conversion**: Convert between different image formats
- **Image Resizing**: Resize images to specific dimensions
- **Filter Application**: Apply various image filters
- **File Organization**: Automatically organize images by format
- **Colorful Interface**: User-friendly CLI with progress bars

## Installation 🚀

1. Clone this repository or download the script:
```bash
git clone <your-repository-url>
cd image-processor
```

2. Install required dependencies:
```bash
pip install Pillow rich opencv-python opencv-contrib-python
```

## Usage 💻

Run the script using Python:
```bash
python image_processor.py
```

### Available Commands

1. **Enhance Images**:
```bash
enhance
```
- Uses AI to upscale images and enhance quality
- Creates enhanced versions with "enhanced_" prefix

2. **Resize Images**:
```bash
resize <width> <height>
```
- Resizes images to specified dimensions
- Example: `resize 800 600`

3. **Convert Format**:
```bash
convert <format>
```
- Converts images to specified format
- Supported formats: jpg, png, bmp
- Example: `convert png`

4. **Apply Filters**:
```bash
filter <name> <value>
```
- Available filters:
  - brightness (0.0-2.0)
  - contrast (0.0-2.0)
  - sharpen (0.0-2.0)
  - grayscale
- Example: `filter brightness 1.5`

5. **Organize Files**:
```bash
organize
```
- Organizes images into folders by format

6. **Help**:
```bash
help
```
- Displays available commands

7. **Exit**:
```bash
exit
```
- Exits the program

## Examples 📝

1. Enhance images in a folder:
```bash
> Enter command: enhance
> Enter images directory path: /path/to/images
```

2. Convert all images to PNG:
```bash
> Enter command: convert png
> Enter images directory path: /path/to/images
```

3. Resize all images:
```bash
> Enter command: resize 1920 1080
> Enter images directory path: /path/to/images
```

## Technical Details 🔧

- AI Enhancement uses OpenCV's Super Resolution with EDSR model
- Supports common image formats (JPG, PNG, BMP)
- Progress tracking for batch operations
- Error handling for invalid inputs and failed operations

## Requirements 📋

- Python 3.6 or higher
- PIL (Pillow)
- OpenCV (opencv-python)
- OpenCV Contrib (opencv-contrib-python)
- Rich (for CLI interface)

## Note 📝

The AI enhancement model (EDSR_x2.pb) will be automatically downloaded on first use.

## Error Handling ⚠️

- Invalid commands display helpful error messages
- Progress bars show operation status
- Keyboard interrupts (Ctrl+C) are safely handled

## Contributing 🤝

Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.
