import itertools as it

string_form = "3 + 4 x 2 / (1 - 5) ^ 2"
split_string = [element for element in string_form if element != ' ']
processed_string = []
merged_string = ""
for i, element in enumerate(split_string):
    if element.isnumeric():
        if merged_string.isnumeric():
            merged_string += element
            processed_string.pop()
        else:
            merged_string = element
    else:
        merged_string = element
    processed_string.append(merged_string)


print(processed_string)

queue = []
stack = []

operator_list = ['+', '-', '/', 'x', '^', '(']
operator_value = [1, 1, 2, 2, 3, 0]
left_side = [True, True, True, True, False, True]

for element in processed_string:
    print(element)
    if element.isnumeric():
        queue.append(element)
    elif element == '(':
        stack.append(element)
    elif element == ')':
        while True:
            if len(stack) == 0:
                print("Bad parentheses")
                break
            top_el = stack[-1]
            if top_el != '(':
                queue.append(top_el)
                stack.pop()
            else:
                stack.pop()
                break
    elif element in operator_list:
        i = operator_list.index(element)
        value = operator_value[i]
        print(value)
        if len(stack) > 0:
            while True:
                top_el = stack[-1]
                top_in = operator_list.index(top_el)
                if left_side[i]:
                    if value <= operator_value[top_in]:
                        queue.append(top_el)
                        stack.pop()
                    else:
                        stack.append(element)
                        break
                elif value < operator_value[top_in]:
                    queue.append(top_el)
                    stack.pop()
                else:
                    stack.append(element)
                    break

                if len(stack) == 0:
                    break

        else:
            stack.append(element)

final_string = queue.extend(stack)
print(queue)





