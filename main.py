import os, sys
import skimage
import numpy as np
from PIL import Image
from utils import rgb_to_binary, add_leading_zeros, get_binary_pixel_values

def main():
	if len(sys.argv) < 3 or len(sys.argv) > 4:
		# HEEEEY
		return
	if len(sys.argv) >= 3:
		img_visible_path = sys.argv[1]
		img_hidden_path = sys.argv[2]
	if len(sys.argv) >= 4:
		output_path = sys.argv[3]
		filename, file_ext = os.path.splitext(output_path)
		output_path = filename + '.png'
	else:
		output_path = 'encoded_image.png'
	decoding = 1
	if decoding == 1:
		decoded_image = decode(Image.open(img_visible_path))
		decoded_image.save('decoded_image.png')
		return
	img_visible = Image.open(img_visible_path)
	img_hidden = Image.open(img_hidden_path)
	encoded_image = encode(img_visible, img_hidden)
	#img_visible.putdata(encoded_image)
	encoded_image.save(output_path)

def add_leading_zeros(binary_number, expected_length):
	length = len(binary_number)
	return (expected_length - length) * '0' + binary_number

def rgb_to_binary(r, g, b):
	return add_leading_zeros(bin(r)[2:], 8), add_leading_zeros(bin(g)[2:], 8), add_leading_zeros(bin(b)[2:], 8)

def get_binary_pixel_values(img, width, height):
	hidden_image_pixels = ''
	for col in range(width):
		for row in range(height):
			pixel = img[col, row]
			r = pixel[0]
			g = pixel[1]
			b = pixel[2]
			r_binary, g_binary, b_binary = rgb_to_binary(r, g, b)
			hidden_image_pixels += r_binary + g_binary + b_binary
	return hidden_image_pixels

def change_binary_values(img_visible, hidden_image_pixels, width_visible, height_visible, width_hidden, height_hidden):
	idx = 0
	for col in range(width_visible):
		for row in range(height_visible):
			if row == 0 and col == 0:
				width_hidden_binary = add_leading_zeros(bin(width_hidden)[2:], 12)
				height_hidden_binary = add_leading_zeros(bin(height_hidden)[2:], 12)
				w_h_binary = width_hidden_binary + height_hidden_binary
				img_visible[col, row] = (int(w_h_binary[0:8], 2), int(w_h_binary[8:16], 2), int(w_h_binary[16:24], 2))
				continue
			r, g, b = img_visible[col, row]
			r_binary, g_binary, b_binary = rgb_to_binary(r, g, b)
			r_binary = r_binary[0:4] + hidden_image_pixels[idx:idx+4]
			g_binary = g_binary[0:4] + hidden_image_pixels[idx+4:idx+8]
			b_binary = b_binary[0:4] + hidden_image_pixels[idx+8:idx+12]
			idx += 12
			img_visible[col, row] = (int(r_binary, 2), int(g_binary, 2), int(b_binary, 2))
			if idx >= len(hidden_image_pixels):
				return img_visible
	# can never be reached, but let's return the image anyway
	return img_visible

def extract_hidden_pixels(image, width_visible, height_visible, pixel_count):
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

def encode(img_visible, img_hidden):
	encoded_image = img_visible.load()
	img_hidden_copy = img_hidden.load()
	width_visible, height_visible = img_visible.size
	width_hidden, height_hidden = img_hidden.size
	hidden_image_pixels = get_binary_pixel_values(img_hidden_copy, width_hidden, height_hidden)
	encoded_image = change_binary_values(encoded_image, hidden_image_pixels, width_visible, height_visible, width_hidden, height_hidden)
	return img_visible

def decode(image):
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



