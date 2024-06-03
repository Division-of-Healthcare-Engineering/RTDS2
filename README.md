# RTDS2

## Description

RTPlanAI is a comprehensive repository for developing, evaluating, and applying innovative AI/ML algorithms to reduce variability and improve the accuracy of radiation therapy (RT) treatment planning. This project enhances RT providers' performance during pre-treatment peer-review processes, aiming to reduce treatment planning errors and improve patient safety across multiple cancer sites.

## Specific Aims

### Aim #1
Develop and assess the effectiveness of innovative AI/ML algorithms focused on reducing RT providers’ variability in key treatment planning steps (e.g., defining target volumes, prescribed doses) during pre-treatment peer-review processes to improve RT providers’ performance.

- **Hypothesis 1**: Innovative AI/ML algorithms focused on reducing physicians’ variability during the pre-treatment peer-review processes will improve RT providers’ performance during peer-review.
- **Metrics**: Number/severity of identified treatment planning errors, average time to complete pre-treatment peer-review processes, cognitive workload, and perceived usability of visual summaries.

### Aim #2
Assess the impact of our intervention into the RT work system on patient safety.

- **Hypothesis 2**: Implementing our intervention into the RT work system will improve patient safety.
- **Metrics**: Number & severity of clinically relevant errors not detected during pre-treatment peer-review processes, rate per 1000 RT fractions delivered, evaluated using linear mixed effect regression (LMER) model.


## Directory Structure
```plaintext
RTPlanAI/
│
├── data/
│   ├── raw/                   # Raw DICOM files
│   ├── processed/             # Processed images and labels
│   └── samples/               # Sample data for quick testing
│
├── docs/
│   ├── code_documentation/    # Detailed explanations of codebase
│   ├── data_documentation/    # Information about the data used
│   ├── models/                # Documentation for each model
│   └── project_goals.md       # Overall objectives and goals of the project
│
├── notebooks/
│   ├── data_preprocessing.ipynb   # Jupyter notebook for data preprocessing
│   ├── model_training.ipynb       # Jupyter notebook for model training
│   └── evaluation.ipynb           # Jupyter notebook for model evaluation
│
├── src/
│   ├── common/                   # Common code shared across models
│   │   ├── data_loader.py
│   │   ├── preprocessing.py
│   │   └── utils.py
│   │
│   ├── nodal_coverage/            # Model-specific directory
│   │   ├── common/                # Common code for nodal coverage model
│   │   │   ├── preprocessing.py
│   │   │   └── model.py
│   │   ├── prostate/              # Prostate-specific code
│   │   │   ├── src/
│   │   │   │   ├── model.py
│   │   │   │   └── train.py
│   │   │   ├── data/
│   │   │   ├── notebooks/
│   │   │   ├── tests/
│   │   │   ├── .gitignore
│   │   │   ├── README.md
│   │   │   ├── requirements.txt
│   │   │   └── setup.py
│   │   ├── breast/                # Breast-specific code
│   │   │   ├── src/
│   │   │   │   ├── model.py
│   │   │   │   └── train.py
│   │   │   ├── data/
│   │   │   ├── notebooks/
│   │   │   ├── tests/
│   │   │   ├── .gitignore
│   │   │   ├── README.md
│   │   │   ├── requirements.txt
│   │   │   └── setup.py
│   │   └── ...
│   │
│   ├── volume_variability/       # Model-specific directory
│   │   ├── common/               # Common code for volume variability model
│   │   │   ├── preprocessing.py
│   │   │   └── model.py
│   │   ├── prostate/             # Prostate-specific code
│   │   │   ├── src/
│   │   │   │   ├── model.py
│   │   │   │   └── train.py
│   │   │   ├── data/
│   │   │   ├── notebooks/
│   │   │   ├── tests/
│   │   │   ├── .gitignore
│   │   │   ├── README.md
│   │   │   ├── requirements.txt
│   │   │   └── setup.py
│   │   └── ...
│   │
│   ├── train.py                   # Common training script
│   ├── evaluate.py                # Common evaluation script
│
├── tests/
│   ├── test_data_loader.py        # Unit tests for data loading
│   ├── test_preprocessing.py      # Unit tests for preprocessing
│   ├── test_utils.py              # Unit tests for utility functions
│
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                 # GitHub Actions CI workflow
│
├── .gitignore                     # Git ignore file
├── README.md                      # Project README file
├── requirements.txt               # Global requirements file
└── setup.py                       # Setup script for installing the package
```

## Getting Started

### Prerequisites

Make sure you have the following dependencies installed:

- Python 3.x
- TensorFlow
- NumPy
- SciPy
- Matplotlib
- DicomRTTool

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/RTPlanAI.git
    cd RTPlanAI
    ```

2. Install the global dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Install the subproject-specific dependencies:
    ```bash
    pip install -r projects/prostate/nodal_coverage/requirements.txt
    ```

## Usage

1. **Data Preprocessing**:
    Run the data preprocessing script to convert raw DICOM files into numpy arrays and preprocess them for training:
    ```bash
    python src/data/data_loader.py
    ```

2. **Model Training**:
    Train the desired model using the training script:
    ```bash
    python src/train.py --model unet  # Example for U-Net
    ```

3. **Model Evaluation**:
    Evaluate the trained model on the test dataset:
    ```bash
    python src/evaluate.py --model unet  # Example for U-Net
    ```

## Running All Models

To execute all models across all cancer sites, use the `run_all_models.py` script:

```python
import os
import subprocess

# List of all subprojects and models
subprojects = [
    'projects/prostate/nodal_coverage',
    'projects/lung/nodal_coverage',
    # Add other subprojects here
]

# Command to install subproject-specific requirements
def install_requirements(subproject):
    subprocess.run(['pip', 'install', '-r', f'{subproject}/requirements.txt'])

# Command to run training script
def run_training(subproject):
    subprocess.run(['python', f'{subproject}/src/train.py'])

# Iterate through subprojects, install requirements, and run training
for subproject in subprojects:
    install_requirements(subproject)
    run_training(subproject)

```
## Running All Models

To execute all models across all cancer sites, use the `run_all_models.py` script:

```bash
python src/run_all_models.py

```
## CI/CD

A GitLab CI/CD pipeline is set up to automate testing and deployment:

**`.gitlab-ci.yml`**:

```yaml
stages:
  - build
  - test
  - deploy

build:
  stage: build
  script:
    - python -m pip install --upgrade pip
    - pip install -r requirements.txt

test:
  stage: test
  script:
    - pytest

deploy:
  stage: deploy
  script:
    - ./deploy.sh
  only:
    - main
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
