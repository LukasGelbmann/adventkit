from adventkit import helpers


WIDTH = 25
HEIGHT = 6


def solve(puzzle_input):
    image_data = puzzle_input.strip()
    layers = list(helpers.chunked(image_data, WIDTH * HEIGHT))

    chosen_layer = min(layers, key=lambda layer: layer.count('0'))
    print(chosen_layer.count('1') * chosen_layer.count('2'))

    data_by_pixel = helpers.transpose(layers)
    for row_data in helpers.chunked(data_by_pixel, WIDTH):
        print(' '.join(decode(pixel_data) for pixel_data in row_data))


def decode(pixel_data):
    for color in pixel_data:
        if color == '0':
            return ' '
        if color == '1':
            return '#'
    raise ValueError("pixel is transparent all the way through")
