import sys
import os
sys.path.append(os.path.join('.', '..', '..', '..', '..'))
from src.InfoStructure.RaystationExportTools import *
import pandas as pd


def excel_to_text():
    excel_path = os.path.join('.', "ProstateNodePatients.xlsx")
    df = pd.read_excel(excel_path, sheet_name="Selected Prostate Patients")
    fid = open(os.path.join('.', 'rs_patients.txt'), 'w+')
    for i in range(df.shape[0]):
        if df['ROIName'][i].lower() == 'prostate':
            if 30 <= df['ROIVolume'][i] <= 50:
                fid.write(df["MRN"][i] + '|' + df['Case'][i] + '|' + df['Exam'][i] + '|' + df['ROIName'][i] + '\n')
    fid.close()


def main():
    if not os.path.exists(os.path.join('.', 'rs_patients.txt')):
        excel_to_text()
        return
    pats_to_export = []
    fid = open(os.path.join('.', 'rs_patients.txt'))
    pats = fid.readlines()
    fid.close()
    for i in pats:
        pat_info = i.strip('\n').split('|')
        patient = PatientClass()
        patient.MRN = pat_info[0]
        patient.define_rs_uid()
        case = CaseClass()
        case.CaseName = pat_info[1]
        exam = ExaminationClass()
        exam.ExamName = pat_info[2]
        exam.ROIs = []
        roi = RegionOfInterest()
        roi.define_name(pat_info[3])
        exam.ROIs.append(roi)
        case.Examinations.append(exam)
        patient.Cases.append(case)
        pats_to_export.append(patient)
    export_class = ExportBaseClass()
    base_export_path = r'\\vscifs1\PhysicsQAdata\BMA\Prostate_Nodes'
    export_class.set_export_path(base_export_path)
    for pat in pats_to_export:
        if os.path.exists(os.path.join(base_export_path, pat.RS_UID)):
            continue
        try:
            export_class.set_patient(pat)
        except:
            continue
        if export_class.RSPatient is None:
            continue
        export_class.export_examinations_and_structures(pat)
        export_class.export_rois_as_meta_images(pat)


if __name__ == '__main__':
    main()
