def find_column(input_text, token):
    last_cr = input_text.rfind('\n', 0, token.lexpos)
    if last_cr < 0:
        last_cr = -1
    column = token.lexpos - last_cr
    return column

def print_error(char, row, column):
    print(f"Error: Unexpected character \"{char}\" in row {row}, column {column}")