from typing import Dict, Any


# ============================================================
# CLASSIFICATION
# ============================================================

def classify(score):

    if score < 25:
        return "LOW"

    elif score < 50:
        return "MODERATE"

    elif score < 75:
        return "HIGH"

    else:
        return "CRITICAL"


# ============================================================
# SAFE NUMBER
# ============================================================

def number(value, default=0):

    if value is None:
        return default

    try:
        return float(value)

    except (ValueError, TypeError):
        return default


# ============================================================
# AIR QUALITY
# ============================================================

def assess_air_quality(data):

    score = 20

    reasons = []

    # Explicit emissions
    if data.get("has_emissions"):

        score += 35

        reasons.append(
            "Project description indicates atmospheric emissions."
        )

    # Industrial activity
    if data.get("project_type") in [

        "Chemical / Chemical Manufacturing",
        "Cement Manufacturing",
        "Mining Project",
        "Power Generation Project",
        "Industrial Project"

    ]:

        score += 20

        reasons.append(
            "Project type has potential for significant air emissions."
        )

    # Population exposure
    if data.get("has_population"):

        score += 15

        reasons.append(
            "Nearby population may be exposed to project emissions."
        )

    return min(score, 100), reasons


# ============================================================
# WATER RESOURCES
# ============================================================

def assess_water(data):

    score = 15

    reasons = []

    water = number(
        data.get("water_consumption")
    )

    # Water consumption
    if water > 1:

        score += 25

        reasons.append(
            "High freshwater requirement."
        )

    elif water > 0.5:

        score += 15

        reasons.append(
            "Significant freshwater requirement."
        )

    # Effluent
    if data.get("has_effluent"):

        score += 25

        reasons.append(
            "Project generates wastewater/effluent."
        )

    # River proximity
    river_distance = data.get(
        "river_distance"
    )

    if river_distance is not None:

        river_distance = number(
            river_distance
        )

        if river_distance < 1:

            score += 30

            reasons.append(
                "Project is located very close to a water body."
            )

        elif river_distance < 5:

            score += 20

            reasons.append(
                "Project is located within potential influence "
                "distance of a water body."
            )

    return min(score, 100), reasons


# ============================================================
# SOIL
# ============================================================

def assess_soil(data):

    score = 20

    reasons = []

    land = number(
        data.get("land_area")
    )

    if land > 100:

        score += 25

        reasons.append(
            "Large land requirement may increase land disturbance."
        )

    elif land > 50:

        score += 15

        reasons.append(
            "Moderate land disturbance is expected."
        )

    if data.get("hazardous_material"):

        score += 30

        reasons.append(
            "Hazardous materials may create soil contamination risk."
        )

    if data.get("has_effluent"):

        score += 10

        reasons.append(
            "Improper wastewater handling could affect soil quality."
        )

    return min(score, 100), reasons


# ============================================================
# NOISE
# ============================================================

def assess_noise(data):

    score = 15

    reasons = []

    project_type = data.get(
        "project_type",
        ""
    )

    industrial_projects = [

        "Textile Manufacturing",
        "Chemical / Chemical Manufacturing",
        "Cement Manufacturing",
        "Mining Project",
        "Power Generation Project",
        "Industrial Project"

    ]

    if project_type in industrial_projects:

        score += 30

        reasons.append(
            "Industrial machinery and continuous operation "
            "may generate significant noise."
        )

    if data.get("has_population"):

        score += 20

        reasons.append(
            "Nearby population may experience noise exposure."
        )

    return min(score, 100), reasons


# ============================================================
# ECOLOGY
# ============================================================

def assess_ecology(data):

    score = 15

    reasons = []

    land = number(
        data.get("land_area")
    )

    if land > 100:

        score += 25

        reasons.append(
            "Large project footprint may affect ecological resources."
        )

    if data.get("has_forest"):

        score += 40

        reasons.append(
            "Project description indicates ecological/forest sensitivity."
        )

    if data.get("river_distance") is not None:

        distance = number(
            data.get("river_distance")
        )

        if distance < 5:

            score += 15

            reasons.append(
                "Proximity to a water body may affect aquatic ecology."
            )

    return min(score, 100), reasons


# ============================================================
# WASTE
# ============================================================

def assess_waste(data):

    score = 15

    reasons = []

    if data.get("has_effluent"):

        score += 20

        reasons.append(
            "Wastewater generation requires appropriate treatment."
        )

    if data.get("hazardous_material"):

        score += 35

        reasons.append(
            "Hazardous materials can generate hazardous waste."
        )

    land = number(
        data.get("land_area")
    )

    if land > 100:

        score += 10

        reasons.append(
            "Large-scale operations may generate significant waste."
        )

    return min(score, 100), reasons


# ============================================================
# POPULATION
# ============================================================

