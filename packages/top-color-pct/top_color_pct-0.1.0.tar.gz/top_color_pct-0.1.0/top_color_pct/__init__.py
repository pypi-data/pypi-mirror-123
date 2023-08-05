from webcolors import rgb_to_hex

def get_n_top_colors(image, n):
    '''Takes an RGB Image(tested with Pil.Image type)
   Return a dict with hex color value and its percentage on the image
   return example {1: {'hex_name': '#ffffff', 'percentage': 5.50}} 
    '''
    color_pct = {}
    top_n_color_dict = {}
    x, y = image.size

    for x in range(image.width - 1):
        for y in range(image.height - 1):
            pixel = image.getpixel((x, y))
            pixel = rgb_to_hex(pixel)
            if pixel in color_pct:
                color_pct[pixel] += 1
            else:
                color_pct[pixel] = 1

    total_pixels = sum(color_pct.values())

    color_pct = {k:(v / total_pixels * 100) for (k, v) in color_pct.items()}
    sorted_color_pct = dict(sorted(color_pct.items(), key=lambda x: x[1], reverse=True))


    top_n_colors = list(sorted_color_pct.items())[0:n]
    for idx, color in enumerate(top_n_colors):
        top_n = idx + 1
        hex_name = color[0]
        pct = f'{color[1]:.2f}'
        pct = float(pct)
        
        new_value = {
            top_n: {
                'hex_name': hex_name,
                'percentage': pct
            }
        }
        top_n_color_dict.update(new_value)

    return top_n_color_dict