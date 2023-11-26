# Tugas Besar TBFO IF2124
<p align="center">
    <h1 align="center">HTML Parser</h3>
</p>
This program is developed to to fulfill the Major Assignment of IF2124 Formal Language and Automata Theory course. Here we use Python programming languages to develop this program. This program is intended to:
Evaluate program syntax in HTML.

## Table of Contents
1. [General Information](#general-information)
2. [Author](#author)
3. [Technologies Used](#technologies-used)
4. [Features](#features)
5. [How To Run](#how-to-run)
   - [Prerequisites](#prerequisites)
   - [Clone the Repository](#clone-the-repository)
   - [Navigate to the Source (src) Directory](#navigate-to-the-source-src-directory)
   - [Run the main program](#run-the-main-program)
   - [Test Input](#test-input)
6. [Project Status](#project-status)
7. [Acknowledgements](#acknowledgements)



## General Information
In program development, parsing is a crucial stage where the syntax of the programming language is checked to ensure it complies with the language rules. This is done by programmers to confirm that the instructions adhere to the specified syntax of the programming language.

Whether in an interpreted or compiled language, syntax checking is a standard practice. The difference lies in the subsequent steps after the checking process. In a compiler, after parsing, the program is transformed into an executable form, whereas in an interpreter, syntax checking and execution occur directly without additional compilation steps.

## Author:
| NIM      | Nama                      | Tugas         |
| -------- | ------------------------- | ------------- |
| 13522015 | Yusuf Ardian Sandi        | Diagram state |
| 13522032 | Tazkia Nizami             | PDA           |
| 13522057 | Moh Fairuz Alauddin Yahya | Tokenizer     |

## Technologies Used
- Python 3.9.6

## Features
**HTML PDA Parser:**
   The HTML PDA (Pushdown Automaton) Parser is a crucial component of the project. It is designed to analyze and process HTML documents using a pushdown automaton model. This parser efficiently handles the hierarchical structure of HTML tags, ensuring accurate parsing and extraction of information from HTML files.

   - *Tag Recognition:* The parser recognizes and categorizes HTML tags, allowing for targeted extraction of specific elements within the document.

   - *Attribute Handling:* It efficiently handles attributes associated with HTML tags, enabling precise retrieval of attribute values.

   - *Nested Structure Support:* The parser is capable of navigating through nested HTML structures, ensuring comprehensive parsing of complex documents.

## How To Run

### Prerequisites
Before starting the development process, make sure you have the following software installed on your machine:

- [Python](https://www.python.org/) (3.6 or later)


### 1. Clone the Repository

```bash
git clone https://github.com/fairuzald/HTML-Parser
cd HTML-Parser
```

### 2. Navigate to the Source (src) Directory

```bash
cd src

```

### 3. Run the main program

```bash
python main.py
```

### Test Input

For all kinds of HTML test case inputs, please place them in the 'test' folder which is located at the same level as the 'src' folder.

## Project Status

Project is complete

## Acknowledgements

- Thanks To Allah SWT
- Many thanks to Dr. Judhi Santoso, M.Sc. for his guidance and support
