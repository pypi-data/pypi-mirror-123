import yaml
import argparse
from argparse import Namespace

def yaml2args(config_file, args):
    """
    config_file: Path to yaml file
    args: args object which after parser.parse_args()
    """
    with open(config_file, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    
    config.update(vars(args))
    args = Namespace(**config)

    return args
