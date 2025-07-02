# 1. Introduction

## 1.1. Purpose
The product represents a web application called Corporative Task Manager, which allows employees of the company to
create and distiribute job tasks between each other.

This document is the System Requirements Specification (SRS) for the product. It describes all its functions and purposes.

## Area of application
The developed product – Corporate Task Manager (CTM) – must help the company to organize employees' work process by
building and storing the employees hierarchy tree, where each employee (excluding administrator – root node) has one
chief and any amount of subordinates. Main functions of the product are connected to "chief-subordinates" relation in
that tree.

## Document conventions
| Term | Definition |
| --- | --- |
| Company | The hypothetical client company for which the product is developed |
| Product | CTM, the software under development |
| System | The product's backend part, providing the main functions |
| Task | An action required to be performed by the person to whom it is assigned |
| Subtask | A task created by dividing another task |
| Report | A document attached to a completed task if neccessary |
| Hierarchy tree | A tree-like data structure representing employees' relations |

## Intended audience and reading suggestions
## Project scope
## References


# Overall description

## Product perspective
The product is a pet project imagined as a custom solution for inner use by the company.

## Product features
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

## User classes and characteristics
The users of the product are the company's employees. They are split into 3 types:
* employee – every entity of User class belongs to this type,
* chief – user that has at least 1 subordinate in the hierarchy tree,
* administrator – Django superuser that has permission to change any data in database.

## Operating environment
## Design and implementation constraints
## User documentation
## Assumptions and dependencies

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

# Appendix
## Subject area
The goal is to create a web application for company's work process organization. The application should be provided with roles:
- Employee
- Chief
- Administrator
### Roles
#### Employee
- contains information: name, e-mail, password, chief, qualifications, programming languages knowledge
- function of completing tasks (appending report if neccessary)
#### Chief
- has their subordinates list
- function of creating tasks and splitting them into subtasks distributed between them and their subordinates taking qualifications into account
#### Administrator
- functions of adding, editing and deleting data about employees, qualifications and languages
### Other functions
- employees must be able to get access to their accounts using their e-mail and password

## Use cases
### Case: Authorization

Subject: Unauthorized user

Goal: Give employee access to their account

Preconditions: -

#### Main sequence:
1. System shows login window with input fields (e-mail, password) and "Login" button
2. User enters e-mail and password and presses the button
3. System authorizes the user
#### Alternative sequence (user with entered e-mail and password doesn't exist in system):
1. System shows login window with input fields (e-mail, password) and "Login" button
2. User enters e-mail and password and presses the button
3. System notifies user about incorrect input

### Case: Account view

Subject: Employee

Goal: Provide employee with information about account

Preconditions: -

#### Main sequence:
1. Employee pressed "Account" button or a name in employees list
2. System shows window with information about account:
   - name
   - e-mail
   - qualifications
   - programming languages knowledge
   - chief
   - subordinates (if the employee has them)
#### Alternative sequence (visited account belongs to the employee):
1. Employee pressed "Account" button or a name in employees list
2. System shows window with information about account:
   - name
   - e-mail
   - button "Change password"
   - qualifications
   - programming languages knowledge
   - chief
   - subordinates (if the employee has them)

 ### Case: Employees view

Subject: Employee

Goal: Provide employee with information about other employees

Preconditions: -

