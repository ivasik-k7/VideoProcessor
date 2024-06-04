import re  # noqa


class SSMLConverter:
    def __init__(
        self,
        srt_file,
        output_file,
        voice_name=None,
        duration_attribute_name="duration",
        use_inner_duration_tag=False,
    ):
        self.srt_file = srt_file
        self.output_file = output_file
        self.voice_name = voice_name
        self.duration_attribute_name = duration_attribute_name
        self.use_inner_duration_tag = use_inner_duration_tag

    def escape_chars(self, text):
        """Escape special characters such as: & " ' < >"""
        text = text.replace("&", "&amp;")
        text = text.replace('"', "&quot;")
        text = text.replace("'", "&apos;")
        text = text.replace("<", "&lt;")
        text = text.replace(">", "&gt;")
        return text

    def parse_srt_file(self):
        """Parse SRT file and return a dictionary of subtitles"""
        subs_dict = {}
        with open(self.srt_file, "r", encoding="utf-8-sig") as f:
            lines = f.readlines()

        for line_num, line in enumerate(lines):
            line = line.strip()
            if line.isdigit():
                time_line = lines[line_num + 1].strip()
                text_line = lines[line_num + 2].strip()

                count = 3
                while line_num + count < len(lines) and lines[line_num + count].strip():
                    text_line += " " + lines[line_num + count].strip()
                    count += 1

                start_time, end_time = map(lambda x: x.strip(), time_line.split("-->"))
                start_time_ms = sum(
                    int(t) * 10 ** (3 - i * 3)
                    for i, t in enumerate(start_time.replace(",", ":").split(":"))
                )
                end_time_ms = sum(
                    int(t) * 10 ** (3 - i * 3)
                    for i, t in enumerate(end_time.replace(",", ":").split(":"))
                )
                duration_ms = end_time_ms - start_time_ms

                subs_dict[line] = {
                    "start_ms": start_time_ms,
                    "end_ms": end_time_ms,
                    "duration_ms": duration_ms,
                    "text": text_line,
                    "break_until_next": 0,
                }

                if line_num > 0:
                    subs_dict[str(int(line) - 1)]["break_until_next"] = (
                        start_time_ms - subs_dict[str(int(line) - 1)]["end_ms"]
                    )

        return subs_dict

    def generate_ssml_file(self, subs_dict):
        """Generate SSML file from the parsed subtitles dictionary"""
        with open(self.output_file, "w", encoding="utf-8-sig") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write(
                '<speak xmlns="http://www.w3.org/2001/10/synthesis" version="1.0" xml:lang="en-US">\n'
            )

            for _, value in subs_dict.items():
                text = self.escape_chars(value["text"])
                break_time_string = (
                    f'<break time="{value["break_until_next"]}ms"/>'
                    if value["break_until_next"]
                    else ""
                )
                duration_attribute = (
                    f'{self.duration_attribute_name}="{value["duration_ms"]}ms"'
                )

                if not self.use_inner_duration_tag:
                    prosody_tag = f"<prosody {duration_attribute}>{text}</prosody>"
                else:
                    duration_tag = f'<mstts:audioduration="{value["duration_ms"]}ms"/>'
                    prosody_tag = (
                        f'<voice name="{self.voice_name}">{duration_tag}{text}</voice>'
                    )

                f.write(f"\t{prosody_tag}{break_time_string}\n")

            f.write("</speak>\n")

    def convert(self):
        """Main method to convert SRT to SSML"""
        subs_dict = self.parse_srt_file()
        self.generate_ssml_file(subs_dict)
