import pickle
import random
from Functions import Patient, Hospital

num_patient = [5000, 1000, 3000, 2000, 10000]
num_hospital = len(num_patient)
num_disease = 10
prob_live = 0.3

hospitals = []

for i in range(num_hospital):
    patients = []
    for j in range(num_patient[i]):
        r = random.random()
        if r<prob_live: live = True
        else: live = False
        gender = random.randrange(0,2)
        age = random.randrange(0,6)
        t = random.randrange(0,200)
        dt = random.randrange(1,100)
        num_com = random.randrange(1, 3)
        health = random.random()
        diseases = []
        for k in range(num_com):
            diseases.append(random.randrange(0, num_disease))
        patients.append(Patient(age, gender, t, dt, health, diseases, live))
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
