# Folders_Syncronization

Implementation of a program that synchronizes two folders: source and replica. 
The program maintains a full, identical copy of source folder at replica folder.
Synchronization has been implemented one-way: after the synchronization, content of the replica folder can be modified to exactly match content of the source folder.
Synchronization is performed periodically.
File creation/copying/removal operations is logged to a file and to the console output.
Folder paths, synchronization interval and log file path is provided using the command line arguments.
