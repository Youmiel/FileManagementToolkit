# File Management Toolkit

Useful tools related to files, mainly for personal usage.

List:
- Code Counters
- Old File Mover
- Duplicate File Detector

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

Check duplicate files by comparing md5 and output reports to `data\duplicate_index\record.json`

### Usage

```shell
python duplicate_file_detector.py [-h] <source_folder>
```
