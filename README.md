# Introduction

## Purpose
The product represents a web application called Corporative Task Manager, which allows employees of the company to
create and distiribute job tasks between each other.

This document is the System Requirement Specifications (SRS) for the product. It describes all its functions and purposes.

## Area of application
The developed product – Corporate Task Manager (CTM) – must help the company to organize employees' work process by
building and storing the employees hierarchy tree, where each employee (excluding administrator – root node) has one
chief and any amount of subordinates. Main functions of the product are connected to "chief-subordinates" relation in
that tree.

## Definitions, acronyms and abbreviations
| Term | Definition |
| --- | --- |
| Company | The hypothetical client company for which the product is developed |
| Product | CTM, the software under development |
| System | The product's backend part, providing the main functions |
| Task | An action required to be performed by the person to whom it is assigned |
| Subtask | A task created by dividing another task |
| Report | A document attached to a completed task if neccessary |
| Hierarchy tree | A tree-like data structure representing employees' relations |

# Overall description

## Product positioning
The product is a pet project imagined as a custom solution for inner use by the company.

## Product functions
User related functions:
* authorization in system;
* for administrators:
  * adding new employees into the system;
  * editing employees' data;
  * editing the hierarchy tree (chief appointments and reappointments);
  * removing employees from the system.
Task related functions:
* for chiefs:
  * assignment of tasks with priorities and deadlines;
  * dividing an assigned task into subtasks between self and subordinates;
* for employees:
  * completing a task and attaching a report if neccessary.

## Classes and user characteristics
The users of the product are the company's employees. They are split into 3 types:
* employee – every entity of User class belongs to this type,
* chief – user that has at least 1 subordinate in the hierarchy tree,
* administrator – Django superuser that has permission to change any data in database.

## Constraints
### Employees' data storing
In terms of accounts' security passwords must be written in system using Django's password hashing mechanisms.

# Detailed requirements

## Outer interfaces requirements
### User interfaces
User interface is a web page.
### Software interfaces
Product requires a web-browser to lauch.

## Functional requirements
### Unauthorized user
#### System entrance
The system must authorize the user after authentication with e-mail address and password.

### Employee
#### System exit
System must cancel employee authorization when they log out of it.
#### Profile view
System must provide information about employees' accounts to authorized users.
#### Task list view
System must provide authorized user with tasks assigned to them.
#### Task archivation
System must add completed tasks into archive with completion datestamps and appended reports.

### Chief
#### Task assignment
System must let chiefs assign tasks to themselves or their subordinates indicating the title, description,
deadline, and report neccessity.
#### Task splitting
System must let chiefs split their tasks into subtasks distributed between them and their subordinates.

### Administrator
#### Employee adding
System must let administrator create new employee accounts.
#### Employee removing
System must let administrator remove existing employee accounts.
#### Employee data editing
System must let administrator change data in existing employee accounts.
#### Hierarchy change
System must let administrator assign and reassign employees' chiefs.

## Performance requirements
### User requests
The time of response to user requests mustn't be more than 5s.
