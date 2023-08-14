from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__, template_folder='C:\\Users\\ashto\\Project\\Template')

@app.route('/')
def index():
    return render_template('index.html', columns=[])

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']
    if file.filename == '':
        return "No selected file"

    data = pd.read_csv(file)
    columns = data.columns.tolist()

    x_column = request.form.get('x_column')
    y_column = request.form.get('y_column')

    plt.figure(figsize=(10, 6))

    if data[y_column].dtype == 'object':
        data[y_column].value_counts().plot(kind='bar')
        plt.title('Categorical Data Visualization')
        plt.xlabel('Categories')
        plt.ylabel('Frequency')
    else:
        plt.scatter(data[x_column], data[y_column])
        plt.title('Numerical Data Visualization')
        plt.xlabel('X Column')
        plt.ylabel('Y Column')

    img_stream = io.BytesIO()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)
    img_base64 = base64.b64encode(img_stream.read()).decode('utf-8')

    plt.close()

    return render_template('result.html', img_base64=img_base64)

if __name__ == '__main__':
    app.run(debug=True)
