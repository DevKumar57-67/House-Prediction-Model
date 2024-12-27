from flask import Flask, request, render_template_string
import pandas as pd
from sklearn.linear_model import LinearRegression

# Initialize Flask app
app = Flask(__name__)

# Create a sample dataset and train the model
df = pd.DataFrame({'bath': [1, 2, 3, 4, 5], 'price': [100, 200, 300, 400, 500]})
X = df[['bath']]
y = df['price']

# Train the Linear Regression model
model = LinearRegression()
model.fit(X, y)

# HTML Template as a string
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>House Price Prediction</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 50px;
        }
        .container {
            max-width: 500px;
            margin: auto;
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        h1 {
            text-align: center;
        }
        input[type="number"] {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        button {
            width: 100%;
            padding: 10px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
        .result {
            text-align: center;
            margin-top: 20px;
            font-size: 1.2em;
            color: green;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>House Price Prediction</h1>
        <form action="/predict" method="post">
            <label for="bathrooms">Enter the number of bathrooms:</label>
            <input type="number" id="bathrooms" name="bathrooms" min="1" required>
            <button type="submit">Predict</button>
        </form>
        {% if prediction_text %}
            <div class="result">
                {{ prediction_text }}
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

# Home route
@app.route('/')
def home():
    return render_template_string(html_template)

# Predict route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get user input
        bathrooms = int(request.form['bathrooms'])
        
        # Prepare data for prediction
        new_data = pd.DataFrame({'bath': [bathrooms]})
        predicted_price = model.predict(new_data)[0]
        
        # Return the result
        return render_template_string(html_template, prediction_text=f'Predicted price for {bathrooms} bathrooms: {predicted_price}')
    except Exception as e:
        return render_template_string(html_template, prediction_text=f'Error: {str(e)}')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
