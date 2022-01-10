# gimp-thumb-grid

This plug-in for gimp was created to make a grid image containing thumbnail images of movie posters. The grid image is used as a single "sprite image" that can be reused for a catalog-type page with lots of thumbnails linking to different detail pages. 

## Basic usage

1. In gimp, open all the full-size images (posters, in our case) that you want to include in your thumbnail grid
2. In gimp, pen the thumb_grid.xcf
3. Select the command under the File menu called "IFS Size Open Poster Then Shrink And Add to Thumbgrid"

The script will run. When it finishes you should see

1. In gimp, in your thumb_grid.xcf file, a thumbnail image for each poster you had open
2. In the folder containing your original posters, a new copy of each file resized to 400px

## Adding additional thumbnails to an existing grid

If your thumb_grid.xcf file contains thumbnails, you can add new thumbnails to it by opening the new posters, opening the existing .xcf file, and rerunning the command.

## Installing (adding menu shortcut to the gimp)

You can [RTFM here](https://docs.gimp.org/2.10/en_US/install-script-fu.html). We recommend that you simply add this project to your Scripts folders (Preferences > Folders > Scripts). The script is supposed to appear under the File menu. 
