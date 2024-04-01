import os
from googletrans import Translator, LANGUAGES


def replace_lang_code_in_file_name(file_path, dest):
    """
    Replace the language code in the file name with the destination language code.

    Args:
        file_path (str): The path to the file.
        dest (str): The destination language code.

    Returns:
        str: The updated file path.
    """
    # Extract file directory, file name, and extension
    file_dir, file_name = os.path.split(file_path)
    file_name_no_ext, file_ext = os.path.splitext(file_name)

    # Split the file name by dot (.)
    parts = file_name_no_ext.split(".")

    # Replace the value before the last dot with the destination language code
    parts[-1] = dest

    # Construct updated file name
    new_file_name_no_ext = ".".join(parts)
    new_file_name = f"{new_file_name_no_ext}{file_ext}"

    # Construct updated file path
    new_file_path = os.path.join(file_dir, new_file_name)

    return new_file_path


def detect_language(file_path):
    """
    Detect the language of the text in a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The detected language code.
    """
    with open(file_path, "r", encoding="utf-8") as infile:
        # Read a few lines from the file to detect the language
        sample_text = "".join(infile.readlines()[:10])  # Read first 10 lines
        detected_language = Translator().detect(sample_text)
        detected_language_code = detected_language.lang
        detected_language_name = LANGUAGES[detected_language_code]
        print(f"Detected language: {detected_language_name} ({detected_language_code})")
        return detected_language_code


def translate_file(input_file, dest="en"):
    """
    Translate the contents of a file line by line.

    Args:
        input_file (str): The path to the input file.
        output_file (str): The path to the output file.
        dest (str): The destination language code (default is 'en' for English).
    """
    translator = Translator(
        service_urls=[
            "translate.google.com",
        ]
    )

    output_file = replace_lang_code_in_file_name(input_file, dest)

    with open(input_file, "r", encoding="utf-8") as infile, open(
        output_file, "w", encoding="utf-8"
    ) as outfile:
        for line in infile:
            translated_line = translator.translate(line.strip(), dest=dest).text + "\n"
            outfile.write(translated_line)
