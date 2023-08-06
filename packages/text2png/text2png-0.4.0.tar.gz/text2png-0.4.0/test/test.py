from text2png import *


t2p = TextToPng(
    # absolute path to font file
    font_file="C:\\Windows\\Fonts\\msgothic.ttc",
    # font size, integer
    font_size=64,
    # background color, RGB value
    background_color=(0, 0, 0),
    # text color, RGB value
    text_color=(255, 255, 255),
    # png file save directory
    save_dir="C:\\Temp"
)
print(
    t2p.create(
        # what text
        text="HELLO",
        # text padding, in pixels
        padding=15,
        # file name
        filename="hello.png"
    )
)
# C:\\Temp\\hello.png
