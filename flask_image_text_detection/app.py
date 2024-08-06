from flask import Flask, request, render_template, url_for
import cv2
import numpy as np
import easyocr
import imutils
from gtts import gTTS
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
RESULT_FOLDER = 'static/results/'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(RESULT_FOLDER):
    os.makedirs(RESULT_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    if not file:
        return "No file uploaded", 400

    # Generate a unique filename
    filename = str(uuid.uuid4()) + '.jpg'
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # Read the image
    img = cv2.imread(filepath)

    try:
        # Process the image and save intermediate steps
        original_img_path = os.path.join(RESULT_FOLDER, 'original_' + filename)
        cv2.imwrite(original_img_path, img)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray_img_path = os.path.join(RESULT_FOLDER, 'gray_' + filename)
        cv2.imwrite(gray_img_path, gray)

        bfilter = cv2.bilateralFilter(gray, 11, 17, 17)
        bfilter_img_path = os.path.join(RESULT_FOLDER, 'bfilter_' + filename)
        cv2.imwrite(bfilter_img_path, bfilter)

        edged = cv2.Canny(bfilter, 30, 200)
        edged_img_path = os.path.join(RESULT_FOLDER, 'edged_' + filename)
        cv2.imwrite(edged_img_path, edged)

        keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(keypoints)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

        location = None
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 10, True)
            if len(approx) == 4:
                location = approx
                break

        if location is None:
            return "Could not find document contour", 400

        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [location], 0, 255, -1)
        new_image = cv2.bitwise_and(img, img, mask=mask)
        mask_img_path = os.path.join(RESULT_FOLDER, 'mask_' + filename)
        cv2.imwrite(mask_img_path, new_image)

        (x, y) = np.where(mask == 255)
        (x1, y1) = (np.min(x), np.min(y))
        (x2, y2) = (np.max(x), np.max(y))
        cropped_image = gray[x1:x2 + 1, y1:y2 + 1]
        cropped_img_path = os.path.join(RESULT_FOLDER, 'cropped_' + filename)
        cv2.imwrite(cropped_img_path, cropped_image)

        reader = easyocr.Reader(['en'])
        result = reader.readtext(cropped_image)

        if not result:
            return "No text found in the image", 400

        text = result[0][-2]

        font = cv2.FONT_HERSHEY_SIMPLEX
        res = cv2.putText(img, text=text, org=(location[0][0][0], location[1][0][1] + 60), fontFace=font, fontScale=1,
                          color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
        res = cv2.rectangle(img, tuple(location[0][0]), tuple(location[2][0]), (0, 255, 0), 3)
        final_img_path = os.path.join(RESULT_FOLDER, 'final_' + filename)
        cv2.imwrite(final_img_path, res)

        # Generate voice note
        tts = gTTS(text=text, lang='en')
        voice_path = os.path.join(RESULT_FOLDER, 'voice_' + filename.split('.')[0] + '.mp3')
        tts.save(voice_path)

        return render_template('result.html', 
                               original_img='results/original_' + filename, 
                               gray_img='results/gray_' + filename, 
                               bfilter_img='results/bfilter_' + filename, 
                               edged_img='results/edged_' + filename, 
                               mask_img='results/mask_' + filename, 
                               cropped_img='results/cropped_' + filename, 
                               final_img='results/final_' + filename, 
                               text=text, 
                               voice_path='results/voice_' + filename.split('.')[0] + '.mp3')

    except Exception as e:
        return f"Error: {e}", 500

@app.route('/final')
def final():
    text = request.args.get('text')
    final_img = request.args.get('final_img')
    voice_path = request.args.get('voice_path')
    return render_template('final.html', text=text, final_img=final_img, voice_path=voice_path)

if __name__ == '__main__':
    app.run(debug=True)
