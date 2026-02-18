import sys

def analyze_terraform(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    risk_score = 0
    findings = []

    if "0.0.0.0/0" in content:
        risk_score += 40
        findings.append("Public exposure detected (0.0.0.0/0).")

    if 'instance_type = "t3.large"' in content:
        risk_score += 20
        findings.append("High-cost instance detected (t3.large).")

    if "encrypted = false" in content:
        risk_score += 30
        findings.append("Encryption disabled.")

    risk_score = min(risk_score, 100)
    return risk_score, findings


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python agents\\terraform_guardian.py <terraform_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    score, findings = analyze_terraform(file_path)

    print(f"\nRisk Score: {score}/100\n")

    if findings:
        print("Findings:")
        for f in findings:
            print(f"- {f}")
    else:
        print("No major risks detected.")
