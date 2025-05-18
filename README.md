# NLP Agents Toolbox

This is a toolbox for creating realistic NLP social agent 
personalities suitable for juror duty in the US.

## Installation and dependencies

Some python libs require a virtual environment in recent macos versions 
```
cd NLPAgentsToolbox
chmod -R 755 *.py
python3 -m venv .
source bin/activate
pip3 install sqlite3 numpy requests-cache pandas
```

## Config

The following global variables are read or set in some scripts:

| var           | description                   | default                                 | mkbio | lsbio | rmbio | dbcontroller | _10-base-info |
|---------------|-------------------------------|-----------------------------------------|-------|-------|-------|--------------|---------------|
| BUILD_DIR     | File path to build directory  | build                                   | r     | r     | r     | -            | -             |
| DATABASE_FILE | File path to juror.db         | juror.db                                | rw    | rw    | rw    | r            | -             |
| EXPORT_FILE   | File path to export.json      | export.db                               | -     | rw    |       | -            | -             |
| API_CENSUS    | Connection to US Census DB    | https://api.census.gov/data/2020/dec/pl | r     | -     | -     | -            | r             |

Override:
```
export DATABASE_FILE=~/Desktop/juror.db
```

### Optional: PATH
Call scripts in tools/ without their full path:
```
cd /path/to/NLPAgentsToolbox && export PATH="$PATH:$PWD/tools"
```

## Usage 

### Generate juror
```
./tools/mkbio.py -h     
usage: mkbio.py [-h] [-n NUM] [--version]

mkbio – make some American jurors

optional arguments:
  -h, --help         show this help message and exit
  -n NUM, --num NUM  Amount of jurors to generate
  --version          show program's version number and exit
```

### List columns, rows, all; Export JSON; Query SQL
```
./tools/lsbio.py -h
usage: lsbio.py [-h] [--version] [-c] [-i BY_ID] [-l] [-a] [-e] [-q QUERY]

lsbio – print juror information

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -c, --columns         List column names only
  -i BY_ID, --by-id BY_ID
                        Show records for specified ID
  -l, --latest          Show the latest juror entry (default)
  -a, --all             Show all entries
  -e, --export          Export full database as JSON
  -q QUERY, --query QUERY
                        Run a custom SQL query on the person table
```

### Delete (all) rows or database file
```
 ./tools/rmbio.py -h
usage: rmbio.py [-h] [--version] (-i ID | -a | -A)

rmbio – remove jurors from the database

optional arguments:
  -h, --help         show this help message and exit
  --version          show program's version number and exit
  -i ID, --id ID     Remove juror by ID
  -a, --all          Remove all jurors
  -A, --delete-file  Delete the entire database file
```

## Data flow 

| Stage | Existing columns that can be accessed |
|-|-|
| _10-base_info | |
| _12-name |  ``ID`` ``AGE`` ``GENDER`` ``STATE`` ``INCOME`` ``RACE`` ``EDUCATION`` ``OCCUPATION`` |
| _13-religion | ++ ``FIRST_NAME`` ``MIDDLE_NAME`` ``LAST_NAME`` |
| _14.. | ++ ``RELIGION`` |
| _90 | all non-LLM generated fields |
| _99 | all except final prompt for this person |
