# Lock-in-amp
Lock in amplifier calibration routine, using the ref-step framework. Code is now sent through the control table too. Perhaps working towards a more general instrument control tool, or perhaps making it more specific than before. 
To run the simulated experiment:
1) run Main.py
2) select a user-specified control sequence, use LOAD.xlsx (file>open dictionary)
3) select simulated instruments (file>control settings>simulated)
4) Press 'Run' in the control tab
Note there are multiple tabs in the grid window, and two tabs for controlling.

Things to add:
1) some graphs, real and imaginary components?
2) how should data be saved? currently the only option is to run it, then hit file>savetables. No use for the raw file just yet.
