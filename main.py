import itertools as it


class Evaluator:

    def __init__(self):
        self.operators = {
            '+': [1, True],
            '-': [1, True],
            '/': [2, True],
            'x': [2, True],
            '^': [3, False],
            '(': [0, True]
        }

    @staticmethod
    def process_string(string_form):
        processed_string = []
        split_string = [element for element in string_form if element != ' ']
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

        return processed_string

    def convert_to_rpn(self, string):
        queue = []
        stack = []

        for element in string:
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
            elif element in self.operators.keys():
                value = self.operators[element][0]
                if len(stack) > 0:
                    while True:
                        top_el = stack[-1]
                        if self.operators[element][1]:
                            if value <= self.operators[top_el][0]:
                                queue.append(top_el)
                                stack.pop()
                            else:
                                stack.append(element)
                                break
                        elif value < self.operators[top_el][0]:
                            queue.append(top_el)
                            stack.pop()
                        else:
                            stack.append(element)
                            break
                        if len(stack) == 0:
                            break
                else:
                    stack.append(element)

        queue.extend(stack)
        return queue


def main():
    string_form = "3 + 4 x 2 / (1 - 5) ^ 2"

    evaluator = Evaluator()
    processed_form = evaluator.process_string(string_form)
    rpn = evaluator.convert_to_rpn(processed_form)
    print(rpn)


main()
