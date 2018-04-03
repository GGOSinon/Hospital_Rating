from math import exp, log
import math
import numpy as np

class Patient:
    # age: int(0~5)
    # gender : int(0~1)
    # t, dt : int(0~200)
    # disease : int (0~7)
    # live : bool(False if dead, True if live)

    def __init__(self, age, gender, t, dt, health, disease, com, live):
        self.t = t
        self.dt = t+dt
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
        self.num_disease = 7
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
        self.num_disease = 7
        self.num_age = 5
        self.p_max_disease = np.zeros(self.num_disease).tolist()
        for D in range(self.num_disease):
            for i in range(self.num_age):
                for j in range(2):
                    self.p_max_disease[D] = max(self.p_max_disease[D], p_disease[D][i][j])
        #print(self.p_disease)
        #print(self.p_max_disease)

    def T(self, D, t):
        if D==0:
            if t>20: return 10 
            if t<20: return 1
        if D==1:
            if t>13: return 65
            if t<13: return 1
        if D==2:
            if t>30: return 15
            if t<30: return 1
        if D==3:
            if t>80: return 90
            if t<80: return 1
        if D==4:
            return math.sqrt(1+t*624/12)
        if D==5:
            return 0.5
        if D==6:
            return math.sqrt(1+t*624/12)

    def P_max(self, t, T_d):
        return 0.5*(-1.31*np.tanh(t/T_d-1)+1)

    def P_live(self, t, dt, D, K6):
        return 0.5*(np.tanh(dt/(self.T(D, t)*K6) - 1) + 1) # Sensitivity 6

    def total_prob(self, t, dt, D, T_d, K6):
        return self.P_live(t, dt, D, K6) * self.P_max(t, T_d)

    def f(self, P, K1 = 0.7, K2 = 1, K3 = 1, K6 = 1):
        p_lethal = 1.0
        D = P.disease
        val_lethal = self.p_disease[D][P.age][P.gender] / self.p_max_disease[D]
        val_com = 1 + K3 * (P.com - 1) # Sensitivity 3
        ctime = self.time_disease[D][P.age][P.gender] * K2# Sensitivity 2
        val_time = self.total_prob(P.t, P.dt, D, ctime, K6)
        #print(P.health)
        val_health = K1 + (1 - K1) * P.health # Sensitivity 1
        p_live = max(0.0, 1 - (1 - val_lethal * val_time * val_health) * val_com)
        #print(val_time, val_lethal*val_time*val_health, p_live)
        # probability to live
        if P.live: return (2.0 / (p_live+1)) - 1
        else: return 1 - (2.0 / (2-p_live))

    def g(self, H, D, K4 = 0.33, K5 = 1):
        c_g = K4 # Sensitivity 4
        d1 = H.exp_d1[D]
        d2 = H.exp_d2[D]
        t = 50 - 0.75 * d1
        val_exp_doc = pow(62.5*t/(t*t+25*25), 2*log(d2)/log(10))
        val_equip = math.sqrt(H.equipments[D])
        val_num_nurse = (1 + exp(-8))/(1 + exp(H.num_nurse-8))
        #print(val_equip, val_time_doc, val_lev_doc)
        if K5==1: return c_g * min(val_equip, val_exp_doc) * val_num_nurse
        if K5==2: return c_g * (val_equip + val_exp_doc) * val_num_nurse / 2.0



