import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import shutil
import dotenv
dotenv.load_dotenv()

class PhotoSorter:
    SUB_SAVE_PATH = "PhotoAlbum1"

    def __init__(self, root):  

        # You can change os.getenv() to the path you want to save your photos to    
        self.SAVE_PATH = os.path.join(os.getenv("SAVE_PATH"), self.SUB_SAVE_PATH)
        self.root = root

        # self.root.title("Photo Sorter")
        self.photo_index = 0
        self.photo_paths = []  # List of photo file paths
        self.load_photos()  # Load photos from a directory
        self.save_paths = []  # List of save paths

        self.display = tk.Label(root)
        self.display.pack()

         # Display current save path in a text box
        self.save_path_display = tk.Text(root, height=1, width=60)
        self.save_path_display.pack()

        self.save_button = tk.Button(root, text="Save (->)", command=self.save_photo)
        self.save_button.pack()

        self.skip_button = tk.Button(root, text="Skip (<-)", command=self.load_next_photo)
        self.skip_button.pack()    

        # associate the right arrow key with the skip button
        root.bind("<Left>", lambda event: self.skip_button.invoke())
        # associate the left arrow key with the save button
        root.bind("<Right>", lambda event: self.save_button.invoke())

        #Display total number of photos next to buttons
        self.total_photos = tk.Label(root, text="Photos: 0/{}".format(len(self.photo_paths)))
        self.total_photos.pack()

        self.save_path = tk.Entry(root)
        self.save_path.insert(0, "misc")
        self.save_path.bind("<Return>", lambda event: self.change_save_path())
        self.save_path.pack()

        # Display all pre-existing save paths (already existing folders) in buttons
        # and add them to self.save_paths to be used easily later
        folders = []
        for root_path, dirnames, _ in os.walk(self.SAVE_PATH):
            for dirname in dirnames:
                if not dirname.startswith('.'):
                    folder_path = os.path.join(root_path, dirname)
                    folders.append(folder_path)

        for folder in folders:
            folder = folder[len(self.SAVE_PATH) + 1:] 
            tk.Button(root, text=folder, command=lambda folder=folder: self.change_save_path(folder)).pack()
            self.save_paths.append(folder)

        # Add a button for the default misc folder if it doesn't exist
        if os.path.join(self.SAVE_PATH, "misc") not in self.save_paths:
            self.save_paths.append(os.path.join(self.SAVE_PATH, "misc"))
            if not os.path.exists(os.path.join(self.SAVE_PATH, "misc")):
                os.makedirs(os.path.join(self.SAVE_PATH, "misc"))
            button = tk.Button(self.root, text="misc", command=lambda: self.change_save_path("misc"))
            button.pack()
        
        # Set the current save path to the first save path in the list
        self.current_save_path = self.save_paths[0]  # Current save path
        self.save_path_display.insert(tk.END, self.current_save_path)
        self.load_photo()

    def change_save_path(self, folder=None):
        '''
        Change the current save path to the path specified in the save_path text box
        if folder is None. Else, change the current save path to the path specified
        in the folder argument.
        '''
        if folder is None:
            new_save_path = os.path.join(self.SAVE_PATH, self.save_path.get())
            folder = self.save_path.get()
        else: 
            new_save_path = os.path.join(self.SAVE_PATH, folder)

        if new_save_path not in self.save_paths:
            self.save_paths.append(new_save_path)
            # create directory if it doesn't exist
            if not os.path.exists(new_save_path):
                os.makedirs(new_save_path)
            # add a button for the new save path
            button = tk.Button(self.root, text=folder, command=lambda: self.change_save_path(folder))
            button.pack()
        # change the current save path and display it in the text box
        self.current_save_path = new_save_path
        self.save_path.delete(0, 'end')
        self.save_path.insert(0, os.path.basename(folder))
        self.save_path_display.delete('1.0', tk.END)
        self.save_path_display.insert(tk.END, self.current_save_path)


    def load_photos(self):
        '''
        Load photos from a directory
        '''
        directory = filedialog.askdirectory()
        self.photo_paths = [os.path.join(directory, filename) for filename in os.listdir(directory) if filename.lower().endswith(('.jpg', '.jpeg', '.png'))]

    def load_photo(self):
        '''
        Load a photo from the list of photo paths        
        '''
        if self.photo_index < len(self.photo_paths):
            self.total_photos.config(text="Photos: {}/{}".format(self.photo_index + 1, len(self.photo_paths)))
            photo_path = self.photo_paths[self.photo_index]
            img = Image.open(photo_path)
            img = img.resize((600, 600))
            self.photo = ImageTk.PhotoImage(img)
            self.display.config(image=self.photo)
        else:
            # remove currenctly displayed photo
            self.display.config(image="")
            self.display.config(text="No more photos to sort")

    def save_photo(self):
        '''
        Save the current photo to the current save path
        '''
        # Read path written in save_path text box
        save_path = self.current_save_path
        # Create directory if it doesn't exist
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        # Copy Photo to directory with shutils
        shutil.copy(self.photo_paths[self.photo_index], save_path)
        # Load next photo
        self.load_next_photo()
        

    def load_next_photo(self):
        '''
        Load the next photo in the list of photo paths
        '''
        self.photo_index += 1
        self.load_photo()

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Photo Sorter")
    app = PhotoSorter(root)
    root.mainloop()
