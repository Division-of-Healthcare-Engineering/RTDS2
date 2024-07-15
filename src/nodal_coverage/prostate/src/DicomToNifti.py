import os
import SimpleITK as sitk
from PlotScrollNumpyArrays.Plot_Scroll_Images import plot_scroll_Image
from DicomRTTool.ReaderWriter import DicomReaderWriter, ROIAssociationClass
from typing import *

def sum_images(image_handles: List[sitk.Image]):
    # Read the first image
    sum_image = image_handles[0]

    # Iterate over the remaining images and add them to the sum_image
    for image_handle in image_handles[1:]:
        sum_image = sitk.Add(sum_image, image_handle)

    return sum_image


base_path = r'\\vscifs1\PhysicsQAdata\BMA\Prostate_Nodes'
associations = [ROIAssociationClass('prostate', ['prostate', 'prostate only'])]
for root, directories, files in os.walk(base_path):
    if [i for i in files if i.endswith('.dcm')]:
        print(f"Running {root}")
        if 'Image.nii.gz' not in files:
            reader = DicomReaderWriter()
            reader.down_folder(root)
            for i in reader.series_instances_dictionary.keys():
                reader.set_index(i)
                reader.get_images()
                sitk.WriteImage(reader.dicom_handle, os.path.join(root, f"Image.nii.gz"))
                break
        if 'Mask.nii.gz' not in files:
            mhd_files = [i for i in files if i.endswith('.mhd')]
            if mhd_files:
                image_handles = [sitk.ReadImage(os.path.join(root, f)) for f in mhd_files]
                mask_handle = sum_images(image_handles)
                sitk.WriteImage(mask_handle, os.path.join(root, "Mask.nii.gz"))