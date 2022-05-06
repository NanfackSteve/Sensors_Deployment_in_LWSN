# This version has parallel and sequential code

The purpose of this version is to <b>compare the execution time</b> of sequential and parallel code. 

<img src="./resultats_par_vs_seq.png" alt="grapic" width="300" height="280"/>

[ ![ C/C++ CI ](https://github.com/NanfackSteve/Sensors_Deployment_in_LWSN/actions/workflows/c-actions-CI.yml/badge.svg?branch=main&event=push) ](https://github.com/NanfackSteve/Sensors_Deployment_in_LWSN/actions/workflows/c-actions-CI.yml)

<br/><em>parallel_datas</em> and <em>sequential_datas</em> <b>folders</b> will contains datas of each deployment (with specific parameters <b>N, K , λ, α, p</b>).

## How to use ?

To run all automatically just run `make all` command.

<ul>
    <li>For Sequential deploy, use like this:</li>
</ul>

`sensors_deploy.exe N K λ α p `
then choose 1

```
./sensors_deploy.exe 30 10 1 0.4 0.5

Sensors Deployment with N = 30, K = 10, lambda = 1, alpha = 0.4, p = 0.5  

0 - Exit 
1 - Sequential Deployement 
2 - Parallel deployement

Enter an option : 1
```

<ul>
    <li>For Parallel deploy, use like this :</li>
</ul>

`sequential_deploy.exe N K λ α p then choose 2 and enter the number of Thread to use`

```
./sequential_deploy.exe 30 10 1 0.4 0.5
Sensors Deployment with N = 30, K = 10, lambda = 1, alpha = 0.4, p = 0.5  

0 - Exit 
1 - Sequential Deployement 
2 - Parallel deployement

Enter an option : 2

Give Thread number: 
```
