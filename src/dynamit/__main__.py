
import sys

import dynamit
import xmltodict


def main(argv: list[str]):

    print("Starting DYNAMIT1")
    print()

    tasks = {
        'ROIMeans': dynamit.task_roi_means,
        'TACFit': dynamit.task_tac_fit
    }

    # Parse XML input file
    if len(argv) != 1:
        exit("Missing command line argument: path to an XML file.")
    xml_file = open(argv[0], "r")
    task_tree = xmltodict.parse(xml_file.read(), force_list=('task'))
    root = task_tree['dynamit1']

    for task in root['task']:
        tasks[task['@name']](task)

    print("DYNAMIT1 ended!")


if __name__ == "__main__":
    main(sys.argv[1:])
