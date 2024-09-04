# Single Responsibility Principle
# Open Closed Principle
# Liskov Substitution Principle
# Interface Segregation Principle
# Dependency Inversion Principle

###############################################################################
## Single Responsibility Principle
# A class should have one, and only one, reason to change.
# Just avoid anti-patterns like God Object.

###############################################################################
## Open Closed Principle
# A class, module, function should be open for extension, but closed for modification.

###############################################################################
## Liskov Substitution Principle
# Parent class should be able to be replaced by child class without affecting the
# program.

###############################################################################
## Interface Segregation Principle
# No code should not be forced to depend on methods it does not use.
# Split interfaces into smaller ones.
# If we have Database class, with read, write, delete, and update methods, and
# we have a class that only needs to read from the database, it should not be
# forced to implement the write, delete, and update methods.
# So we can have DRead, DWrite, DDelete, and DUpdate interfaces, and the Database
# class can implement all of them, and the class that only needs to read from the
# database can implement only the DRead interface.

###############################################################################
## Dependency Inversion Principle
# High level modules should not depend on low level modules. Both should depend
# on abstractions.
