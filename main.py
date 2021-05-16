import logging
import argparse
import sys
from datetime import datetime
from pathlib import Path
import regexhelper


def main():
    # Setup
    args = parse_args()
    output_configuration = {            # This configuration dictionary is sent to PrintToTerminal()
        'underline': args.underline,
        'color': args.color,
        'machine': args.machine
    }
    try:
        Path('logs/').mkdir(exist_ok=True)  # Create 'logs' in cwd if it doesn't already exist
    except:
        logging.error("Failed to create logs folder")
    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M')
    log_filename = ("logs/regex_main_{timestamp}.log".format(timestamp=timestamp))
    logging.basicConfig(filename=log_filename,
                        format="%(asctime)s.%(msecs)03d [%(levelname)s]  %(message)s",
                        datefmt="%Y/%m/%d %H:%M:%S",
                        level=logging.INFO)
    # Execute
    logging.info("Session started")
    text_generator = input_generator(args)      # Using Yield generator to share code for input file/STDIN
    for item in text_generator:
        matches = item.find_pattern()
        terminal_printer = regexhelper.PrintToTerminal(matches, output_configuration)
        terminal_printer.trigger_output()


def input_generator(args):
    if not args.file_input:
        logging.info("Did not receive input files. Attempting to get user input")
        text_input = get_user_input()
        yield regexhelper.PatternFinder(text_input, args.regex_pattern, 'STDIN')
    else:
        for each_file in args.file_input:
            if Path(each_file).is_file():
                loader_context = regexhelper.RegexInputLoader(each_file)
                text_input = loader_context.load_text()
                yield regexhelper.PatternFinder(text_input, args.regex_pattern, each_file)
            else:
                logging.error("{file} doesn't exist.".format(file=each_file))


def get_user_input():

    lines = []
    print("Expected at least one input file. Please provide raw text to search. ")
    print("")
    while True:
        line = input()
        if line:
            lines.append(line)
        else:
            break
    return lines


def parse_args():
    parser = argparse.ArgumentParser(description='Regex finder')
    group = parser.add_mutually_exclusive_group()
    parser.add_argument('-r', '--regex',
                        dest='regex_pattern',
                        required=True,
                        help='Regular expression to search for')
    parser.add_argument('-f', '--files',
                        nargs='+',
                        dest='file_input',
                        help='A list of files to search in. When omitted, input will be taken from STDIN')
    group.add_argument('-u', '--underline',
                       dest='underline',
                       action='store_true',
                       help='"^" will be printed underneath the matched text.')
    group.add_argument('-c', '--color',
                       # choices=['Red', 'Green', 'Blue'],
                       action='store_true',
                       dest='color',
                       help='The matched text is highlighted. Options are Red/Blue/Green')
    group.add_argument('-m', '--machine',
                       dest='machine',
                       action='store_true',
                       help='Print the output in the format: "file_name:line_number:start_position:matched_text".')
    result = parser.parse_args()
    return result


if __name__ == '__main__':
    main()