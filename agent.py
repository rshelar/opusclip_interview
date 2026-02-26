import json

from dotenv import load_dotenv
from openai import OpenAI

from tools import (
    LOAD_USER_PROFILES_TOOL,
    READ_USER_INPUT_TOOL,
    SAVE_TRAVEL_PLAN_TOOL,
    load_user_profiles,
    read_user_input,
    save_travel_plan,
)

load_dotenv()
client = OpenAI()

SYSTEM_PROMPT = """You are a friendly and knowledgeable travel assistant.

Follow these steps in order:
1. Call load_user_profiles to retrieve all available user profiles.
2. Use read_user_input to present the profiles to the user and ask which one to use.
3. Engage in a natural multi-turn conversation using read_user_input to help the
   user brainstorm travel ideas based on their profile. Ask follow-up questions
   to refine destination, activities, accommodation, and timing.
4. When the user says they are ready for a final travel plan, generate and save it.

Important: always use read_user_input to communicate with the user.
Do not emit standalone assistant messages."""

TOOLS = [READ_USER_INPUT_TOOL, LOAD_USER_PROFILES_TOOL, SAVE_TRAVEL_PLAN_TOOL]

TOOL_DISPATCH = {
    "read_user_input": read_user_input,
    "load_user_profiles": load_user_profiles,
    "save_travel_plan": save_travel_plan,
}


def _dispatch(tool_name: str, arguments: str) -> str:
    args = json.loads(arguments)
    fn = TOOL_DISPATCH.get(tool_name)
    if fn is None:
        return json.dumps({"error": f"Unknown tool: {tool_name}"})
    return str(fn(**args))


def run():
    # Seed the conversation with only the system prompt.
    # The LLM drives everything from here via tool calls.
    response = client.responses.create(
        model="gpt-4.1",
        input=[{"role": "system", "content": SYSTEM_PROMPT}],
        tools=TOOLS,
    )

    while True:
        tool_calls = [item for item in response.output if item.type == "function_call"]

        # No tool calls means the LLM finished the conversation
        if not tool_calls:
            for item in response.output:
                if item.type == "message":
                    for block in item.content:
                        if hasattr(block, "text"):
                            print(f"\nAssistant: {block.text}")
            break

        # Execute every tool the LLM requested and collect results
        tool_results = []
        plan_saved = False
        for tc in tool_calls:
            result = _dispatch(tc.name, tc.arguments)
            tool_results.append(
                {"type": "function_call_output", "call_id": tc.call_id, "output": result}
            )
            if tc.name == "save_travel_plan":
                print(f"\n{result}")
                plan_saved = True

        if plan_saved:
            break

        # Feed results back; previous_response_id keeps the full history server-side
        response = client.responses.create(
            model="gpt-4.1",
            previous_response_id=response.id,
            input=tool_results,
            tools=TOOLS,
        )


if __name__ == "__main__":
    run()