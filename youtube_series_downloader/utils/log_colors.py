import colored


class LogColors:
    header = colored.attr("bold")
    skipped = colored.fg("orange_1")
    added = colored.fg("light_green")
    error = colored.fg("red")
    warning = colored.fg("orange_1")
    passed = colored.fg("green")
    filtered = colored.fg("red")
    no_match = colored.fg("yellow")
