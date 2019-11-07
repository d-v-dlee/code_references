## This directory is a reference for logging.
Logging is important because it allows you to more easily identify which parts of your code has been executed or where there is a problem. This can be especially helpful when writing large chunks of complicated code or running a program.  Instead of having to slowly sift through all your code, you can use the breadcrumbs provided by logging to quickly identify the problem area.

#### Logging Note (corresponding levels):
Notset: 0, Debug: 10, Info: 20, Warning: 30, Error: 40, Critical: 50 \
When you set `logger.setLevel({something})` the logger will only return logger thangs that are equal to or greater than that level. So if I set it to `logger.setLevel(logging.Notset)`, it would show everything as that is level 0. The `get_logger` function in this directory is set to `logging.Info` aka 20 points.

#### Whats in here
`logging.py` has the code to build a logger object while `logging_example.ipynb` has an example of how to use it.
