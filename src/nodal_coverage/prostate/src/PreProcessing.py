from src.InfoStructure.EvaluationTools import *
import os
from tqdm import tqdm
import pandas as pd


def return_dataframe_from_class_list(list_classes):
    return pd.DataFrame([vars(f) for f in list_classes])


def write_dataframe_to_excel(excel_path: Union[str, bytes, os.PathLike], dataframe: pd.DataFrame):
    with pd.ExcelWriter(excel_path) as writer:
        dataframe.to_excel(writer, index=False)
    return


def update_database(network_path, local_path):
    today = DateTimeClass()
    today.from_python_datetime(datetime.today())
    last_update_date = os.path.join(local_path, "Last_Updated.txt")
    if not os.path.exists(last_update_date):
        update_local_database(local_database_path=local_path,
                              network_database_path=network_path, tqdm=tqdm)
    else:
        last_update = DateTimeClass()
        fid = open(last_update_date)
        dates = fid.readline().split('.')
        fid.close()
        last_update.year = int(dates[0])
        last_update.month = int(dates[1])
        last_update.day = int(dates[2])
        if (today - last_update).days >= 1:
            update_local_database(local_database_path=local_path,
                                  network_database_path=network_path, tqdm=tqdm)


def identify_wanted_headers(patient_header_dbs: PatientHeaderDatabases,
                            wanted_roi_list: List[str], wanted_type: List[str]):
    out_header_dbs = PatientHeaderDatabases()
    wanted_type = [i.lower() for i in wanted_type]
    for pat_header_db in patient_header_dbs.HeaderDatabases.values():
        out_header_db = PatientHeaderDatabase(pat_header_db.DBName)
        for pat in pat_header_db.PatientHeaders.values():
            has_roi = False
            for case in pat.Cases:
                wanted_rois = [r for r in case.ROIS if r.Name.lower() in wanted_roi_list and
                               r.Type.lower() in wanted_type]
                if wanted_rois:
                    has_roi = True
            if has_roi:
                out_header_db.PatientHeaders[pat.RS_UID] = pat
        out_header_dbs.HeaderDatabases[out_header_db.DBName] = out_header_db
    return out_header_dbs


def find_all_rois(header_databases: PatientHeaderDatabases):
    """
    Code snippet to find the names of all rois
    Args:
        header_databases:

    Returns:

    """
    all_rois = []
    for header_database in header_databases.HeaderDatabases.values():
        for pat in header_database.PatientHeaders.values():
            for case in pat.Cases:
                for roi in case.ROIS:
                    if roi.Name.lower() not in all_rois:
                        all_rois.append(roi.Name.lower())
    reduced_all_rois = [i for i in all_rois if i.find('ptv') == -1 and i.find('0') == -1 and i.find('1') == -1 and i.find('opt') == -1 and i.find('2') == -1 and i.find('3') == -1 and i.find('hot') == -1 and i.find('cold') == -1 and i.find('avo') == -1 and i.find('norm') == -1 and i.find('tune') == -1 and i.find('5') == -1 and len(i) > 2 and i.find('ring') == -1 and i.find('couch') == -1 and i.find('arti') == -1 and i.find('max') == -1 and i.find('min') == -1 and i.find('4') == -1 and i.find('push') == -1 and i.find('shell') == -1 and i.find('warm') == -1]
    wanted_rois = [i for i in all_rois if i.find('nodes') != -1 or i.find('prost') != -1]


class RegionOfInterestClass:
    DataBase: str
    MRN: str
    ROIName: str  # Prostate, Breast
    ROIVolume: float
    ROIType: str  # CTV, PTV, GTV, Organ
    Case: str
    Exam: str


def find_prostate_patients():
    network_path = r'\\vscifs1\PhysicsQAdata\BMA\RayStationDataStructure\DataBases'
    local_db_path = r'C:\Users\u376045\Modular_Projects\Local_Databases'
    if not os.path.exists(local_db_path) and os.path.exists(r'C:\Users\Markb\Modular_Projects'):
        local_db_path = r'C:\Users\Markb\Modular_Projects\Local_Databases'
    MRNs = None
    """
    If we have a list of MRNs that we want specifically, we can add them
    """
    if os.path.exists(network_path):
        update_database(network_path, local_db_path)
    """
    Lets first load up just the basic information from all patients in our databases
    """
    header_databases: PatientHeaderDatabases
    header_databases = PatientHeaderDatabases()
    header_databases.build_from_folder(local_db_path, specific_mrns=MRNs, tqdm=tqdm)
    """
    We only want patients who have had approved plans
    """
    header_databases.delete_unapproved_patients()
    """
    Based on the desired ROIs, send back a subset of patients
    """
    roi_associations = {}
    roi_associations['prostate'] = ['prostate', 'prostate only']
    roi_associations['nodes'] = ['nodes', 'pelvic nodes', 'lymph nodes',
                                 'lymphnodes', 'pelvicnodes']
    wanted_rois = []
    for key in roi_associations.keys():
        wanted_rois += roi_associations[key]
    header_databases = identify_wanted_headers(header_databases,
                                               wanted_type=['gtv', 'ctv'],
                                               wanted_roi_list=wanted_rois)

    """
    Now, load up all patient info
    Note that this includes all plans
    """
    databases = header_databases.return_patient_databases(tqdm)
    databases.delete_unapproved_patients()
    out_rois: List[RegionOfInterestClass]
    out_rois = []
    mrns = []
    db_list = ['10ASP1', 'Deceased', '2023', '2022', '2021', '2020', '2019', '2018',
               '2017', '2016']
    for db_name in db_list:
        db = databases.Databases[db_name]
        for patient in db.Patients.values():
            if patient.MRN in mrns:
                continue
            mrns.append(patient.MRN)
            for case in patient.Cases:
                for exam in case.Examinations:
                    for roi in exam.ROIs:
                        if roi.Name.lower() in wanted_rois:
                            base_roi = [i for i in case.Base_ROIs if i.RS_Number == roi.RS_Number]
                            new_roi = RegionOfInterestClass()
                            new_roi.DataBase = db_name
                            new_roi.MRN = patient.MRN
                            new_roi.Exam = exam.ExamName
                            new_roi.Case = case.CaseName
                            new_roi.ROIName = roi.Name
                            new_roi.ROIType = base_roi[0].Type
                            new_roi.ROIVolume = roi.Volume
                            out_rois.append(new_roi)
    out_dataframe = return_dataframe_from_class_list(out_rois)
    write_dataframe_to_excel(os.path.join('.', "ProstateNodePatients.xlsx"), out_dataframe)


if __name__ == '__main__':
    find_prostate_patients()
