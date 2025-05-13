#!/usr/bin/env python3

from DBController import check_environment_variables, save_person_to_db
from mkbio_01 import mkbioMain
from name_12 import addName
from religion_13 import addReligion

# Create complete person from scratch interactively
# 1. mkbio
# 2. namebio
# 3. addsigmemory
# 4. generateprompt






if __name__ == '__main__':

    check_environment_variables()
    bioWithoutName = mkbioMain()
    bioWithName = addName(bioWithoutName)
    bioWithReligion = addReligion(bioWithName)
    save_person_to_db(bioWithReligion)



