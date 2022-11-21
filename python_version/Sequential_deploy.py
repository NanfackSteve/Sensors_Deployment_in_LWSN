#!/bin/python3
# -*-coding: utf-8-*

import matplotlib.pyplot as plt
from collections import OrderedDict

# ------------------ Define Differents Line Style -------------------

linestyles_dict = OrderedDict(
    [
        ("solid", (0, ())),
        ("loosely dotted", (0, (1, 10))),
        ("dotted", (0, (1, 5))),
        ("densely dotted", (0, (1, 1))),
        ("loosely dashed", (0, (5, 10))),
        ("dashed", (0, (5, 5))),
        ("densely dashed", (0, (5, 1))),
        ("loosely dashdotted", (0, (3, 10, 1, 10))),
        ("dashdotted", (0, (3, 5, 1, 5))),
        ("densely dashdotted", (0, (3, 1, 1, 1))),
        ("loosely dashdotdotted", (0, (3, 10, 1, 10, 1, 10))),
        ("dashdotdotted", (0, (3, 5, 1, 5, 1, 5))),
        ("densely dashdotdotted", (0, (3, 1, 1, 1, 1, 1))),
    ]
)


class LWSN:
    """LWSN - Linear Wireless Sensors Network

    Args:
        N: "Number of sensors"
        K: "Number of Virtual Nodes"
    """

    def __init__(self, N, K):
        """initialize the LWSN with K and N"""

        self.K = K
        self.N = N
        self.T = list()
        self.Oi = list([0] * K)
        self.n = list([0] * K)
        self.Ei = list([0] * K)

    def greedy_deployment(self, lambda_, alpha, p):
        """Determines the number of sensors of each Virtual Node"""

        # remise a zero
        if (sum(self.n) != 0):
            self.T.clear()
            self.Oi = list([0] * self.K)
            self.n = list([0] * self.K)
            self.Ei = list([0] * self.K)

        for virtual_node in range(0, self.K):
            self.T.append(self.calculate_T(virtual_node, lambda_, p))

        self.n = [1 for _ in range(0, self.K)]  # ajoute 1 capteur dans chaq Bi
        remaining_sensors = self.N - self.K  # il reste N - K capteurs

        while remaining_sensors >= 0:
            for virtual_node in range(0, self.K):
                self.Oi[virtual_node] = self.calculate_O(
                    virtual_node, lambda_, alpha, p
                )

            setI = [i for i, o in enumerate(self.Oi) if o == max(self.Oi)]
            i = max(setI)
            self.n[i] = self.n[i] + 1
            remaining_sensors = remaining_sensors - 1
        return self.n

    def uniform_deployment(self, lambda_, alpha, p):
        """Uniform sensors deployment"""

        # remise a zero
        if (sum(self.n) != 0):
            self.T.clear()
            self.Oi = list([0] * self.K)
            self.n = list([0] * self.K)
            self.Ei = list([0] * self.K)

        for virtual_node in range(0, self.K):
            self.n[virtual_node] = self.N / self.K

        for virtual_node in range(0, self.K):
            self.T.append(self.calculate_T(virtual_node, lambda_, p))

        for virtual_node in range(0, self.K):
            self.Oi[virtual_node] = self.calculate_O(virtual_node, lambda_, alpha, p)

    # -------------------------------------------------------------------

    def calculate_T(self, i, lambda_, p):
        """Virtual Node Traffic calculation"""

        Ti = (lambda_ / (p + 1)) * (
            (p / (p + 1)) + (((-p) ** (i + 1)) / (p + 1)) + (i + 1)
        )
        return Ti

    def calculate_O(self, i, lambda_, alpha, p):
        """Calculation of the maximum number of operations of a sensor"""

        Ti_bar = (
            self.T[i] / self.n[i]
        )  # nbre moy. de transmission de chaque capteur de Bi
        Ri_rsc = self.T[i] * ((self.n[i] - 1) / self.n[i])
        Ri_ps = 0

        if i == 0:  # sur le 1er noeud virtuel Ri_rsnr=0, Ri_rsf=0,Ri_rsr=0
            Ri_ps = ((self.T[i] - lambda_) / self.n[i]) + alpha * Ri_rsc

        if i > 0 and i < self.K - 2:  # Pour les 2 et K - 2 noeuds Virt.
            Ri_rsnr = p * self.T[i - 1]
            Ri_rsf = self.T[i + 1] + p * self.T[i + 2]
            Ri_rsr = ((self.T[i] - lambda_) * (self.n[i] - 1)) / self.n[i]
            Ri_ps = ((self.T[i] - lambda_) / self.n[i]) + alpha * (
                Ri_rsr + Ri_rsnr + Ri_rsf + Ri_rsc
            )

        if i == self.K - 2:
            Ri_rsnr = p * self.T[i - 1]
            Ri_rsf = self.T[i + 1]
            Ri_rsr = ((self.T[i] - lambda_) * (self.n[i] - 1)) / self.n[i]
            Ri_ps = ((self.T[i] - lambda_) / self.n[i]) + alpha * (
                Ri_rsr + Ri_rsnr + Ri_rsf + Ri_rsc
            )

        if i == self.K - 1:  # sur le dernier noeud Ri_rsf = 0
            Ri_rsnr = p * self.T[i - 1]
            Ri_rsr = ((self.T[i] - lambda_) * (self.n[i] - 1)) / self.n[i]
            Ri_ps = ((self.T[i] - lambda_) / self.n[i]) + alpha * (
                Ri_rsr + Ri_rsnr + Ri_rsc
            )

        return Ti_bar + Ri_ps

    def calculate_Ei(self, P, t):
        """Calculation of average Energy consumed by a sensor,
        in the Virtual Node Bi per time unit"""

        for i in range(0, self.K):
            self.Ei[i] = self.Oi[i] * P * t

    def life_Time(self, delta, Enode):
        """Calculation of the Lifetime of Network"""

        self.calculate_Ei(0.0619, 0.004096)
        Emax = max(self.Ei)
        return (Enode / Emax) * delta


