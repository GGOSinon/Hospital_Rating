import pickle
import random
import numpy as np
from Functions import Patient, Hospital
from G_Functions import GCalculator

def make_random(P):
    r = random.random()
    S = 0.0
    #print(P)
    for i in range(len(P)):
        S+=P[i]
        if r<S: return i

num_patient = [10000]*50
num_disease = 7
num_hospital = len(num_patient)

with open('disease_preval.pkl', 'rb') as F:
    p_preval = pickle.load(F)

with open('disease_lethal.pkl', 'rb') as F:
    p_lethal = pickle.load(F)

with open('time_find.pkl', 'rb') as F:
    T_find = pickle.load(F)

Cal = GCalculator(p_preval, p_lethal, T_find)
hospitals = []
alphas = np.ones((num_hospital, num_disease)).tolist()

#for i in range(num_disease): 
    #alphas[0][i] = 0

for i in range(num_hospital):
    patients = []
    for j in range(num_patient[i]):
        patients.append(Cal.get_patient(alphas[i]))
    equipments = []
    exp_d1 = []
    exp_d2 = []
    for D in range(num_disease):
        r = random.randrange(1,6)
        equipments.append(r)
        r = random.random()
        exp_d1.append(r*50)
        r = random.random()
        exp_d2.append(r*99+1)
    r = random.random()
    num_nurse = r*9+3
    hospitals.append(Hospital(equipments, exp_d1, exp_d2, num_nurse, patients))

with open('hospitals.pkl', 'wb') as F:
    pickle.dump(hospitals, F)
