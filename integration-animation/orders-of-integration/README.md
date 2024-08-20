These six Python files are for the six individual orders of integration. 
I have commented the code as best as I can but to speed processes up I often just changed the variable values/points instead of the variable names. 
As such, there is a discrepancy between these features which is confusing!

Depending on the final volume sweep, 'the generatevolume' function needs a different config.
For example, if the last sweep was Z you would use the config YXZ in the 'generatevolume' definition
ZYX for a x volume sweep
ZXY for a y volume sweep

With an understanding of Manim and Python, this should provide a sufficient framework to create further applied integration videos if necessary.

These files are more powerful than the one used in the applied integration video because they allow for all 6 orders of integration. 