def graphic_greedy_deployment(symbol, color):

    # ------------------ Parametres d'Affichage -------------------

    plt.title(
        "Spatial nodes Distribution with \n " + "K = 10, N = 30  and p = 0.5 ",
        color="blue",
    )
    plt.xlabel(" Virtual Node Index ")
    plt.xlim(1, 10)

    plt.ylim(0, 22)
    plt.ylabel(" Deployed Nodes")

    # ------------------ Deploiement en fonction de Alpha --------------

    alpha_values = [0.0, 0.1, 0.4, 0.6, 1]

    for j, alpha in enumerate(alpha_values):

        Si = LWSN(30, 10).greedy_deployment(1, alpha, 0.5)

        plt.plot(
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            Si,
            symbol[j],
            label="\u03B1 : {}".format(alpha * 1),
            color=color[j],
            lw=1,
            linestyle=linestyles_dict["densely dotted"],
        )
    plt.legend()
    plt.grid()
    plt.show()


def graphic_LifeTime(symbol):

    # ------------------ Parametres d'Affichage -------------------

    plt.title(
        "Impact of node's number on LWSN Lifetime \n "
        + "K = 10, p = 0.0  and \u03B1 = 0.1 ",
        color="red",
    )
    plt.xlabel(" Number of Deployed nodes ")
    plt.xlim(10, 200)

    # plt.ylim(0, 5000)
    plt.ylabel(" Lifetime (Year) ")

    # ------------------ Deploiement en fonction de N --------------

    sensors_deplyed = [i for i in range(10, 220, 20)]
    LTi_greedy = list()
    LTi_uniform = list()

    for N in sensors_deplyed:
        Si = LWSN(N, 10)
        Si.greedy_deployment(1, 0.1, 0.5)
        LTi_greedy.append(Si.life_Time(1, 5)/(24*365))

        Si.uniform_deployment(1, 0.1, 0.5)
        LTi_uniform.append(Si.life_Time(1, 5)/(24*365))   

    # -------------------- Construction des Graphes -----------------

    plt.plot(
        sensors_deplyed,
        LTi_greedy,
        symbol,
        label="Greedy",
        color="red",
        lw=1,
        linestyle=linestyles_dict["dashed"],
    )

    plt.plot(
        sensors_deplyed,
        LTi_uniform,
        symbol,
        label="Uniform",
        color="blue",
        lw=1,
        linestyle=linestyles_dict["dashed"],
    )

    plt.legend()
    plt.grid()
    plt.show()


