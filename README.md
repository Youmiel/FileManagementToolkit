# File Management Toolkit

Useful tools related to files, mainly for personal usage.

List:
- Code Counters
- Old File Mover
- Duplicate File Detector
- Duplicate File Size Calculator

## Code Counters

Line / class counter for coding.

### Usage

Sub arguments:
  - count_line
  - count_class

```shell
python code_counter.py count_class [-h] <path> <lang>
python code_counter.py count_line [-h] <path> <file_ext>
```

## Old File Mover
 
Moves old files to the target folder.

### Usage

```shell
python old_file_mover.py [-h] <source_folder> <target_folder>
```

## Duplicate File Detector

Checks duplicate files by comparing md5 and output reports to `data\duplicate_index\record.json`

### Usage

```shell
python duplicate_file_detector.py [-h] <source_folder>
```

## Duplicate File Size Calculator

Calculates duplicate file size and output optional reports to `data\size_index.json`

### Usage

```shell
python duplicate_file_size.py [-h] [--report] <index_file>
```
