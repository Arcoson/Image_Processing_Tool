import os
import sys
from PIL import Image, ImageEnhance
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich import print
from rich.panel import Panel
from rich.progress import Progress
import time
import cv2
import numpy as np

console = Console()

class ImageProcessor:
    def __init__(self):
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.bmp']
        self.filters = {
            'brightness': self.adjust_brightness,
            'contrast': self.adjust_contrast,
            'sharpen': self.adjust_sharpness,
            'grayscale': self.convert_grayscale
        }
        # Initialize AI model
        self.setup_ai_model()

    def setup_ai_model(self):
        """Setup the OpenCV Super Resolution model"""
        try:
            self.sr = cv2.dnn_superres.DnnSuperResImpl_create()
            model_path = "EDSR_x2.pb"
            
            # Download the model if it doesn't exist
            if not os.path.exists(model_path):
                console.print("[yellow]Downloading AI enhancement model...[/yellow]")
                url = "https://github.com/Saafke/EDSR_Tensorflow/raw/master/models/EDSR_x2.pb"
                import urllib.request
                urllib.request.urlretrieve(url, model_path)
            
            self.sr.readModel(model_path)
            self.sr.setModel("edsr", 2)  # 2x upscaling
            console.print("[green]AI Enhancement model loaded successfully! 🤖[/green]")
        except Exception as e:
            console.print(f"[red]Failed to load AI model: {str(e)}[/red]")
            self.sr = None

    def show_welcome(self):
        welcome_text = """
        [bold cyan]🖼  Image Processing Tool v1.1[/bold cyan]
        [green]A powerful CLI tool for batch image processing with AI Enhancement[/green]
        """
        console.print(Panel(welcome_text, border_style="blue"))

    def show_help(self):
        table = Table(title="Available Commands", border_style="cyan")
        table.add_column("Command", style="cyan")
        table.add_column("Description", style="green")
        
        commands = {
            "resize <width> <height>": "Resize images to specified dimensions",
            "convert <format>": "Convert images to specified format (jpg/png/bmp)",
            "filter <name> <value>": "Apply filter (brightness/contrast/sharpen/grayscale)",
            "enhance": "Apply AI enhancement to improve image quality (2x upscale)",
            "organize": "Organize images into folders by format",
            "help": "Show this help message",
            "exit": "Exit the program"
        }
        
        for cmd, desc in commands.items():
            table.add_row(cmd, desc)
        
        console.print(table)

    def enhance_image(self, img_path):
        """Enhance image using AI super resolution"""
        if self.sr is None:
            raise Exception("AI Enhancement model not available")
        
        # Read image using OpenCV
        img = cv2.imread(img_path)
        if img is None:
            raise Exception(f"Failed to load image: {img_path}")
        
        # Apply super resolution
        enhanced = self.sr.upsample(img)
        
        # Apply additional enhancements
        enhanced = cv2.detailEnhance(enhanced, sigma_s=10, sigma_r=0.15)
        
        # Adjust contrast and brightness
        alpha = 1.2  # Contrast control
        beta = 10    # Brightness control
        enhanced = cv2.convertScaleAbs(enhanced, alpha=alpha, beta=beta)
        
        # Save enhanced image
        output_path = f"enhanced_{os.path.basename(img_path)}"
        cv2.imwrite(output_path, enhanced)
        return output_path

    def process_images(self, input_path, operation, *args):
        if not os.path.exists(input_path):
            console.print("[red]Error: Input path does not exist![/red]")
            return

        files = [f for f in os.listdir(input_path) if os.path.splitext(f)[1].lower() in self.supported_formats]
        
        if not files:
            console.print("[yellow]No supported image files found in the directory![/yellow]")
            return

        with Progress() as progress:
            task = progress.add_task("[cyan]Processing images...", total=len(files))

            for file in files:
                try:
                    image_path = os.path.join(input_path, file)
                    
                    if operation == "enhance":
                        self.enhance_image(image_path)
                    else:
                        img = Image.open(image_path)
                        
                        if operation == "resize":
                            width, height = map(int, args)
                            img = img.resize((width, height), Image.Resampling.LANCZOS)
                            img.save(f"resized_{file}")
                        
                        elif operation == "convert":
                            new_format = args[0].lower()
                            new_filename = os.path.splitext(file)[0] + f".{new_format}"
                            img.save(new_filename)
                        
                        elif operation == "filter":
                            filter_name, value = args[0], float(args[1])
                            if filter_name in self.filters:
                                img = self.filters[filter_name](img, value)
                                img.save(f"filtered_{file}")
                    
                    progress.advance(task)
                    time.sleep(0.1)
                
                except Exception as e:
                    console.print(f"[red]Error processing {file}: {str(e)}[/red]")

        console.print("[green]Processing complete! ✨[/green]")

    def adjust_brightness(self, img, factor):
        enhancer = ImageEnhance.Brightness(img)
        return enhancer.enhance(factor)

    def adjust_contrast(self, img, factor):
        enhancer = ImageEnhance.Contrast(img)
        return enhancer.enhance(factor)

    def adjust_sharpness(self, img, factor):
        enhancer = ImageEnhance.Sharpness(img)
        return enhancer.enhance(factor)

    def convert_grayscale(self, img, _):
        return img.convert('L')

    def organize_images(self, path):
        for file in os.listdir(path):
            ext = os.path.splitext(file)[1].lower()
            if ext in self.supported_formats:
                folder_name = ext[1:]  # Remove the dot
                folder_path = os.path.join(path, folder_name)
                
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                
                os.rename(
                    os.path.join(path, file),
                    os.path.join(folder_path, file)
                )

def main():
    processor = ImageProcessor()
    processor.show_welcome()
    processor.show_help()

    while True:
        try:
            command = Prompt.ask("\n[bold cyan]Enter command[/bold cyan]")
            parts = command.lower().split()

            if not parts:
                continue

            if parts[0] == "exit":
                console.print("[yellow]Goodbye! 👋[/yellow]")
                break
            
            elif parts[0] == "help":
                processor.show_help()
            
            else:
                path = Prompt.ask("[bold cyan]Enter images directory path[/bold cyan]")
                
                if parts[0] == "resize" and len(parts) == 3:
                    processor.process_images(path, "resize", parts[1], parts[2])
                
                elif parts[0] == "convert" and len(parts) == 2:
                    processor.process_images(path, "convert", parts[1])
                
                elif parts[0] == "filter" and len(parts) == 3:
                    processor.process_images(path, "filter", parts[1], parts[2])
                
                elif parts[0] == "enhance":
                    processor.process_images(path, "enhance")
                
                elif parts[0] == "organize":
                    processor.organize_images(path)
                    console.print("[green]Images organized successfully! 📁[/green]")
                
                else:
                    console.print("[red]Invalid command! Use 'help' to see available commands.[/red]")

        except KeyboardInterrupt:
            console.print("\n[yellow]Operation cancelled by user. Use 'exit' to quit.[/yellow]")
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")

if __name__ == "__main__":
    main()
