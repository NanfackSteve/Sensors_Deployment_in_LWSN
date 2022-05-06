set title "{/:Bold Execution Time of Deployment Algorithm with 4 CPUs}" 

set xlabel "Sensors Deployed (N)"
set xrange [0:]

set yrange [-0.5:]
set ylabel "Time (s)"
set ytics nomirror

set y2label "{/:Bold SpeedUp}" offset -1,0 textcolor rgb "orange"
set y2range[0:4]
set y2tics nomirror tc "orange"


# set label "Time" at 4242, 0.2 ecrire du texte a une coordonnee
#set autoscale
set bmargin at screen 0.2
set rmargin at screen 0.83
set lmargin at screen 0.18
set mapping cartesian

plot \
"par_vs_seq.dat" u 1:2 with lp linewidth 2.5 linetype 7 title "Parallel Exec. time  " at 0.57, 0.7,\
"" u 1:3 with lp linewidth 2.5 linetype 6 title "Seqauential Exec. time " at 0.57, 0.65,\
"" u 1:4 with lp linewidth 2.5  linetype 1 lc "orange"  title "SpeedUp " at 0.57, 0.6