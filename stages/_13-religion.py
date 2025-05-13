import random
# List of religions with their probabilities
RELIGIONS = [
    ("Protestant", 0.40),
    ("Catholic", 0.19),
    ("Unaffiliated", 0.29),
    ("Other Christian", 0.03),
    ("Other religions", 0.03),
    ("Jewish", 0.02),
    ("Muslim", 0.01),
    ("Buddhist", 0.01),
    ("Hindu", 0.01)
]

# Sort by probability descending
RELIGIONS.sort(key=lambda x: x[1], reverse=True)

def suggest_religion():
    religions = [r[0] for r in RELIGIONS]
    probs = [r[1] for r in RELIGIONS]
    return random.choices(religions, weights=probs, k=1)[0]

def print_religion_list():
    print("\nAvailable religions:")
    for i, (religion, prob) in enumerate(RELIGIONS, start=1):
        print(f"{i}. {religion} ({round(prob * 100, 2)}%)")
    print()

def getReligion():
    while True:
        suggestion = suggest_religion()
        prob = dict(RELIGIONS)[suggestion]
        print(f"\nSuggested religion: {suggestion} ({round(prob * 100, 2)}%)")
        choice = input("Accept (a), New suggestion (n), or Enter your own (e)? ").strip().lower()

        if choice == 'a':
            print(f"Religion accepted: {suggestion}")
            return suggestion
        elif choice == 'e':
            print_religion_list()
            try:
                num = int(input("Enter the number of your religion choice: "))
                if 1 <= num <= len(RELIGIONS):
                    chosen = RELIGIONS[num - 1][0]
                    print(f"Religion selected: {chosen}")
                    return chosen
                else:
                    print("Invalid number. Try again.")
            except ValueError:
                print("Please enter a valid number.")
        # otherwise loop again



def addReligion(bioWithoutReligion):
    religion = getReligion()
    return bioWithoutReligion + [religion]

