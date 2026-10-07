from flask import Flask, render_template, request, session, redirect, url_for
import os

from modules.document_reader import read_document
from modules.extractor import (
    extract_project_information,
    identify_missing_information
)
from modules.assessment import assess_project
from modules.optimizer import optimize_project


app = Flask(__name__)

app.secret_key = "eia-plan-development-key"

UPLOAD_FOLDER = "uploads"

ALLOWED_EXTENSIONS = {
    "pdf",
    "docx",
    "txt"
}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024


# ---------------------------------------------------------
# HELPER
# ---------------------------------------------------------

def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# ---------------------------------------------------------
# HOME
# ---------------------------------------------------------

@app.route("/")
def index():

    return render_template("index.html")


# ---------------------------------------------------------
# ANALYZE PROJECT
# ---------------------------------------------------------

@app.route("/analyze", methods=["POST"])
def analyze():

    project_text = request.form.get(
        "project_text",
        ""
    ).strip()

    uploaded_file = request.files.get(
        "project_file"
    )

    # -----------------------------------------------------
    # OPTION 1 — TEXT INPUT
    # -----------------------------------------------------

    if project_text:

        text = project_text

    # -----------------------------------------------------
    # OPTION 2 — FILE UPLOAD
    # -----------------------------------------------------

    elif uploaded_file and uploaded_file.filename:

        filename = uploaded_file.filename

        if not allowed_file(filename):

            return "Unsupported file format", 400

        os.makedirs(
            app.config["UPLOAD_FOLDER"],
            exist_ok=True
        )

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        uploaded_file.save(filepath)

        text = read_document(filepath)

    else:

        return "Please enter project information or upload a document.", 400


    # -----------------------------------------------------
    # EXTRACT PROJECT INFORMATION
    # -----------------------------------------------------

    data = extract_project_information(text)


    # -----------------------------------------------------
    # IDENTIFY MISSING INFORMATION
    # -----------------------------------------------------

    missing_information = identify_missing_information(
        data
    )


    # -----------------------------------------------------
    # SAVE INFORMATION IN SESSION
    # -----------------------------------------------------

    session["project_text"] = text

    session["project_data"] = data

    session["missing_information"] = missing_information


    # -----------------------------------------------------
    # SHOW EXTRACTED INFORMATION
    # -----------------------------------------------------

    return render_template(
        "extracted.html",
        data=data,
        missing_information=missing_information
    )


# ---------------------------------------------------------
# ENVIRONMENTAL ASSESSMENT
# ---------------------------------------------------------

@app.route("/assess", methods=["GET", "POST"])
def assess():

    data = session.get(
        "project_data"
    )

    if not data:

        return redirect(
            url_for("index")
        )


    assessment = assess_project(
        data
    )


    session["assessment"] = assessment


    return render_template(
        "assessment.html",
        data=data,
        assessment=assessment
    )


# ---------------------------------------------------------
# OPTIMIZATION PAGE
# ---------------------------------------------------------

@app.route("/optimize", methods=["GET"])
def optimize():

    data = session.get(
        "project_data"
    )

    assessment = session.get(
        "assessment"
    )

    if not data or not assessment:

        return redirect(
            url_for("index")
        )


    return render_template(
        "optimize.html",
        data=data,
        assessment=assessment
    )


# ---------------------------------------------------------
# SIMULATE REVISED PROJECT
# ---------------------------------------------------------

@app.route("/simulate", methods=["POST"])
def simulate():

    data = session.get(
        "project_data"
    )

    if not data:

        return redirect(
            url_for("index")
        )


    interventions = {

        "water_recycling": float(
            request.form.get(
                "water_recycling",
                0
            )
        ),

        "effluent_treatment": float(
            request.form.get(
                "effluent_treatment",
                0
            )
        ),

        "hazardous_material_control": float(
            request.form.get(
                "hazardous_material_control",
                0
            )
        ),

        "flood_protection": float(
            request.form.get(
                "flood_protection",
                0
            )
        ),

        "ecology_protection": float(
            request.form.get(
                "ecology_protection",
                0
            )
        ),

        "community_protection": float(
            request.form.get(
                "community_protection",
                0
            )
        ),

        "emission_control": float(
            request.form.get(
                "emission_control",
                0
            )
        )
    }


    result = optimize_project(
        data,
        interventions
    )


    session["optimization"] = result


    return render_template(
        "comparison.html",
        result=result
    )


# ---------------------------------------------------------
# RUN APPLICATION
# ---------------------------------------------------------

if __name__ == "__main__":

    os.makedirs(
        UPLOAD_FOLDER,
        exist_ok=True
    )

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )