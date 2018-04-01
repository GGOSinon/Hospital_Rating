import numpy as np
import random as random
from Functions import Patient, Hospital
from scipy.stats import truncnorm

class GCalculator:

    def normalize(self, P):
        S = 0.0 
        for i in range(len(P)): S+=P[i]
        for i in range(len(P)): P[i]/=S
        return P

    def __init__(self, p_preval, p_lethal, t_find):
        self.p_preval = p_preval
        self.p_lethal = p_lethal
        self.num_disease = 7
        self.num_age = 5
        self.t_find = t_find
        self.dt_find = [100]*self.num_disease

        prob_disease = [0]*self.num_disease
        for i in range(self.num_disease):
            for j in range(self.num_age):
                for k in range(2):
                    prob_disease[i]+=p_preval[i][j][k]
        prob_disease = [1]*self.num_disease
        self.prob_disease = self.normalize(prob_disease)
        
        PG = np.zeros((self.num_disease, 2)).tolist()
        self.PG = np.zeros((self.num_disease, 2)).tolist()
        for D in range(self.num_disease):
            for i in range(2):
                for j in range(self.num_age):
                    PG[D][i] += self.p_preval[D][j][i]
            self.PG[D] = self.normalize(PG[D])

        PA = np.zeros((self.num_disease, self.num_age)).tolist()
        self.PA = np.zeros((self.num_disease, self.num_age)).tolist()
        for D in range(self.num_disease):
            for i in range(2):
                for j in range(self.num_age):
                    PA[D][j] += self.p_preval[D][j][i]
            self.PA[D] = self.normalize(PA[D])

    def make_random(self, P):
        r = random.random()
        S = 0.0
        #print(P)
        for i in range(len(P)):
            S+=P[i]
            if r<S: return i

    def set_ga(self, D):        
        gender = self.make_random(self.PG[D])
        age = self.make_random(self.PA[D])
        return gender, age

    def set_tdt(self, D):
        t = self.t_find[D]*max(np.random.normal(loc = 1, scale = 0.5), 0) 
        dt = self.dt_find[D]*max(np.random.normal(loc = 1, scale = 0.3), 0)
        return t, dt

    def set_live(self, D, age, gender, alpha = 1):  
        r = random.random()
        #print(D, age, gender)
        if r<self.p_lethal[D][age][gender]*alpha: return True
        return False

    def get_patient(self, alphas):
        disease = self.make_random(self.prob_disease)
        gender, age = self.set_ga(disease)
        t, dt = self.set_tdt(disease)
        live = self.set_live(disease, age, gender, alphas[disease])
        health = np.random.normal(loc = 0.8, scale = 0.1)
        #print(health)
        com = 1 + abs(np.random.normal(loc = 0, scale = 0.1))
        #com = abs(truncnorm(a = -10, b = 10, scale = 0.1).rvs()) * 1.5 + 1 # 1~2.5
        return Patient(age, gender, t, dt, health, disease, com, live)


