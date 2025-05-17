# HR Documents Processor

An application that helps automate the process of filling out document templates. The application takes a .docx template file and replaces placeholders with provided data.

## Features

- Process .docx template files
- Replace placeholders ($1, $2, etc.) with user-provided data
- Support for multiple admin notifications
- Rate limiting to prevent abuse
- Easy-to-use interface

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file with the following variables:
   ```
   TOKEN=your_api_token
   ADMIN=["admin_id"]
   ```

## Usage

1. Start the application:
   ```bash
   python run.py
   ```
2. Using the application:
   - Upload your .docx template with placeholders ($1, $2, etc.)
   - Provide the data as comma-separated values
   - Receive the processed document

## Template Format

Create your .docx templates with numbered placeholders:
- Use $1, $2, $3, etc. for where you want the data to be inserted
- Example: "Dear $1, your position will be $2 with a salary of $3"

## Technical Details

- Built with Python 3.11+
- Uses in-memory storage for state management
- Includes rate limiting (2 requests per second limit)
- Supports admin notifications for application status 