import pickle
import numpy as np
import openpyxl

# name of diseases 
label = ['Liver cancer', 'Lung Cancer', 'Stomach cancer', 'Brain cancer', 'Respiratory diseases', 'Pneumonia', 'Heart diseases']

sheet_name = ['15-39', '40-49', '50-59', '60-69', '70-79']
num_disease = len(label)
num_age = 5

# 'Survive_d(s_age, s_gender) in the paper
p_lethal = np.zeros((num_disease, num_age, 2)).tolist()

p_preval = np.zeros((num_disease, num_age, 2)).tolist()
t_lethal = np.zeros((num_disease, num_age, 2)).tolist()
T_lethal = [51.09, 107.13, 47.98, 39.87, 32.96, 1, 69] # T_d for diseases
T_find = [20.73, 13.86, 26.89, 22.06, 3, 0.1, 10] # avg s_td for diseases

wb = openpyxl.load_workbook('death_rate.xlsx')

for i in range(num_age):
    ws = wb.get_sheet_by_name(sheet_name[i])
    j = 0
    chk = True
    for r in ws.rows:
        if chk:
            chk = False
            continue
        if r[0].value==None: break
        if r[1].value==None:p_lethal[j][i][0] = 1.0
        else: p_lethal[j][i][0] = 1-(r[1].value/100.0)
        if r[2].value==None:p_lethal[j][i][1] = 1.0
        else: p_lethal[j][i][1] = 1-(r[2].value/100.0)
        j+=1

wb = openpyxl.load_workbook('preval_rate.xlsx') 

for i in range(num_age):
    ws = wb.get_sheet_by_name(sheet_name[i])
    j = 0
    chk = True
    for r in ws.rows:
        if chk:
            chk = False
            continue
        else: p_preval[j][i][0] = r[1].value/100.0
        if r[0].value==None:break
        if r[1].value==None:p_preval[j][i][0] = 1.0
        if r[2].value==None:p_preval[j][i][1] = 1.0
        else: p_preval[j][i][1] = r[2].value/100.0
        j+=1
       
for i in range(num_disease):
    for j in range(num_age):
        for k in range(2):
            t_lethal[i][j][k] = T_lethal[i]

print(p_lethal) 
with open('disease_label.pkl', 'wb') as F:
    pickle.dump(label, F)

with open('disease_lethal.pkl', 'wb') as F:
    pickle.dump(p_lethal, F)

with open('time_lethal.pkl', 'wb') as F:
    pickle.dump(t_lethal, F)

with open('disease_preval.pkl', 'wb') as F:
    pickle.dump(p_preval, F)

with open('time_find.pkl', 'wb') as F:
    pickle.dump(T_find, F)
