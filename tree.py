class Node():
    def __init__(self, key, childs = []):
        self.key = key
        self.childs = childs

    def __str__(self):
        return f"{self.key}"
    
    # Draw tree
    def visualize(self):
        stack = [(self, 0, True)]
        has_sibling_depts = []

        while stack:
            node, depth, is_last_child = stack.pop()

            if depth > len(has_sibling_depts) - 1:
                has_sibling_depts.append(True)
            elif not has_sibling_depts[depth]:
                has_sibling_depts[depth] = True

            if is_last_child:
                has_sibling_depts[depth] = False
            
            buffer = ''
            for has_sibling in has_sibling_depts[1 : depth]:
                buffer += '|    ' if has_sibling else '    '

            buffer += '' if depth == 0 else ('└── ' if is_last_child else '├── ')
            buffer += str(node)

            for index, child in enumerate(node.child[::-1]):
                stack.append((child, depth + 1, True if index == 0 else False))

            print(buffer)