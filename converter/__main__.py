from . import main
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Convert from SDF to WoT and vice versa.')

    from_group = parser.add_mutually_exclusive_group(required=True)
    from_group.add_argument('--from-sdf', metavar='SDF', dest="from_sdf", help='SDF input JSON file')
    from_group.add_argument('--from-tm', metavar='TM', dest="from_tm", help='WoT TM input JSON file')

    to_group = parser.add_mutually_exclusive_group(required=True)
    to_group.add_argument('--to-tm', metavar='TM', dest="to_tm", help='WoT TM output file')
    to_group.add_argument('--to-sdf', metavar='SDF', dest="to_sdf", help='SDF output file')
    args = parser.parse_args()

    main(args)
