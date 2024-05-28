# Statement Parser

This project extracts and processes bank statements using OCR and various Python libraries, to give a useable dataframe. The Pandas dataframe can then be used for expenditure analysis and tracking data.

Currently, this parser works only for HDFC Bank and Kotak Mahindra Bank statements.

## Installation

### Prerequisites

Before you can run this project, you need to install some system dependencies and Python libraries.

#### For Linux (Ubuntu)

1. **Update the package list**:

    ```sh
    sudo apt-get update
    ```

2. **Install Poppler-utils**:

    ```sh
    sudo apt-get install -y poppler-utils
    ```

3. **Install Tesseract-OCR**:

    ```sh
    sudo apt-get install -y tesseract-ocr
    ```

4. **Install the required Python libraries**:

    ```sh
    pip install -r requirements.txt
    ```

#### For Windows

1. **Install Poppler**:

    - Download Poppler for Windows from [http://blog.alivate.com.au/poppler-windows/](http://blog.alivate.com.au/poppler-windows/).
    - Extract the downloaded zip file and add the `bin` folder to your system PATH.

2. **Install Tesseract-OCR**:

    - Download the Tesseract installer from [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki).
    - Run the installer and add Tesseract to your system PATH.

3. **Install the required Python libraries**:

    ```sh
    pip install -r requirements.txt
    ```

### Setting Tesseract Path in Python

In your Python script, you might need to set the path to the Tesseract executable if it's not in your system PATH.

```python
import pytesseract

# Example for Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Example for Linux (if not in default path)
# pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract
```

## Usage

Replace the filePath variable with the path of the bank statement to be processed.

```python
filePath = "samples/Statement April-Aug 2021.pdf"
```

To get output use the following command.
```python
python3 main.py
```

Thank You!
