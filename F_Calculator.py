import pickle
import numpy as np
from Functions import Calculator

with open('disease_label.pkl', 'rb') as F:
    label = pickle.load(F)

with open('disease_lethal.pkl', 'rb') as F:
    p_lethal = pickle.load(F)

with open('time_lethal.pkl', 'rb') as F:
    t_lethal = pickle.load(F)

with open('hospitals.pkl', 'rb') as F:
    hospitals = pickle.load(F)

print(p_lethal)
#with open('patients.pkl', 'rb') as F:
    #patients = pickle.load(F)

Cal = Calculator(p_lethal, t_lethal)
num_disease = len(p_lethal)
num_hospital = len(hospitals)

tot_val = []

print(num_hospital)

for i in range(num_hospital):
    H = hospitals[i]
    num_patients = len(H.patients)
    cnt = np.zeros(num_disease)
    val_f = [0]*num_disease
    val_g = [0]*num_disease
    for P in H.patients:
        val_moral = Cal.f(P)
        D = P.disease
        if i==4 and D==6: print(val_moral)
        cnt[D] += 1
        val_f[D] += val_moral
 
    for D in range(num_disease):
        val_f[D] /= cnt[D]
    
    for D in range(num_disease):
        val_g[D] = Cal.g(H, D)
     
    val_h = []
    for D in range(num_disease):
        print(val_f[D], val_g[D])
        val_h.append(val_f[D]+val_g[D])
    print('\n')
    tot_val.append(val_h)

F = open('data.txt', 'w')
for D in range(num_disease):
    F.write(label[D]+" ")
    for h in range(num_hospital):
        F.write(str(tot_val[h][D])+" ")
    F.write("\n")

        