def assess_population(data):

    score = 10

    reasons = []

    workforce = number(
        data.get("workforce")
    )

    if workforce > 1000:

        score += 20

        reasons.append(
            "Large workforce increases occupational and "
            "emergency-management requirements."
        )

    elif workforce > 500:

        score += 10

        reasons.append(
            "Project involves a significant workforce."
        )

    if data.get("has_population"):

        score += 35

        reasons.append(
            "Nearby communities may be exposed to project impacts."
        )

    if data.get("hazardous_material"):

        score += 20

        reasons.append(
            "Hazardous-material use increases potential "
            "community exposure during an incident."
        )

    return min(score, 100), reasons


# ============================================================
# DISASTER RISK
# ============================================================

def assess_disaster(data):

    score = 10

    reasons = []

    # Hazardous material
    if data.get("hazardous_material"):

        score += 30

        reasons.append(
            "Hazardous-material storage introduces chemical, "
            "fire and explosion hazards."
        )

    # Flood
    if data.get("has_flood"):

        score += 25

        reasons.append(
            "Project description indicates flood exposure."
        )

    # Water proximity
    river_distance = data.get(
        "river_distance"
    )

    if river_distance is not None:

        distance = number(
            river_distance
        )

        if distance < 1:

            score += 25

            reasons.append(
                "Close proximity to a water body may increase "
                "flood exposure."
            )

        elif distance < 5:

            score += 15

            reasons.append(
                "Location may have potential flood exposure."
            )

    # Industrial project
    industrial_projects = [

        "Chemical / Chemical Manufacturing",
        "Cement Manufacturing",
        "Mining Project",
        "Power Generation Project",
        "Industrial Project"

    ]

    if data.get("project_type") in industrial_projects:

        score += 15

        reasons.append(
            "Industrial operations require dedicated "
            "emergency preparedness."
        )

    return min(score, 100), reasons


# ============================================================
# MAIN ASSESSMENT
# ============================================================

def assess_project(data):

    assessments = {}

    # ------------------------------------------
    # Individual factors
    # ------------------------------------------

    functions = {

        "Air Quality": assess_air_quality,

        "Water Resources": assess_water,

        "Soil": assess_soil,

        "Noise": assess_noise,

        "Ecology": assess_ecology,

        "Waste": assess_waste,

        "Population": assess_population,

        "Disaster Risk": assess_disaster

    }

    for factor, function in functions.items():

        score, reasons = function(data)

        assessments[factor] = {

            "score": round(score, 2),

            "level": classify(score),

            "reasons": reasons

        }


    # ------------------------------------------
    # Overall score
    # ------------------------------------------

    scores = [

        item["score"]

        for item in assessments.values()

    ]

    overall_score = sum(scores) / len(scores)


    # ------------------------------------------
    # Major concerns
    # ------------------------------------------

    major_concerns = []

    for factor, result in assessments.items():

        if result["level"] in [

            "HIGH",
            "CRITICAL"

        ]:

            major_concerns.extend(
                result["reasons"]
            )


    # Remove duplicates
    major_concerns = list(
        dict.fromkeys(
            major_concerns
        )
    )


    # ------------------------------------------
    # Mitigation recommendations
    # ------------------------------------------

    mitigation = []


    if assessments[
        "Air Quality"
    ]["level"] in ["HIGH", "CRITICAL"]:

        mitigation.append(
            "Install or upgrade emission-control systems."
        )


    if assessments[
        "Water Resources"
    ]["level"] in ["HIGH", "CRITICAL"]:

        mitigation.append(
            "Implement water recycling and "
            "effluent-treatment systems."
        )


    if assessments[
        "Soil"
    ]["level"] in ["HIGH", "CRITICAL"]:

        mitigation.append(
            "Provide hazardous-material containment "
            "and soil-monitoring measures."
        )


    if assessments[
        "Noise"
    ]["level"] in ["HIGH", "CRITICAL"]:

        mitigation.append(
            "Use acoustic barriers, equipment enclosures "
            "and noise monitoring."
        )


    if assessments[
        "Ecology"
    ]["level"] in ["HIGH", "CRITICAL"]:

        mitigation.append(
            "Develop green-belt and ecological-buffer measures."
        )


    if assessments[
        "Waste"
    ]["level"] in ["HIGH", "CRITICAL"]:

        mitigation.append(
            "Implement waste minimization, segregation "
            "and appropriate treatment."
        )


    if assessments[
        "Population"
    ]["level"] in ["HIGH", "CRITICAL"]:

        mitigation.append(
            "Develop community-safety and emergency "
            "communication measures."
        )


    if assessments[
        "Disaster Risk"
    ]["level"] in ["HIGH", "CRITICAL"]:

        mitigation.append(
            "Develop an emergency response plan and "
            "strengthen disaster-resilience infrastructure."
        )


    return {

        "factors": assessments,

        "overall_score": round(
            overall_score,
            2
        ),

        "overall_level": classify(
            overall_score
        ),

        "major_concerns": major_concerns,

        "mitigation": mitigation

    }