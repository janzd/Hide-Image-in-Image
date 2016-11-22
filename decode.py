#!/usr/bin/python

import os, sys
from PIL import Image
from utils import rgb_to_binary

def main():
	"""
	Opens an image which contains information of a hidden image,
	recovers the hidden image and saves it in a specified or
	default location.

	Call example:
	    python decode.py img/output.png img/res.png
	"""
	if len(sys.argv) < 2 or len(sys.argv) > 3:
		print "--------------------HIiI v1.0--------------------"
		print "-- DECODING"
		print "-- To recover a concealed image, specify the"
		print "-- path to the image in which it is hidden."
		print "-- As an optional argument, you can specify the"
		print "-- path to save the restored image to."
		print "--"
		print "-- python decode.py path/to/image/to/restore/from"
		print "--     path/to/save/to"
		print "--"
		print "-- Example:"
		print "--   python decode.py img/output.png img/res.png"
		print "--"
		print "-------------------------------------------------"
		return
	if len(sys.argv) >= 2:
		img_path = sys.argv[1]
	if len(sys.argv) >= 3:
		output_path = sys.argv[2]
		filename, file_ext = os.path.splitext(output_path)
		output_path = filename + '.png'
	else:
		output_path = 'images/decoded_image.png'
	decoded_image = decode(Image.open(img_path))
	decoded_image.save(output_path)

def extract_hidden_pixels(image, width_visible, height_visible, pixel_count):
	"""
	Extracts a sequence of bits representing a sequence of binary values of 
	all pixels of the hidden image.
	The information representing a hidden image is stored in the 4 least significant
	bits of a subset of pixels of the visible image.

	Args:
	    image:            An RGB image to recover a hidden image from
	    width_visible:    Width of the visible image
	    height_visible:   Height of the visible image
	    pixel_count:      Number of pixels in the hidden image

	Returns:
	    A binary string representing pixel values of the hidden image
	"""
	hidden_image_pixels = ''
	idx = 0
	for col in range(width_visible):
		for row in range(height_visible):
			if row == 0 and col == 0:
				continue
			r, g, b = image[col, row]
			r_binary, g_binary, b_binary = rgb_to_binary(r, g, b)
			hidden_image_pixels += r_binary[4:8] + g_binary[4:8] + b_binary[4:8]
			if idx >= pixel_count * 2:
				return hidden_image_pixels
	return hidden_image_pixels

def reconstruct_image(image_pixels, width, height):
	"""
	Recontructs the hidden image using the extracted string of pixel binary values.

	Args:
	    image_pixels:    A string of binary values of all pixels of the image to be recovered
	    width:           Width of the image to be recovered
	    height:          Height of the image to be recovered

	Returns:
	    The recovered image
	"""
	image = Image.new("RGB", (width, height))
	image_copy = image.load()
	idx = 0
	for col in range(width):
		for row in range(height):
			r_binary = image_pixels[idx:idx+8]
			g_binary = image_pixels[idx+8:idx+16]
			b_binary = image_pixels[idx+16:idx+24]
			image_copy[col, row] = (int(r_binary, 2), int(g_binary, 2), int(b_binary, 2))
			idx += 24
	return image
	
def decode(image):
	"""
	Loads the image to recover a hidden image from, retrieves the information about the
	size of the hidden image stored in the top left pixel of the visible image,
	extracts the hidden binary pixel values from the image and reconstructs the hidden
	image.

	Args:
	    image:    An RGB image to recover a hidden image from

	Returns:
	    A recovered image, which was hidden in the binary representation of the visible image
	"""
	image_copy = image.load()
	width_visible, height_visible = image.size
	r, g, b = image_copy[0, 0]
	r_binary, g_binary, b_binary = rgb_to_binary(r, g, b)
	w_h_binary = r_binary + g_binary + b_binary
	width_hidden = int(w_h_binary[0:12], 2)
	height_hidden = int(w_h_binary[12:24], 2)
	pixel_count = width_hidden * height_hidden
	hidden_image_pixels = extract_hidden_pixels(image_copy, width_visible, height_visible, pixel_count)
	decoded_image = reconstruct_image(hidden_image_pixels, width_hidden, height_hidden)
	return decoded_image

if __name__ == '__main__':
	main()