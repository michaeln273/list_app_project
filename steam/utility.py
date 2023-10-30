def int_input(input_text):
    response = input(input_text)

    if not response.isdigit():
        print("You must enter an integer, try again")
        return int_input(input_text)

    return int(response)

# In this program, choices always start at one so the min is 1 instead of 0
def range_input(input_text, max):
    response = int_input(input_text)

    if response < 1 or response > max:
        print(f"You must enter an integer between 1 and {max}, try again")
        return range_input(input_text, max)
    
    return response

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