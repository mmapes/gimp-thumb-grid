#!/usr/bin/env python

# Tutorial available at: https://www.youtube.com/watch?v=nmb-0KcgXzI
# Feedback welcome: jacksonbates@hotmail.com
# https://gist.github.com/JacksonBates/cd98675d58403d295dee

from gimpfu import *
import os

inverse_aspect = 1.5  # aspect ratio of .66:1
thumb_grid_file_name = 'thumb_grid.xcf'
grid_size_x = 10

def ifs_size_open_poster_then_shrink_and_add_to_thumbgrid(image, drawable):
    pdb.gimp_message("running main method")
    all_images = gimp.image_list()
    pdb.gimp_message("got all images")
    if not there_is_a_thumb_grid_image_open(all_images):
        pdb.gimp_message("Open a thumb_grid.xcf file and re-run me ")
        return

    for image in all_images:
        if not image.filename.endswith(thumb_grid_file_name):
            do_for_each_image(image, all_images)


def do_for_each_image(current_image, all_images):
    poster_name = get_poster_name(current_image)

    # first_image.undo_freeze

    # Shrink and save poster
    copy_to_shrink = pdb.gimp_image_duplicate(current_image)
    pdb.gimp_message("copied image name is " + copy_to_shrink.name)
    (shrunk_image, shrunk_layer) = shrink_poster(copy_to_shrink, 400)
    new_name = get_new_name(current_image, shrunk_image)
    pdb.gimp_message("we have a new name:  %s " % (new_name))
    save_shrunk(shrunk_image, new_name)
    pdb.gimp_image_delete(copy_to_shrink)

    # Now make another copy
    # Shrink it to thumbnail size 100 x 150
    # Copy the layer
    # https://stackoverflow.com/a/8312792
    # paste it into the thumb_grid
    # https: // stackoverflow.com / a / 8312792
    copy_for_thumbnail = pdb.gimp_image_duplicate(current_image)
    pdb.gimp_message("copied image for thumb name is " + copy_for_thumbnail.name)

    target_layer = get_thumb_grid_target_layer(all_images, poster_name)
    pdb.gimp_message("got target layer and it is %s " % (target_layer))

    (thumb_image, thumb_layer) = shrink_poster(copy_for_thumbnail, 100)

    pdb.gimp_message("shrank poster and got thumb layer %s %s %s %s" % (thumb_layer.image.filename, thumb_layer, thumb_layer.width, thumb_layer.height))

    buffer_index = pdb.gimp_edit_copy(thumb_layer)
    pdb.gimp_message("copied thumb layer and got %s" % buffer_index)

    floating_layer = pdb.gimp_edit_paste(target_layer, buffer_index)
    pdb.gimp_message("pasted to floating layer")
    pdb.gimp_floating_sel_anchor(floating_layer)
    pdb.gimp_message("realized layer")

    pdb.gimp_image_delete(copy_for_thumbnail)
    pdb.gimp_message("deleted thumb image")

    # first_image.undo_thaw


def get_number_of_layers_in_thumb_grid(all_images):
    thumb_grid_image = get_thumb_grid_image(all_images)
    return len(thumb_grid_image.layers)


def get_thumb_grid_image(all_images):
    for image in all_images:
        if image.filename.endswith(thumb_grid_file_name):
            return image


def get_x_y_of_thumbnail_number(num):
    rows = num / grid_size_x
    cols = num % grid_size_x
    return (cols * 100, rows * 150)


def there_is_a_thumb_grid_image_open(all_images):
    pdb.gimp_message("checking for thumb grid")
    for image in all_images:
        if image.filename.endswith(thumb_grid_file_name):
            pdb.gimp_message("found thumb grid %s" + thumb_grid_file_name)
            return True
    pdb.gimp_message("did not find thumb grid %s" + thumb_grid_file_name)
    return False


def get_thumb_grid_target_layer(all_images, layer_name):
    num_layers = get_number_of_layers_in_thumb_grid(all_images)
    (offs_x, offs_y) = get_x_y_of_thumbnail_number(num_layers)
    pdb.gimp_message("layer %s wil go at %s, %s" % (num_layers, offs_x, offs_y))
    pos = 1 # position within layers
    # http://gimpchat.com/viewtopic.php?f=9&t=13643#
    for image in all_images:
        if image.filename.endswith(thumb_grid_file_name):
            thisLayer = image.new_layer(layer_name, 100, 150, offs_x, offs_y, 0, pos, 100)
            return thisLayer


def shrink_poster(image, new_width):
    new_height = int(new_width * inverse_aspect)
    current_width = image.width
    current_height = image.height
    pdb.gimp_message("current width and height are %s and %s " % (current_width, current_height))
    layer = image.layers[0]
    if current_height / current_width > inverse_aspect:
        pdb.gimp_message("aaaacurrent width and height are %s and %s " % (current_width, current_height))

        if current_height >= new_height:
            new_width = new_width
            layer.scale(new_width, int(new_width * inverse_aspect))
            image.resize(new_width, int(new_width * inverse_aspect))
        else:
            new_width = new_width / 2
            layer.scale(new_width, int(new_width * inverse_aspect))
            image.resize(new_width, int(new_width * inverse_aspect))
    else:
        pdb.gimp_message("bbbbcurrent width and height are %s and %s " % (current_width, current_height))

        if current_width >= new_width:
            new_width = new_width
            layer.scale(new_width, int(new_width * inverse_aspect))
            image.resize(new_width, int(new_width * inverse_aspect))
        else:
            new_width = new_width / 2
            layer.scale(new_width, int(new_width * inverse_aspect))
            image.resize(new_width, int(new_width * inverse_aspect))

    pdb.gimp_message("cutmesomeslack %s %s" % (image.width, image.height) )
    return (image, layer)


def save_shrunk(shrunk_image, new_name):
    layer = pdb.gimp_image_merge_visible_layers(shrunk_image, CLIP_TO_IMAGE)
    pdb.gimp_file_save(shrunk_image, layer, new_name, '?')


def get_new_name(image, shrunk_image):
    filename = image.filename
    path = os.path.dirname(filename)
    return os.path.join(path, str(shrunk_image.width) + "_" + os.path.basename(filename))


def get_poster_name(first_image):
    filename = first_image.filename
    return os.path.basename(filename)


register(
    "python-fu-ifs_size_open_poster_then_shrink_and_add_to_thumbgrid",
    "SHORT DESCRIPTION",
    "LONG DESCRIPTION",
    "Jackson Bates", "Jackson Bates", "2015",
    "IFS Size Open Poster Then Shrink And Add to Thumbgrid",
    "",  # type of image it works on (*, RGB, RGB*, RGBA, GRAY etc...)
    [
        # basic parameters are: (UI_ELEMENT, "variable", "label", Default)
        (PF_IMAGE, "image", "takes current image", None),
        (PF_DRAWABLE, "drawable", "Input layer", None)
        # PF_SLIDER, SPINNER have an extra tuple (min, max, step)
        # PF_RADIO has an extra tuples within a tuple:
        # eg. (("radio_label", "radio_value), ...) for as many radio buttons
        # PF_OPTION has an extra tuple containing options in drop-down list
        # eg. ("opt1", "opt2", ...) for as many options
        # see ui_examples_1.py and ui_examples_2.py for live examples
    ],
    [],
    ifs_size_open_poster_then_shrink_and_add_to_thumbgrid, menu="<Image>/File")  # second item is menu location

main()
