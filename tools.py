import json
from pathlib import Path

from schemas.profile import UserProfile
from schemas.travel_plan import TravelPlan

# ---------------------------------------------------------------------------
# Tool definitions (passed to OpenAI)
# ---------------------------------------------------------------------------

READ_USER_INPUT_TOOL = {
    "type": "function",
    "name": "read_user_input",
    "description": (
        "Display a message to the user and wait for their response. "
        "Use this for every question, prompt, or message you want to show the user. "
        "Returns the user's typed input as a string."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "prompt": {
                "type": "string",
                "description": "The message or question to display to the user.",
            }
        },
        "required": ["prompt"],
        "additionalProperties": False,
    },
}

LOAD_USER_PROFILES_TOOL = {
    "type": "function",
    "name": "load_user_profiles",
    "description": (
        "Load all user profiles from a data source. "
        "Returns a list of profiles containing each user's name, location, "
        "travel preferences, budget, and available time."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "source": {
                "type": "string",
                "description": "Data source to read profiles from.",
                "enum": ["file", "database"],
            }
        },
        "required": [],
        "additionalProperties": False,
    },
}

SAVE_TRAVEL_PLAN_TOOL = {
    "type": "function",
    "name": "save_travel_plan",
    "description": (
        "Validate and save the final travel plan to a destination. "
        "Call this only when the user has confirmed they are ready for their final plan."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "user_name":        {"type": "string", "description": "Name of the user this plan is for."},
            "destination":      {"type": "string", "description": "Travel destination."},
            "activities":       {"type": "array", "items": {"type": "string"}, "description": "List of recommended activities."},
            "accommodation":    {"type": "string", "description": "Lodging recommendation."},
            "transportation":   {"type": "string", "description": "How the user will get there and get around."},
            "estimated_budget": {"type": "string", "description": "Total estimated cost."},
            "travel_dates":     {"type": "string", "description": "Suggested travel dates or timeframe."},
            "notes":            {"type": "string", "description": "Personalised tips based on the user profile."},
            "output":           {"type": "string", "description": "Output destination: 'file' or 'database'."},
        },
        "required": [
            "user_name", "destination", "activities",
            "accommodation", "transportation", "estimated_budget",
        ],
        "additionalProperties": False,
    },
}

# ---------------------------------------------------------------------------
# Tool implementations
# ---------------------------------------------------------------------------

USER_PROFILES_FILE = Path(__file__).parent / "user_profiles.txt"


def _parse_profile_block(block: str) -> UserProfile:
    fields: dict[str, str] = {}
    for line in block.strip().splitlines():
        if ": " in line:
            key, _, value = line.partition(": ")
            fields[key.strip()] = value.strip()
    return UserProfile(
        name=fields["Name"],
        current_location=fields["Current Location"],
        preferences=fields["Prefer"],
        budget=fields.get("Budget"),
        available_time=fields.get("Available Time"),
    )


def read_user_input(prompt: str) -> str:
    """Display a prompt and return the user's input."""
    print(f"\nAssistant: {prompt}")
    return input("You: ").strip()


def save_travel_plan(
    user_name: str,
    destination: str,
    activities: list[str],
    accommodation: str,
    transportation: str,
    estimated_budget: str,
    travel_dates: str | None = None,
    notes: str | None = None,
    output: str = "file",
) -> str:
    """Validate and persist the final travel plan. Returns a confirmation message."""
    if output == "database":
        raise NotImplementedError("Database output not yet implemented")

    plan = TravelPlan(
        user_name=user_name,
        destination=destination,
        activities=activities,
        accommodation=accommodation,
        transportation=transportation,
        estimated_budget=estimated_budget,
        travel_dates=travel_dates,
        notes=notes,
    )

    filename = f"travel_plan_{user_name.lower()}.json"
    output_path = Path(__file__).parent / filename
    output_path.write_text(plan.model_dump_json(indent=2))
    return f"Travel plan saved to {filename}"


def load_user_profiles(source: str = "file") -> str:
    """Load user profiles and return them as a JSON string."""
    if source == "database":
        raise NotImplementedError("Database source not yet implemented")

    raw = USER_PROFILES_FILE.read_text()
    blocks = [b for b in raw.strip().split("\n\n") if b.strip()]
    profiles = [_parse_profile_block(b) for b in blocks]
    return json.dumps([p.model_dump() for p in profiles], indent=2)