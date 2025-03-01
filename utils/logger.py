import logging
import sys
import unicodedata

norm = sys.stdout


class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """

    def __init__(self, logger, level: int = logging.INFO):
        self.logger = logger
        self.level = level
        self.linebuf = ""

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.level, line.rstrip())

    def flush(self):
        pass

    def read(self):
        text1, text2 = "", ""
        with open("log.log", "r") as f:
            text1 = f.read()

        try:
            with open("out.log", "r") as f:
                text2 = f.read()
        except:
            self.write("out.log does not exist")

        return text1 + "\n" + text2


class Logger:
    def __init__(self, DEBUG=False, level: int = logging.INFO, allowJoin=False):
        """Initializes the logger class

        Args:
            DEBUG (bool, optional): Show debugging. Defaults to False.
        """
        self.DEBUG = DEBUG
        self.logger = logging

        logging.basicConfig(
            level=level,
            format="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
            filename="log.log",
            filemode="a",
        )

        self.log = logging.getLogger("STDOUT")
        self.out = StreamToLogger(self.log, level)
        sys.stdout = self.out

        # if allowJoin:
        #     # output js console to log.log
        #     from javascript import On, require, console
        #     log4js = require("log4js")
        #     log4js.configure({
        #         "appenders": {
        #             "out": {"type": "stdout"},
        #             "app": {"type": "file", "filename": "out.log"}
        #         },
        #         "categories": {
        #             "default": {"appenders": ["out", "app"], "level": "debug"}
        #         }
        #     })

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        sys.stdout = norm  # output to console
        print(message)
        sys.stdout = self.out  # output to log.log
        self.logger.error(message)

    def critical(self, message):
        sys.stdout = norm
        print(message)
        sys.stdout = self.out
        self.logger.critical(message)

    def debug(self, *args, **kwargs):
        self.logger.debug(" ".join([str(arg) for arg in args]))
        if self.DEBUG:
            self.print(*args, **kwargs)

    def warning(self, message):
        self.logger.warning(message)

    def critical(self, message):
        self.logger.critical(message)

    def exception(self, message):
        self.logger.exception(message)

    def read(self):
        text1, text2 = "", ""
        with open("log.log", "r") as f:
            text1 = f.read()

        try:
            with open("out.log", "r") as f:
                text2 = f.read()[3:]
                text2 = "".join(
                    ch
                    for ch in text2
                    if unicodedata.category(ch)[0] != "C" or ch in "\t" or ch in "\n"
                )
                text2 = text2.replace("\n\n", "\n")
        except:
            self.write("out.log does not exist")

        return text1 + "\n" + text2

    def print(self, *args, **kwargs):
        msg = " ".join([str(arg) for arg in args])
        sys.stdout = norm  # output to console
        print(msg, **kwargs)
        sys.stdout = self.out  # output to log.log
        self.info(msg)

    def clear(self):
        with open("log.log", "w") as f:
            f.write("")

    def __repr__(self):
        return self.read()

    def __str__(self):
        return self.read()
