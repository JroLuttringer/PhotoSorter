# PHOTO SORTER 

This program creates a window that lets you choose a given folder within your file system. 

Then, the program goes through each photo, displaying them on the screen. The user can choose to save the photo (right arrow) or skip the photo (left arrow) 

The photo is then copied in a save folder. By default, it is placed in a subdirectory called "misc". However, you can create another subdirectory by writing the name in the textbox and pressing enter. This changes the subdirectory the photos are saved to, and create a button to quickly return to this subdirectory later on. 

The current "save" directory is written in the UI.

The save path is composed of the concatenation of a base save path (e.g., /user/sorted_photos), concatenated with another name (e.g., "firstAlbum", leading to the full save path being /user/sorted_photo/firstAlbum/{misc, vacations...}). 

You can change the save path and the following folder within the code. By default, the base save path is empty (it uses dotenv to read a path that is not directly within the code) and the subfolder is "PhotoAlbum1".


For example : 

Let's suppose that my save path in /home/sorted_photos

At the start, a photo is display. Pressing "->" will save it in /home/sorted_photos/misc and going to the next photo. 

The next photo is maybe related to vacations. You can then write "vacations" in the textbox and press Enter, which will create the /home/sorted_photos/vacations directory. You can then press -> to save the photo in this folder 

The next photo may not be interesting. You can press "<-" to skip it. 

The next photo may be "misc" again. You can then click the "misc" button to change the save path back to /home/sorted_photos/misc/. 

Similarly, you can go back to saving photos to /home/sorted_photos/vacations/ by clicking on the button. 

You can use as many subdirectory as you want.

Note that if you already have some folders in the save path, (e.g., /home/sorted_photos/test exist), buttons to change the save file to these folders will be added automatically.


