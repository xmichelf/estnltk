EstNLTK -- Open source tools for Estonian natural language processing
=====================================================================

EstNLTK provides common natural language processing functionality such as paragraph, sentence and word tokenization,
morphological analysis, named entity recognition, etc. for the Estonian language.

The project is funded by EKT ([Eesti Keeletehnoloogia Riiklik Programm](https://www.keeletehnoloogia.ee/)).

Currently, there are two branches of EstNLTK:

* version **1.6** -- the new branch, which is in a beta status and under development. The version 1.6.4beta is available from [Anaconda package repository](https://anaconda.org/estnltk/estnltk). It contains basic analysis tools up to morphological analysis and syntactic parsing, but it does not contain all the functionalities available in **1.4.1**. Supported Python versions are 3.5 and 3.6. The source of the latest release is available at the branch [version_1.6](https://github.com/estnltk/estnltk/tree/version_1.6), and the development source can be found at [devel_1.6](https://github.com/estnltk/estnltk/tree/devel_1.6). 
  
* version **1.4.1** -- the old branch, which contains full functionality of different analysis tools. Available via [Anaconda package repository](https://anaconda.org/estnltk/estnltk/files) for Python 3.5. PyPI packages are also available for Python 3.4, 3.5 and 2.7. Python 3.6 and 3.7 are not supported;

## Version 1.6

### Installation
The recommended way of installing EstNLTK is by using the [anaconda python distribution](https://www.anaconda.com/download) and python 3.5+.

Installable packages have been built for osx, windows-64, and linux-64.

As some of the EstNLTK's dependencies are not yet compatible with the newest version of python (3.7), we recommend to install EstNLTK inside a conda environment that contains python 3.6:

1. [create a conda environment](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands) with python 3.6, for instance:
```
conda create -n py36 python=3.6
```

2. [activate the environment](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#activating-an-environment), for instance:
```
conda activate py36
```

3. install EstNLTK with the command:
```
conda install -c estnltk -c conda-forge estnltk
```

The alternative way for installing if you are unable to use the anaconda distribution is:
```
python -m pip install estnltk
```

This is slower, more error-prone and requires you to have the appropriate compilers for building the scientific computation packages for your platform.

_Note_: for using some of the tools in estnltk, you also need to have Java installed in your system. We recommend using Oracle Java http://www.oracle.com/technetwork/java/javase/downloads/index.html, although alternatives such as OpenJDK (http://openjdk.java.net/) should also work.

### Documentation

Documentation for 1.6 currently comes in the form of [jupyter notebooks](http://jupyter.org), which are available here: https://github.com/estnltk/estnltk/tree/version_1.6/tutorials

Note: if you have trouble viewing jupyter notebooks in github (you get an error message _Sorry, something went wrong. Reload?_ at loading a notebook), then try to open notebooks with the help of [https://nbviewer.jupyter.org](https://nbviewer.jupyter.org)

### Source

The source of the latest release is available at the branch [version_1.6](https://github.com/estnltk/estnltk/tree/version_1.6), and the development source can be found at [devel_1.6](https://github.com/estnltk/estnltk/tree/devel_1.6). 

## Version 1.4.1

### Installation
The recommended way of installing estnltk is by using the [anaconda python distribution](https://www.anaconda.com/download) and python 3.5.

We have installable packages built for osx, windows-64, and linux-64. Installation steps:

1. [create a conda environment](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands) with python 3.5, for instance:
```
conda create -n py35 python=3.5
```

2. [activate the environment](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#activating-an-environment), for instance:
```
conda activate py35
```

3. install estnltk with the command:
```
conda install -c estnltk -c conda-forge estnltk=1.4.1
```

_Note_: for using some of the tools in estnltk, you also need to have Java installed in your system. We recommend using Oracle Java http://www.oracle.com/technetwork/java/javase/downloads/index.html, although alternatives such as OpenJDK (http://openjdk.java.net/) should also work.

If you have [jupyter notebook installed](https://test-jupyter.readthedocs.io/en/rtd-theme/install.html#using-anaconda-and-conda-recommended), you can use EstNLTK in an interactive web application. For that, type the command:

```
jupyter notebook
```

To run our tutorials, [download them as a zip file](https://github.com/estnltk/tutorials/archive/master.zip), unpack them to a directory and run the command `jupyter notebook` in that directory.  

---------

The alternative way for installing if you are unable to use the anaconda distribution is:

`python -m pip install estnltk==1.4.1.1`

This is slower, more error-prone and requires you to have the appropriate compilers for building the scientific computation packages for your platform. 

Find more details in the [installation tutorial for version 1.4](https://estnltk.github.io/estnltk/1.4/tutorials/installation.html).

### Documentation

Release 1.4.1 documentation is available at https://estnltk.github.io/estnltk/1.4.1/index.html.
For previous versions refer to https://estnltk.github.io/estnltk.
For more tools see https://estnltk.github.io.

Additional educational materials on EstNLTK version 1.4 are available on web pages of the NLP courses taught at the University of Tartu:

  * https://github.com/d009/EstNLP
  * https://courses.cs.ut.ee/2015/pynlp/fall

### Source

The source of the latest v1.4 release is available at the [master branch](https://github.com/estnltk/estnltk/tree/master).

## Citation

In case you use EstNLTK in your work, please cite us as follows:

    @InProceedings{ORASMAA16.332,
    author = {Siim Orasmaa and Timo Petmanson and Alexander Tkachenko and Sven Laur and Heiki-Jaan Kaalep},
    title = {EstNLTK - NLP Toolkit for Estonian},
    booktitle = {Proceedings of the Tenth International Conference on Language Resources and Evaluation (LREC 2016)},
    year = {2016},
    month = {may},
    date = {23-28},
    location = {Portorož, Slovenia},
    editor = {Nicoletta Calzolari (Conference Chair) and Khalid Choukri and Thierry Declerck and Marko Grobelnik and Bente Maegaard and Joseph Mariani and Asuncion Moreno and Jan Odijk and Stelios Piperidis},
    publisher = {European Language Resources Association (ELRA)},
    address = {Paris, France},
    isbn = {978-2-9517408-9-1},
    language = {english}
    }
