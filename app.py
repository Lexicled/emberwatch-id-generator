from PIL import Image, ImageDraw, ImageFont
from flask import Flask, render_template, request, make_response
from io import BytesIO
import base64

app = Flask(__name__)
image_path = "template.png"  
font_path = "font.ttf"

@app.route('/', methods=['GET', 'POST'])
def profile_form():
    if request.method == 'POST':
        # When the button is clicked, data will be available here
        disc_username = request.form['disc_username']
        rank = request.form['rank']
        ss_class = request.form['ss_class'] + "-Class"
        ss_desc = request.form['ss_desc']
        nms_username = "NMS: " + request.form['nms_username']
        social = request.form['social']
        fc = "FC: " + request.form['fc']
        platform = "Platform: " + request.form['platform']

        # Call the add_profile_info function 
        img = add_profile_info(image_path, font_path, disc_username, rank, ss_class, ss_desc, nms_username, social, fc, platform)
        img = img.convert('RGB')
        output = BytesIO()
        img.save(output, format='PNG')
        image_data = output.getvalue()

        image_data_base64 = base64.b64encode(image_data).decode('utf-8')
        return render_template('success.html', image_data=image_data_base64)
    else:
        return render_template('profile_form.html')

def add_profile_info(image_path, font_path, disc_username, rank, ss_class, 
                     ss_desc, nms_username, social, fc, platform):

    try:
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)

        # Hard-coded text positions, sizes, and boldness
        text_settings = {
            "disc_username": (246, 131, 34, True),
            "rank": (237, 158, 25, False),
            "ss_class": (31, 69, 22, False),
            "ss_desc": (33, 85, 22,  False),
            "nms_username": (36, 180, 22, True),
            "social": (36, 199, 22, True),
            "fc": (36, 218, 22, True),
            "platform": (36, 237, 22, True)
        }

        for key, (x, y, size, bold) in text_settings.items():
            if bold:
                font_path = "font-bold.ttf"
            else:
                font_path = "font.ttf" 

            font = ImageFont.truetype(font_path, size)
            font = ImageFont.truetype(font_path, size)
            font_weight = "bold" if bold else "normal"
            font = ImageFont.truetype(font_path, size, encoding="unic", layout_engine=ImageFont.Layout.BASIC)

            text_value = locals()[key]  # Dynamically fetch the text content
            draw.text((x, y), text_value, font=font, fill="black")

        return image 

    except FileNotFoundError:
        print(f"Image not found at: {image_path}")

if __name__ == '__main__':
    app.run(debug=True)
