# ExamBuilder

A Python tool to automate creation of multiple-choice questions on [exam.net](https://exam.net) via Playwright and Chrome’s remote-debugging protocol.

## Features

- **Modular design**  
  - `browser_manager.py` manages Chrome launch/connection  
  - `json_loader.py` loads & validates your questions JSON  
  - `question_form.py` handles all UI interactions (create, fill, mark, save)  
  - `automator.py` orchestrates the end-to-end flow  
  - `main.py` is the simple CLI entry point  

- **Flexible JSON**  
  Supports single or multiple correct answers per question.

- **Robust error handling**  
  Validates JSON structure, prompts on missing files, logs any selector mismatches.

## Prerequisites

- Python 3.8+  
- [Playwright](https://playwright.dev/python/)  
- Google Chrome

## Installation

```bash
# Clone your fork
git clone https://github.com/MrHoran8120/ExamBuilder.git
cd ExamBuilder

# Install Playwright and browsers
pip install playwright
playwright install
