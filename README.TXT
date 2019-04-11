Install Python3
Requires Tkinter. If on Windows, the Windows Python installer has an option to install tkinter automatically. Otherwise use pip.

Run GUI.py 


Explaination of options
  1. Window: this option specifies how close peaks of interest can be to each other in terms of Mass/Charge. If you set this to 1.0, it will go through every Peak of Interest and see if it is the highest intensity within a 1.0 Mass/Charge range, if not, it will not return that Peak of Interest. 
  2. Threshold: The minimum intensity require for a peak of interest. If left blank, it uses a dynamic algorithm, by taking every point that is not a peak of interest and averaging those values.
  3. Column A: Since this program can process multiple source files at once, it exports a Column A for every row specificing what file that row came from. You can use either the Filename (xwafdafaf.csv), or the Full Path (C:\My Data\xwafdafaf.csv)
  4. Output: Determines the number of rows and columns exported. 
      A) Filtered Only: Exports only rows that are Peaks of Interest, and 3 columns, Column A described in #3, the Mass/Charge, and the Intensity.
      B) Max values at each M/C: Exports the rows that have the Max intensity for each Mass/Charge value, for each file. It includes the same columns as 4A, with an additional column Peak of Interest that is True/False. True for Point of Interest. Exporting this mode and filtering to Peak of Interest = True should provide the same data as 4A.
      C) All Data: Exports every row of data that went into the program. If processing a lot of files this will A) Be a large file, B) utilize a lot of RAM during the process. This is an item to fix in a future version. 
       This exports the same columns as 4B, with 2 additional columns. Maxiumum: A True/False value, basically saying whether it would have been included in 4B results, same criteria. And Inflection: a True/False value, if True, it means that this point was a maxiumum in at that Mass/Charge value, and was larger (in intensity) than its neighboring Maximums at the nearest Mass/Charge values. 
  5. My Data has Headers: If this box is checked, the first row of each file is thrown away.
  
  Input data: This program expects all input files to be .csv (comma separated values) files, with 2 columns all the way through the file. It will throw an error message if it finds more or less than 2 columns in a file. Both columns must be numberic. They will be cast as Floating Point numbers (5.6, 5.0.) If any fails to be cast as a number, an error will be raised and the program will halt. 
  When selecting a source directory, be cautious. It will recursively search for CSV files. So it could potentially scan your entire hard drive if you select C:\ for example. That will probably take awhile.
