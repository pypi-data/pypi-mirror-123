from ..node import Node

userFragment = """
fragment User on User {
    id
    name
}
"""


class User(Node):
    def __init__(self, data, context):
        super().__init__(data, context=context)
