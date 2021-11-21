import itertools as it


class Evaluator:

    def __init__(self):
        self.operators = {
            '~': [5, True],
            '^': [4, True],
            'v': [3, True],
            '=>': [2, False],
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

    def process_helper(self, string_form):
        all_operators = list(self.operators.keys())
        all_operators.append(')')

        if len(string_form) == 1 or string_form in all_operators:
            return [string_form]
        if len(string_form) > 3:
            if string_form[:3] in all_operators:
                r = [string_form[:3]]
                r.extend(self.process_helper(string_form[3:]))
                return r
            if string_form[:2] in all_operators:
                r = [string_form[:2]]
                r.extend(self.process_helper(string_form[2:]))
                return r
            r = [string_form[0]]
            r.extend(self.process_helper(string_form[1:]))
            return r
        if len(string_form) > 2:
            if string_form[:2] in all_operators:
                r = [string_form[:2]]
                r.extend(self.process_helper(string_form[2:]))
                return r
            r = [string_form[0]]
            r.extend(self.process_helper(string_form[1:]))
            return r
        if len(string_form) > 1:
            r = [string_form[0]]
            r.extend(self.process_helper(string_form[1:]))
            return r

    def process_string(self, string_form):
        stripped_list = [element for element in string_form if element != ' ']
        stripped_string = "".join(stripped_list)
        return self.process_helper(stripped_string)

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
            elif element == '~':
                a = stack.pop()
                stack.append(self.operations[element](a))
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

    def get_variable_names(self, processed_form):
        variable_names = set()
        for element in processed_form:
            if element not in self.operators.keys() and element != ')':
                variable_names.add(element)
        return variable_names

    def are_equal(self, *args):
        new_form = ''

        if len(args) == 1:
            new_form = args[0]
            return self.is_tautology(new_form)

        if len(args) > 1:
            equal = True

            for arg in args[1:]:
                new_form = '( ' + args[0] + ' ) <=> ( ' + arg + ' )'
                value = self.is_tautology(new_form)
                if not value:
                    equal = False

            return equal

    def is_satisfiable(self, form):
        form = self.process_string(form)
        variable_names = self.get_variable_names(form)

        combination_set = self.generate_combination_set(variable_names)
        satisfiable = False

        for combination in combination_set:
            bool_form = self.set_bool_values(form, combination)
            rpn = self.convert_to_rpn(bool_form)
            if self.evaluate_value(rpn):
                satisfiable = True

        return satisfiable

    def is_tautology(self, form):
        form = self.process_string(form)
        print(form)
        variable_names = self.get_variable_names(form)

        combination_set = self.generate_combination_set(variable_names)
        tautology = True

        for combination in combination_set:
            bool_form = self.set_bool_values(form, combination)
            rpn = self.convert_to_rpn(bool_form)
            if not self.evaluate_value(rpn):
                tautology = False

        return tautology


def main():

    variable_names = ['p', 'q', 'r']
    string_form = "p=>q<=> ~p v q"

    evaluator = Evaluator()
    combination_set = evaluator.generate_combination_set(variable_names)
    processed_form = evaluator.process_string(string_form)

    # for combination in combination_set:
    #     bool_form = evaluator.set_bool_values(processed_form, combination)
    #     rpn = evaluator.convert_to_rpn(bool_form)
    #     value = evaluator.evaluate_value(rpn)

    # print("Forms p => q and ~ p v q and ~ p v q are equal: " + str(evaluator.are_equal("p => q", "~ p v q", "~ ( p ^ ~ q )")))
    print("Form " + string_form + " is a tautology: " + str(evaluator.is_tautology(string_form)))
    # print("Form " + string_form + " is a satisfiable: " + str(evaluator.is_satisfiable(string_form)))


main()
