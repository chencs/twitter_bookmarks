import logging
from .globals import PATH, Colors

first_format = "%(asctime)s "
colored_format = "[%(levelname)s] "
last_format = "%(message)s (%(filename)s:%(lineno)d)"

class ColorFormatter(logging.Formatter):
	FORMATS = {
		logging.DEBUG: first_format + Colors.GREY + colored_format + Colors.RESET + last_format,
		logging.INFO: first_format + Colors.GREEN + colored_format + Colors.RESET + last_format,
		logging.WARNING: first_format + Colors.YELLOW + colored_format + Colors.RESET + last_format,
		logging.ERROR: first_format + Colors.RED + colored_format + Colors.RESET + last_format,
		logging.CRITICAL: first_format + Colors.BOLD_RED + colored_format + Colors.RESET + last_format
	}

	def format(self, record):
		log_fmt = self.FORMATS.get(record.levelno)
		formatter = logging.Formatter(log_fmt)
		return formatter.format(record)


def setup_logger(name):
	log = logging.getLogger(name)
	log.setLevel(logging.DEBUG)
	formatter = logging.Formatter(first_format+colored_format+last_format)

	# create console handler and set level to info
	ch = logging.StreamHandler()
	ch.setLevel(logging.INFO)
	ch.setFormatter(ColorFormatter())
	log.addHandler(ch)

	fh = logging.FileHandler(f'{PATH}/{log.name}.log', mode='a', delay=False)
	fh.setLevel(logging.DEBUG)
	fh.setFormatter(formatter)
	log.addHandler(fh)


	return log