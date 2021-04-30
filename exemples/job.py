import json
import logging
import sys

import treefiles as tf


def main():
    log.info(f"Received {args}")


log = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    log = tf.get_logger(default=False, handlers=[tf.stream_csv_handler()])

    args = json.loads(sys.argv[1])

    main()