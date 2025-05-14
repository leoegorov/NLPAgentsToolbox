# NLP Agents Toolbox

This is a toolbox for creating realistic NLP social agent 
personalities suitable for juror duty in the US.

## Installation and dependencies

Some python libs require a virtual environment in recent macos versions 
```
cd NLPAgentsToolbox
python3 -m venv .
source bin/activate
pip3 install requests-cache pandas
```

## Environment variables

Make sure to export these shared variables before invoking commands. 
They allow for seemless interoperability and modularity of the 
individual commands.

| VAR           | Description                | mkbio | lsbio | rmbio |
|---------------|----------------------------|-------|-------|-------|
| DATABASE_FILE | File path to juror.db      | req   | req   | req   |
| API_CENSUS    | Connection to US Census DB | opt   | -     | -     |

## Usage 

```
cd path/to/NLPAgentsToolbox
chmod 755 *.py
```

```
./main.py -h     
usage: main.py [-h] [--num NUM]

optional arguments:
  -h, --help  show this help message and exit
  --num NUM   Amount of jurors to generate
```

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
(NLPAgentsToolbox) leo@lavanshakhor NLPAgentsToolbox % 
```

## Data flow 

| Stage | Existing columns |
|-|-|
| _10-mkbio | |
| _12-name |  ``ID`` ``AGE`` ``GENDER`` ``STATE`` ``INCOME`` ``RACE`` ``EDUCATION`` ``OCCUPATION`` |
| _13-religion | ++ ``FIRST_NAME`` ``MIDDLE_NAME`` ``LAST_NAME`` |
| _14.. | ++ ``RELIGION`` |
| _90 | all non-LLM generated fields |
| _99 | all except final prompt for this person |