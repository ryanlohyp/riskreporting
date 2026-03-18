from PIL import Image, ImageDraw
import itertools

ICON_SIZE = 140
SPACING = 40
CANVAS_HEIGHT = 240
CIRCLES = 4

CANVAS_WIDTH = CIRCLES * ICON_SIZE + (CIRCLES-1) * SPACING + 120

def normalize_icon(img):
    bbox = img.getbbox()
    img = img.crop(bbox)
    img = img.resize((ICON_SIZE, ICON_SIZE), Image.LANCZOS)
    return img

icons = {
    "Science": normalize_icon(Image.open("Science.png").convert("RGBA")),
    "People": normalize_icon(Image.open("People.png").convert("RGBA")),
    "Growth": normalize_icon(Image.open("Growth.png").convert("RGBA")),
    "Target": normalize_icon(Image.open("Target.png").convert("RGBA"))
}

# blank circle
blank = Image.new("RGBA",(ICON_SIZE,ICON_SIZE),(0,0,0,0))
draw = ImageDraw.Draw(blank)
draw.ellipse((0,0,ICON_SIZE,ICON_SIZE), outline=(200,200,200,255), width=8)

categories = ["Science","People","Growth","Target"]

for combo in itertools.product([0,1], repeat=4):

    canvas = Image.new("RGBA",(CANVAS_WIDTH,CANVAS_HEIGHT),(0,0,0,0))

    y = (CANVAS_HEIGHT-ICON_SIZE)//2
    start_x = (CANVAS_WIDTH - (ICON_SIZE*CIRCLES + SPACING*(CIRCLES-1)))//2

    x = start_x
    name_parts = []

    for i,val in enumerate(combo):

        if val == 1:
            icon = icons[categories[i]]
            name_parts.append(categories[i])
        else:
            icon = blank
            name_parts.append("Blank")

        canvas.paste(icon,(x,y),icon)
        x += ICON_SIZE + SPACING

    filename = "_".join(name_parts) + ".png"
    canvas.save(filename)

    print("Created", filename)