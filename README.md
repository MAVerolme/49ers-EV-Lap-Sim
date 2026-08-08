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


