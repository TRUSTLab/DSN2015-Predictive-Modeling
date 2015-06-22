Author: Ulya Bayram

Contact: ulyabayram@gmail.com

Copyright
---------

 Copyright (c) 2015 Trustworthy Systems Laboratory at the University of Cincinnati 
 All rights reserved.

 Developed by: 		
	  		Trustworthy Systems Laboratory
                      	University of Cincinnati
                        http://dataengineering.org

 Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal with the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

 Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimers.

 Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimers in the documentation and/or other materials provided with the distribution.
 Neither the names of the Trustworthy Systems Laboratory, the University of Cincinnati, nor the names of its contributors may be used to endorse or promote products derived from this Software without specific prior written permission.
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE CONTRIBUTORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS WITH THE SOFTWARE.

Citation:
---------

Dataset is obtained from Illinois Natural History Survey, for the following paper, in case of using the dataset, please cite this paper:

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
