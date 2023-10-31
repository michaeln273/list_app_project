# Input function that ensures that the user inputs an integer and will automatically return the conversion
def int_input(input_text):
    response = input(input_text)

    if not response.isdigit():
        print("You must enter an integer, try again")
        return int_input(input_text)

    return int(response)

# This function uses the int_input function and checks if it's result is within a minimum of 1 and the specified max range
# In this program, choices always start at one so the min is 1 instead of 0
def range_input(input_text, max):
    response = int_input(input_text)

    if response < 1 or response > max:
        print(f"You must enter an integer between 1 and {max}, try again")
        return range_input(input_text, max)
    
    return response

# This input function uses the range_input function and prints a formatted result from a list
def choice_input(input_text, list):
    formatted = ""

    list_len = len(list)
    for i in range(list_len):
        formatted += f"({i + 1}) {list[i]}"

        if i == list_len - 2:
            formatted += " or "
        elif i != list_len - 1:
            formatted += ", "

    return range_input(f"{input_text} {formatted}? ", max=list_len)
