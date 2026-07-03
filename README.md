# Multiple Disease Prediction System

This repository contains a **machine-learning** based web application that predicts the likelihood of multiple diseases such as diabetes, heart disease, and Parkinson’s disease based on user-provided health parameters.

## Features

- Predicts multiple diseases (diabetes, heart disease, Parkinson’s) using trained models.
- Uses pre-trained models stored in the repository (`trained_diabetes.model`, `heart_disease.pkl`, `parkinson_disease.pkl`). [page:1]
- Single interface for entering health data and viewing predictions.
- Built with Python and common ML libraries (see `requirements.txt`). [page:1]

## Project structure

Key files and folders in this project: [page:1]

- `.devcontainer/` – Dev container configuration for running the project in a consistent environment. [page:1]
- `dataset_links` – References or links to the datasets used to train the models.
- `heart_disease.pkl` – Saved model for heart disease prediction. [page:1]
- `parkinson_disease.pkl` – Saved model for Parkinson’s disease prediction. [page:1]
- `trained_diabetes.model` – Saved model for diabetes prediction. [page:1]
- `multiple_prediction_upgrade11.py` – Main Python script for running the prediction logic / app. [page:1]
- `requirements.txt` – Python dependencies needed to run the project. [page:1]

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Rithishkumar7/multiple_disease_prediction_system.git
   cd multiple_disease_prediction_system
   ```

2. Create and activate a virtual environment (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Running the application

1. Make sure you are in the project folder and your virtual environment is active.
2. Run the main script:

   ```bash
   python multiple_prediction_upgrade11.py
   ```

3. Open the link printed in the terminal (if it is a web app) and provide the required health parameters to get predictions.

> If your script name or run command is different, update this section to match how you actually start the app.

## Models and data

- The models in `.pkl` and `.model` files were trained on standard health datasets (see `dataset_links` for details). [page:1]
- Each model expects specific input features; ensure your UI/form matches the features used during training.

## Contributing

- Fork the repository.
- Create a new branch for your feature or bug fix.
- Submit a pull request with a clear description of your changes.

## License

Specify the license here (for example, MIT). If you haven’t chosen one yet, you can add a `LICENSE` file later and update this section.
