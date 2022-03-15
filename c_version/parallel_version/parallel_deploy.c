#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <time.h>

//DEFINITION DE LA STRUCTURE
typedef struct Inter
{
    int begin;
    int end;
} Interval;

int lambda;
float alpha;
float p;

int N, K;
double *T;
double *O;
int *n;
int threadNbr = 0;

void sensors_deployment();
void *calculate_Oi(void *args);
void save_datas(int number, double time);
void graphic(int number);

int main(int argc, char *argv[])
{
    int i = 0, Totalcores = 0, filenumber = 0;
    clock_t start, end;
    double exec_time;

    //Test du Nombre de Parametres
    if (argc < 6 && argc > 8)
    {
        printf("\nError !!! Many/Few arguments\n\n");
        return EXIT_FAILURE;
    }

    // Parametres des coeurs
    threadNbr = atoi(argv[6]);
    // recuperation du nbre de coeurs du PC
    char tmp[2];
    FILE *f = popen("cat /proc/cpuinfo | grep processor | wc -l", "r");
    fgets(tmp, 2, f);
    pclose(f);
    Totalcores = atoi(tmp);

    // if (threadNbr > Totalcores || threadNbr < 1)
    // {
    //     printf("\nError in The Thread's Number !!!\n\n");
    //     return EXIT_FAILURE;
    // }

    // Initialisation des Parametres de l'algo de Deploiement
    N = atoi(argv[1]);
    K = atoi(argv[2]);
    lambda = atoi(argv[3]);
    alpha = atof(argv[4]);
    p = atof(argv[5]);
    if (argc == 8)
        filenumber = atoi(argv[7]);

    T = malloc(K * sizeof(double));
    O = malloc(K * sizeof(double));
    n = malloc(K * sizeof(int));

    // Evaluation du Temps
    start = clock();
    sensors_deployment();
    end = clock();
    exec_time = ((double)(end - start)) / CLOCKS_PER_SEC;

    // Affichage
    printf("\nAfter deployment of N = %d sensors in K = %d Virtual nodes we have:\n", N, K);
    for (i = 0; i < K; i++)
        printf(" \nVirt. Node %d \t =    %d sensor(s)\n", i + 1, n[i]);
    printf("\n+-----------------------+\n| Time Exec. = %lf |\n+-----------------------+\n\n", exec_time);

    save_datas(filenumber, exec_time);

    return 0;
}

void sensors_deployment()
{
    int i = 0, j = 0, remaining_sensors = 0, indice = 0;
    float maxO = 0.0;
    pthread_t threads[threadNbr];
    Interval interval;

    // Calcul de Ti
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
        for (i = 0; i < threadNbr; i++)
        {
            //Lancement des Threads
            pthread_create(&threads[i], NULL, calculate_Oi, (void *)&i);
            pthread_join(threads[i], NULL);
        }

        //Remise a 0
        maxO = 0;
        indice = 0;

        //Recherche du Nbr d'Oper. Max
        for (j = 0; j < K; j++)
        {
            if (O[j] >= maxO)
            {
                maxO = O[j];
                indice = j;
            }
        }

        n[indice] += 1;
        remaining_sensors -= 1;
    }
}

void *calculate_Oi(void *args)
{
    int virtNode = (int)args;
    double Ti_bar = 0.0;
    double Ri_rsc = 0.0;
    double Ri_ps = 0.0;
    double Ri_rsnr = 0.0;
    double Ri_rsf = 0.0;
    double Ri_rsr = 0.0;

    Ri_ps = 0.0;
    Ti_bar = 0.0;
    Ti_bar = T[virtNode] / n[virtNode];
    Ri_rsc = T[virtNode] * ((n[virtNode] - 1) / n[virtNode]);

    if (virtNode == 0)
        Ri_ps = ((T[virtNode] - lambda) / n[virtNode]) + (alpha * Ri_rsc);

    if (virtNode > 0 && virtNode < K - 2)
    {
        Ri_rsnr = p * T[virtNode - 1];
        Ri_rsf = T[virtNode + 1] + (p * T[virtNode + 2]);
        Ri_rsr = ((T[virtNode] - lambda) * (n[virtNode] - 1)) / n[virtNode];
        Ri_ps = ((T[virtNode] - lambda) / n[virtNode]) + alpha * (Ri_rsr + Ri_rsnr + Ri_rsf + Ri_rsc);
    }

    if (virtNode == K - 2)
    {
        Ri_rsnr = p * T[virtNode - 1];
        Ri_rsf = T[virtNode + 1];
        Ri_rsr = ((T[virtNode] - lambda) * (n[virtNode] - 1)) / n[virtNode];
        Ri_ps = ((T[virtNode] - lambda) / n[virtNode]) + alpha * (Ri_rsr + Ri_rsnr + Ri_rsf + Ri_rsc);
    }

    // pour K - 1, Ri_rsf = 0
    if (virtNode == K - 1)
    {
        Ri_rsnr = p * T[virtNode - 1];
        Ri_rsr = ((T[virtNode] - lambda) * (n[virtNode] - 1)) / n[virtNode];
        Ri_ps = ((T[virtNode] - lambda) / n[virtNode]) + alpha * (Ri_rsr + Ri_rsnr + Ri_rsc);
    }

    O[virtNode] = Ti_bar + Ri_ps;
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