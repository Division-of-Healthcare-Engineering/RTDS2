import os
import SimpleITK as sitk
from PlotScrollNumpyArrays.Plot_Scroll_Images import plot_scroll_Image
from DicomRTTool.ReaderWriter import DicomReaderWriter, ROIAssociationClass


base_path = r'\\vscifs1\PhysicsQAdata\BMA\Prostate_Nodes'
associations = [ROIAssociationClass('prostate', ['prostate', 'prostate only']),
                ROIAssociationClass('nodes', ['nodes', 'pelvic nodes', 'lymph nodes',
                                              'lymphnodes', 'pelvicnodes'])]
for root, directories, files in os.walk(base_path):
    if [i for i in files if i.endswith('.dcm')]:
        if 'Image.nii.gz' in files:
            continue
        reader = DicomReaderWriter(description='Prosate_and_nodes', associations=associations,
                                   arg_max=True, Contour_Names=['nodes', 'prostate'])
        reader.down_folder(root)
        for i in reader.indexes_with_contours:
            reader.set_index(i)
            reader.get_images_and_mask()
            sitk.WriteImage(reader.dicom_handle, os.path.join(root, f"Image.nii.gz"))
            sitk.WriteImage(reader.annotation_handle, os.path.join(root, f"Mask.nii.gz"))
            break
        x = 1