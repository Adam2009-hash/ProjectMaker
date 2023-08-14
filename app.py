from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']
    if file.filename == '':
        return "No selected file"

    data = pd.read_csv(file)

    # Perform data analysis and visualization
    plt.figure(figsize=(10, 6))
    data.plot(kind='bar', x='x_column', y='y_column')
    plt.title('Data Visualization')
    plt.xlabel('X Column')
    plt.ylabel('Y Column')

    # Save the plot to a BytesIO object
    img_stream = io.BytesIO()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)
    img_base64 = base64.b64encode(img_stream.read()).decode('utf-8')

    plt.close()

    return render_template('result.html', img_base64=img_base64)

if __name__ == '__main__':
    app.run(debug=True)