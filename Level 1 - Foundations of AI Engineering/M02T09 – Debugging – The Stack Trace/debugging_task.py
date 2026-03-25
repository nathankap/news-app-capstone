def print_values_of(dictionary, keys):
    for key in keys:
        print(dictionary[key])  # corrected variable name from k to key


# Print dictionary values from simpson_catch_phrases
simpson_catch_phrases = {"lisa": "BAAAAAART!",
                         "bart": "Eat My Shorts!",
                         "marge": "Mmm~mmmmm",
                         "homer": 'd\'oh!',  # corrected string literal
                         "maggie": "(Pacifier Suck)"
                         }

# corrected keys argument to be a list of keys
print_values_of(simpson_catch_phrases, ['lisa', 'bart', 'homer'])

'''
    Expected console output:

    BAAAAAART!
    Eat My Shorts!
    d'oh!

'''

