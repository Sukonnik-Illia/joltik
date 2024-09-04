## Is python OOP ##
### Variation: What is OOP + discuss on its principles ###
Pure OOP languages: Ruby, Scala, JADE, Emerald.
Python is designed primarily for OOP, though not pure OOP.

0. OOP structure (supports Classes, Objects, Methods, Attributes)

**1. Encapsulation:**
* allows attributes and methods to be bundled together within a class
* no access restriction to private functions, acheived via naming convension (prefixing "_" or "__")

**2. Abstraction:**

Is acheived by defining classes and methods that provide a simple interface to the user while hiding the complex internal workings.

**3. Inheritance:**

Python allows a class to inherit attributes and methods from another class.

**4. Polymorphism:**

Different classes can be treated as instances of the same class through a common interface (animals = [Dog(), Cat()])

## Abstract Classes vs Interfaces ##

**ABC:**
- cannot be instantiated on its own and is meant to be subclassed
- can contain both abstract and concrete methods
- serves as a blueprint for other classes
- can provide a common base with some shared code.

**Interface:**
- defines a contract or a set of methods that implementing classes must provide
- typically contains only abstract methods and no attributes or instance variables
- used to define a set of methods that a class must implement

**Method Implementation**
* Abstract Class can contain both abstract and concrete methods
* Interface only contains abstract methods

In Python, the closest concept to an interface is achieved through ABC with only abstract methods.

**Inheritance and Implementation**
* ABC can inherit from only one abstract class
* class can implement multiple Interfaces
* ABC can provide some shared implementation that can be inherited by subclasses
* Interfaces do not provide any implementation, just the method signatures
* subclasses can extend or override methods from ABC

Python achieves Interfaces functionality through multiple inheritance with ABCs.

**Use Cases**
* Use ABC when you have a base class that should not be instantiated on its own, but should be extended by other classes. You want to share some common code among related classes while enforcing certain methods to be implemented.
* Use Interfaces when you want to enforce certain methods across different classes that may not share a common ancestor. You want to define a common protocol that unrelated classes should adhere to.


## Why is python slow ##
https://www.youtube.com/watch?v=x2IQP8iug3c

* **Interpritation vs compilation.** Works each time code launched, executed line by line at runtime vs once translated into machine code before execution
* **Lack of concurrency.** Global Interpreter Lock (GIL) allows only one thread to execute at a time.
* **Dynamic Typing.** Interpreter has to do type checking at a runtime.
* **High-Level Abstractions**:
    * prevents low-level memory management
    * Python objects are more memory-intensive than the lower-level data structures

Python can be fast in **I/O operations, scripting, or data analysis**, where the time spent in execution is dominated by external factors like disk or network speed.

Some Python interpreters like PyPy do have Just-In-Time Compilation.

## How to speed up python ##

Runtime improvements:
* use libraries like NumPy or Cython
* Just-In-Time Compilation is used by interpreters like PyPy
* C code as extension to Python lybrary

Inside Python code:
* list comprehension vs loop
* generators for large data sets
* avoid using global variables (slow toaccess them)
* join() for string concatenation
* 'in' for membership checks in sets and dictionaries (not lists?)
* profiling tools like (cProfile, timeit) to find and optimize performance bottlenecks
* caching for expensive function calls when the same inputs are used repeatedly

## Python data collection types ##

**List** is a collection which is ordered and changeable
+ flexible (mixed data types, can be dynamically resized)
+ built-in methods like append(), remove(), sort()
+ slicing, allowing you to access sublists with ease

**Tuple** is a collection which is ordered and unchangeable.
Use cases: fixed set of coordinates, complex dict key.
+ immutabile, so safer to use for fixed data
+ more memory-efficient and slightly faster than lists
+ hashable: can be used as dict keys or stored in sets

**Set** is a collection which is unordered and unindexed. Sets are mutable, but elemants are unchangeable. Use cases: store collection of unique items (IDs), perform unions, intersection, difference and other math set operations.
+ automatically handle duplicates, ensuring all elements are unique
+ optimized for fast membership checks, ideal for frequent lookups tasks
+ support union, intersection, difference, and symmetric difference operations

**Dictionary** is a collection which is ordered (in v >=3.7) and changeable. Use cases: store pairs of related data (word - definition), storing configurations or caching results for fast lookup, custom indexing key.
+ optimized for fast lookups, insertion, and deletion
+ can be dynamically resized
+ can store complex data structures, such as lists or other dictionaries

## Circular reference in data collections ##
    list1 = []
    list2 = []

    list1.append(list2)
    list2.append(list1)

If you try to print a list, python will indicate a recursive reference

    print(list1)  # Outputs: [[...]]
    print(list2)  # Outputs: [[...]]
    print(list1[0])     # Outputs: [[...]]
    print(list1[0][0])  # Outputs: [[...]]
    print(list1[0][0][0])  # Outputs: [[...]] (and so on...)

**Memory Management:**
* Python uses reference counting, objects are auto destroyed when their reference count drops to zero. Circular references cannot be resolved by reference counting alone.
* For circular references, garbage collector has a mechanism to detect and clean up objects involved in circular references that are no longer accessible from any part of the program.

## *Multyprocessing, Multithreading, Asyncio ##
...
* if treads amount can be limited (i.e. <100) it would be easier in debug
* asyncio ib better whether there is more connections (like >500)
...

## *Tests, test types, test structure ##

## *Factories ##
factoryboy
