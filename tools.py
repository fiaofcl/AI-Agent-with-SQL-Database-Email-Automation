from langchain.tools import tool
import json
import mysql.connector
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

# DATABASE CONNECTIONS
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
def get_db_connection_log():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_LLM")
    )


# LOGGING FUNCTION
def log_interaction(
    user_query="",
    agent_response="",
    input_tokens=0,
    output_tokens=0,
    reasoning_tokens=0,
    model_name="",
    tool_name="",
    tool_call_id="",
    tool_query="",
    tool_message="",
    tool_status="",
    finish_reason="",
    raw_response=""
):

    connection = None
    cursor = None

    try:
        connection = get_db_connection_log()
        cursor = connection.cursor()

        total_tokens = input_tokens + output_tokens

        sql = """
        INSERT INTO log
        (
            user_query,
            agent_response,
            input_tokens,
            output_tokens,
            reasoning_tokens,
            total_tokens,
            model_name,
            tool_name,
            tool_call_id,
            tool_query,
            tool_status,
            tool_message,
            finish_reason,
            raw_response
        )
        VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        values = (
            user_query,
            agent_response,
            input_tokens,
            output_tokens,
            reasoning_tokens,
            total_tokens,
            model_name,
            tool_name,
            tool_call_id,
            tool_query,
            tool_status,
            tool_message,
            finish_reason,
            raw_response
        )
        cursor.execute(sql, values)
        connection.commit()

    except Exception as e:
        print("[LOGGING ERROR]:", e)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# SQL TOOL
@tool
def execute_sql(query: str) -> str:
    """
    Execute SQL queries on the employee table.
    Supports SELECT, INSERT and UPDATE.
    DELETE operations are not allowed.
    """

    connection = None
    cursor = None

    try:

        if query.strip().lower().startswith("delete"):
            return json.dumps(
                {
                    "status": "error",
                    "message": "DELETE operation is not allowed."
                },
                indent=4
            )

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(query)

        if cursor.description is not None:

            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()

            result = [
                dict(zip(columns, row))
                for row in rows
            ]

            response = {
                "status": "success",
                "type": "select",
                "data": result
            }

        else:

            connection.commit()

            response = {
                "status": "success",
                "type": "modify",
                "rows_affected": cursor.rowcount,
                "message": "Query executed successfully."
            }

        return json.dumps(
            response,
            indent=4,
            default=str
        )

    except Exception as e:

        return json.dumps(
            {
                "status": "error",
                "message": str(e)
            },
            indent=4
        )

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# EMAIL TOOL
@tool
def send_email(
    receiver: str,
    subject: str,
    body: str
) -> str:
    """
    Send an email.
    """

    server = None

    try:

        sender = os.getenv("EMAIL_ADDRESS")
        password = os.getenv("EMAIL_PASSWORD")

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = receiver

        server = smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465
        )

        server.login(sender, password)

        server.sendmail(
            sender,
            receiver,
            msg.as_string()
        )

        return f"Email successfully sent to {receiver}."

    except Exception as e:

        return f"Email sending failed: {str(e)}"

    finally:
        if server:
            server.quit()