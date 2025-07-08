# 1. Introduction

## 1.1. Purpose

The purpose of this document is to present a detailed description of the Corporate Task Manager. It will explain the purpose and features of the system,the interfaces of the system, what the system will do, the constraints under which it must operate and how the system will react to external stimuli.

This document is intended for anyone interested in this project.

## 1.2. Scope

The product to be produced – Corporate Task Manager (CTM) – must help the company to organize employees' work process by building and storing the employees hierarchy tree, where each employee (excluding administrator – root node) has one chief and any amount of subordinates. Main functions of the product are connected to "chief-subordinates" relation in that tree. The product is to be used for assigning and delegating work tasks between the employees and managing the inner structure of the company.

## 1.3. Definitions, acronyms, and abbreviations

| Term | Definition |
| --- | --- |
| Company | The hypothetical client company for which the product is developed |
| Product/System | CTM, the software under development |
| Task | An action required to be performed by the person to whom it is assigned |
| Subtask | A task created by splitting another task |
| Report | A document attached to a completed task if neccessary |
| Hierarchy tree/Tree | A tree-like data structure representing employees' relations |
| Data | Everything stored in system's database: users, qualifications, languages etc |
| Skills | A set of qualifications a user has and languages they know |

## 1.4. References

- IEEE Std 830-1998 Recommended Practice for Software Requirements Specifications

## 1.5. Overview

The following parts of this document contain more specific descriptions of product requirements.

Table of contents:
TODO

# 2. Overall description

## 2.1. Product perspective

The product is a pet project imagined as a custom solution for inner use by the company. It is independent and totally self-contained.

## 2.2. Product functions

User related functions:
* authorization in system;
* changing password;
* for administrators:
  * adding new employees;
  * editing employees' data;
  * editing the hierarchy tree (chief appointments and reappointments);
  * deleting employees.
Task related functions:
* for chiefs:
  * assignment of tasks with priorities and deadlines;
  * dividing an assigned task into subtasks between self and subordinates with suitable qualifications and skills;
* for employees:
  * completing a task and attaching a report to it if neccessary.
Data related functions:
* for administrators:
  * editing data.

## 2.3. User characteristics

The users of the product are the company's employees. All of them have a high level of computer literacy.

## 2.4. Constraints

* System must work properly on Edge, Chrome, Opera, Firefox and Safari browsers.

## 2.5. Assumptions and dependencies

The system will be deployed on a server with the Linux Ubuntu 20.04 operating system.

# 3. Specific requirements

## 3.1. External interface requirements

### 3.1.1. User interfaces

User interface is realized as a web interface, available through modern browsers (Chrome, Firefox, Safari, Edge).

### 3.1.2. Hardware interfaces

System doesn't require special hardware and works on a standard server. Interaction with hardware components is maintained through standard OS and browser means.

### 3.1.3. Software interfaces

Server:
* Python 3.10+
* Django 5.2.3
* Django REST Framework (DRF)
* SQLite3
Client:
* Web browser with JavaScript ES6+ support
* HTML5, CSS3

### 3.1.4. Communication interfaces

RESTful API is used for server-client communication.
* request/response format: JSON
* protocol: HTTPS
* methods: GET, POST, PUT, DELETE

## 3.2. Functional requirements

### 3.2.1. Unauthorized user

#### 3.2.1.1. Authentication

System must let unauthorized user perform an authentication using their e-mail and password

#### 3.2.1.2. Authorization

System must autorize unauthorized user after a successful authentication

#### 3.2.1.3. Page access

System must redirect unauthorized user from any product's page they visit to authentication page

### 3.2.2. Authorized user

#### 3.2.2.1. Users table

System must provide authorized user with information about all users:
* name (must have a hyperlink to the user's profile page)
* e-mail
* chief's name

#### 3.2.2.2. User profile

System must provide authorized user with detailed information about any specific user:
* name
* e-mail
* qualifications
* languages knowledge
* chief's name

#### 3.2.2.3. Password change

System must let authorized user change their password when they are on their profile page

#### 3.2.2.4. Logout

System must let authorized user end their authorization

#### 3.2.2.5. Tasks table

System must provide authorized user with list of tasks assigned to them:
* name
* deadline

#### 3.2.2.6. Report appending

System must let authorized user append a report to their task if neccessary

#### 3.2.2.7. Task completion

System must let authorized user mark a task assigned to them as completed if:
* report is appended to the task,

or
* report is not required for the task

### 3.2.3. Chief

#### 3.2.3.1. Tasks table

*(Appendix to 3.2.2.5)* System must provide chief with list of their subordinates' tasks:
* name
* deadline
* performer's name

#### 3.2.3.2. Task assigning

System must let chief create new tasks and assign them to themself or their subordinates with suitable skills

#### 3.2.3.2. Task split

System must let chief split a task assigned to them into subtasks distibuted between them and their subordinates with suitable skills

### 3.2.4. Administrator

#### 3.2.4.1. User creation

System must let administrator create new users

#### 3.2.4.2. User editing

System must let administrator edit existing users fields excluding passwords

#### 3.2.4.3. User removing

System must let administrator remove users from it

#### 3.2.4.4. Tasks table

*(Appendix to 3.2.3.1)* System must provide administrator with list of tasks not assigned to them or their subordinates

#### 3.2.4.5. Data tables

System must provide administrator with information about all qualifications and languages stored in database

#### 3.2.4.6. Data creation

System must let administrator create new qualifications and languages

#### 3.2.4.7. Data editing

System must let administrator edit existing qualifications and languages

#### 3.2.4.8. Data removing

System must let administrator remove existing qualifications and languages and perform cascade delete on all links pointing to that data

## 3.3. Performance requirements

| Operation | Maximal response time, ms |
| --- | --- |
| GET request | 300 |
| Authorization | 500 |
| POST request | 600 |
| PUT requiest | 400 |

## 3.4. Software system attributes

### 3.4.1. Reliability

The system must ensure the correct operation of all functions under normal load. The probability of failure during basic operations (e.g. authorization, reading data) should not exceed 0.1%.

### 3.4.2. Availability

The application must be available at least 99.9% of the time per month, except for cases of scheduled maintenance or external failures (e.g. DDoS attacks).

### 3.4.3. Security

- All data is transmitted via the secure HTTPS protocol.
- Passwords are stored in hashed form.
- Protection against XSS, CSRF, SQL Injection is implemented through Django mechanisms.
- Access to the API is protected by Token-based authentication.
- Security audit is conducted quarterly.

### 3.4.4. Maintainability

- Clean, documented code in accordance with PEP8.
- Test coverage should be at least 80%.
- Use of CI/CD to automate build and testing.

### 3.4.5. Usability

- The interface should be intuitive and meet modern UX standards.
- Minimum number of steps to complete key tasks.

# Appendix A: Glossary

# Appendix B: Analysis models

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

# Appendix C: Issues list
