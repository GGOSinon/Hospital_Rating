import pickle
import numpy as np
from Functions import Calculator
from operator import itemgetter
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

print(num_hospital)

for K1 in np.arange(0.6, 0.8+0.01, 0.1):
#for K2 in np.arange(0.75, 1.25+0.01, 0.25):
#for K3 in np.arange(1, 1.2+0.01, 0.1):
#for K6 in np.arange(0.8, 1.2+0.01, 0.1):
#for K4 in np.arange(0.22, 0.44+0.01, 0.11):
#for K5 in range(1, 3):
    tot_val = []
    tot_valf = []
    for i in range(num_hospital):
        H = hospitals[i]
        num_patients = len(H.patients)
        cnt = np.zeros(num_disease)
        val_f = [0]*num_disease
        val_g = [0]*num_disease
        for P in H.patients:	
            val_moral = Cal.f(P, K1=K1)
            D = P.disease
            #if i==4 and D==6: print(val_moral)
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
        tot_valf.append(val_f)

    F = open('./result/data'+'K1='+str(K1)+'.txt', 'w')
    for D in range(num_disease):
        F.write(label[D]+" ")
        for H in range(num_hospital):
            F.write(str(tot_val[H][D])+" ")
        F.write("\n")

    F = open('./result/top3'+'K1='+str(K1)+'.txt', 'w')
    for D in range(num_disease):
        L = []
        for H in range(num_hospital):
            L.append((tot_val[H][D], H))   
        L = sorted(L, key=itemgetter(0), reverse=True)
        for i in range(3):
            F.write(str(L[i][1])+" ")
        F.write("\n")

    F = open('./result/top3f'+'K1='+str(K1)+'.txt', 'w')
    for D in range(num_disease):
        L = []
        for H in range(num_hospital):
            L.append((tot_valf[H][D], H))   
        L = sorted(L, key=itemgetter(0), reverse=True)
        for i in range(3):
            F.write(str(L[i][1])+" ")
        F.write("\n")

