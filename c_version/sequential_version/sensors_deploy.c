#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <pthread.h>

int N, K;
double *T;
double *O;
int *n;
int lambda;
float alpha;
float p;
//#define NUM_THREADS 1
int NUM_THREADS = 1;

double parallel_sensors_deployment(int numThreads);
void *par_calculate_Oi(void *arg);
void *par_calculate_Ti(void *arg);

double seq_sensors_deployment();
double calculate_Oi(int i, int lambda, float alpha, float p);

void save_datas(int number, double time);
void graphic(int number);

int main(int argc, char *argv[])
{
    int i = 0, filenumber = 0, choice = 0;
    double exec_time;

    // Test du Nombre de Parametres
    if (argc < 6 || argc > 7)
    {
        printf("\nError !!! Many/Few arguments\n\n");
        return EXIT_FAILURE;
    }

    // Initialisation des Parametres de l'algo de Deploiement
    N = atoi(argv[1]);
    K = atoi(argv[2]);
    lambda = atoi(argv[3]);
    alpha = atof(argv[4]);
    p = atof(argv[5]);
    if (argc == 7)
        filenumber = atoi(argv[6]);

    T = malloc(K * sizeof(double));
    O = malloc(K * sizeof(double));
    n = malloc(K * sizeof(int));

    // Message d'entre
    printf("\nSensors Deployment with N = %d, K = %d, lambda = %d, alpha = %.1f, p = %.1f  \n\n", N, K, lambda, alpha, p);

    printf("0 - Exit \n1 - Sequential Deployement \n2 - Parallel deployement\n\nEnter an option : ");
    scanf("%d", &choice);

    switch (choice)
    {

    case 0:
        printf("\nExit\n\n");
        return 0;

    case 1:
    {
        exec_time = seq_sensors_deployment();
        printf("\nSeq. Time Exec. = %lf sec\n\n", exec_time);
    };
    break;

    case 2:
    {
        printf("Give Thread number: ");
        scanf("%d", &NUM_THREADS);

        exec_time = parallel_sensors_deployment(NUM_THREADS);
        printf("\nParal. Time Exec. = %lf sec\n\n", exec_time);
    }
    break;

    default:
        printf("\nError unknow choice !!! Program will exit !!\n\n");

        system("sleep 2");
        return 0;
        break;
    }

    // Affichage
    // printf("\nAfter deployment of N = %d sensors in K = %d Virtual nodes we have:\n", N, K);
    // for (i = 0; i < K; i++)
    //     printf(" \nVirt. Node %d \t =    %d sensor(s)\n", i + 1, n[i]);
    // printf("\n+-----------------------+\n| Time Exec. = %lf |\n+-----------------------+\n\n", exec_time);

    // save_datas(filenumber, exec_time);
    //  graphic(filenumber); //decommente pour visualiser le deploiement

    free(T);
    free(O);
    free(n);

    return 0;
}

double parallel_sensors_deployment(int numThreads)
{
    // Variables Threads
    pthread_t threads[numThreads];
    pthread_attr_t attr;
    pthread_attr_init(&attr);
    pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_JOINABLE);

    // Varriables de boucles
    long i, j, t;

    // Variables deploiement
    int remaining_sensors = 0, indice = 0;
    float maxO = 0.0;

    // variables Temps
    clock_t start, end;
    double exec_time;

    // Evaluation du Temps
    start = clock();

    // Calcul de Ti

    for (t = 0; t < numThreads; t++)
    {
        // Lancement des Threads
        pthread_create(&threads[t], &attr, par_calculate_Ti, (void *)t);
    }

    /* Free attribute and wait for the other threads */
    for (t = 0; t < numThreads; t++)
    {
        pthread_join(threads[t], NULL);
    }

    remaining_sensors = N - K;

    while (remaining_sensors != 0)
    {
        // Calcul du Nbr d'Oper. Oi de chaq Bi
        for (t = 0; t < numThreads; t++)
        {
            // Lancement des Threads
            pthread_create(&threads[t], &attr, par_calculate_Oi, (void *)t);
        }

        /* Free attribute and wait for the other threads */
        for (t = 0; t < numThreads; t++)
        {
            pthread_join(threads[t], NULL);
        }

        // Remise a 0
        maxO = 0;
        indice = 0;

        // Recherche du Nbr d'Oper. Max
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

    end = clock();
    exec_time = ((double)(end - start)) / CLOCKS_PER_SEC;

    // printf("\nAfter deployment of N = %d sensors in K = %d Virtual nodes we have:\n", N, K);
    // for (i = 0; i < K; i++)
    //     printf(" \nVirt. Node %ld \t =    %d sensor(s)\n", i + 1, n[i]);

    return exec_time;
}

void *par_calculate_Ti(void *arg)
{
    long debut, fin, idThread = 0, virtNode = 0;
    idThread = (long)arg;

    // Calcul des Bornes
    debut = idThread * (K / NUM_THREADS);

    if (idThread == (NUM_THREADS - 1))
        fin = K;

    else
        fin = debut + (K / NUM_THREADS);

    // Variables du calcul de Ti

    for (virtNode = debut; virtNode < fin; virtNode++)
    {
        T[virtNode] = (lambda / (p + 1)) * ((p / (p + 1)) + (pow(-(p), virtNode + 1) / (p + 1)) + (virtNode + 1));

        // printf("(%ld , %.2f ) ", virtNode, T[virtNode]);
        n[virtNode] = 1;
    }
}

void *par_calculate_Oi(void *arg)
{
    long debut, fin, idThread, virtNode = 0;

    // Calcul des Bornes
    idThread = (long)arg;
    debut = idThread * (K / NUM_THREADS);

    if (idThread == (NUM_THREADS - 1))
        fin = K;
    else
        fin = debut + (K / NUM_THREADS);

    // variables du calcul de Oi
    double Ti_bar = 0.0;
    double Ri_rsc = 0.0;
    double Ri_ps = 0.0;
    double Ri_rsnr = 0.0;
    double Ri_rsf = 0.0;
    double Ri_rsr = 0.0;

    // calcul
    for (virtNode = debut; virtNode < fin; virtNode++)
    {
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
}

double seq_sensors_deployment()
{
    int i = 0, j = 0, remaining_sensors = 0, indice;
    float maxO = 0.0;

    clock_t start, end;
    double exec_time;

    // Evaluation du Temps
    start = clock();

    // Calcul de Ti de chaq Bi
    for (i = 0; i < K; i++)
    {
        T[i] = (lambda / (p + 1)) * ((p / (p + 1)) + (pow(-p, i + 1) / (p + 1)) + (i + 1));
        // printf("%.2f _ ", T[i]);
    }
    for (i = 0; i < K; i++)
        n[i] = 1; // Affectation d'1 capt dans chaq Bi

    remaining_sensors = N - K;

    while (remaining_sensors != 0)
    {
        // Calcul du Nbr d'Oper. Oi de chaq Bi
        for (i = 0; i < K; i++)
            O[i] = calculate_Oi(i, lambda, alpha, p);

        // Remise a 0
        maxO = 0;
        indice = 0;

        // Recherche du Nbr d'Oper. Max
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
    end = clock();
    exec_time = ((double)(end - start)) / CLOCKS_PER_SEC;

    // printf("\nAfter deployment of N = %d sensors in K = %d Virtual nodes we have:\n", N, K);
    // for (i = 0; i < K; i++)
    //     printf(" \nVirt. Node %d \t =    %d sensor(s)\n", i + 1, n[i]);

    return exec_time;
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

    // pour K - 1, Ri_rsf = 0
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