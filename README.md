## AI Personal Agent built using:
* LangChain
* LangGraph
* Groq LLM
* MySQL
* Python

The agent can:
* Execute SQL queries on a database
* Send emails automatically
* Maintain conversation memory
* Log all interactions
* Track token usage
* Track reasoning tokens
* Track tool calls
* Track tool outputs
* Store execution metadata in MySQL

---

# Features

## SQL Agent
The agent can:
* SELECT data
* INSERT data
* UPDATE data
The agent is instructed not to perform DELETE operations.

Example:
User:
Show all employees
Generated SQL:
SELECT * FROM emp;

---

## Email Agent
The agent can send emails using Gmail SMTP.
Example:
User:Send an email to [example@gmail.com](mailto:example@gmail.com) saying hello
Tool Used:send_email

---

## Conversation Memory

Conversation history is maintained during runtime.
Previous messages are passed back to the model so it can remember context within the session.

---

## Logging System

Every interaction is stored in MySQL.
Stored information:
* User query
* Agent response
* Input tokens
* Output tokens
* Reasoning tokens
* Total tokens
* Model name
* Tool name
* Tool call ID
* Tool query
* Tool status
* Tool message
* Timestamp

---

# Project Structure

mainllmagent/

├── main.py

├── tools.py

├── .env

├── requirements.txt

└── README.md

---

# Environment Variables
Create a file named: .env

Add:
DB_HOST=localhost 

DB_USER=your_mysql_username

DB_PASSWORD=your_mysql_password

DB_NAME=your_database_name

DB_LLM=your_logging_database_name

EMAIL_ADDRESS=[your_email@gmail.com](mailto:your_email@gmail.com)

EMAIL_PASSWORD=your_gmail_app_password

GROQ_API_KEY=your_groq_api_key

---

# Gmail App Password Setup

The email tool uses Gmail SMTP authentication.
Google no longer allows normal account passwords for SMTP access.
You must create an App Password.

Step 1: Enable 2-Step Verification

1. Open:
https://myaccount.google.com/security

2. Under **Signing in to Google**
Click: 2-Step Verification

3. Complete the setup process.


Step 2: Create an App Password

1. Open:
https://myaccount.google.com/apppasswords

2. Sign in to your Google account.

3. Under:
Select App
Choose:Mail

4. Under:
Select Device

Choose:Other (Custom Name)

Example:AI Personal Agent

5. Click:Generate

##Google will generate a 16-character password.

Example:abcd efgh ijkl mnop



Step 3: Store Credentials in .env

Add:
EMAIL_ADDRESS=[your_email@gmail.com](mailto:your_email@gmail.com)
EMAIL_PASSWORD=abcdefghijklmnop

Important:
* Remove spaces from the generated password.
* Do NOT use your normal Gmail password.
* Use only the generated App Password.

Example:
EMAIL_ADDRESS=[john@gmail.com](mailto:john@gmail.com)
EMAIL_PASSWORD=abcdefghijklmnop


Step 4: Test Email Functionality

Run the project and enter:
Send an email to [example@gmail.com](mailto:example@gmail.com) saying hello
If configured correctly, the email should be delivered successfully.

---

## Common Errors

### Authentication Failed

Error:
535 Username and Password not accepted

Fix:

* Ensure 2-Step Verification is enabled.
* Generate a fresh App Password.
* Verify EMAIL_ADDRESS and EMAIL_PASSWORD inside .env.

---

### Less Secure Apps Error

Google no longer supports Less Secure Apps.Use App Passwords instead.

---

### Connection Refused

Verify:
SMTP Server:smtp.gmail.com
Port:465

Code:server = smtplib.SMTP_SSL("smtp.gmail.com", 465)

---

## Security Notes

Never upload the following to GitHub:
* .env
* Gmail App Password
* Groq API Key
* Database Passwords

Create a .gitignore file:
.env
venv/
**pycache**/
*.pyc
.idea/
.vscode/

---

# MySQL Database Setup

## Employee Table

Run:

CREATE TABLE emp (
emp_id INT PRIMARY KEY,
emp_name VARCHAR(100)
);


## Log Table

Run:
CREATE TABLE log (
id INT AUTO_INCREMENT PRIMARY KEY,

```
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

user_query TEXT,

agent_response LONGTEXT,

input_tokens INT,

output_tokens INT,

reasoning_tokens INT,

total_tokens INT,

model_name VARCHAR(100),

tool_name VARCHAR(100),

tool_call_id VARCHAR(255),

tool_query LONGTEXT,

tool_status VARCHAR(50),

tool_message LONGTEXT,

finish_reason VARCHAR(100)
```

);

---

# Installation

Create virtual environment:python3 -m venv venv
Activate:

Mac/Linux:source venv/bin/activate
Windows:venv\Scripts\activate

---

Install packages:

pip install langchain

pip install langgraph

pip install langchain-groq

pip install python-dotenv

pip install mysql-connector-python

---

Or install everything using:
pip install -r requirements.txt

---

# Running the Project

Start the agent:python3 main.py

Example:

You: add employee id 1 name John
Agent: Employee added successfully.

---

# Logged Metadata

For every request the system records:

## User Information

* User Query
* Timestamp

## Model Information

* Model Name
* Finish Reason

## Token Information

* Input Tokens
* Output Tokens
* Reasoning Tokens
* Total Tokens

## Tool Information

* Tool Name
* Tool Call ID
* Tool Query
* Tool Status
* Tool Response

---

# Example Log Entry

id: 3
created_at: 2026-06-17 10:42:08
user_query:send an email to [abc@gmail.com](mailto:abc@gmail.com) saying hello
agent_response:The email has been sent successfully.
input_tokens:506
output_tokens:89
reasoning_tokens:17
total_tokens:595
model_name:openai/gpt-oss-120b
tool_name:send_email
tool_call_id:fc_d3476495-65b8-411f-b174-9170a74e0ced
tool_query:
{
"receiver":"[abc@gmail.com](mailto:abc@gmail.com)",
"subject":"Hello",
"body":"Hello"
}
tool_status:success
tool_message:Email successfully sent.
finish_reason:stop

---

# Future Improvements

* Multi-table database support
* Role-based SQL permissions
* Agent analytics dashboard
* Tool usage statistics
* Streamlit frontend
* Authentication layer
* Vector database memory
* Multi-agent workflows

---

# Technologies Used

* Python
* LangChain
* LangGraph
* Groq
* MySQL
* SMTP
* dotenv

---

# License

Educational and Learning Purpose Project.
