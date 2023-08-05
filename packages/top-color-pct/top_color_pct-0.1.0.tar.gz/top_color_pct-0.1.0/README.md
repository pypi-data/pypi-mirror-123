# Top-color-ptc 
## Library that allows you to input an image and get top N colors as output in percentage rate
```python
from top-color-pct import get_n_top_colors

image = Image.open('EiImg.png').convert('RGB')

top_5 = get_n_top_colors(image=image, n=5)
```
> it returns you a dict of top 5 colors from image. For 0.1.1 version it can work with pillow RGB image type.