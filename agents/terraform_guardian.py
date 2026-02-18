import os
import sys
import json
from dotenv import load_dotenv

load_dotenv()


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def mock_analysis(tf_content):
    """
    Simulated AI response when API is unavailable
    """
    risk_score = 0
    findings = []

    if "0.0.0.0/0" in tf_content:
        risk_score += 40
        findings.append({
            "title": "Public exposure detected",
            "severity": "HIGH",
            "evidence": "Security group allows 0.0.0.0/0"
        })

    if "instance_type" in tf_content:
        risk_score += 20
        findings.append({
            "title": "Potential cost optimization issue",
            "severity": "MEDIUM",
            "evidence": "Instance type detected"
        })

    if risk_score == 0:
        findings.append({
            "title": "No major risks detected",
            "severity": "LOW",
            "evidence": "Basic scan clean"
        })

    return {
        "risk_score": min(risk_score, 100),
        "summary": "Mock analysis mode (AI disabled).",
        "findings": findings,
        "recommendations": [
            {"action": "Review network exposure rules", "priority": "P1"},
            {"action": "Validate cost configuration", "priority": "P2"}
        ]
    }


def analyze_with_openai(tf_content):
    try:
        from openai import OpenAI

        api_key = os.getenv("OPENAI_API_KEY")
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        if not api_key:
            raise Exception("No API key")

        client = OpenAI(api_key=api_key)

        system_prompt = "Analyze Terraform code and return JSON."

        user_prompt = "Terraform code:\n" + tf_content

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,
        )

        content = response.choices[0].message.content.strip()
        return json.loads(content)

    except Exception:
        print("\n⚠ Running in MOCK mode (API unavailable)")
        return mock_analysis(tf_content)


def print_report(result):
    print("\nRisk Score:", result.get("risk_score"))
    print("Summary:", result.get("summary"))

    print("\nFindings:")
    for f in result.get("findings", []):
        print("-", f["severity"], "-", f["title"])
        print("  Evidence:", f["evidence"])

    print("\nRecommendations:")
    for r in result.get("recommendations", []):
        print("-", r["priority"], ":", r["action"])


def main():
    if len(sys.argv) != 2:
        print("Usage: python agents\\terraform_guardian.py <terraform_file>")
        sys.exit(1)

    tf_content = read_file(sys.argv[1])
    result = analyze_with_openai(tf_content)
    print_report(result)


if __name__ == "__main__":
    main()
