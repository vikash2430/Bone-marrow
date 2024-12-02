from flask import Flask, request, render_template
import joblib
import numpy as np

# Load the trained model using joblib
model_path = "C:/Users/User/render-demo/best_model1.pkl" # Make sure the model file is in the correct path
model = joblib.load(model_path)

app = Flask(__name__)

@app.route('/')
def home():
    # Render the home page with the input form
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract data from the form
        patient_name = request.form['patientName']
        patient_age = int(request.form['patientAge'])
        donor_age = int(request.form['donorAge'])
        time_to_agvhd = int(request.form['timeToAGvHD'])
        recipient_abo = int(request.form['recipientABO'])
        gender = request.form['patientGender']
        disease = request.form['disease']
        
        # Prepare features for the model (following the same format as used during training)
        features = [
            patient_age,
            donor_age,
            time_to_agvhd,
            recipient_abo,
            1 if gender == 'male' else 0,  # Binary encoding for gender
            1 if disease == 'acute' else 0  # Binary encoding for disease
        ]
        
        final_features = [np.array(features)]  # Convert the features into a NumPy array
        
        # Make prediction using the trained model
        prediction = model.predict(final_features)
        
        # Interpret the prediction result
        output = 'Survived' if prediction[0] == 1 else 'Not Survived'
        
        # Render the result on the web page
        return render_template('index.html', prediction_text=f'Prediction: {output}')
    
    except Exception as e:
        # Handle errors and return the error message
        return render_template('index.html', prediction_text=f'Error: {str(e)}')

if __name__ == "__main__":
    app.run(debug=True)