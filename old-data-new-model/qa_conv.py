from qa_input import QA_input


count = 0

my_dict = {}
my_array = []
def append_to_dict(key, value):
    if key in my_dict:
        my_dict[key].add(value)  # Add to the existing set
    else:
        my_dict[key] = {value} 

for _ in QA_input:
    x = QA_input[count]  # Access the current item in QA_input
    new_data = x['Context'] + ' ' + x['Response']  # Combine 'Context' and 'Response'
    my_array += new_data
    
    append_to_dict("content", new_data)
    
    count += 1  # Increment count for the next iteration

# Optionally, print the dictionary and array to check the result
print(my_dict.values())

new_dict = my_dict