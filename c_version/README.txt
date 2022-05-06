>>>>>>>>>>>>>>>>>>>>> How to Compile ? <<<<<<<<<<<<<<<<<<<<<<<<<<<<

gcc -o sensors_deploy.exe sensors_deploy.c -lm -lpthread

>>>>>>>>>>>>>>>>>>>>> How to use ? <<<<<<<<<<<<<<<<<<<<<<<<<<<<

------------------- Sequential --------------------------------

For Sequential deploy, use like this:

Execute "sensors_deploy.exe N K λ α p" then choose 1

Output:

./sensors_deploy.exe 30 10 1 0.4 0.5

Sensors Deployment with N = 30, K = 10, lambda = 1, alpha = 0.4, p = 0.5  

0 - Exit 
1 - Sequential Deployement 
2 - Parallel deployement

Enter an option : 1

------------------- Parallel --------------------------------

For Parallel deploy, use like this :

Execute "sequential_deploy.exe N K λ α p" then choose 2 and enter 
the number of Thread to use

Output:

./sequential_deploy.exe 30 10 1 0.4 0.5

Sensors Deployment with N = 30, K = 10, lambda = 1, alpha = 0.4, p = 0.5  

0 - Exit 
1 - Sequential Deployement 
2 - Parallel deployement

Enter an option : 2

Give Thread number: 4
