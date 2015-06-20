Author: Ulya Bayram

Contact: ulyabayram@gmail.com

Dataset is obtained from Illinois Natural History Survey, for the following paper, in case of using the dataset, pleace cite this paper:

Ulya Bayram, Dwight Divine, Pin Zhou, Eric W. D. Rozier, "Improving reliability with dynamic syndrome allocation in intelligent software defined data centers", 45th Annual IEEE/IFIP International Conference on Dependable Systems and Networks (DSN), 2015.


Dataset:
========

Dataset consists of dat files, that is a format of text file, you do not need any library to open and modify these files.

Every column inside the file represents something. List is in the following:

* Column 1 : Row number of the data, such as time step

* Column 2 : User ID number, same as the ID at the filename

* Column 3 : Change (delta) in terms of writes or deletes in bytes observed in current time step

* Column 4 : Change (delta) in terms of writes or deletes in giga-bytes (GB) observed in current time step

* Column 5 : Disk usage of this user in bytes observed in this time step

* Column 6 : Disk usage of this user in giga-bytes (GB) observed in this time step

* Column 7 : Time stamp of the measurements at the time step (row number), concatenated as the following;  year(last 2 digits)-month-day-hour of day
