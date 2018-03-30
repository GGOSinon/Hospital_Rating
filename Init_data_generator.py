import pickle
import numpy as np
import openpyxl

label = ['Liver cancer', 'Lung Cancer', 'Stomach cancer', 'Brain cancer', 'Alzheimer', 'Respirstory diseases', 'Stroke', 'Diabetes', 'Pneumonia', 'Heart diseases']

num_disease = len(label)

p_lethal = np.ones((num_disease, 6, 2)).tolist()
t_lethal = np.ones((num_disease, 6, 2)).tolist()

wb = openpyxl.load_workbook('data.xlsx')
for i in range(6):
    ws = wb.get_sheet_by_name("Sheet"+str(i+1))
    j = 0
    for r in ws.rows:
        if r[0].value==None: break
        p_lethal[j][i][0] = r[1].value
        p_lethal[j][i][1] = r[2].value
        j+=1
    
with open('disease_label.pkl', 'wb') as F:
    pickle.dump(label, F)

with open('disease_lethal.pkl', 'wb') as F:
    pickle.dump(p_lethal, F)

with open('time_lethal.pkl', 'wb') as F:
    pickle.dump(t_lethal, F)
