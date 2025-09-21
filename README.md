# Librus Module

The Librus module is a Python-based tool designed for interacting with the Librus educational platform's API. It facilitates operations such as logging in to the platform, retrieving student information, grades, and managing subject data.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [Documentation](#documentation)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Contributors](#contributors)
- [License](#license)

## Introduction

The Librus module automates the process of fetching data from the Librus platform, which is often used by educational institutions in Poland. It can be utilized by developers to integrate Librus data with other applications, perform data analysis, or enhance the educational experience through custom apps.

## Installation

To install the Librus module, you need Python installed on your system. Python 3.6 or later is recommended. You can install the module using the following pip command:

```bash
pip install -r requirements.txt
```
## Usage
To use the Librus module, import it into your Python script. Here’s how to initialize a session and log in:

```python
from main import Librus

session = Librus()
session.login('your_username', 'your_password')
```

## Features
- **Login**: Authenticates users against the Librus API.
- **Fetch Student Information**: Retrieves detailed information about students, such as name, class, and educator.
- **Fetch Grades**: Gathers detailed grade information from the student's records.
- **Teacher and Subject Management**: Allows retrieval of all teachers and subjects associated with the student.
- **Event Management**: Retrieves events and exams from the student's calendar.

## Dependencies

- **Python 3.6+**: The minimum Python version required.
- **requests**: A library for making HTTP requests in Python.
- **beautifulsoup4**: A library for parsing HTML and XML documents.


## Configuration

No additional configuration is needed outside of the initial setup and login credentials.

## Documentation

The module functions are well-documented within the code. Each method includes docstrings that describe its purpose, parameters, and return type.

## Examples

Retrieving student information:

```python 
student_info = session.get_student_info()
print(student_info)
```

Retrieving every teachers fullname:

```python
teachers = session.get_teachers()
print(teachers)
```

Retrieving all the students subjects

```python 
subjects = session.get_subjects()
print(subjects)
```

Retrieving every subject's final grade:

```python
grades = session.get_final_grades()
print(grades)
```

Retrieving the grades for a specific subject:

```python
math_grades = session.get_grades_for_specific_subject('Matematyka')
print(math_grades)
```

Retrieving the all the events for this month

```python 
events = session.get_events()
print(events)
```

Retrieving the events for today

```python
events_for_today = session.get_today_events()
print(events_for_today)
```

Checking if theres an exam today

```python 
exam = session.is_there_a_test_today()
if exam:
    print("There is an exam today")
else:
    print("There is no exam today")
```

## Troubleshooting
If you encounter issues with logging in or fetching data, ensure that your credentials are correct and that you have internet access. For HTTP or connection errors, verify that the Librus API is accessible.

## Contributors

- **Valentin Bańobre Kalinowski** - Initial Creator and Maintainer

## License
This project is licensed under the MIT License - see the LICENSE file for details.

