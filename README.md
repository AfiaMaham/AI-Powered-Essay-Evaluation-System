#  AI-Powered Essay Evaluation System

An intelligent essay assessment tool built using **Natural Language Processing (NLP)**, designed to analyze and score essays based on structure, grammar, spelling, vocabulary richness, content relevance, and readability. Includes a user-friendly GUI developed with **CustomTkinter**, supports secure user login via **SQLite**, and allows detailed report generation in **PDF** format.

---

##  Features

-  **Login & Registration System**
  - Secure user login and registration using SQLite database
  - Username uniqueness check and strong password validation

-  **Essay Upload & Topic Input**
  - Accepts `.txt` essay file and custom topic input via GUI
  - User-friendly interface for seamless interaction

-  **Automated Essay Evaluation**
  - **Structure Detection**: Intro, body, conclusion, transition words
  - **Content Relevance**: Keyword overlap and semantic similarity with the topic
  - **Vocabulary Analysis**: Identifies basic vs. advanced words from word frequency file
  - **Grammar & Spelling**: Detected using [LanguageTool](https://languagetool.org/)
  - **Readability**: Scores based on Flesch Reading Ease and Grade Level

-  **Scoring System**
  - Individual scores for each component (out of 5 or 10)
  - Aggregated final score out of 100

-  **PDF Report Download**
  - One-click download of a detailed evaluation report in PDF format

---

##  Tech Stack

| Component              | Library/Tool              |
|------------------------|---------------------------|
| GUI                    | `CustomTkinter`, `tkinter`|
| NLP Processing         | `spaCy` (`en_core_web_sm`)|
| Spelling & Grammar     | `language_tool_python`    |
| Readability Scoring    | `textstat`                |
| Stopword Filtering     | `spaCy.STOP_WORDS`        |
| Unicode Normalization  | `unicodedata`             |
| Regex Text Cleaning    | `re` (built-in)           |
| Word Frequency Matching| `en_50k.txt` (custom list)|
| Database               | `SQLite` (`sqlite3`)      |
| PDF Generation         | `fpdf` or `reportlab` *(your choice)* |

---

##  How to Run

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/essay-evaluator.git
   cd essay-evaluator
