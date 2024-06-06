import re  # noqa


class SSMLConverter:
    def __init__(
        self,
        srt_file,
        output_file,
        voice_name=None,
        duration_attribute_name="duration",
        use_inner_duration_tag=False,
        service_mode="generic",
        ssml_version="1.0",
        language="en-US",
    ):
        self.srt_file = srt_file
        self.output_file = output_file
        self.voice_name = voice_name
        self.duration_attribute_name = duration_attribute_name
        self.use_inner_duration_tag = use_inner_duration_tag
        # Possible Values: "azure", "amazon-standard-voice", "generic"
        self.service_mode = service_mode
        self.ssml_version = ssml_version
        self.language = language

    @property
    def voice_tag(self) -> tuple:
        if (
            self.voice_name is None
            or self.voice_name == ""
            or self.voice_name.lower() == "none"
        ):
            opening = ""
            closing = ""
        else:
            opening = '<voice name="' + self.voice_name + '">'
            closing = "</voice>"

        return opening, closing

    @property
    def duration_tag(self) -> str:
        if self.use_inner_duration_tag and self.service_mode == "azure":
            return "mstts:audioduration"

    @property
    def xmlns_attributes(self) -> dict:
        return {
            "xmlns": "http://www.w3.org/2001/10/synthesis",
            "xmlns:mstts": "http://www.w3.org/2001/mstts",
            "xmlns:emo": "http://www.w3.org/2009/10/emotionml",
        }

    @property
    def xmlns_attributes_string(self) -> str:
        attributes = ""
        for key, value in self.xmlns_attributes.items():
            attributes += f'{key}="{value}" '
        return attributes.strip()

    @property
    def timeline_regexp(self) -> re.Pattern:
        return re.compile(r"\d\d:\d\d:\d\d,\d\d\d --> \d\d:\d\d:\d\d,\d\d\d")

    def escape_chars(self, text):
        """Escape special characters such as: & " ' < >"""
        text = text.replace("&", "&amp;")
        text = text.replace('"', "&quot;")
        text = text.replace("'", "&apos;")
        text = text.replace("<", "&lt;")
        text = text.replace(">", "&gt;")
        return text

    def parse_srt_file(self) -> dict:
        """Parse SRT file and return a dictionary of subtitles"""
        subs_dict = {}
        with open(self.srt_file, "r", encoding="utf-8-sig") as f:
            lines = f.readlines()

        for line_num, line in enumerate(lines):
            line = line.strip()

            if line.isdigit() and self.timeline_regexp.match(lines[line_num + 1]):
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
                f'<speak {self.xmlns_attributes_string} version="{self.ssml_version}" xml:lang="{self.language}">\n'
            )

            voice_open, voice_end = self.voice_tag

            if self.service_mode != "azure":
                f.write(f"{voice_open}\n")

            for _, value in subs_dict.items():
                text = self.escape_chars(value["text"])

                break_time_string = (
                    f'<break time="{value["break_until_next"]}ms"/>'
                    if value["break_until_next"] or value["break_until_next"] == "0"
                    else ""
                )

                duration_attribute = (
                    f'{self.duration_attribute_name}="{value["duration_ms"]}ms"'
                )

                if not self.use_inner_duration_tag:
                    prosody_tag = f'\t<prosody {duration_attribute}="{value["duration_ms"]}ms">{text}</prosody>{break_time_string}\n'
                else:
                    prosody_tag = f'\t{voice_open}<{self.duration_tag}="{value["duration_ms"]}ms"/>{text}{voice_end}{break_time_string}\n'

                f.write(prosody_tag)

            f.write("</speak>\n")

    def convert(self):
        """Main method to convert SRT to SSML"""
        subs_dict = self.parse_srt_file()
        self.generate_ssml_file(subs_dict)
