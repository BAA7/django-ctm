# 1. Introduction

## 1.1. Purpose

The purpose of this document is to present a detailed description of the Corporate Task Manager. It will explain the purpose and features of the system, the interfaces of the system, what the system will do, the constraints under which it must operate and how the system will react to external stimuli.

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

2. Overall description
   
   2.1. Product perspective
   
   2.2. Product functions
   
   2.3. User characteristics
   
   2.4. Constraints
   
   2.5. Assumptions and dependencies
   
3. Specific requirements
   
   3.1. External interface requirements
   
   3.2. Functional requirements
   
   3.3. Performance requirements
   
   3.4. Software system attributes

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

