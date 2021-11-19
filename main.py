import itertools as it


class Evaluator:

    def __init__(self):
        self.operators = {
            '~': [5, True],
            '^': [4, True],
            'v': [3, True],
            '=>': [2, True],
            '<=>': [1, True],
            '(': [0, True]
        }

        self.operations = {
            '~': lambda a: not a,
            '^': lambda a, b: a and b,
            'v': lambda a, b: a or b,
            '=>': lambda a, b: (not a) or b,
            '<=>': lambda a, b: a == b,
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
            if type(element) == bool:
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
                                if len(stack) == 0:
                                    stack.append(element)
                                    break
                            else:
                                stack.append(element)
                                break
                        elif value < self.operators[top_el][0]:
                            queue.append(top_el)
                            stack.pop()
                            if len(stack) == 0:
                                stack.append(element)
                                break
                        else:
                            stack.append(element)
                            break
                else:
                    stack.append(element)

        queue.extend(stack.__reversed__())
        return queue

    def evaluate_value(self, rpn_string):
        stack = []

        for element in rpn_string:
            if type(element) == bool:
                stack.append(element)
            else:
                a = stack.pop()
                b = stack.pop()
                stack.append(self.operations[element](b, a))

        return stack[0]

    @staticmethod
    def set_bool_values(form, combination):
        result_form = []
        for i, element in enumerate(form):
            result_form.append(element)
            if element in combination.keys():
                result_form[i] = combination[element]
        return result_form

    @staticmethod
    def generate_combination_set(variable_names):
        combinations = it.product(*[[True, False] for _ in range(len(variable_names))])
        combination_set = []

        for combination in combinations:
            comb_dict = {}
            for i, name in enumerate(variable_names):
                comb_dict[name] = combination[i]
            combination_set.append(comb_dict)

        return combination_set


def main():

    variable_names = ['p', 'q']
    string_form = "~p ^ q"

    evaluator = Evaluator()
    combination_set = evaluator.generate_combination_set(variable_names)
    processed_form = evaluator.process_string(string_form)

    for combination in combination_set:
        bool_form = evaluator.set_bool_values(processed_form, combination)
        print(bool_form)
        rpn = evaluator.convert_to_rpn(bool_form)
        print(rpn)
        value = evaluator.evaluate_value(rpn)
        print(value)


main()
