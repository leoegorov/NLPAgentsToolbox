# NLP Agents Toolbox

This is a toolbox for creating realistic NLP social agent 
personalities suitable for juror duty in the US.

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
./mkbio.py
./lsbio.py
./rmbio.py -h
```

### Example: Find and remove all Florida citizens from database

``./lsbio.py | grep "Florida" | cut -c1 | xargs -n1 ./rmbio.py -i``

**TODO: ``get_table_field.py`` instead of grep cut

## Data flow

| Stage | Existing columns |
|-|-|
| 01-mkbio | |
| 12-name |  ``ID`` ``AGE`` ``GENDER`` ``STATE`` ``INCOME`` ``RACE`` ``EDU`` ``OCCUPATION`` |
| 13-religion | ++ ``FIRST_NAME`` ``MIDDLE_NAME`` ``LAST_NAME`` |
| 14.. | ++ ``RELIGION`` |
| 90 | all non-LLM generated fields |
| 99 | all except final prompt for this person |