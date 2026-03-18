from PIL import Image, ImageDraw
import itertools

ICON_SIZE = 140
SPACING = 40
CIRCLES = 4

# Canvas width based on layout
CANVAS_WIDTH = CIRCLES * ICON_SIZE + (CIRCLES - 1) * SPACING + 120

# 🔥 CRITICAL: No vertical padding at all
CANVAS_HEIGHT = ICON_SIZE


def normalize_icon(img):
    img = img.convert("RGBA")

    # Remove transparent padding
    bbox = img.getbbox()
    img = img.crop(bbox)

    # Ensure square (important for alignment consistency)
    w, h = img.size
    max_dim = max(w, h)

    square = Image.new("RGBA", (max_dim, max_dim), (0, 0, 0, 0))
    square.paste(img, ((max_dim - w) // 2, (max_dim - h) // 2))

    # Resize to final size
    img = square.resize((ICON_SIZE, ICON_SIZE), Image.LANCZOS)

    return img


# Load and normalize icons
icons = {
    "Science": normalize_icon(Image.open("Science.png")),
    "People": normalize_icon(Image.open("People.png")),
    "Growth": normalize_icon(Image.open("Growth.png")),
    "Target": normalize_icon(Image.open("Target.png"))
}

# Create blank circle (same size, no padding)
blank = Image.new("RGBA", (ICON_SIZE, ICON_SIZE), (0, 0, 0, 0))
draw = ImageDraw.Draw(blank)
draw.ellipse((0, 0, ICON_SIZE, ICON_SIZE), outline=(200, 200, 200, 255), width=8)

categories = ["Science", "People", "Growth", "Target"]

# Generate all combinations
for combo in itertools.product([0, 1], repeat=4):

    # Transparent canvas with NO vertical padding
    canvas = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (0, 0, 0, 0))

    y = 0  # 🔥 No top/bottom padding

    start_x = (CANVAS_WIDTH - (ICON_SIZE * CIRCLES + SPACING * (CIRCLES - 1))) // 2

    x = start_x
    name_parts = []

    for i, val in enumerate(combo):

        if val == 1:
            icon = icons[categories[i]]
            name_parts.append(categories[i])
        else:
            icon = blank
            name_parts.append("Blank")

        canvas.paste(icon, (x, y), icon)
        x += ICON_SIZE + SPACING

    filename = "_".join(name_parts) + ".png"
    canvas.save(filename)

    print("Created", filename)