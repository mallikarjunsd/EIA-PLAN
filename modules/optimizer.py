from modules.assessment import assess_project


def apply_interventions(data, interventions):
    """
    Apply real project-planning interventions to the extracted
    project information.

    The intervention values represent implementation levels
    from 0 to 100 percent.
    """

    revised = data.copy()

    # ---------------------------------------------------------
    # WATER RECYCLING
    # ---------------------------------------------------------

    if "water_recycling" in interventions:
        reduction = interventions["water_recycling"] / 100

        if revised.get("water_consumption") is not None:
            revised["water_consumption"] = round(
                revised["water_consumption"] * (1 - reduction),
                2
            )

    # ---------------------------------------------------------
    # EFFLUENT TREATMENT
    # ---------------------------------------------------------

    if "effluent_treatment" in interventions:
        treatment = interventions["effluent_treatment"]

        # Strong treatment reduces the effective environmental
        # significance of wastewater.
        if treatment >= 50:
            revised["has_effluent"] = False

    # ---------------------------------------------------------
    # HAZARDOUS MATERIAL CONTROL
    # ---------------------------------------------------------

    if "hazardous_material_control" in interventions:
        control = interventions["hazardous_material_control"]

        # At high implementation level, hazardous-material
        # exposure is considered substantially controlled.
        if control >= 70:
            revised["hazardous_material"] = False

    # ---------------------------------------------------------
    # FLOOD PROTECTION
    # ---------------------------------------------------------

    if "flood_protection" in interventions:
        protection = interventions["flood_protection"]

        if protection >= 70:
            revised["has_flood"] = False

    # ---------------------------------------------------------
    # ECOLOGICAL PROTECTION
    # ---------------------------------------------------------

    if "ecology_protection" in interventions:
        protection = interventions["ecology_protection"]

        if protection >= 70:
            revised["has_forest"] = True

    # ---------------------------------------------------------
    # POPULATION / COMMUNITY PROTECTION
    # ---------------------------------------------------------

    if "community_protection" in interventions:
        protection = interventions["community_protection"]

        if protection >= 70:
            revised["has_population"] = False

    # ---------------------------------------------------------
    # EMISSION CONTROL
    # ---------------------------------------------------------

    if "emission_control" in interventions:
        control = interventions["emission_control"]

        if control >= 70:
            revised["has_emissions"] = False

    return revised


def optimize_project(original_data, interventions):
    """
    Assess the original project, apply planning interventions,
    reassess the revised project and calculate improvement.
    """

    original_assessment = assess_project(original_data)

    revised_data = apply_interventions(
        original_data,
        interventions
    )

    revised_assessment = assess_project(revised_data)

    improvement = (
        original_assessment["overall_score"]
        - revised_assessment["overall_score"]
    )

    return {
        "original": original_assessment,
        "revised": revised_assessment,
        "improvement": round(improvement, 2),
        "revised_data": revised_data,
        "interventions": interventions
    }