set title "Execution Time of Deployment Algorithm" 
set xlabel "Sensors Deployed (N)"
set yrange [-0.5:3.5]
set ylabel "Time (s)"
set xrange [0:10500]
# set label "Time" at 4242, 0.2 ecrire du texte a une coordonnee
#set autoscale
set bmargin at screen 0.2
set rmargin at screen 0.9
set lmargin at screen 0.18
set mapping cartesian

plot "par_vs_seq.dat" u 1:2 with lp linewidth 2.5 linetype 7 title "Parallel Exec. time " at 0.47, 0.8, "" u 1:3 with lp linewidth 2.5 linetype 6 title "Seqauential Exec. time " at 0.47, 0.75 