def graphic_LifeTime_Gain(K, p, symbol, color):

    # ------------------ Parametres d'Affichage -------------------

    plt.title(
        "Normalized lifetime virtual node-based: " + "K = {}, p = {}".format(K, p),
        color="m",
    )
    plt.xlabel(" Number of Deployed nodes ")
    plt.xlim(10, 200)

    # plt.ylim(0, 5000)
    plt.ylabel(" Normalized Lifetime ")

    # ------------------ Deploiement en fonction de N --------------

    sensors_deplyed = [i for i in range(10, 220, 20)]
    alpha_values = [0.0, 0.1, 0.2, 0.8, 1]
    r=list()
    LTi_greedy = list()
    LTi_uniform = list()
    
    for j, alpha in enumerate(alpha_values):

        LTi_greedy.clear()
        LTi_uniform.clear()
        r.clear()

        # Sensors Deployment
        for i, N in enumerate(sensors_deplyed):
            Si = LWSN(N, 10)

            Si.greedy_deployment(1, alpha, p)
            LTi_greedy.append(Si.life_Time(5, 5))

            Si.uniform_deployment(1, alpha, p)
            LTi_uniform.append(Si.life_Time(5, 5))  

            r.append(LTi_greedy[i] / LTi_uniform[i])

        # -------------------- Construction des Graphes -----------------

        plt.plot(
            sensors_deplyed,
            r,
            symbol[j],
            label="\u03B1 : {}".format(alpha * 1),
            color=color[j],
            lw=1,
            linestyle=linestyles_dict["dashed"],
        )

    plt.legend()
    plt.grid()
    plt.show()

def graphic_LifeTime_Gain_2(K, p, symbol, color):

    # ------------------ Parametres d'Affichage -------------------

    plt.title(
        "Normalized lifetime virtual node-based: " + "K = {}, p = {}".format(K, p),
        color="m",
    )
    plt.xlabel(" \u03B1 ")
    plt.xlim(0, 1)
    plt.ylabel(" Normalized Lifetime ")

    # ------------------ Deploiement en fonction de N --------------

    sensors_deplyed = [10, 20, 40, 80, 100]
    alpha_values = [0.0, 0.2, 0.4, 0.6,0.8, 1]
    r=list()
    LTi_greedy = list()
    LTi_uniform = list()
    
    for j, N in enumerate(sensors_deplyed):

        LTi_greedy.clear()
        LTi_uniform.clear()
        r.clear()

        # Sensors Deployment
        for i, alpha in enumerate(alpha_values):
            Si = LWSN(N, K)

            Si.greedy_deployment(1, alpha, p)
            LTi_greedy.append(Si.life_Time(5, 5))

            Si.uniform_deployment(1, alpha, p)
            LTi_uniform.append(Si.life_Time(5, 5))  

            r.append(LTi_greedy[i] / LTi_uniform[i])

        # -------------------- Construction des Graphes -----------------

        plt.plot(
            alpha_values,
            r,
            symbol[j],
            label="N : {}".format(N),
            color=color[j],
            lw=1,
            linestyle=linestyles_dict["dashed"],
        )

    plt.legend()
    plt.grid()
    plt.show()

