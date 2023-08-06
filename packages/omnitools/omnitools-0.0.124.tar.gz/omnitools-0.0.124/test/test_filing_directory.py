from omnitools import *


# to be re-implemented
root = r"I:\test"
tree = create_tree(root)
print(jd(tree, indent=4))
print(format_cascade(create_cascade(root, tree)))
input("browse_directory next?")
browse_directory(root)

