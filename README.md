# **49ers-EV-Lap-Sim**
**Point mass simulation tool designed for FSAE car optimization.**
Created by Matt Verolme for use by the UNC Charlotte FSAE EV Team

## Description:
### *TrackMapGenerator.py:*
- Reads MoTeC CSV exports containing latitude and longitude
- Smooths data to eliminate noise and generates track profile
- Exports track data to CSV that can be read by *LapSim.py*

### *LapSim.py:*
- Reads track file from *TrackMapGenerator.py*
- Opens GUI window that allows user to change key car parameters
- Computes FSAE event times using current car parameters

# **User Guide**

### **Software Setup:**

Running this lap sim requires installing Python and an Integrated Development Environment (IDE)

To download Python, use this [link](https://www.python.org/downloads/). Click 'download' on the latest non pre-release version. 
This will take you to another page, where you can select your operating system. 

After downloading Python, you will need to download an Integrated Development Environment (IDE).
There are many options for this such as PyCharm, Spyder, Visual Studio, Jupyter, etc.

For this guide I will be utilizing PyCharm, which can be downloaded [here](https://www.jetbrains.com/pycharm/download/).

Download the PyCharm installer, and open the downloaded file. Navigate through the setup menu, and begin the PyCharm installation.

After the installation is complete, press finish. 

From here, I recommend making a project folder. Click 'File' in the top left, then 'New Project', then 'Create'. 

Download TrackMapGenerator.py and LapSim.py and place them in the newly created folder.

### **Using Track Map Generator:**

Using the Track Map Generator requires a MoTeC CSV export containing latitude and longitude.

Once you have this, run TrackMapGenerator.py from the IDE. This will open a window that looks like this:
<br />
<br />
<br />
<img width="352" height="338" alt="image" src="https://github.com/user-attachments/assets/c40ba49e-d50c-4048-8850-480b1fdb5b3b" />
<br />
<br />
<br />
Clicking the 'Data File' button will open your files. Select the MoTeC export you wish to convert to a track file, and press open.

Next, press 'Output Folder' and open the folder you wish to save the track file export to.

Then, enter the column numbers for the latitude and longitude data. Python indexing starts at 0, so treat the first column in the data (should be the time column) as column 0. Finally, enter a name for the track file output, and press the 'Set Choices' button.

Once a track map is generated, a plot of it should be displayed. Verify that it looks accurate.
<br />
<br />
<br />
<img width="400" height="405" alt="image" src="https://github.com/user-attachments/assets/3a81e341-2f7c-4618-976a-cf739342ef36" />
<br />
<br />
<br />
- If the track layout shown looks too rounded, you may need to lower the value of the 'smoothing' variable near the top of the Python script.
- If the track looks too rough/jagged, the smoothing value may need to be increased.
- If the track doesn't resemble anything close to what is expected, it may be due to bad data.

Additionally, the console should also print the track length (in feet). Verify that this number is also close to what is expected

There should now be a .csv file saved in the specified folder. This is what will be fed into the lap sim program.

## **Using LapSim.py**

Once you have a representative track map, you can use it to run the lap sim program. Once you run the program, a file selection window will open.
<br />
<br />
<br />
<img width="335" height="172" alt="image" src="https://github.com/user-attachments/assets/938f305f-7a10-4d46-8dd6-e0e894209e27" />
<br />
<br />
<br />
Press the 'Track File' button to view your files, and select the track file .csv export you should have generated. Press 'Confirm File Choice' once you have selected the track file you wish to use. This should open a new window where you can edit car parameters and simulate event times.
<br />
<br />
<br />
<img width="434" height="318" alt="image" src="https://github.com/user-attachments/assets/26f97a1b-274e-4e94-9dc0-8cec94f66d6c" />
<br />
<br />
<br />
Any of the parameters shown can be edited by simply clicking on the current value and replacing it with a new value.

Once you have configured the parameters, press the 'Compute' button at the bottom of the window. This should update the values in the 'Event Times' section to reflect the parameters you have selected.
<br />
<br />
<br />
<img width="300" height="220" alt="image" src="https://github.com/user-attachments/assets/548a5ae6-7299-4d35-90cd-863bbd4327d1" />
<br />
<br />
<br />

The only parameters that are not currently editable in the app interface are the following:
- PDY1 &mdash; This is the nominal lateral friction, Mu_y
- PDY2 &mdash; This is the variation of friction, Mu_y, with load
- FZ0 &mdash; This is the nominal tire load used in generating a tire model
- Scaling factor &mdash; This is rough estimate of the factor at which the track surface Mu_y varies from the ideal tire test conditions

If you wish to change any of these values, they must be edited in the code directly. They can be found in the Car class setup:
<br />
<br />
<br />
<img width="732" height="110" alt="image" src="https://github.com/user-attachments/assets/6bb694c7-25b9-4369-bed6-cbfff995a917" />
<br />
<br />
<br />

If you wish to simulate a different tire (currently using Hoosier 18x6 on 7 inch rims at 12 psi), you can find them by generating a tire model, or looking at the parameters in an existing tire model file.





