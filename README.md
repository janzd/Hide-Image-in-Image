# Hide Image in Image

The script lets you hide an image by encoding it into the least significant bit positions of a subset of pixels in another image. The encoded image can be afterwards decoded and recovered without any information loss.

## Encoding

`python encode.py image_for_hiding image_to_hide encoded_output_destination`

The encoding takes two images as the input. The first image is the one that we want to use to hide something in.

![image to hide in another image](img/chicken.png)

The second image is the one that we want to hide and conceal in the first image.

![image used to hide another image](img/lena.jpg)

The first image, used for hiding, has to satisfy the condition that the number of its pixels is at least two times bigger than that of the image which we hide.

The result of the encoding is an image that visually should not look much different from the original image, but the least significant bits of a subset of pixels are replaced with the pixel information of the image that we want to hide.

![image with an image encoded inside](img/output.jpg)

## Decoding

`python decode.py encoded_image decoded_output_destination`

The decoding takes an image with another image encoded inside as the input.

![image with another image encoded inside](img/output.jpg)

The decoded output image is identical to the image that was hidden and encoded in another image.

![decoded image](img/lena.png)