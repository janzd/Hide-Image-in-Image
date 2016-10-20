def add_leading_zeros(binary_number, expected_length):
	"""
	Adds leading zeros to a binary number so that the number of characters
	in the binary string matches the specified expected length and the value
	of the binary sring remains unchanged.

	Args:
		binary_number:    A string representation of a number in base 2
		expected_length:  Expected length of the binary number string

	Returns:
	    A binary string of a length specified by the argument with the 
	    same numerical value as the binary number from the first argument.
	"""
	length = len(binary_number)
	return (expected_length - length) * '0' + binary_number

def rgb_to_binary(r, g, b):
	"""
	Converts decimal numbers representing RGB values of a pixel into
	binary numbers of the same values.

	Args:
	    r:    Decimal representation of the red channel value
	    g:    Decimal representation of the green channel value
	    b:    Decimal representation of the blue channel value

	Returns:
	    Binary representations of the red, green, and blue channel values
	"""
	return add_leading_zeros(bin(r)[2:], 8), add_leading_zeros(bin(g)[2:], 8), add_leading_zeros(bin(b)[2:], 8)
