# Mathstein Library
It is a comprehensive mathematical library.

For more information regarding the library and the tech used, view the project initiation report, https://docs.google.com/document/d/1Dk4yudvDK3usb3OyoYYEHR77Hj99lypwsUJVXQLax1o/edit 

## Directory Setup

* Mathstein
* docs
* test_cases
* LICENSE.txt
* README.md
* changelog.txt
* setup.py

## Installation and Uninstallation
* Users can install the library by simply using the `pip install Mathstein` command.
* The module is dependent on libraries like math, numpy and cmath which will be automatically installed.
* To install the library, user can simply use the `pip uninstall Mathstein` command.

## Mathstein 
This directory consists of the main functionality of our library.
Components of this directory are:
* matheqn.py contains the functionality for a one variable solver and a multi variable solver.
* mathroot.py contains the functionality for a quadratic solver, a cubic solver and a bi quadratic solver and also helps generating the graphs for the same.
* matharea.py contains the functionality for calculating area under a straight line and a curve and also gives a visual representation of how the area under a line or a curve would look.
* mathmatcalc.py contains the functionality for calculating various operations on matrices includind addition, subtraction, multiplication and finding determinant.

## test_cases
This direcctory consists of all the test cases for the files present in the Mathstein directory. The test cases have been designed using the unittest module.
To run any test case file successfully, user to use the command prompt, go to test_case directory and run the command: `python file_name.py` . This will successfully compile the test case files.


## Docs
This directory basically consists of all the documentation of our entire library. Documentation was created using Sphinx framework.
For generating documentation of additional files added, simply go to command prompt, direct to the Docs directory and run the command `make html`. This automatically generates the documentary for any new code added.
