import logging
# check https://www.blog.pythonlibrary.org/2012/08/02/python-101-an-intro-to-logging/

logging.basicConfig(filename="sample.log", level=logging.INFO)
log = logging.getLogger(__name__)

try:
    raise RuntimeError
except Exception as err:
    log.error("Error!")
    log.warning(
        'Encounter an error during parsing TCP option field.'
        'Skip parsing TCP option.')
print("moving on")