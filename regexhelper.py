import logging
import re
from pathlib import Path

COLOR_MAP = {  # This mapper can be extended as needed
    'ColorStart': '\033[33m',
    'ColorStop': '\033[0m'
}


class RegexInputLoader(object):
    def __init__(self, txt_file):
        self.file_path = txt_file
        self.text_store = []

    def load_text(self):
        try:
            logging.info("trying to load text from {file}".format(file=self.file_path))
            with open(self.file_path, "r") as myfile:
                self.text_store = myfile.readlines()
                logging.info("returning loaded text")
                return self.text_store
        except UnicodeDecodeError as unicode_error:
            logging.error("Failed to load text from {file}, Reason: {reason}".format(file=self.file_path,
                                                                                     reason=unicode_error))
            return self.text_store


class PatternFinder(object):
    def __init__(self, loaded_txt, regex_pattern, file_name):
        self.loaded_txt = loaded_txt
        self.pattern = regex_pattern
        self.file_name = file_name

    def find_pattern(self):
        i = 1  # Line number tracker
        match_summary = []
        for each_line in self.loaded_txt:
            for match in re.finditer(self.pattern, each_line):
                hit_data = {}
                hit_data.update({'file_name': self.file_name,  # collecting relevant hit information in Dictionary
                                 'line_number': i,
                                 'full_line': each_line,
                                 's_position': match.start(),
                                 'e_position': match.end(),
                                 'pattern_match': match.group(0)
                                 })
                match_summary.append(hit_data)
            i += 1
        return match_summary


class PrintToTerminal(object):
    def __init__(self, hits, configuration):
        self.hits = hits
        self.color = configuration['color']
        self.underline = configuration['underline']
        self.machine_format = configuration['machine']

    def trigger_output(self):
        if self.color:
            self.color_print()
        elif self.underline:
            self.clean_print()
        else:
            self.machine_print()

    def color_print(self):
        for hit in self.hits:
            match_prefix = (hit['full_line']).split(hit['pattern_match'])[0]  # Splitting matched line to 3 parts
            match_suffix = (hit['full_line']).split(hit['pattern_match'])[1]
            match = hit['pattern_match']
            full_line = (match_prefix + COLOR_MAP['ColorStart']  # Attaching the parts with the match colored
                         + match + COLOR_MAP['ColorStop']
                         + match_suffix).strip()
            print("{f_name} {line_num} {line}".format(
                f_name=hit['file_name'],
                line_num=hit['line_number'],
                line=full_line).strip()
                  )

    def clean_print(self):
        # This method clean prints in default format, then calls add_caret_underline() to add underline
        for hit in self.hits:
            print("{f_name} {line_num} {line}".format(
                f_name=hit['file_name'],
                line_num=hit['line_number'],
                line=hit['full_line']).strip()
                  )
            if self.underline:
                len_tuple = (len(hit['file_name']),  # Characters length of file_name
                             len(str(hit['line_number'])),  # Characters length of line number
                             hit['s_position']  # Character length of pattern start position
                             )
                self.add_caret_underline(sum(len_tuple, 2))  # Set caret position as the sum of len_tuple and 2 space
            # characters

    def machine_print(self):
        # Printing in machine format
        for hit in self.hits:
            print("{f_name}:{line_num}:{s_pos}:{pattern}".format(
                f_name=hit['file_name'],
                line_num=hit['line_number'],
                s_pos=hit['s_position'],
                pattern=hit['pattern_match']).strip()
                  )

    @staticmethod
    def add_caret_underline(total_len):
        print("." * total_len + '^')
        print("")
