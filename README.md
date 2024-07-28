# UKOOA Cleaner

## United Kingdom Offshore Operators Association (UKOOA) File
A UKOOA (United Kingdom Offshore Operators Association) file contains text with navigation information extracted from a geometry database. When loaded into a seismic processing software, the file properly defines the geometric position of trace data for accurate processing in velocity analysis, static correction (first break picking), denoising and filtering, and deconvolution.
The file normally contains information on the nature of the acquisition, including the number of receiver elements, the terrain, and the kind of acquisition, organized in a specific format. Receiver coordinates are stacked in rows of 3, incrementing horizontally to the right, row-by-row.

## ukooa_cleaner
`ukooa_cleaner` is a python module for cleaning 3D marine UKOOA files. This `README.md` details the steps to getting it to run on your machine locally.
You can read this [Medium article](https://blog.stackademic.com/cleaning-ukooa-files-using-ukooa-cleaner-6eb436ceda13) on why I designed this module and how it works.

## Step 1
Navigate to your choice directory and clone this repository.

```bash
$ cd /directory
$ git clone https://github.com/alfiinyang/ukooa_cleaner.git
```
> Replace `/directory` with your choice directory path.

## Step 2
Navigate to cloned repo `/ukooa_cleaner` and make `clean` and `ukooa_exe.py` executables.

```bash
$ cd /ukooa_cleaner
$ su chmod +x clean ukooa_exe.py
```

## Step 3
Create a symbolic link for `clean` in `/usr/local/bin` to make it executable from anywhere.

```bash
$ ln -s /your-directory/ukooa_cleaner/clean /usr/local/bin/clean
```
> You can change the name of the symbolic link in case of naming conflicts.

To confirm your symbolic link has been created you can `ll` its path.

```bash
$ ll /usr/local/bin/clean
```

> output:
```bash
lrwxrwxrwx. 1 root root 18 Jun 27 09:13 /usr/local/bin/clean -> /your-directory/ukooa_cleaner/clean
```

## Step 4
Call `clean` on the UKOOA file to be cleaned, specifying its path.

```bash
$ clean /filepath/ukooa_file
```
The script will run, cleaning the UKOOA file and saving it with a new name (`ukooa_file_clean`) in the same location as the original file.
> [!NOTE]
> Steps 1–3 are only needed when you first clone the repository. Going forward, Step 4 is all you’ll do.

Happy cleaning 😊!
