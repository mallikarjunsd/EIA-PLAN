import re


def find_number(text, patterns):

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            try:
                return float(match.group(1))
            except (ValueError, IndexError):
                pass

    return None


def contains(text, keywords):

    text = text.lower()

    return any(
        keyword.lower() in text
        for keyword in keywords
    )


def extract_project_information(text):

    text_lower = text.lower()

    # =========================================================
    # PROJECT TYPE
    # =========================================================

    project_type = "Not identified"

    # More specific project types first
    project_types = [

        ("textile manufacturing", "Textile Manufacturing"),
        ("textile plant", "Textile Manufacturing"),
        ("textile industry", "Textile Manufacturing"),

        ("chemical manufacturing", "Chemical / Chemical Manufacturing"),
        ("chemical plant", "Chemical / Chemical Manufacturing"),
        ("chemical industry", "Chemical / Chemical Manufacturing"),

        ("cement manufacturing", "Cement Manufacturing"),
        ("cement plant", "Cement Manufacturing"),

        ("mining project", "Mining Project"),
        ("mining operation", "Mining Project"),
        ("mine", "Mining Project"),

        ("highway", "Highway / Road Infrastructure"),
        ("expressway", "Highway / Road Infrastructure"),

        ("power plant", "Power Generation Project"),
        ("power generation", "Power Generation Project"),

        ("hospital", "Healthcare Facility"),

        ("industrial project", "Industrial Project"),
        ("industrial plant", "Industrial Project"),
        ("industrial facility", "Industrial Project")
    ]

    for keyword, name in project_types:

        if keyword in text_lower:

            project_type = name
            break


    # =========================================================
    # LAND AREA
    # =========================================================

    land_area = find_number(
        text,
        [
            r"(\d+(?:\.\d+)?)\s*acres?",
            r"(\d+(?:\.\d+)?)\s*hectares?",
            r"land\s*(?:area|requirement)?\s*(?:of|:)?\s*(\d+(?:\.\d+)?)"
        ]
    )


    # =========================================================
    # WATER CONSUMPTION
    # =========================================================

    water_consumption = find_number(
        text,
        [
            # 2 million litres per day
            r"(\d+(?:\.\d+)?)\s*million\s*litres?\s*(?:of\s*)?(?:water\s*)?(?:per\s*day|/day)",

            # 2 million litres of water per day
            r"(\d+(?:\.\d+)?)\s*million\s*litres?\s*(?:of\s*)?water",

            # 2 million litres/day
            r"(\d+(?:\.\d+)?)\s*million\s*litres?\s*/\s*day",

            # 2,000,000 litres per day
            r"([\d,]+(?:\.\d+)?)\s*litres?\s*(?:of\s*)?(?:water\s*)?(?:per\s*day|/day)",

            # 2 MLD
            r"(\d+(?:\.\d+)?)\s*mld",

            # water consumption: 2
            r"water\s*consumption\s*(?:of|:)?\s*(\d+(?:\.\d+)?)"
        ]
    )


    # =========================================================
    # EFFLUENT / WASTEWATER
    # =========================================================

    effluent_generation = find_number(
        text,
        [
            r"([\d,]+(?:\.\d+)?)\s*litres?\s*(?:of\s*)?(?:wastewater|effluent)",

            r"(\d+(?:\.\d+)?)\s*mld\s*(?:of\s*)?(?:wastewater|effluent)",

            r"([\d,]+(?:\.\d+)?)\s*litres?\s*(?:of\s*)?wastewater",

            r"effluent\s*(?:generation|quantity|volume)?\s*(?:of|:)?\s*([\d,]+(?:\.\d+)?)"
        ]
    )


    # =========================================================
    # WORKFORCE
    # =========================================================

    workforce = find_number(
        text,
        [
            r"(\d+)\s*(?:workers|employees|staff|people)",

            r"workforce\s*(?:of|:)?\s*(\d+)",

            r"employment\s*(?:of|:)?\s*(\d+)"
        ]
    )


    # =========================================================
    # DISTANCE FROM RIVER / WATER BODY
    # =========================================================

    river_distance = find_number(
        text,
        [
            r"(\d+(?:\.\d+)?)\s*km\s*(?:from|away\s*from)\s*(?:the\s*)?(?:river|water\s*body)",

            r"(?:river|water\s*body)[^.]{0,80}?(\d+(?:\.\d+)?)\s*km",

            r"(\d+(?:\.\d+)?)\s*km\s*(?:to|from)\s*(?:the\s*)?river",

            r"river\s*(?:distance)?\s*(?:of|:)?\s*(\d+(?:\.\d+)?)\s*km"
        ]
    )


    # =========================================================
    # HAZARDOUS MATERIAL
    # =========================================================

    hazardous_material = contains(
        text,
        [
            "hazardous chemical",
            "hazardous chemicals",
            "hazardous material",
            "hazardous materials",
            "toxic chemical",
            "toxic chemicals",
            "chemical storage",
            "hazardous substance",
            "hazardous substances",
            "flammable material",
            "flammable materials",
            "chemical dyes",
            "chlorine",
            "ammonia",
            "solvent",
            "petroleum",
            "fuel storage"
        ]
    )


    # =========================================================
    # EFFLUENT
    # =========================================================

    has_effluent = contains(
        text,
        [
            "effluent",
            "wastewater",
            "industrial discharge",
            "waste water"
        ]
    )


    # =========================================================
    # EMISSIONS
    # =========================================================

    has_emissions = contains(
        text,
        [
            "emission",
            "emissions",
            "air pollution",
            "stack emission",
            "stack emissions",
            "smoke",
            "particulate",
            "particulate matter",
            "dust",
            "air pollutant"
        ]
    )


    # =========================================================
    # FLOOD
    # =========================================================

    has_flood = contains(
        text,
        [
            "flood",
            "flood-prone",
            "flood prone",
            "flood risk",
            "floodplain",
            "flood plain",
            "inundation"
        ]
    )


    # =========================================================
    # FOREST / ECOLOGY
    # =========================================================

    has_forest = contains(
        text,
        [
            "forest",
            "reserved forest",
            "protected forest",
            "wildlife",
            "biodiversity",
            "ecologically sensitive",
            "ecological sensitive area",
            "wetland"
        ]
    )


    # =========================================================
    # POPULATION
    # =========================================================

    has_population = contains(
        text,
        [
            "residential",
            "population",
            "village",
            "town",
            "urban area",
            "settlement",
            "community"
        ]
    )


    # =========================================================
    # RETURN STRUCTURED DATA
    # =========================================================

    return {

        "raw_text": text,

        "project_type": project_type,

        "land_area": land_area,

        "water_consumption": water_consumption,

        "effluent_generation": effluent_generation,

        "workforce": workforce,

        "river_distance": river_distance,

        "hazardous_material": hazardous_material,

        "has_effluent": has_effluent,

        "has_emissions": has_emissions,

        "has_flood": has_flood,

        "has_forest": has_forest,

        "has_population": has_population
    }
def identify_missing_information(data):
    """
    Identifies important project information that was not explicitly
    provided in the project description.
    """

    missing = []

    if data.get("river_distance") is None:
        missing.append(
            "Exact distance from the nearest river/water body was not provided."
        )

    if not data.get("has_emissions"):
        missing.append(
            "Air-emission quantity/source details were not provided."
        )

    if data.get("hazardous_material"):
        missing.append(
            "Exact hazardous-material type and storage quantity were not provided."
        )

    if not data.get("has_effluent"):
        missing.append(
            "Wastewater/effluent generation details were not provided."
        )

    # Current extractor does not yet calculate solid-waste quantity
    missing.append(
        "Solid-waste generation quantity was not provided."
    )

    if data.get("workforce") is None:
        missing.append(
            "Project workforce size was not provided."
        )

    if data.get("land_area") is None:
        missing.append(
            "Project land area was not provided."
        )

    return missing