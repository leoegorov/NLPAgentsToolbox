#!/usr/bin/env python3



# Create complete person from scratch interactively
# 1. mkbio
# 2. namebio
# 3. addsigmemory
# 4. generateprompt

# if __name__ == '__main__':

#     check_environment_variables()
#     bioWithoutName = mkbioMain()
#     bioWithName = addName(bioWithoutName)
#     bioWithReligion = addReligion(bioWithName)
#     save_person_to_db(bioWithReligion)



if __name__ == '__main__':
    import os
    import re
    import importlib.util

    # Set fallback variables
    os.environ.setdefault('DATABASE_FILE', 'build/juror.db')
    os.environ.setdefault('API_CENSUS', 'https://api.census.gov/data/2020/dec/pl')
    # API_KEY = None  # Optional: Replace with your key like 'your_api_key_here'

    stages_dir = os.path.join(os.path.dirname(__file__), 'stages')
    stage_files = []

    for filename in os.listdir(stages_dir):
        match = re.match(r'_([0-9]{2})-.*\.py$', filename)
        if match:
            stage_files.append((int(match.group(1)), filename))

    for _, filename in sorted(stage_files):
        module_path = os.path.join(stages_dir, filename)
        module_name = os.path.splitext(filename)[0]

        spec = importlib.util.spec_from_file_location(module_name, module_path)
        stage_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(stage_module)

        if hasattr(stage_module, 'main'):
            stage_module.main()
        else:
            print(f"Warning: {filename} has no main() function.")
