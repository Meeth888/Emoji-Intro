from flask import Flask, render_template, request
from PIL import Image, ImageDraw, ImageFont
import os

app = Flask(__name__)

# Ensure the avatars directory exists
AVATAR_DIR = "static/avatars"
os.makedirs(AVATAR_DIR, exist_ok=True)

def generate_avatar(name, traits):
    img = Image.new("RGB", (500, 500), "white")
    draw = ImageDraw.Draw(img)

    # Define trait-based colors
    colors = {
        "hardworking": "blue",
        "creative": "purple",
        "smart": "green",
        "kind": "orange",
        "ambitious": "red",
    }

    color1 = colors.get(traits[0], "black")
    color2 = colors.get(traits[1], "black")

    # Draw a round face
    draw.ellipse([(150, 100), (350, 300)], fill=(255, 220, 180), outline="black", width=3)

    # Eyes
    eye_size = 15 if "smart" in traits else 10
    draw.ellipse([(200, 180), (200+eye_size, 180+eye_size)], fill="black")
    draw.ellipse([(300, 180), (300+eye_size, 180+eye_size)], fill="black")

    # Glasses for "hardworking"
    if "hardworking" in traits:
        draw.rectangle([(190, 175), (220, 195)], outline="black", width=2)
        draw.rectangle([(290, 175), (320, 195)], outline="black", width=2)
        draw.line([(220, 185), (290, 185)], fill="black", width=2)

    # Mouth
    if "kind" in traits:
        draw.arc([(220, 230), (280, 270)], start=0, end=180, fill="black", width=3)
    else:
        draw.line([(220, 250), (280, 250)], fill="black", width=3)

    # Hair
    if "creative" in traits:
        draw.rectangle([(150, 80), (350, 130)], fill="brown", outline="black", width=3)

    # Add Name
    try:
        font = ImageFont.truetype("arial.ttf", 30)
    except:
        font = ImageFont.load_default()

    draw.text((170, 20), name, fill="black", font=font)

    # Save avatar
    filename = f"{name.lower()}_avatar.png"
    img_path = os.path.join(AVATAR_DIR, filename)
    img.save(img_path)

    return filename

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        traits = request.form.getlist("traits")

        if len(traits) != 2:
            return "Please select exactly two traits."

        avatar_filename = generate_avatar(name, traits)
        return render_template("result.html", name=name, avatar_filename=avatar_filename)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
