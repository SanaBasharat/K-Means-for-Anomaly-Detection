# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 20:07:01 2020

@author: Fahad Siddiqui
"""

import pandas as pd

class DATAPREPROCESSING:
    
    
    def __init__(self, TrainBenifile, TrainInfile, TrainOutfile, Trainfile):
        print("Initializing Object...")
        self.TrainBenifile = TrainBenifile
        self.TrainInfile = TrainInfile
        self.TrainOutfile = TrainOutfile
        self.Trainfile = Trainfile
    
    
    def Processing(self):
        self.TrainBeni = pd.read_csv(self.TrainBenifile)
        self.TrainBeni['DOB'] = pd.to_datetime(self.TrainBeni['DOB'] , format = '%Y/%m/%d')
        self.TrainBeni['DOD'] = pd.to_datetime(self.TrainBeni['DOD'],format = '%Y/%m/%d',errors='ignore')
        self.TrainBeni['Age'] = round(((self.TrainBeni['DOD'] - self.TrainBeni['DOB']).dt.days)/365)
        self.TrainBeni.Age.fillna(round(((pd.to_datetime('2009-12-01' , format = '%Y-%m-%d') - self.TrainBeni['DOB']).dt.days)/365),inplace=True)
        self.TrainBeni.loc[self.TrainBeni.DOD.isna(),'IsDead']=0
        self.TrainBeni.loc[self.TrainBeni.DOD.notna(),'IsDead']=1
        self.TrainIn = pd.read_csv(self.TrainInfile)
        self.TrainIn['AdmissionDt'] = pd.to_datetime(self.TrainIn['AdmissionDt'] , format = '%Y-%m-%d')
        self.TrainIn['DischargeDt'] = pd.to_datetime(self.TrainIn['DischargeDt'],format = '%Y-%m-%d')
        self.TrainIn['AdmitDays'] = ((self.TrainIn['DischargeDt'] - self.TrainIn['AdmissionDt']).dt.days)+1
        self.TrainOut = pd.read_csv(self.TrainOutfile)
        self.TrainInOut=pd.merge(self.TrainOut,self.TrainIn,
                              left_on=['BeneID', 'ClaimID', 'ClaimStartDt', 
                                        'ClaimEndDt', 'Provider','InscClaimAmtReimbursed', 
                                        'AttendingPhysician', 'OperatingPhysician',
                                        'OtherPhysician', 'ClmDiagnosisCode_1', 
                                        'ClmDiagnosisCode_2','ClmDiagnosisCode_3', 
                                        'ClmDiagnosisCode_4', 'ClmDiagnosisCode_5',
                                        'ClmDiagnosisCode_6', 'ClmDiagnosisCode_7', 
                                        'ClmDiagnosisCode_8','ClmDiagnosisCode_9', 
                                        'ClmDiagnosisCode_10', 'ClmProcedureCode_1',
                                        'ClmProcedureCode_2', 'ClmProcedureCode_3', 
                                        'ClmProcedureCode_4','ClmProcedureCode_5', 
                                        'ClmProcedureCode_6', 'DeductibleAmtPaid',
                                        'ClmAdmitDiagnosisCode'],
                              right_on=['BeneID', 'ClaimID', 'ClaimStartDt', 'ClaimEndDt', 
                                        'Provider','InscClaimAmtReimbursed', 
                                        'AttendingPhysician', 'OperatingPhysician',
                                        'OtherPhysician', 'ClmDiagnosisCode_1', 
                                        'ClmDiagnosisCode_2','ClmDiagnosisCode_3', 
                                        'ClmDiagnosisCode_4', 'ClmDiagnosisCode_5',
                                        'ClmDiagnosisCode_6', 'ClmDiagnosisCode_7', 
                                        'ClmDiagnosisCode_8','ClmDiagnosisCode_9', 
                                        'ClmDiagnosisCode_10', 'ClmProcedureCode_1',
                                        'ClmProcedureCode_2', 'ClmProcedureCode_3', 
                                        'ClmProcedureCode_4','ClmProcedureCode_5', 
                                        'ClmProcedureCode_6', 'DeductibleAmtPaid',
                                        'ClmAdmitDiagnosisCode']
                              ,how='outer')
        
        self.TrainInOutBeni=pd.merge(self.TrainInOut,self.TrainBeni,left_on='BeneID',right_on='BeneID',how='inner')
        self.Train = pd.read_csv(self.Trainfile)
        self.Train = pd.merge(self.Train,self.TrainInOutBeni, on='Provider')
        remove=['BeneID', 'ClaimID', 'ClaimEndDt',
               'OperatingPhysician', 'OtherPhysician', 'ClmDiagnosisCode_1',
               'ClmDiagnosisCode_2', 'ClmDiagnosisCode_3', 'ClmDiagnosisCode_4',
               'ClmDiagnosisCode_5', 'ClmDiagnosisCode_6', 'ClmDiagnosisCode_7',
               'ClmDiagnosisCode_8', 'ClmDiagnosisCode_9', 'ClmDiagnosisCode_10',
               'ClmProcedureCode_1', 'ClmProcedureCode_2', 'ClmProcedureCode_3',
               'ClmProcedureCode_4', 'ClmProcedureCode_5', 'ClmProcedureCode_6',
               'ClmAdmitDiagnosisCode', 'AdmissionDt',
               'DischargeDt', 'DiagnosisGroupCode','DOB', 'DOD', 'County','AdmitDays', 'RenalDiseaseIndicator',
                'NoOfMonths_PartACov', 'NoOfMonths_PartBCov', 'ChronicCond_Alzheimer', 'ChronicCond_Heartfailure',
                'ChronicCond_KidneyDisease', 'ChronicCond_Cancer', 'ChronicCond_ObstrPulmonary', 'ChronicCond_Depression',
                'ChronicCond_Diabetes', 'ChronicCond_IschemicHeart', 'ChronicCond_Osteoporasis',
                'ChronicCond_rheumatoidarthritis', 'ChronicCond_stroke', 'IsDead', 'ClaimStartDt', 'DeductibleAmtPaid', 'AttendingPhysician']
        self.TrainClean = self.Train.drop(axis=1,columns=remove)
        # self.TrainClean['ClaimStartDt'] = pd.to_datetime(self.TrainClean['ClaimStartDt'] , format = '%Y/%m/%d')
        self.TrainClean['Provider'] = self.TrainClean['Provider'].str.replace("PRV","")
        self.TrainClean['Provider'] = self.TrainClean['Provider'].astype(int)
        # self.TrainClean['AttendingPhysician'] = self.TrainClean['AttendingPhysician'].str.replace("PHY", "")
        # self.TrainClean['AttendingPhysician'] = self.TrainClean['AttendingPhysician'].astype(float)
        return self.TrainClean
        
