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

Cal = Calculator(p_lethal, t_lethal)
num_disease = len(p_lethal)
num_hospital = len(hospitals)

# For sensitivity analysis
#----------------------------------------------------
#for K1 in np.arange(0.6, 0.8+0.01, 0.1):
#for K2 in np.arange(0.75, 1.25+0.01, 0.25):
#for K3 in np.arange(1, 1.2+0.01, 0.1):
#for K4 in np.arange(0.22, 0.44+0.01, 0.11):
#for K5 in range(1, 3):
#for K6 in np.arange(0.9, 1.1+0.01, 0.1):
#----------------------------------------------------
if True:
    tot_val = [] # score_mor,d(H) for all hospitals
    tot_valf = [] # score_d(H) for all hospitals
    for i in range(num_hospital):
        H = hospitals[i]
        num_patients = len(H.patients)
        cnt = np.zeros(num_disease)
        val_f = [0]*num_disease # score_mor,d(H)
        val_g = [0]*num_disease # score_extra,d(H)
        for P in H.patients:	
            val_moral = Cal.f(P, K1=K1) # val_mor,d(s)
            D = P.disease 
            cnt[D] += 1
            val_f[D] += val_moral
     
        for D in range(num_disease):
            val_f[D] /= cnt[D] 
        
        for D in range(num_disease):
            val_g[D] = Cal.g(H, D)
         
        val_h = [] # score_d(H)
        for D in range(num_disease):
            print(val_f[D], val_g[D])
            val_h.append(val_f[D]+val_g[D]) 
        tot_val.append(val_h)
        tot_valf.append(val_f)
    # For sensitivity analysis
    #----------------------------------------------------
    '''
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
    '''
    #-----------------------------------------------------
