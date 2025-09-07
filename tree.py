import sys

class Node():
    def __init__(self, key, childs = []):
        self.key = key
        self.childs = childs

    def __str__(self):
        return f"{self.key}"
    
    def visualize(self, stream=None):
        if stream is None:
            stream = sys.stdout
            
        stack = [(self, 0, True)]
        has_sibling_depths = []

        while stack:
            node, depth, is_last_child = stack.pop()

            if depth > len(has_sibling_depths) - 1:
                has_sibling_depths.append(True)
            elif not has_sibling_depths[depth]:
                has_sibling_depths[depth] = True
            
            if is_last_child:
                has_sibling_depths[depth] = False

            buffer = ''
            for has_sibling in has_sibling_depths[1 : depth]:
                buffer += '│   ' if has_sibling else '    '

            buffer += '' if depth == 0 else ('└── ' if is_last_child else '├── ')
            buffer += str(node)

            for index, child in enumerate(node.childs[::-1]):
                stack.append((child, depth + 1, True if index == 0 else False))

            print(buffer, file=stream)