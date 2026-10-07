import os
from pypdf import PdfReader
from docx import Document


def read_pdf(filepath):

    reader = PdfReader(filepath)

    text = []

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text.append(page_text)

    return "\n".join(text)


def read_docx(filepath):

    document = Document(filepath)

    paragraphs = []

    for paragraph in document.paragraphs:

        if paragraph.text.strip():

            paragraphs.append(
                paragraph.text.strip()
            )

    return "\n".join(paragraphs)


def read_txt(filepath):

    with open(
        filepath,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as file:

        return file.read()


def read_document(filepath):

    extension = os.path.splitext(filepath)[1].lower()

    if extension == ".pdf":

        return read_pdf(filepath)

    elif extension == ".docx":

        return read_docx(filepath)

    elif extension == ".txt":

        return read_txt(filepath)

    else:

        raise ValueError(
            "Unsupported document format"
        )