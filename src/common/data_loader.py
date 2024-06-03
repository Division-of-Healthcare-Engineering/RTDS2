import os
import numpy as np
import pandas as pd
import xml.etree.ElementTree as ET
from PIL import Image
import SimpleITK as sitk
import nibabel as nib
import pydicom
import cv2
from dicomrt import DicomReader  # Assuming DICOM RT Tool by Brian Anderson
import requests
import zipfile

def load_data(file_path):
    """
    Load data based on file extension.
    
    Args:
        file_path (str): Path to the data file.
    
    Returns:
        data: Loaded data.
    """
    extension = os.path.splitext(file_path)[1].lower()
    
    if extension in ['.dcm']:
        return load_dicom(file_path)
    elif extension in ['.nii', '.nii.gz']:
        return load_nifti(file_path)
    elif extension in ['.jpg', '.jpeg', '.png', '.bmp']:
        return load_image(file_path)
    elif extension in ['.nrrd']:
        return load_nrrd(file_path)
    elif extension in ['.xlsx', '.xls']:
        return load_excel(file_path)
    elif extension in ['.xml']:
        return load_xml(file_path)
    else:
        raise ValueError(f"Unsupported file extension: {extension}")

def load_dicom(file_path):
    """
    Load a DICOM file using DICOM RT Tool.
    
    Args:
        file_path (str): Path to the DICOM file.
    
    Returns:
        tuple: (np.array: DICOM image data, dict: metadata).
    """
    dicom_reader = DicomReader(file_path)
    return dicom_reader.get_image(), dicom_reader.get_metadata()

def load_nifti(file_path):
    """
    Load a NIfTI file.
    
    Args:
        file_path (str): Path to the NIfTI file.
    
    Returns:
        tuple: (np.array: NIfTI image data, dict: metadata).
    """
    img = nib.load(file_path)
    return img.get_fdata(), img.header

def load_image(file_path):
    """
    Load an image file.
    
    Args:
        file_path (str): Path to the image file.
    
    Returns:
        np.array: Image data.
    """
    image = Image.open(file_path)
    return np.array(image)

def load_nrrd(file_path):
    """
    Load an NRRD file.
    
    Args:
        file_path (str): Path to the NRRD file.
    
    Returns:
        tuple: (np.array: NRRD image data, dict: metadata).
    """
    img = sitk.ReadImage(file_path)
    return sitk.GetArrayFromImage(img), sitk.ReadImage(file_path)

def load_excel(file_path):
    """
    Load an Excel file.
    
    Args:
        file_path (str): Path to the Excel file.
    
    Returns:
        pd.DataFrame: Loaded Excel data.
    """
    return pd.read_excel(file_path)

def load_xml(file_path):
    """
    Load an XML file.
    
    Args:
        file_path (str): Path to the XML file.
    
    Returns:
        ET.Element: Root element of the XML tree.
    """
    tree = ET.parse(file_path)
    return tree.getroot()

def download_sample_data(output_dir):
    """
    Download and extract sample data from the DICOM RT Tool repository.
    
    Args:
        output_dir (str): Directory to save the sample data.
    """
    url = "https://github.com/brianmanderson/DICOM_RT_and_Images_to_Mask/archive/refs/heads/master.zip"
    local_zip = os.path.join(output_dir, "dicom_rt_sample_data.zip")
    
    # Download the sample data
    response = requests.get(url)
    with open(local_zip, 'wb') as f:
        f.write(response.content)
    
    # Extract the zip file
    with zipfile.ZipFile(local_zip, 'r') as zip_ref:
        zip_ref.extractall(output_dir)
    
    # Cleanup
    os.remove(local_zip)
    print("Sample data downloaded and extracted.")

