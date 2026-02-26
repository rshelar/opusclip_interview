from openai import OpenAI
from dotenv import load_dotenv
from schemas.summary import SummaryOutput

load_dotenv()
client = OpenAI()

topic = "US Economy"

response = client.responses.create(
    model="gpt-4.1",
    input=[
        {
            "role": "system",
            "content": (
                "You are a research assistant. Summarize the given topic and exactly 3 points."
            ),
        },
        {
            "role": "user",
            "content": f"Topic: {topic}",
        },
    ],
    text={
        "format": {
            "type": "json_schema",
            "name": "insights_output",
            "schema": {**SummaryOutput.model_json_schema(), "additionalProperties": False},
            "strict": True,
        }
    },
)

summary = SummaryOutput.model_validate_json(response.output[0].content[0].text)
for point in summary.bullet_points:
    print(point)

