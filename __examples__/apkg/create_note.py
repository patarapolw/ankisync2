import sys
import ruamel.yaml as yaml

from common.notes import create_note, create_notes


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    if sys.argv[1].endswith(".yaml"):
        with open(sys.argv[1], "r", encoding="utf8") as f:
            d_map = dict()
            for k, ts in yaml.safe_load(f).items():
                for t in ts:
                    d_map[t] = k

            create_notes(d_map)
    else:
        create_note(sys.argv[1], *sys.argv[2:])
