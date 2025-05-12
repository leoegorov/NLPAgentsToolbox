from mkbio_01 import mkbioMain
from name_12 import addName
from religion_13 import addReligion

# Create complete person from scratch interactively
# 1. mkbio
# 2. namebio
# 3. addsigmemory
# 4. generateprompt






if __name__ == '__main__':
    bioWithoutName = mkbioMain()
    #bioWithoutName = ['sad', 'Female']
    bioWithName = addName(bioWithoutName)
    bioWithReligion = addReligion(bioWithName)

    #TODO save the full bio in DB



