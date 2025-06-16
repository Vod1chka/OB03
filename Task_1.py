# 1. Создайте базовый класс `Animal`, который будет содержать общие атрибуты (например, `name`, `age`) и методы (`make_sound()`, `eat()`) для всех животных.
# 2. Реализуйте наследование, создав подклассы `Bird`, `Mammal`, и `Reptile`, которые наследуют от класса `Animal`. Добавьте специфические атрибуты и переопределите методы, если требуется (например, различный звук для `make_sound()`).
# 3. Продемонстрируйте полиморфизм: создайте функцию `animal_sound(animals)`, которая принимает список животных и вызывает метод `make_sound()` для каждого животного.=
# 4. Используйте композицию для создания класса `Zoo`, который будет содержать информацию о животных и сотрудниках. Должны быть методы для добавления животных и сотрудников в зоопарк.
# 5. Создайте классы для сотрудников, например, `ZooKeeper`, `Veterinarian`, которые могут иметь специфические методы (например, `feed_animal()` для `ZooKeeper` и `heal_animal()` для `Veterinarian`).

# Дополнительно:
# Попробуйте добавить дополнительные функции в вашу программу, такие как сохранение информации о зоопарке в файл и возможность её загрузки, чтобы у вашего зоопарка было "постоянное состояние" между запусками программы.


import json

class Animal():
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def make_sound(self):
        pass

    def eat(self):
        print (f"{self.name} ест")

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "name": self.name,
            "age": self.age
        }

class Bird(Animal):
    def __init__(self, name, age, color_wings):
        super().__init__(name, age)
        self.color_wings = color_wings

    def make_sound(self):
        print(f'{self.name} говорит "Чи-чи-пи"')

    def to_dict(self):
        data = super().to_dict()
        data["color_wings"] = self.color_wings
        return data

class Mammal(Animal):
    def __init__(self,name, age, length_mane):
        super().__init__(name, age)
        self.length_mane = length_mane

    def make_sound(self):
        print(f'{self.name} говорит "Аррр"')

    def to_dict(self):
        data = super().to_dict()
        data["length_mane"] = self.length_mane
        return data

class Reptile(Animal):
    def __init__(self, name, age, body_length):
        super().__init__(name, age)
        self.body_length = body_length

    def make_sound(self):
        print(f'{self.name} говорит "Тссс"')

    def to_dict(self):
        data = super().to_dict()
        data["body_length"] = self.body_length
        return data

def animal_sound(animals):
    for animal in animals:
        animal.make_sound()
        animal.eat()

class Zoo():
    def __init__(self):
        self.animals = {} # Словарь для хранения животных
        self.employees = {} # Словарь для хранения сотрудников

    def add_animal(self, animal):
        self.animals[animal.name] = animal
        print(f"{animal.name} привезен в зоопарк")

    def add_employee(self, employee):
        self.employees[employee.name] = employee
        print(f"{employee.name} устроился на работу в зоопарк")

    def save_to_file(self, filename):
        data = {
            "animals": [animal.to_dict() for animal in self.animals.values()],
            "employees": [employee.to_dict() for employee in self.employees.values()]
        }
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Данные сохранены в файле {filename}")

    def load_from_file(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for animal_data in data.get("animals", []):
                    self._load_animal_from_dict(animal_data)
                for emp_data in data.get("employees", []):
                    self._load_employee_from_dict(emp_data)
            print(f"Данные загружены из файла {filename}")
        except FileNotFoundError:
            print(f"Файл {filename} не найден")

    def _load_animal_from_dict(self, data):
        animal_type = data.get("type")
        name = data.get("name")
        age = data.get("age")

        if animal_type == "Bird":
            color_wings = data.get("color_wings", "неизвестный")
            animal = Bird(name, age, color_wings)
        elif animal_type == "Mammal":
            length_mane = data.get("length_mane", "неизвестная")
            animal = Mammal(name, age, length_mane)
        elif animal_type == "Reptile":
            body_length = data.get("body_length", "неизвестная")
            animal = Reptile(name, age, body_length)
        else:
            print(f"Неизвестный тип животного: {animal_type}")
            return

        self.add_animal(animal)

    def _load_employee_from_dict(self, data):
        emp_type = data.get("type")
        name = data.get("name")

        if emp_type == "ZooKeeper":
            employee = ZooKeeper(name)
        elif emp_type == "Veterinarian":
            employee = Veterinarian(name)
        else:
            print(f"Неизвестный тип сотрудника: {emp_type}")
            return

        self.add_employee(employee)

class ZooKeeper():
    def __init__(self,name):
        self.name = name

    def to_dict(self):
        return {
            "type": "ZooKeeper",
            "name": self.name
        }
    def feed_animal(self, animal):
        print(f"{self.name} кормит {animal.name}")
        animal.eat()

class Veterinarian():
    def __init__(self,name):
        self.name = name

    def to_dict(self):
        return {
            "type": "Veterinarian",
            "name": self.name
        }
    def heal_animal(self, animal):
        print(f"{self.name} лечит {animal.name}")
        animal.make_sound()



keeper = ZooKeeper("Вася")
veterinarian = Veterinarian("Анна")

zoo = Zoo()
zoo.add_animal(Bird("Воробей", 3, "Коричневый"))
zoo.add_animal(Mammal("Лев", 5, "Длинная"))
zoo.add_animal(Reptile("Змея", 2, "короткий"))
zoo.add_employee(keeper)
zoo.add_employee(veterinarian)


zoo.save_to_file("zoo_data.json")
# zoo.load_from_file("zoo_data.json")

keeper.feed_animal(zoo.animals['Воробей'])
veterinarian.heal_animal(zoo.animals['Змея'])
keeper.feed_animal(zoo.animals['Лев'])

