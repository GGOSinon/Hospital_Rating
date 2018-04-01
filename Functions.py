from math import exp, log
import math
import numpy as np

class Patient:
    # age: int(0~5)
    # gender : int(0~1)
    # t, dt : int(0~200)
    # disease : int (0~8)
    # live : bool(False if dead, True if live)

    def __init__(self, age, gender, t, dt, health, disease, com, live):
        self.time_s = t
        self.time_e = t+dt
        self.gender = gender
        self.age = age
        self.health = health
        self.disease = disease
        self.com = com
        self.live = live

class Hospital:

    def __init__(self, equipments, exp_d1, exp_d2, num_nurse, patients):
        self.equipments = equipments
        self.exp_d1 = exp_d1
        self.exp_d2 = exp_d2
        self.num_nurse = num_nurse
        self.patients = patients
        self.num_disease = 8
        cnt_disease = [0]*self.num_disease
        for P in patients:
            D = P.disease
            cnt_disease[D] += 1
        print(cnt_disease)
        self.num_patients = cnt_disease


class Calculator:

    # p_disease: [disease_num][age][gender]
    # time_disease: [disease_num][age][gender]
    def __init__(self, p_disease, time_disease):
        self.p_disease = p_disease
        self.time_disease = time_disease
        self.num_disease = 8
        self.num_age = 5
        self.p_max_disease = np.zeros(self.num_disease).tolist()
        for D in range(self.num_disease):
            for i in range(self.num_age):
                for j in range(2):
                    self.p_max_disease[D] = max(self.p_max_disease[D], p_disease[D][i][j])
        #print(self.p_disease)
        #print(self.p_max_disease)
        self.c_health = 1

    def F(self, x):
        return 1-(log(exp(1-x)+1) / log(math.e+1))

    def total_prob(self, s, e):
        #print(s, e)
        return self.F(e)-self.F(s) 
        # F is a antiderivative of time-prob function.

    def f(self, P):
        p_lethal = 1.0
        D = P.disease
        val_lethal = self.p_disease[D][P.age][P.gender] / self.p_max_disease[D]
        #if self.p_max_disease[D]<1: print(val_lethal, self.p_disease[D][P.age][P.gender], self.p_max_disease[D])
        val_com = P.com
        ctime = self.time_disease[D][P.age][P.gender]
        val_time = self.total_prob(P.time_s / ctime, P.time_e / ctime)
        val_health = self.c_health * P.health
        p_live = max(0.0, 1 - (1 - val_lethal * val_time * val_health) * val_com)
        # probability to live
        #print(val_time, val_lethal * val_time * val_health, p_live, D)
        if P.live: return (2.0 / (p_live+1)) - 1
        else: return 1 - (2.0 / (2-p_live))

    def g(self, H, D):
        c_g = 0.33
        d1 = H.exp_d1[D]
        d2 = H.exp_d2[D]
        t = 50 - 0.75 * d1
        val_exp_doc = pow(62.5*t/(t*t+25*25), 2*log(d2)/log(10))
        val_equip = math.sqrt(H.equipments[D])
        val_num_nurse = (1 + exp(-8))/(1 + exp(H.num_nurse-8))
        #print(val_equip, val_time_doc, val_lev_doc)
        return c_g * min(val_equip, val_exp_doc) * val_num_nurse



