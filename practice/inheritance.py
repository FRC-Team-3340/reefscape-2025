class Fruit():
    def __init__(self, name: str, color: str, count: int):
        self.name = name;
        self.color = color;
        self.count = count;

    def print_info(self):
        print(f"This is {self.name}, which is the color {self.color}. There are {self.count} of them")


class Apple(Fruit):
    def __init__(self, count: int, apple_type: str):
        self.type = apple_type

        super().__init__("Apple", "red", count)

        print(self.type)


one_fruit = Fruit("Orange", "Orange", 6)
one_apple = Fruit("Apple", "Red", 9)

a_apple = Apple(9, "Fuji")


a_apple.print_info()

