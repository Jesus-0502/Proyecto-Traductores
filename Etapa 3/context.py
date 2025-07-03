# Traductores e Interpretadores
# Etapa 3 del Proyecto
# Elaborado por: Mauricio Fragachan 20-10265
#                Jesus Gutierrez 20-10332

import sys

class SymbolTable:
    def __init__(self, parent=None):
        self.parent = parent
        self.symbols = {}  # nombre -> tipo

    def declare(self, name, type_):
        if name in self.symbols:
            raise Exception(f"Redeclaration error: '{name}' already declared in this scope.")
        self.symbols[name] = type_

    def lookup(self, name):
        if name in self.symbols:
            return self.symbols[name]
        elif self.parent:
            return self.parent.lookup(name)
        else:
            raise Exception(f"Undeclared variable error: '{name}' not declared.")

    def print_table(self, indent=0):
        print("-" * indent + "Symbols Table")
        for name, type_ in self.symbols.items():
            print("-" * (indent + 1) + f"{name} : {type_}")


def context_analysis(ast, table=None):
    if table is None:
        table = SymbolTable()

    if isinstance(ast, tuple):
        node_type = ast[0]

        if node_type == "Block":
            new_table = SymbolTable(parent=table)
            if len(ast) == 3:
                _, declare_node, instr_node = ast
                process_declarations(declare_node, new_table)
                context_analysis(instr_node, new_table)
            else:
                _, instr_node = ast
                context_analysis(instr_node, new_table)
            new_table.print_table(indent=1)

        elif node_type == "Sequencing":
            context_analysis(ast[1], table)
            context_analysis(ast[2], table)

        elif node_type == "Asig":
            ident = ast[1].split(": ")[-1]
            try:
                var_type = table.lookup(ident)
            except Exception as e:
                print(e)
                sys.exit(1)
            expr_type = context_analysis(ast[2], table)
            if expr_type != var_type:
                print(f"Type error: cannot assign {expr_type} to variable '{ident}' of type {var_type}.")
                sys.exit(1)
            return var_type

        elif node_type in {"Plus", "Minus", "Mult"}:
            left = context_analysis(ast[1], table)
            right = context_analysis(ast[2], table)
            if left != "int" or right != "int":
                print(f"Type error in '{node_type}': both operands must be int.")
                sys.exit(1)
            return "int"

        elif node_type in {"And", "Or"}:
            left = context_analysis(ast[1], table)
            right = context_analysis(ast[2], table)
            if left != "bool" or right != "bool":
                print(f"Type error in '{node_type}': both operands must be bool.")
                sys.exit(1)
            return "bool"

        elif node_type in {"Equal", "NotEqual", "Less", "Greater", "Leq", "Geq"}:
            left = context_analysis(ast[1], table)
            right = context_analysis(ast[2], table)
            if left != "int" or right != "int":
                print(f"Type error in comparison '{node_type}': both operands must be int.")
                sys.exit(1)
            return "bool"

        elif node_type.startswith("Literal"):
            if "true" in node_type or "false" in node_type:
                return "bool"
            else:
                return "int"

        elif node_type.startswith("Ident"):
            name = ast.split(": ")[-1]
            return table.lookup(name)

        elif node_type == "Print":
            context_analysis(ast[1], table)

        elif node_type == "If":
            process_guards(ast[1], table)

        elif node_type == "While":
            _, then_node = ast
            cond_type = context_analysis(then_node[1], table)
            if cond_type != "bool":
                print("Type error: condition of while must be bool.")
                sys.exit(1)
            context_analysis(then_node[2], SymbolTable(parent=table))

        else:
            for child in ast[1:]:
                context_analysis(child, table)


def process_declarations(declare_node, table):
    if declare_node[0] == "Declare":
        process_declarations(declare_node[1], table)
    elif declare_node[0] == "Sequencing":
        process_declarations(declare_node[1], table)
        process_declarations(declare_node[2], table)
    else:
        decl = declare_node
        if ":" in decl:
            names, type_ = decl.split(":")
            type_ = type_.strip()
            for name in names.split(","):
                table.declare(name.strip(), type_)


def process_guards(guards, table):
    if guards[0] == "Guard":
        process_guards(guards[1], table)
        process_guards(guards[2], table)
    elif guards[0] == "Then":
        cond_type = context_analysis(guards[1], table)
        if cond_type != "bool":
            print("Type error: condition in if must be bool.")
            sys.exit(1)
        context_analysis(guards[2], SymbolTable(parent=table))


def print_ast_with_types(ast, indent=0):
    if isinstance(ast, tuple):
        print("-" * indent + str(ast[0]))
        for child in ast[1:]:
            print_ast_with_types(child, indent + 1)
    else:
        print("-" * indent + str(ast))


if __name__ == "__main__":
    import parser
    if len(sys.argv) != 2:
        print("Uso: python context.py <archivo.imperat>")
        sys.exit(1)

    with open(sys.argv[1], encoding="utf-8") as f:
        source_code = f.read()

    result = parser.parse(source_code, lexer=parser.lexer)

    print("\n--- Análisis de contexto ---")
    context_analysis(result)

    print("\n--- AST Decorado ---")
    print_ast_with_types(result)