def graphic_NetwkLenght_Impact(N, p, symbol, color):
    
    # ------------------ Parametres d'Affichage -------------------

    plt.title(
        "Normalized lifetime with Network_Lenght-based: " + "N = {}, p = {}".format(N, p),
        color="m",
    )
    plt.xlabel(" Number of Virtual Nodes ")
    plt.xlim(0, 100)
    plt.ylabel(" Normalized Lifetime ")

    # ------------------ Deploiement en fonction de K --------------

    Virtual_nodes_values = [1, 2, 4, 5, 8, 10, 20, 25, 40, 50, 100]
    alpha_values = [0.2, 0.4, 0.6]
    r=list()
    LTi_greedy = list()
    LTi_uniform = list()

    for j, alpha in enumerate(alpha_values):
        
        LTi_greedy.clear()
        LTi_uniform.clear()
        r.clear()

        for i, K in enumerate(Virtual_nodes_values):
            Si = LWSN(N, K)

            Si.greedy_deployment(1, alpha, p)
            LTi_greedy.append(Si.life_Time(5, 5))

            Si.uniform_deployment(1, alpha, p)
            LTi_uniform.append(Si.life_Time(5, 5))  

            r.append(LTi_greedy[i] / LTi_uniform[i])

        # -------------------- Construction des Graphes -----------------

        plt.plot(
            Virtual_nodes_values,
            r,
            symbol[j],
            label="\u03B1 : {}".format(alpha * 1),
            color=color[j],
            lw=1,
            linestyle=linestyles_dict["dashed"],
        )

    plt.legend()
    plt.grid()
    plt.show()


def graphic_Residual_Energy(N, K, p, Enode):

    # ------------------ Parametres d'Affichage -------------------

    plt.title(
        "Residual Energy with N = {} | K = {} | p = {}".format(N, K, p),
        color="m",
    )
    plt.xlabel(" Virtual Node Index ")
    plt.xlim(1, 10)
    plt.ylabel(" Residual energy (%) ")
    #plt.ylim(0, 100)
    symbols_greedy = ['o-', 's']
    symbols_uniform = ['p','*-']

    # ------------------ Deploiement en fonction de N K alpha --------------

    virtual_nodes = [i for i in range(1, K+1)]
    alpha_values = [0.1, 0.4]
    Residual_greedy = list()
    Residual_uniform = list()
    
    for j, alpha in enumerate(alpha_values):

        Residual_greedy.clear()
        Residual_uniform.clear()
        Emax_greedy = 0
        Emax_Uniform = 0
        
        # Sensors Deployment
        Si = LWSN(N, K)

        Si.greedy_deployment(1, alpha, p)
        Si.calculate_Ei(0.0619, 0.004096)
        Emax_greedy = max(Si.Ei)
        Residual_greedy = [(1-(Ei/Emax_greedy))*100 for Ei in Si.Ei]

        Si.uniform_deployment(1, alpha, p)
        Si.calculate_Ei(0.0619, 0.004096)
        Emax_Uniform = max(Si.Ei)
        Residual_uniform = [(1-(Ei/Emax_Uniform))*100 for Ei in Si.Ei]  

        # -------------------- Construction des Graphes -----------------

        plt.plot(
            virtual_nodes,
            Residual_greedy,
            symbols_greedy[j],
            label="Greddy:  \u03B1 = {}".format(alpha * 1),
            color="red",
            lw=1,
            linestyle=linestyles_dict["dashed"],
        )

        plt.plot(
            virtual_nodes,
            Residual_uniform,
            symbols_uniform[j],
            label="Uniform: \u03B1 = {}".format(alpha * 1),
            color="blue",
            lw=1,
            linestyle=linestyles_dict["dashed"],
        )

    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":

    colors = ["red", "blue", "green", "m", "orange", "black"]
    symbols = ["o-", "h", "*-", "s", "p"]
    # graphic_greedy_deployment(symbols, colors)
    # graphic_LifeTime(symbols[4])
    # graphic_LifeTime_Gain(10, 0.0, symbols, colors)
    # graphic_LifeTime_Gain_2(10, 0.5, symbols, colors,)
    # graphic_NetwkLenght_Impact(200, 0.5, symbols, colors)
    graphic_Residual_Energy(30, 10, 0.5, 5)

    # Si = LWSN(30, 10)
    # Si.greedy_deployment(1, 0.4, 0.5)
    # print("Oi= ", Si.Oi)
