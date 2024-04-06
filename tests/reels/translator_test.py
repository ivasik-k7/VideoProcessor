# import unittest
# import os
# from reels.translator import (
#     replace_lang_code_in_file_name,
#     detect_language,
#     translate_file,
# )


# class TestReplaceLangCodeInFileName(unittest.TestCase):
#     def test_replace_lang_code_in_file_name(self):
#         original_file_path = "example_file_fr.txt"
#         dest_language_code = "es"
#         expected_new_file_path = "example_file_es.txt"
#         new_file_path = replace_lang_code_in_file_name(
#             original_file_path, dest_language_code
#         )
#         self.assertEqual(new_file_path, expected_new_file_path)


# class TestDetectLanguage(unittest.TestCase):
#     def test_detect_language(self):
#         test_file_path = "example_file_fr.txt"
#         detected_language_code = detect_language(test_file_path)
#         self.assertEqual(detected_language_code, "fr")


# class TestTranslateFile(unittest.TestCase):
#     def test_translate_file(self):
#         test_input_file = "example_file_fr.txt"
#         dest_language_code = "es"
#         expected_output_file = "example_file_es.txt"
#         translate_file(test_input_file, dest_language_code)
#         self.assertTrue(os.path.exists(expected_output_file))


# if __name__ == "__main__":
#     unittest.main()
