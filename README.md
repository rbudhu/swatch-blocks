# swatch-blocks
Swatch Blocks

Swatch Blocks is a Python program inspired by this Reddit post: https://www.reddit.com/r/puzzles/comments/fqvk5k/a_bit_of_a_lockdown_logic_puzzle_1_the_simpsons/

Swatch Blocks takes an input image and converts it to a set of vertical blocks that resemble the input image.  The program is sensitive to the qualities of the input image and not all inputs convert nicely.  See the examples below.

## Running

`python swatch-blocks.py [input image file path]`

This will create an output file named `<file name>-blocks` with the same extension as the input image.

## Examples

| Input | Output | Input | Output |
| :---: | :---:| :---:| :---:|
| <img src="https://mario.nintendo.com/assets/img/home/char-mario.png" height=300px> | ![mario-block](https://user-images.githubusercontent.com/2107153/78367641-6779d700-7590-11ea-8954-156ce7dd012e.png)| <img src="https://vignette.wikia.nocookie.net/mario/images/6/69/696px-Luigi_New_Super_Mario_Bros_U_Deluxe.png/revision/latest?cb=20190623144153" height=300px> | ![luigi-block](https://user-images.githubusercontent.com/2107153/78367800-a740be80-7590-11ea-84ac-c3165d8dd8ea.png)|
|![dexter](https://user-images.githubusercontent.com/2107153/78368054-08689200-7591-11ea-8caf-b5f62ddd10e2.jpg)|![dexter-block](https://user-images.githubusercontent.com/2107153/78368063-0bfc1900-7591-11ea-9140-3df212874255.jpg)| ![peter](https://user-images.githubusercontent.com/2107153/78368161-2fbf5f00-7591-11ea-8b12-31247d2a8c1e.png) | ![peter-block](https://user-images.githubusercontent.com/2107153/78368168-3352e600-7591-11ea-976c-3870dea25bc1.png) |
|![eric-cartman](https://user-images.githubusercontent.com/2107153/78368311-71500a00-7591-11ea-9294-0e6e27563bb5.png)|![eric-cartman-block](https://user-images.githubusercontent.com/2107153/78368325-73b26400-7591-11ea-89ed-5be8b77fa518.png) | <img src="https://www.wired.com/images_blogs/underwire/2010/06/fry_660.jpg" height=300px> | ![fry-block](https://user-images.githubusercontent.com/2107153/78368340-7c0a9f00-7591-11ea-8af8-1a81a42e5a6b.jpg)


## Troubleshooting Tips

1. Make sure your subject is in the foreground of your image and there exists high contrast between the background and the foreground for the segmentation to work properly.
2. Run the program with the `--log` option to output the source HSV image, binary mask image, and show log output.

