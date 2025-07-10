import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os


class SimpleImageViewer:
    def __init__(self):
        # Initialize the main window
        self.window = tk.Tk()
        self.window.title("Simple Image Viewer")
        self.window.geometry("600x500")

        # Variables to store current image data
        self.current_image = None
        self.display_photo = None

        # Initialize UI component attributes
        self.load_btn = None
        self.quit_btn = None
        self.display_canvas = None
        self.status_label = None

        # Create the user interface
        self.create_widgets()

    def create_widgets(self):
        # Create a frame for buttons at the top
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=10)

        # Create buttons
        self.load_btn = tk.Button(button_frame, text="Load Image",
                                  command=self.load_image, width=12)
        self.load_btn.pack(side=tk.LEFT, padx=5)

        self.quit_btn = tk.Button(button_frame, text="Quit",
                                  command=self.close_app, width=12)
        self.quit_btn.pack(side=tk.LEFT, padx=5)

        # Create a canvas with scrollbars for image display
        canvas_frame = tk.Frame(self.window)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Canvas for displaying images
        self.display_canvas = tk.Canvas(canvas_frame, bg='white',
                                        width=560, height=400)

        # Scrollbars for the canvas
        h_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL,
                                   command=self.display_canvas.xview)
        v_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL,
                                   command=self.display_canvas.yview)

        # Configure canvas scrolling
        self.display_canvas.configure(xscrollcommand=h_scrollbar.set,
                                      yscrollcommand=v_scrollbar.set)

        # Pack scrollbars and canvas
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.display_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Status label
        self.status_label = tk.Label(self.window, text="Ready - Click 'Load Image' to start",
                                     relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def load_image(self):
        # Define supported image formats
        supported_formats = [
            ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff *.ico"),
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("All files", "*.*")
        ]

        # Open file dialog
        file_path = filedialog.askopenfilename(
            title="Select an image file",
            filetypes=supported_formats
        )

        if file_path:
            self.display_selected_image(file_path)

    def display_selected_image(self, file_path):
        try:
            # Open and process the image
            self.current_image = Image.open(file_path)

            # Get image dimensions
            img_width, img_height = self.current_image.size

            # Calculate scaling to fit canvas while maintaining aspect ratio
            canvas_width = 560
            canvas_height = 400

            # Scale image to fit canvas if it's too large
            if img_width > canvas_width or img_height > canvas_height:
                scale_factor = min(canvas_width / img_width, canvas_height / img_height)
                new_width = int(img_width * scale_factor)
                new_height = int(img_height * scale_factor)
                resized_image = self.current_image.resize((new_width, new_height),
                                                          Image.Resampling.LANCZOS)
            else:
                resized_image = self.current_image
                new_width, new_height = img_width, img_height

            # Convert to PhotoImage for display
            self.display_photo = ImageTk.PhotoImage(resized_image)

            # Clear previous image and display new one
            self.display_canvas.delete("all")

            # Calculate position to center the image
            x_pos = max(0, (canvas_width - new_width) // 2)
            y_pos = max(0, (canvas_height - new_height) // 2)

            # Display the image
            self.display_canvas.create_image(x_pos, y_pos, anchor=tk.NW,
                                             image=self.display_photo)

            # Update canvas scroll region
            self.display_canvas.configure(scrollregion=self.display_canvas.bbox("all"))

            # Update status
            filename = os.path.basename(file_path)
            self.status_label.config(text=f"Loaded: {filename} | Size: {img_width}x{img_height}")

        except Exception as e:
            # Show error message if image loading fails
            messagebox.showerror("Error", f"Could not load image:\n{str(e)}")
            self.status_label.config(text="Error loading image")

    def close_app(self):
        # Clean up and close the application
        self.window.destroy()

    def run(self):
        # Start the application
        self.window.mainloop()


# Create and run the image viewer
if __name__ == "__main__":
    viewer = SimpleImageViewer()
    viewer.run()