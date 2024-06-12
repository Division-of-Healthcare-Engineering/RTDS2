import os
from queue import *
from src.InfoStructure.EvaluationTools import *
import os
import numpy as np
from matplotlib import pyplot as plt
from threading import Thread
from multiprocessing import cpu_count
from tqdm import tqdm
from time import time
from glob import glob
import pickle
import pandas as pd


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


class RegionOfInterestClass:
    ROIName: str  # Prostate, Breast
    ROIVolume: float
    ROIType: str  # CTV, PTV, GTV, Organ


class PatientInfo:
    ROIs: List[RegionOfInterestClass]
    MRN: str


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
    header_databases = identify_wanted_headers(header_databases,
                                               wanted_type=['gtv', 'ctv'],
                                               wanted_roi_list=['prostate'])
    """
    Now, load up all patient info
    Note that this includes all plans
    """
    databases = header_databases.return_patient_databases(tqdm)
    databases.delete_unapproved_patients()


if __name__ == '__main__':
    find_prostate_patients()
