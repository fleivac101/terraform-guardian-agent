import os
import sys
import json
from dotenv import load_dotenv

load_dotenv()

def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def analyze_with_openai(tf_content: str) -> dict:
    from openai import OpenAI

    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not found. Add it to your .env file.")

    client = OpenAI(api_key=api_key)

    system = (
        "You are a Terraform security/governance reviewer. "
        "Analyze Terraform code for security, cost, and governance risks. "
        "Return ONLY valid JSON following the schema exactly."
    )

    schema = {
        "risk_score": "integer 0-100",
        "summary": "string (1-2 lines)",
        "findings": [
            {"title": "string", "severity": "LOW|MEDIUM|HIGH|CRITICAL", "evidence": "string"}
        ],
        "recommendations": [
            {"action": "string", "priority": "P1|P2|P3"}
        ]
    }

    user = f"""
Terraform code:
```hcl
{tf_content}
