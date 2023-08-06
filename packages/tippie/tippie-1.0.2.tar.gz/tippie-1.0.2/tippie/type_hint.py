import ast
import sys
import os

def make_ast(filepath):
    with open(filepath) as file:
        return ast.parse(file.read(), filename=filepath)

def write_to_file(filepath, lines):
    with open(filepath, "w") as file:
        file.writelines(lines)

def make_iterables(body):
    iter_type = iterators[types[type(body)]]
    for constant in body.elts:
        iter_type.append(constant.value)
    return iter_type

def get_var_name(body):
    return body.targets[0].id

def get_value(body):
    value = body.value
    if type(value) in types:
        return make_iterables(value)
    return value.value

def get_type(body):
    return types[type(body.value)].__name__ if type(body.value) in types else type(body.value.value).__name__

def parse_assign(body):
    var_name = get_var_name(body)
    _type = get_type(body)
    values = get_value(body)
    if isinstance(values, str):
        return f'{var_name}: {_type} = "{values}"'
    return f"{var_name}: {_type} = {values}"

def dump_ast(body):
    return ast.dump(body, indent=4)

def parse_to_ast(body):
    parsed_lines = []
    for line in body:
        if (t:=type(line)) in parser:
            parsed_lines.append(f"{parser[t](line)}\n")
    return parsed_lines

parser = {
    ast.Assign : parse_assign,
}
types = {
    ast.List:list,
    ast.Tuple:tuple,
    ast.Dict:dict
}
iterators = {
    list:[],
    tuple:(),
    dict:{},
}
def type_hint():
    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        raise FileNotFoundError()
    module = make_ast(filepath)
    parsed_ast = parse_to_ast(module.body)
    write_to_file(filepath, parsed_ast)


if __name__ == "__main__":
    type_hint()