
# Flask Image Text Detection

This project allows you to upload an image, detect text within the image using OCR (Optical Character Recognition), and display the detected text.

## Project Structure

Note:Create A Virtual Environment of Python [python -m venv [nameofurchoice]] in project directory command prompt
```
FLASK_IMAGE_TEXT_DETECTION/
│
├── static/
│   ├── results/
│   ├── uploads/
│   ├── styles.css
│   └── voice.mp3
│
├── templates/
│   ├── index.html
│   └── result.html
│
├── app.py
├── requirements.txt
├── Test1.jpg
└── WIN_20240723_11_45_27_Pro.jpg
```

## Files and Directories

- `static/`: Contains static files such as CSS, uploaded images, and results.
  - `results/`: Directory to store processed images with detected text.
  - `uploads/`: Directory to store uploaded images.
  - `styles.css`: CSS file for styling the HTML templates.
  - `voice.mp3`: Audio file (if used in the project).

- `templates/`: Contains HTML templates for the Flask app.
  - `index.html`: The main page where users can upload images.
  - `result.html`: The page to display the result after processing the image.

- `app.py`: The main Flask application file.

- `requirements.txt`: Lists the dependencies required for the project.

- `Test1.jpg`: A sample image for testing.

- `WIN_20240723_11_45_27_Pro.jpg`: Another sample image for testing.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/FLASK_IMAGE_TEXT_DETECTION.git
   cd FLASK_IMAGE_TEXT_DETECTION
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     venv\Scripts activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Flask application:**
   ```bash
   python app.py
   ```

2. **Open your web browser and go to:**
   ```
   http://127.0.0.1:5000/
   ```

3. **Upload an image and click 'Submit'.** The application will process the image and display the detected text.

## License

This project is licensed under the MIT License.

incase of any error feel free to contact Gautham Prabhu HM


