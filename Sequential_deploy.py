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

    def sensors_deployment(self, lambda_, alpha, p):
        """Determines the number of sensors of each Virtual Node"""

        for virtual_node in range(0, self.K):
            self.T.append(self.calculate_T(virtual_node, lambda_, p))

        self.n = [1 for _ in range(0, self.K)]  # ajoute 1 capteur dans chaq Bi
        remaining_sensors = self.N - self.K  # il reste N - K capteurs

        while remaining_sensors >= 0:
            for virtual_node in range(0, self.K):
                self.Oi[virtual_node] = self.calculate_O(
                    virtual_node, lambda_, alpha, p
                )

            I = [i for i, o in enumerate(self.Oi) if o == max(self.Oi)]
            i = max(I)
            self.n[i] = self.n[i] + 1
            remaining_sensors = remaining_sensors - 1
        return self.n

    # -------------------------------------------------------------------

    def calculate_T(self, i, lambda_, p):
        """Virtual Node Traffic calculation"""

        Ti = (lambda_ / (p + 1)) * ((p / (p + 1)) + (((-p) ** (i + 1)) / (p + 1)) + i)
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


def graphic_LWSN_deployment(symbol, color):

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

        Si = LWSN(30, 10).sensors_deployment(1, alpha, 0.5)

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


def graphic_LWSN_LifeTime(symbol, color):

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
    LTi = list()

    for N in sensors_deplyed:
        Si = LWSN(N, 10)
        Si.sensors_deployment(1, 0.1, 0.5)
        LTi.append(Si.life_Time(5, 5))

    plt.plot(
        sensors_deplyed,
        LTi,
        symbol,
        color=color,
        lw=1,
        linestyle=linestyles_dict["dashed"],
    )

    # plt.legend()
    plt.grid()
    plt.show()


if __name__ == "__main__":

    colors = ["red", "blue", "green", "m", "orange", "black"]
    symbols = ["o-", "h", "*-", "s", "p"]

    graphic_LWSN_deployment(symbols, colors)
    # graphic_LWSN_LifeTime(symbols[4], colors[2])
