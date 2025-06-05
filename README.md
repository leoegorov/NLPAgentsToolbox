# NLP Agents Toolbox

This is a toolbox for creating realistic NLP social agent 
personalities suitable for juror duty in the US.

## Installation and dependencies

Some python libs require a virtual environment in recent macos versions 
```
cd NLPAgentsToolbox
chmod -R 755 *.py
python3 -m venv .venv
source .venv/bin/activate
pip3 install requests_cache pandas pyyaml openai
```

Optional: Add to your `.venv/bin/activate` right before `export PATH`:
```
PATH="$VIRTUAL_ENV/../tools:$PATH"
```

## Config

The following global variables are read or set in some scripts:

| var            | description                   | default                                 | mkbio | lsbio | rmbio | dbcontroller | _10-base-info | _12-name      | _99-biography
|----------------|-------------------------------|-----------------------------------------|-------|-------|-------|--------------|---------------|---------------|--------------------|
| PROJECT_ROOT   | File path to top level        | `os.path.abspath`                       | rw    | rw    | rw    | -            | r             | r             | -                  |
| BUILD_DIR      | File path to build directory  | build                                   | rw    | r     | r     | -            | r             | -             | -                  |
| DATABASE_FILE  | File path to juror.db         | juror.db                                | rw    | rw    | rw    | r            | -             | -             | -                  |
| EXPORT_JSON    | File path to export.json      | jurors.json                             | -     | rw    | -     | -            | -             | -             | -                  |
| EXPORT_YAML    | File path to export.yaml      | jurors.yaml                             | -     | rw    | -     | -            | -             | -             | -                  |
| API_CENSUS     | Connection to US Census DB    | https://api.census.gov/data/2020/dec/pl | r     | -     | -     | -            | r             | -             | -                  |
| OPENAI_API_KEY | OpenAI API key for prompt     | `api_key`                               | -     | -     | -     | -            | -             | -             | r                  |

### Override:
```
export DATABASE_FILE=~/Desktop/juror.db
```

### Add OpenAI API key
#### Recommended:  
In ``.venv/bin/activate``:  
```
source "$VIRTUAL_ENV/../api_key"
```
In ``api_key``:  
```
export OPENAI_API_KEY='sk-proj-....'
```
  
#### Alternative:  
```
echo {api_key} > api_key
```
In ``api_key``:  
```
sk-proj-....
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

### List columns, rows, all; Export YAML, JSON; Query SQL
```
./tools/lsbio.py -h
usage: lsbio.py [-h] [--version] [-c] [-i BY_ID] [-l] [-a] [-j] [-y] [-q QUERY]

lsbio – print juror information

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -c, --columns         List column names only
  -i BY_ID, --by-id BY_ID
                        Show records for specified ID
  -l, --latest          Show the latest juror entry (default)
  -a, --all             Show all entries
  -j, --export-json     Export full database as JSON
  -y, -e, --export-yaml
                        Export full database as YAML
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
| _12-name |  ``id`` ``age`` ``gender`` ``state`` ``income`` ``race`` ``education`` ``occupation`` |
| _13-religion | ++ ``first_name`` ``middle_name (optional)`` ``last_name`` |
| _14.. | ++ ``religion`` |
| _82.. | ++ ``role`` |
| _83.. | ++ ``goal (optional)`` |
| _90 | all non-LLM generated fields |
| _99 | all except biography for this person |
