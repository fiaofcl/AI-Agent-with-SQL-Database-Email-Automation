from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import os
import json

from tools import (
    execute_sql,
    send_email,
    log_interaction
)

load_dotenv()

# =====================================================
# LLM
# =====================================================

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY")
)

# =====================================================
# AGENT
# =====================================================

agent = create_react_agent(
    model=llm,
    tools=[
        execute_sql,
        send_email
    ]
)

print("\n========== AI Personal Agent ==========")
print("Type 'exit' or 'quit' to stop.\n")

messages = []

while True:

    user_input = input("You: ")

    if user_input.lower() in [
        "exit",
        "quit"
    ]:
        print("Goodbye!")
        break

    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    response = agent.invoke(
        {
            "messages": messages
        }
    )

    assistant_reply = response["messages"][-1].content

    # ==========================================
    # EXTRACTION
    # ==========================================

    input_tokens = 0
    output_tokens = 0
    reasoning_tokens = 0

    model_name = ""
    tool_name = ""
    tool_call_id = ""
    tool_query = ""
    tool_message = ""
    tool_status = ""
    finish_reason = ""

    raw_response = json.dumps(
        response,
        default=str,
        indent=4
    )

    for msg in response["messages"]:

        # -----------------------------
        # TOKEN INFO
        # -----------------------------

        if (
            hasattr(msg, "usage_metadata")
            and msg.usage_metadata
        ):

            input_tokens += msg.usage_metadata.get(
                "input_tokens",
                0
            )

            output_tokens += msg.usage_metadata.get(
                "output_tokens",
                0
            )

            reasoning_tokens += (
                msg.usage_metadata
                .get(
                    "output_token_details",
                    {}
                )
                .get(
                    "reasoning",
                    0
                )
            )

        # -----------------------------
        # MODEL METADATA
        # -----------------------------

        if (
            hasattr(msg, "response_metadata")
            and msg.response_metadata
        ):

            model_name = msg.response_metadata.get(
                "model_name",
                model_name
            )

            finish_reason = msg.response_metadata.get(
                "finish_reason",
                finish_reason
            )

        # -----------------------------
        # TOOL CALL
        # -----------------------------

        if (
            hasattr(msg, "tool_calls")
            and msg.tool_calls
        ):

            tool = msg.tool_calls[0]

            tool_name = tool.get(
                "name",
                tool_name
            )

            tool_call_id = tool.get(
                "id",
                tool_call_id
            )

            tool_query = json.dumps(
                tool.get(
                    "args",
                    {}
                ),
                indent=4
            )

        # -----------------------------
        # TOOL RESULT
        # -----------------------------

        if (
            msg.__class__.__name__
            == "ToolMessage"
        ):

            tool_message = msg.content

            try:

                tool_json = json.loads(
                    tool_message
                )

                tool_status = tool_json.get(
                    "status",
                    ""
                )

            except:
                tool_status = "unknown"

    # ==========================================
    # SAVE LOG
    # ==========================================

    log_interaction(
        user_query=user_input,
        agent_response=assistant_reply,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        reasoning_tokens=reasoning_tokens,
        model_name=model_name,
        tool_name=tool_name,
        tool_call_id=tool_call_id,
        tool_query=tool_query,
        tool_message=tool_message,
        tool_status=tool_status,
        finish_reason=finish_reason,
        raw_response=raw_response
    )

    messages.append(
        {
            "role": "assistant",
            "content": assistant_reply
        }
    )

    print("\nAgent:", assistant_reply)
    print()

    # Uncomment for debugging:
    # print("\n========== DEBUG ==========")
    # print("Input Tokens     :", input_tokens)
    # print("Output Tokens    :", output_tokens)
    # print("Reasoning Tokens :", reasoning_tokens)
    # print("Model Name       :", model_name)
    # print("Tool Name        :", tool_name)
    # print("Tool Call ID     :", tool_call_id)
    # print("Tool Query       :", tool_query)
    # print("Tool Status      :", tool_status)
    # print("Finish Reason    :", finish_reason)
    # print("===========================\n")