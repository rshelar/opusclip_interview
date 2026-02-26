# Problem Statement
In this exercise we have to design and implement a multi-turn conversational travel 
assistant using OpenAI with Function/Tool Calling. The assistant should:

1) Hold multi-round conversations with users.
2) Load user profiles from provided files.
3) Generate travel plans based on the profiles and save the results to a file.

User profiles are defined in user_profiles.txt file in this directory.

## Build Travel Assistant
We have to build an agent that will execute following steps:
1. Feed user profiles to the LLM and have the LLM learn about user's preferences for travel plans.
2. Build a multi turn conversation loop with the LLM where the user can brainstorm ideas about the travel plans with the LLM
3. Final stage is the user will tell the LLM to produce a final travel plan based on the user's profile and the conversation with the LLM.

## Constraints
1. Use structured JSON outputs for all LLM role calls.
2. Enforce schema validation for deterministic behavior.

## Architecture:

User -> Agent -> LLM call

User will be interacting with the agent through command line input.
Agent is the orchestration later that supports the steps mentioned above.
LLM call is the OpenAI's call.


## Flow

Agent starts → hands control to LLM with tools available
↓
LLM calls load_user_profiles() → gets all profiles
LLM calls read_user_input("Which profile?") → user picks one
LLM calls read_user_input("What are your travel ideas?") → brainstorm
LLM calls read_user_input(...) → continues conversation freely
↓ (user indicates they want a final plan)
LLM generates structured plan → calls save_travel_plan(plan, "output.json")
Agent exits

