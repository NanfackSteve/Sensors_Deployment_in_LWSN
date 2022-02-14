# This version has parallel and sequential code

The pupose of this version is to <b>compare the execution time</b> of sequential and parallel code. 

<img src="./resultats_par_vs_seq.png" alt="grapic" width="300" height="280"/>

<br/>parallel_datas and sequential_datas folders will contains datas of each deployment (with specific parameters N, K , λ, α, p).

## How to use ?

To run all automatically just run `make all` command.

<ul>
    <li>For parallel_deploy.exe</li>
</ul>

`parallel_deploy.exe N K λ α p Thread_number deployment_number`

```
./parallel_deploy.exe 30 10 1 0.4 0.5 4 3
```

<ul>
    <li>For sequential_deploy.exe</li>
</ul>

`sequential_deploy.exe N K λ α p deployment_number`

```
./sequential_deploy.exe 30 10 1 0.4 0.5 7
```