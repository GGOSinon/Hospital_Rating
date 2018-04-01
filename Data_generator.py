import pickle
import random
from Functions import Patient, Hospital

def make_random(P):
    r = random.random()
    S = 0.0
    #print(P)
    for i in range(len(P)):
        S+=P[i]
        if r<S: return i

num_patient = [5000, 1000, 3000, 2000, 10000]
num_disease = 8
prob_disease = [0]*num_disease
num_hospital = len(num_patient)
t_find = [0]*num_disease
dt_find = [0]*num_disase

with open('disease_perval.pkl', 'rb') as F:
    p_preval = pickle.load(F)

with open('disease_lethal.pkl', 'rb') as F:
    p_lethal = pickle.load(F)

for i in range(num_disease):
    for j in range(num_age):
        for k in range(num_gender):
            prob_disease[i]+=p_preval[i][j][k]

S = 0.0 
for i in range(num_disease): S+=prob_disease[i]
for i in range(num_disease): prob_disease[i]/=S

def set_ga(D):
    PG = [0]*2
    for i in range(2):
        for j in range(6):
            PG[i] += p_preval[i][j]
    gender = make_random(PG)
    PA = [0]*6
    for i in range(2):
        for j in range(6):
            PA[j] += p_preval[i][j]
    age = make_random(PA)
    return gender, age

def set_tdt(D):
    t = t_find[i]*max(np.random.normal(loc = 1, scale = 0.5), 0)
    dt = dt_find[i]*max(np.random.normal(loc = 1, scale = 1), 0)
    return t, dt

def set_live(D, age, gender):
    r = random.random()
    if r<p_lethal[D][age][gender]: return False
    return True

with open('disease_perval.pkl', 'rb') as F:
    p_preval = pickle.load(F)

hospitals = []

for i in range(num_hospital):
    patients = []
    for j in range(num_patient[i]):
        r = random.random()
        disease = make_random(prob_disease)
        gender, age = set_ga(disease)
        t, dt = set_tdt(disease)
        live = set_live(disease, age, gender)
        health = random.random()
        patients.append(Patient(age, gender, t, dt, health, disease, live))
    equipments = []
    lev_doc = []
    num_doc = [] 
    for D in range(num_disease):
        r = random.random()
        equipments.append(int(r*5)+1)
        r = random.random()
        lev_doc.append(int(r*5)+1)
        r = random.random()
        num_doc.append(int(r*100)+1)
    hospitals.append(Hospital(equipments, lev_doc, num_doc, patients))

with open('hospitals.pkl', 'wb') as F:
    pickle.dump(hospitals, F)
