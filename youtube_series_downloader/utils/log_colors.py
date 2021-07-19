import colored


class LogColors:
    header = colored.attr("bold")
    skipped = colored.fg("yellow")
    added = colored.fg("light_green")
    error = colored.fg("red")
    warning = colored.fg("orange_1")
    passed = colored.fg("cyan")
