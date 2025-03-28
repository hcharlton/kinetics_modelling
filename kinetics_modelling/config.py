from pathlib import Path
import configparser 

from dotenv import load_dotenv
from loguru import logger

# Load environment variables from .env file if it exists
load_dotenv()

# Paths
PROJ_ROOT = Path(__file__).resolve().parents[1]
logger.info(f"PROJ_ROOT path is: {PROJ_ROOT}")

DATA_DIR = PROJ_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXTERNAL_DATA_DIR = DATA_DIR / "external"

CONFIG_DIR = PROJ_ROOT / "configs"

MODELS_DIR = PROJ_ROOT / "models"

REPORTS_DIR = PROJ_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

# If tqdm is installed, configure loguru with tqdm.write
# https://github.com/Delgan/loguru/issues/135
try:
    from tqdm import tqdm

    logger.remove(0)
    logger.add(lambda msg: tqdm.write(msg, end=""), colorize=True)
except ModuleNotFoundError:
    pass


def load_config(config_name):
    """
    Load and validate run-specific configuration from an INI file.

    The INI file must have a 
    - [Paths] section
    - [Constants] section

    Args:
        config_name (str): name of the config file in /configs
    
    Returns:
        configparse.ConfigParser: the loaded configuration object
    """
    ini_path = Path(CONFIG_DIR) / Path(config_name)
    if not ini_path.exists():
        raise FileNotFoundError(f"Config file not found at: {ini_path}")
    
    config = configparser.ConfigParser()
    config.read(ini_path)

    # paths existence
    if 'Paths' not in config:
        raise ValueError('Paths sections not found in config')
    # path to bam file existence
    if 'bam_filepath' not in config['Paths']:
        raise ValueError('no bam_file specified in config')
    # path bed file existence
    if 'bed_filepath' not in config['Paths']:
        raise ValueError('no bed_filepath specified in config')
    # constants existence
    if 'Constants' not in config:
        raise ValueError('no Constants section in config')
    # context value existence
    if 'context' not in config['Constants']:
        raise ValueError('no context specified in config')
    
    return config