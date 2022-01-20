#!/bin/python3
import matplotlib.pyplot as plt
from collections import OrderedDict

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
        N: "Nombre de capteurs"
        K: "Nombre de noeud Virtuel"
    """

    def __init__(self, N, K):
        """..."""

        self.K = K
        self.N = N
        self.T = list()
        self.n = list([0] * K)

    def sensors_deployment(self, lambda_, alpha, p):
        """Determine le nombre de capteurs de chaque noeud Virtuel"""

        O = list([0] * self.K)

        for virtual_node in range(0, self.K):
            self.T.append(self.calculate_T(virtual_node, lambda_, p))

        self.n = [1 for _ in range(0, self.K)]  # on ajoute 1 capteur dans chaque Bi
        remaining_sensors = self.N - self.K  # il reste N - K capteurs

        while remaining_sensors != 0:
            for virtual_node in range(0, self.K):
                O[virtual_node] = self.calculate_O(virtual_node, lambda_, alpha, p)

            I = [i for i, o in enumerate(O) if o == max(O)]
            i = max(I)
            self.n[i] = self.n[i] + 1
            remaining_sensors = remaining_sensors - 1
        return self.n

    # -------------------------------------------------------------------

    def calculate_T(self, i, lambda_, p):
        """Calcul du trafique d'un noeud virtuel"""

        Ti = (lambda_ / (p + 1)) * ((p / (p + 1)) + (((-p) ** (i + 1)) / (p + 1)) + i)
        return Ti

    def calculate_O(self, i, lambda_, alpha, p):
        """Calcul du nombre max d'operation d'un capteur"""

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


if __name__ == "__main__":

    # ------------------ Parametres d'Affichage -------------------

    colors = ["red", "blue", "green", "m", "orange"]
    symbols = ["o-", "h", "*-", "s", "p"]
    plt.title(
        "Spatial nodes Distribution with \n K = 10, N = 30  and p = 0.5 ", color="blue"
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
            symbols[j],
            label="\u03B1 : {}".format(alpha * 1),
            color=colors[j],
            lw=1,
            linestyle=linestyles_dict["densely dotted"],
        )

    plt.legend()
    plt.grid()
    plt.show()