def create_feature_vector(patient_data):
    """
    Create a feature vector for a patient from different data sources.
    
    Args:
        patient_data (dict): Dictionary containing patient data.
    
    Returns:
        dict: Feature vector for the patient.
    """
    feature_vector = {
        'ct': None,
        'mri': None,
        'pet': None,
        'clinical': None
    }

    # Add CT data
    if 'ct' in patient_data:
        ct_image, ct_metadata = patient_data['ct']
        feature_vector['ct'] = {'data': ct_image, 'metadata': ct_metadata}
    
    # Add MRI data
    if 'mri' in patient_data:
        mri_image, mri_metadata = patient_data['mri']
        feature_vector['mri'] = {'data': mri_image, 'metadata': mri_metadata}
    
    # Add PET data
    if 'pet' in patient_data:
        pet_image, pet_metadata = patient_data['pet']
        feature_vector['pet'] = {'data': pet_image, 'metadata': pet_metadata}
    
    # Add clinical data
    if 'clinical' in patient_data:
        clinical_data = patient_data['clinical']
        feature_vector['clinical'] = clinical_data
    
    return feature_vector

def export_data_availability(patients_data, output_path):
    """
    Export an Excel sheet indicating data availability for each patient.
    
    Args:
        patients_data (dict): Dictionary containing data for all patients.
        output_path (str): Path to save the Excel sheet.
    """
    records = []
    for patient_id, data in patients_data.items():
        record = {
            'Patient ID': patient_id,
            'CT Available': 'ct' in data,
            'MRI Available': 'mri' in data,
            'PET Available': 'pet' in data,
            'Clinical Data Available': 'clinical' in data
        }
        records.append(record)
    
    df = pd.DataFrame(records)
    df.to_excel(output_path, index=False)

def split_data(patients_data, test_size=0.2):
    """
    Split data into training and testing sets.
    
    Args:
        patients_data (dict): Dictionary containing data for all patients.
        test_size (float): Proportion of the data to include in the test split.
    
    Returns:
        tuple: (training_set, testing_set)
    """
    patient_ids = list(patients_data.keys())
    np.random.shuffle(patient_ids)
    split_index = int(len(patient_ids) * (1 - test_size))
    train_ids = patient_ids[:split_index]
    test_ids = patient_ids[split_index:]
    
    training_set = {pid: patients_data[pid] for pid in train_ids}
    testing_set = {pid: patients_data[pid] for pid in test_ids}
    
    return training_set, testing_set

def load_all_data(directory, use_sample_data=False):
    """
    Load all data files from a directory and organize by patient ID.
    
    Args:
        directory (str): Path to the directory containing data files.
        use_sample_data (bool): Whether to use sample data if actual data is not available.
    
    Returns:
        dict: Dictionary of patients' data organized by patient ID.
    """
    if use_sample_data or not os.listdir(directory):
        print("Using sample data...")
        download_sample_data(directory)
    
    patients_data = {}
    
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            patient_id = os.path.basename(root)
            
            if patient_id not in patients_data:
                patients_data[patient_id] = {}
            
            try:
                data = load_data(file_path)
                
                if isinstance(data, tuple):
                    # Handle different types of medical images and metadata
                    if file.endswith('.dcm'):
                        patients_data[patient_id]['ct'] = data
                    elif file.endswith(('.nii', '.nii.gz')):
                        patients_data[patient_id]['mri'] = data
                    elif file.endswith('.nrrd'):
                        patients_data[patient_id]['pet'] = data
                else:
                    # Handle clinical data
                    if file.endswith(('.xlsx', '.xls')):
                        patients_data[patient_id]['clinical'] = data
                    elif file.endswith('.xml'):
                        patients_data[patient_id]['clinical'] = data
            
            except Exception as e:
                print(f"Error loading file {file_path}: {e}")
    
    return patients_data

# Example usage
if __name__ == "__main__":
    raw_data_directory = r'C:\Users\foste\Documents\_Dev\Github\Academia\RTPlanAI\data\raw'
    processed_data_directory = r'C:\Users\foste\Documents\_Dev\Github\Academia\RTPlanAI\data\processed'
    output_availability_file = os.path.join(processed_data_directory, 'data_availability.xlsx')
    
    # Load all data from the raw data directory
    patients_data = load_all_data(raw_data_directory, use_sample_data=True)
    
    # Export data availability
    export_data_availability(patients_data, output_availability_file)
    
    # Split data into training and testing sets
    training_set, testing_set = split_data(patients_data, test_size=0.2)
    print(f"Training set size: {len(training_set)}, Testing set size: {len(testing_set)}")
