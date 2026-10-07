#from modules.extractor import extract_project_information
from modules.assessment import assess_project
from modules.extractor import (
    extract_project_information,
    identify_missing_information
)

text = """
We are planning to establish a textile manufacturing
plant on 120 acres near a river.

The plant will consume approximately
2 million litres of water per day and generate
500000 litres of wastewater.

The project will employ 800 workers.

The plant will use chemical dyes and hazardous
materials and operate continuously.

A residential area is located approximately
2 km away.
"""


# Extract information
data = extract_project_information(text)

missing_information = identify_missing_information(data)
# Assess project
result = assess_project(data)


print("\n")
print("=" * 60)
print("PROJECT ENVIRONMENTAL ASSESSMENT")
print("=" * 60)


for factor, assessment in result["factors"].items():

    print(
        f"{factor:<25}"
        f"{assessment['level']:<12}"
        f"{assessment['score']}"
    )


print("\n")
print("Overall Environmental Risk Index:",
      result["overall_score"],
      "/ 100")

print(
    "Overall Risk Level:",
    result["overall_level"]
)


print("\n")
print("MAJOR CONCERNS")
print("-" * 40)

for concern in result["major_concerns"]:

    print("•", concern)


print("\n")
print("REQUIRED MITIGATION")
print("-" * 40)

for item in result["mitigation"]:

    print("•", item)

print("\n")
print("=" * 60)
print("DATA COMPLETENESS CHECK")
print("=" * 60)

if missing_information:
    print("\nMISSING / INCOMPLETE INFORMATION")
    print("-" * 40)

    for item in missing_information:
        print("⚠ " + item)

    print("\nAssessment Status:")
    print("PRELIMINARY — ADDITIONAL PROJECT DATA REQUIRED")

else:
    print("\n✓ Required project information is available.")
    print("\nAssessment Status:")
    print("READY FOR PRELIMINARY ASSESSMENT")