import yaml
import sys


### STORE IN DATABASE
def store_word(english_word, meaning):

    print("Store the word: ", english_word, meaning)

    stored = False

    # Load the file
    with open('my_dict.yml', 'r') as yaml_file:
        my_english_dict = yaml.safe_load(yaml_file) or {}
        print("\nContenido del archivo ANTES:\n", my_english_dict, "\n")
        
        my_english_dict[english_word] = meaning

        print("\n\nContenido del archivo DESPUES:\n", my_english_dict, "\n\n")

    if my_english_dict:
        with open('my_dict.yml', 'w') as yaml_file:
            yaml.dump(my_english_dict, yaml_file, default_flow_style=False)
            
    
    yaml_file.close()
    
    print("TO BIEN")


    
 



if __name__ == "__main__":

    english_word = "english_word_2"
    meaning = "meaning_2"
    store_word(english_word, meaning)