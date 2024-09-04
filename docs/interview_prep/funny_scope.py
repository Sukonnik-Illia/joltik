def increment_outside_scope():
    some_outside_var += 10


some_outside_var = 0
try:
    increment_outside_scope()
except UnboundLocalError:
    print("Yep UnboundLocalError raised")


def increment_instance_correct_scope():
    instance.some_instance_var += 10


class SomeClass:
    some_instance_var = 0


instance = SomeClass()

increment_instance_correct_scope()
print(f"No error instance.some_instance_var = {instance.some_instance_var}")
