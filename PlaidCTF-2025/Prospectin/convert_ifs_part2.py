#!uv run
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "z3-solver",
# ]
# ///
import re
import sys

def balanced(s):
    """Return True if s has balanced parentheses."""
    count = 0
    for c in s:
        if c == '(':
            count += 1
        elif c == ')':
            count -= 1
            if count < 0:
                return False
    return count == 0

def find_matching(s, start, open_char, close_char):
    """
    Given a string s and an index start where s[start] == open_char,
    return the index of the matching close_char (taking nested pairs into account).
    """
    count = 0
    for i in range(start, len(s)):
        if s[i] == open_char:
            count += 1
        elif s[i] == close_char:
            count -= 1
            if count == 0:
                return i
    raise ValueError(f"No matching '{close_char}' found in string starting at {start}.")

def parse_statements(text):
    """
    Parse a block of text (a sequence of statements) into a list of nodes.
    A node is a tuple:
      - ('if', condition, children) for an if–statement
      - ('text', text) for non-if text.
    """
    nodes = []
    i = 0
    while i < len(text):
        # Skip whitespace
        while i < len(text) and text[i].isspace():
            i += 1
        if i >= len(text):
            break
        # Check if we have an if statement
        if text[i:i+2] == "if":
            node, new_i = parse_if(text, i)
            nodes.append(node)
            i = new_i
        else:
            # Find the next "if" keyword
            next_if = text.find("if", i)
            if next_if == -1:
                nodes.append(('text', text[i:]))
                i = len(text)
            else:
                nodes.append(('text', text[i:next_if]))
                i = next_if
    return nodes

def parse_if(text, i):
    """
    Parse an if–statement starting at index i.
    Returns a tuple (node, new_index) where node is:
         ('if', condition, children)
    and new_index is the position right after the if–block.
    """
    # Skip "if"
    i += 2
    # Skip whitespace until '('
    while i < len(text) and text[i].isspace():
        i += 1
    if i >= len(text) or text[i] != '(':
        raise ValueError("Expected '(' after if at position {}".format(i))
    cond_start = i + 1
    cond_end = find_matching(text, i, '(', ')')
    condition = text[cond_start:cond_end].strip()
    i = cond_end + 1
    # Skip whitespace until block start
    while i < len(text) and text[i].isspace():
        i += 1
    if i >= len(text) or text[i] != '{':
        raise ValueError("Expected '{' after if condition at position {}".format(i))
    block_start = i + 1
    block_end = find_matching(text, i, '{', '}')
    block_text = text[block_start:block_end]
    # Recursively parse the contents of the block
    children = parse_statements(block_text)
    node = ('if', condition, children)
    return node, block_end + 1

def get_score_from_text(text):
    """
    Extract and sum all occurrences of score increments in text,
    e.g. lines like "scores += 1;".
    """
    return sum(int(x) for x in re.findall(r'scores\s*\+=\s*(\d+)', text))

def convert_condition(expr):
    """
    Convert a C-style boolean expression into a Z3 expression.
    Recursively removes outer parentheses and splits on top-level '&&' or '||'.
    For example:
      "((a < b) && (c < d))" becomes "And(a < b, c < d)"
    """
    expr = expr.strip()
    # Remove outer parentheses that enclose the whole expression.
    while expr.startswith('(') and expr.endswith(')') and balanced(expr[1:-1]):
        expr = expr[1:-1].strip()

    # Split on top-level &&
    parts = split_by_top_level(expr, "&&")
    if len(parts) > 1:
        converted = [convert_condition(part) for part in parts]
        return "And(" + ", ".join(converted) + ")"

    # Then on top-level ||
    parts_or = split_by_top_level(expr, "||")
    if len(parts_or) > 1:
        converted = [convert_condition(part) for part in parts_or]
        return "Or(" + ", ".join(converted) + ")"

    return expr

def split_by_top_level(expr, delimiter):
    """
    Split expr by the given delimiter (e.g. '&&' or '||') at the top level,
    ignoring delimiters inside parentheses.
    """
    parts = []
    current = ""
    i = 0
    level = 0
    delim_len = len(delimiter)
    while i < len(expr):
        if expr[i] == '(':
            level += 1
            current += expr[i]
        elif expr[i] == ')':
            level -= 1
            current += expr[i]
        elif expr[i:i+delim_len] == delimiter and level == 0:
            parts.append(current.strip())
            current = ""
            i += delim_len - 1
        else:
            current += expr[i]
        i += 1
    if current.strip():
        parts.append(current.strip())
    return parts

def emit_nodes(nodes, parent_condition=None):
    """
    Recursively generate Z3 condition lines from the parsed nodes.
    For each if–node, the effective condition is the parent's condition AND its own.
    Returns a tuple (lines, text_score) where:
       - lines is a list of generated Z3 condition lines.
       - text_score is the total score increments from text nodes at this level.
    """
    lines = []
    text_score = 0
    for node in nodes:
        if node[0] == 'text':
            text_score += get_score_from_text(node[1])
        elif node[0] == 'if':
            # Convert the if's condition.
            curr_cond = convert_condition(node[1])
            effective = f"And({parent_condition}, {curr_cond})" if parent_condition else curr_cond
            # Process child nodes recursively.
            child_lines, child_text = emit_nodes(node[2], effective)
            # If there are score increments directly in this if block, emit a line.
            if child_text > 0:
                lines.append(f"score = score + If({effective}, {child_text}, 0)")
            lines.extend(child_lines)
    return lines, text_score

def extract_variables(expr):
    """
    Extract variable names matching the pattern v[0-9a-fA-F]+ (ignoring hex constants).
    """
    tokens = re.findall(r'\b(v[0-9a-fA-F]+)\b', expr)
    return set(tokens)

def main():
    if len(sys.argv) != 3:
        print("Usage: {} input_file output_file".format(sys.argv[0]))
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    with open(input_file, 'r') as f:
        content = f.read()
    
    # Parse the entire file into a list of nodes.
    nodes = parse_statements(content)
    
    # Recursively emit Z3 lines from the nodes.
    condition_lines, top_text = emit_nodes(nodes)
    
    # If there are any score increments at the top level (unlikely), add them.
    if top_text > 0:
        condition_lines.insert(0, f"score = score + If(True, {top_text}, 0)")
    
    # Collect all variables from the generated condition lines.
    all_vars = set()
    for line in condition_lines:
        all_vars.update(extract_variables(line))
    
    if all_vars:
        vars_sorted = sorted(all_vars)
        var_decl = f"{', '.join(vars_sorted)} = Ints('{ ' '.join(vars_sorted) }')"
    else:
        var_decl = "# No variables found"
    
    # Build the output file.
    output_lines = []
    output_lines.append("from z3 import *")
    output_lines.append("")
    output_lines.append(var_decl)
    output_lines.append("")
    output_lines.append("score = Int('score')")
    output_lines.append("opt = Optimize()")
    output_lines.append("opt.add(score == 0)")
    output_lines.append("")
    for cline in condition_lines:
        output_lines.append(cline)
    output_lines.append("")
    output_lines.append("opt.maximize(score)")
    output_lines.append("print(opt.check())")
    output_lines.append("print(opt.model())")
    
    with open(output_file, 'w') as f:
        f.write("\n".join(output_lines))
    
    print("Generated Z3 conditions in", output_file)

if __name__ == '__main__':
    main()
