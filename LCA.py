from graphviz import Digraph

class TreeNode:
    def __init__(self, data, index):
        self.data = data
        self.index = index
        self.children = []
        self.color = "white" 

class Result:
    def __init__(self):
        self.step = 1

    def lowest_common_ancestor(self, root, p, q, dot):
        if root is None:
            return None

        # Highlight current node in yellow for step visualization
        if root.color == "white":
            dot.node(str(root.index), f"{root.data}\n({root.index})", style="filled", fillcolor="yellow")
            dot.render(f"tree_visualization_step_{self.step}", format='png', view=True)
            self.step += 1

        if root == p or root == q:
            root.color = "red"
            dot.node(str(root.index), f"{root.data}\n({root.index})", style="filled", fillcolor="red")
            return root

        count = 0
        temp = None

        for child in root.children:
            res = self.lowest_common_ancestor(child, p, q, dot)
            if res:
                count += 1
                temp = res
                

        # Highlight node in blue if count becomes one
        if count == 1 and root.color == "white":
            root.color = "cyan"
            dot.node(str(root.index), f"{root.data}\n({root.index})", style="filled", fillcolor="cyan")
            dot.render(f"tree_visualization_step_{self.step}", format='png', view=True)
            self.step += 1

        # Highlight node in dark green if count becomes two and return root
        if count == 2:
            root.color = "darkgreen"
            dot.node(str(root.index), f"{root.data}\n({root.index})", style="filled", fillcolor="darkgreen")
            dot.render(f"tree_visualization_step_{self.step}", format='png', view=True)
            self.step += 1
            return root

        # Only reset to white if it hasn't been colored blue or green
        if root.color == "white":
            dot.node(str(root.index), f"{root.data}\n({root.index})", style="filled", fillcolor="white")

        return temp
def create_tree_visualization(root, p=None, q=None):
    dot = Digraph(comment='General Tree')
    dot.attr(rankdir='TB')

    def add_nodes_edges(node):
        if node:
            dot.node(str(node.index), f"{node.data}\n({node.index})", style="filled", fillcolor=node.color)
            
            for child in node.children:
                dot.edge(str(node.index), str(child.index))
                add_nodes_edges(child)

    add_nodes_edges(root)
    return dot
def create_tree_visualization(root, p=None, q=None, lca=None):
    dot = Digraph(comment='General Tree')
    dot.attr(rankdir='TB')

    # Function to find the path from root to a target node
    def find_path(node, target, path=None):
        if path is None:
            path = []
        if node is None:
            return None
        path.append(node)
        if node == target:
            return path
        for child in node.children:
            result = find_path(child, target, path)
            if result is not None:
                return result
        path.pop()
        return None

    # Find the path from root to LCA
    lca_path = find_path(root, lca) if lca else []
    lca_path_set = set(lca_path)

    def add_nodes_edges(node):
        if node:
            if node == lca:
                dot.node(str(node.index), f"{node.data}\n({node.index})", style="filled", fillcolor="darkgreen")
            elif node == p or node == q:
                dot.node(str(node.index), f"{node.data}\n({node.index})", style="filled", fillcolor="orange")
            elif node in lca_path_set:
                dot.node(str(node.index), f"{node.data}\n({node.index})", style="filled", fillcolor="lightgreen")
            else:
                dot.node(str(node.index), f"{node.data}\n({node.index})")
            
            for child in node.children:
                dot.edge(str(node.index), str(child.index))
                add_nodes_edges(child)

    add_nodes_edges(root)
    return dot

def main():
    root = TreeNode(4, 0)
    node_1 = TreeNode(3, 1)
    node_2 = TreeNode(1, 2)
    node_3 = TreeNode(6, 3)
    node_4 = TreeNode(2, 4)
    node_5 = TreeNode(0, 5)
    node_6 = TreeNode(8, 6)
    node_7 = TreeNode(8, 7)
    node_8 = TreeNode(8, 8)
    node_9 = TreeNode(7, 9)
    node_10 = TreeNode(4, 10)
    node_11 = TreeNode(9, 11)
    node_12 = TreeNode(8, 12)
    node_13=TreeNode(130,13)
    node_14=TreeNode(1.4,14)
    # node_15=TreeNode(15,15)
    # node_16=TreeNode(23,16)
    # node_17=TreeNode(112,17)


    root.children = [node_1, node_2]
    node_1.children = [node_3,node_4]
    # node_2.children = [node_4, node_5]
    node_3.children = [node_5,node_13]
    node_4.children = [node_8,node_9]
    node_5.children = [node_6, node_7]
    node_8.children = [node_10]
    node_9.children = [node_11, node_12]
    node_13.children=[node_14]
    # node_12.children=[node_14,node_15,node_16,node_17]

    # Create initial tree visualization
    initial_dot = create_tree_visualization(root)
    initial_dot.render("initial_tree", format='png', view=True)

    # Create a dot object for step-by-step visualization
    step_dot = create_tree_visualization(root)

    result = Result()
    lca = result.lowest_common_ancestor(root, node_14, node_10, step_dot)
    print(f"LCA of {node_10.index} and {node_14.index} is node : {lca.index} with data: {lca.data}")

    # Create final tree visualization
    final_dot = create_tree_visualization(root, node_14, node_10, lca)
    final_dot.render("tree_visualization_final", format='png', view=True)

if __name__ == "__main__":
    main()