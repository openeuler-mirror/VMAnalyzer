"""Check that brackets, braces and parentheses are balanced."""
__all__ = ["is_balanced", "first_unbalanced_index"]

_OPEN = {"(": ")", "[": "]", "{": "}"}
_CLOSE = {v: k for k, v in _OPEN.items()}


def first_unbalanced_index(text):
    """Return the index of the first unmatched bracket, or -1 if balanced."""
    stack, in_string = [], None
    for index, ch in enumerate(str(text)):
        if in_string:
            if ch == in_string:
                in_string = None
        elif ch in "\"'":
            in_string = ch
        elif ch in _OPEN:
            stack.append((ch, index))
        elif ch in _CLOSE:
            if not stack or stack[-1][0] != _CLOSE[ch]:
                return index
            stack.pop()
    return stack[-1][1] if stack else -1


def is_balanced(text):
    """Return True when every bracket in *text* is correctly matched."""
    return first_unbalanced_index(text) == -1
