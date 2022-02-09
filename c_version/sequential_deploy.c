#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int N, K;
double *T;
double *O;
int *n;

void sensors_deployment(int Ni, int Ki, int lambda, float alpha, double p);
double calculate_Oi(int i, int lambda, float alpha, float p);
void save_datas(int number, double time);
void graphic(int number);

int main(int argc, char *argv[])
{
    int i = 0, filenumber = 0;
    clock_t start, end;
    double exec_time;

    //Test du Nombre de Parametres
    if (argc < 6 && argc > 7)
    {
        printf("\nError !!! Many/Few arguments\n\n");
        return EXIT_FAILURE;
    }

    // Initialisation des Parametres de l'algo de Deploiement
    N = atoi(argv[1]);
    K = atoi(argv[2]);
    int lambda = atoi(argv[3]);
    float alpha = atof(argv[4]);
    float p = atof(argv[5]);
    if (argc == 7)
        filenumber = atoi(argv[6]);

    T = malloc(K * sizeof(double));
    O = malloc(K * sizeof(double));
    n = malloc(K * sizeof(int));

    // Evaluation du Temps
    start = clock();
    sensors_deployment(N, K, lambda, alpha, p);
    end = clock();
    exec_time = ((double)(end - start)) / CLOCKS_PER_SEC;

    // Affichage
    printf("\nAfter deployment of N = %d sensors in K = %d Virtual nodes we have:\n", N, K);
    for (i = 0; i < K; i++)
        printf(" \nVirt. Node %d \t =    %d sensor(s)\n", i + 1, n[i]);
    printf("\n+-----------------------+\n| Time Exec. = %lf |\n+-----------------------+\n\n", exec_time);

    save_datas(filenumber, exec_time);
    // graphic(filenumber); //decommente pour visualiser le deploiement

    return 0;
}

void sensors_deployment(int Ni, int Ki, int lambda, float alpha, double p)
{
    int i = 0, j = 0, remaining_sensors = 0, indice;
    float maxO = 0.0;

    // Calcul de Ti de chaq Bi
    for (i = 0; i < K; i++)
    {
        T[i] = (lambda / (p + 1)) * ((p / (p + 1)) + (pow(-p, i + 1) / (p + 1)) + (i + 1));
    }

    for (i = 0; i < K; i++)
        n[i] = 1; // Affectation d'1 capt dans chaq Bi

    remaining_sensors = N - K;

    while (remaining_sensors != 0)
    {
        // Calcul du Nbr d'Oper. Oi de chaq Bi
        for (i = 0; i < K; i++)
        {
            O[i] = calculate_Oi(i, lambda, alpha, p);
        }
        printf("O = ");
        for (i = 0; i < K; i++)
            printf("%.4lf |", O[i]);
        puts("\n");

        //Remise a 0
        maxO = 0;
        indice = 0;

        //Recherche du Nbr d'Oper. Max
        for (i = 0; i < K; i++)
        {
            if (O[i] >= maxO)
            {
                maxO = O[i];
                indice = i;
            }
        }

        n[indice] += 1;
        remaining_sensors -= 1;
    }
}

double calculate_Oi(int i, int lambda, float alpha, float p)
{
    double Ti_bar = T[i] / n[i];
    double Ri_rsc = T[i] * ((n[i] - 1) / n[i]);

    double Ri_ps = 0.0;
    double Ri_rsnr = 0.0;
    double Ri_rsf = 0.0;
    double Ri_rsr = 0.0;

    if (i == 0) // B1 ne recoit rien des Noeud Precedent (absents)
        Ri_ps = ((T[i] - lambda) / n[i]) + alpha * Ri_rsc;

    if (i > 0 && i < K - 2)
    {
        Ri_rsnr = p * T[i - 1];
        Ri_rsf = T[i + 1] + (p * T[i + 2]);
        Ri_rsr = ((T[i] - lambda) * (n[i] - 1)) / n[i];
        Ri_ps = ((T[i] - lambda) / n[i]) + alpha * (Ri_rsr + Ri_rsnr + Ri_rsf + Ri_rsc);
    }

    if (i == K - 2)
    {
        Ri_rsnr = p * T[i - 1];
        Ri_rsf = T[i + 1];
        Ri_rsr = ((T[i] - lambda) * (n[i] - 1)) / n[i];
        Ri_ps = ((T[i] - lambda) / n[i]) + alpha * (Ri_rsr + Ri_rsnr + Ri_rsf + Ri_rsc);
    }

    // pour K -2, Ri_rsf = 0
    if (i == K - 1)
    {
        Ri_rsnr = p * T[i - 1];
        Ri_rsr = ((T[i] - lambda) * (n[i] - 1)) / n[i];
        Ri_ps = ((T[i] - lambda) / n[i]) + alpha * (Ri_rsr + Ri_rsnr + Ri_rsc);
    }

    return Ti_bar + Ri_ps;
}

void save_datas(int number, double time)
{
    int i = 0;

    FILE *file = NULL;
    char filename[20];
    snprintf(filename, 20, "datas_deploy_%d.dat", number);

    file = fopen(filename, "w");
    fprintf(file, "# Virt. Node\tNbr Sensors\n");
    for (i = 0; i < K; i++)
    {
        fprintf(file, "%d\t %d\n", i + 1, n[i]);
    }
    fprintf(file, "# time %lf\n", time);
    fclose(file);
}

void graphic(int number)
{
    char filename[20];
    snprintf(filename, 20, "datas_deploy_%d.dat", number);

    FILE *gnuplot = NULL;
    gnuplot = popen("gnuplot", "w");
    fprintf(gnuplot, "plot \"%s\" w lp \n", filename);
    fflush(gnuplot);

    getchar();
    pclose(gnuplot);
}