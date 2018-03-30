class Patient:
    # age: int(0~5)
    # gender : int(0~1)
    # t, dt : int(0~200)
    # diseases : int[] (0~10)
    # live : bool(False if dead, True if live)

    def __init__(self, age, gender, t, dt, health, diseases, live):
        self.time_s = t
        self.time_e = t+dt
        self.gender = gender
        self.age = age
        self.health = health
        self.diseases = diseases
        self.live = live

class Hospital:

    def __init__(self, equipments, lev_doctors, num_doctors, patients):
        self.equipments = equipments
        self.lev_doctors = lev_doctors
        self.num_doctors = num_doctors
        self.patients = patients
        cnt_disease = [0]*10
        for P in patients:
            for D in P.diseases:
                #print(P.diseases, D, cnt_disease)
                cnt_disease[D] += 1
        self.num_patients = cnt_disease


class Calculator:

    # p_disease: [disease_num][age][gender]
    # time_disease: [disease_num][age][gender]
    def __init__(self, p_disease, time_disease):
        self.p_disease = p_disease
        self.time_disease = time_disease
        self.c_health = 0.1

    def F(self, x):
        return x/200.0

    def total_prob(self, s, e):
        #print(s, e)
        return self.F(e)-self.F(s) 
        # F is a antiderivative of time-prob function.

    def f(self, P):
        p_lethal = 1.0
        D = P.diseases[0]
        #print(d, P.age, P.gender)
        val_lethal = self.p_disease[D][P.age][P.gender]
        #for d in P.diseases:
        #    self.p_disease[d][p.gender][
        ctime = self.time_disease[D][P.age][P.gender]
        val_time = self.total_prob(P.time_s/ctime, P.time_e/ctime)
        val_health = self.c_health * P.health
        #print(val_lethal, val_time, val_health)
        p_live = val_lethal * val_time * val_health
        # probability to live
        if P.live: return (2.0/(p_live+1))-1
        else: return 1-(2.0/(2-p_live))

    def g(self, H, D):
        val_equip = H.equipments[D]
        val_time_doc = float(H.num_doctors[D])/H.num_patients[D]
        val_lev_doc = H.lev_doctors[D]
        #print(val_equip, val_time_doc, val_lev_doc)
        return val_equip*val_time_doc*val_lev_doc