#### Main sequence:
1. Employee pressed "Users" button
2. System shows window with table of information about users:
   - name (has link to user's profile page)
   - e-mail
   - qualifications
   - programming languages knowledge
   - chief
 #### Alternative sequence (employee is administrator):
 1. Administrator presses "Users" button
 2. System shows window with table of information about users:
   - name (has link to user's profile page)
   - e-mail
   - qualifications
   - programming languages knowledge
   - chief
   - "Edit" button
   - "Delete" button
3. System shows empty form for creating a new user with fields:
   - name
   - e-mail
   - qualifications
   - programming languages knowledge
   - chief
   - "Add" button

### Case: Tasks view

Subject: Employee

Goal: Provide employee with information about tasks

Preconditions: Employee presses "Tasks" button

#### Main sequence:
1. System shows window with tasks list, information about each task (name, deadline) and following widgets for each task:
   - "Complete" button, if no report is needed to complete the task
   - file loading widget and disabled "Complete" button, if report is neccessary for the task
   - "Split" button, if employee is a chief

### Case: Completing task

Subject: Employee

Goal: Let employees complete tasks

Preconditions: Employee is on "Tasks" page and has unfinished tasks

#### Main sequence:
1. Employee presses "Complete" button near a task
2. System moves the task to archive
#### Alternative sequence (report is required):
1. Employee presses file loading widget
2. System shows explorer window to choose file
3. Employee chooses task and presses "Complete" button
4. System moves the task to archive, renames the report file to task id and moves it to reports folder

### Case: Splitting task

Subject: Chief

Goal: Let chiefs split tasks between them and their subordinates

Preconditions: Chief is on "Tasks" page and has unfinished tasks

#### Main sequence:
1. Chief presses "Split" button near a task
2. System shows window with "Add subtask" button and disabled "Split" button
3. Chief presses "Add subtask" button
4. System adds empty fields "name", "qualifications", "language", "deadline", "report needed", "performer" to the window
5. Chief fills the fields
6. System makes "Split" button active
7. Steps 3-5 are repeated as much as the chief needs
8. Chief presses "Split" button
9. System deletes the task and adds subtasks to database
#### Alternative sequence (no subordinate has the required qualifications and/or language knowledge for subtask):
1. Chief presses "Split" button near a task
2. System shows window with "Add subtask" button and disabled "Split" button
3. Chief presses "Add subtask" button
4. System adds empty fields "name", "qualifications", "language", "deadline", "report needed", "performer" to the window
5. Chief fills the fields
6. System inserts chief in "performer" field
7. System makes "Split" button active
8. Steps 3-5 are repeated as much as the chief needs
9. Chief presses "Split" button
10. System deletes the task and adds subtasks to database

### Case: Adding employee

Subject: Administrator

Goal: Let administrator add new users

Preconditions: Administrator is on "Users" page

#### Main sequence:
1. Administrator fills the user creation fields and presses "Add" button
2. System creates new user in database
#### Alternative sequence (invalid input data):
1. Administrator fills the user creation fields and presses "Add" button
2. System notifies administrator about invalid input data

### Case: Editing employee

Subject: Administrator

Goal: Let administrator edit users

Preconditions: Administrator is on "Users" page

#### Main sequence:
1. Administrator presses "Edit" button next to user
2. System fills user creation fields with user data and changes "Add" button to "Save" button
3. Administrator fills the user creation fields and presses "Save" button
4. System edits user data
#### Alternative sequence (invalid input data):
1. Administrator presses "Edit" button next to user
2. System fills user creation fields with user data and changes "Add" button to "Save" button
3. Administrator fills the user creation fields and presses "Save" button
4. System notifies administrator about invalid input data

### Case: Removing employee

Subject: Administrator

Goal: Let administrator remove users

Preconditions: Administrator is on "Users" page

#### Main sequence:
1. Administrator presses "Remove" button next to user
2. System shows alert window with buttons "Confirm", "Cancel"
3. Administrator presses "Confirm" button
4. System removes user from database
#### Alternative sequence (cancelling operation):
1. Administrator presses "Remove" button next to user
2. System shows alert window with buttons "Confirm", "Cancel"
3. Administrator presses "Cancel" button
4. System closes the window with no changes to database
#### Alternative sequence (deleted user is a chief):
1. Administrator presses "Remove" button next to user
2. System shows alert window with buttons "Confirm", "Cancel"
3. Administrator presses "Confirm" button
4. System removes user from database, their subordinates become their chief's subordinates

## Classes diagram
![alt text](https://github.com/BAA7/django-ctm/blob/main/Diagrams/classes.png)
