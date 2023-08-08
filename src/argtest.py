import argparse

parser = argparse.ArgumentParser(description='Script so useful.')
parser.add_argument("--opt1", type=int, default=1)
parser.add_argument("--opt2")

args = parser.parse_args()

opt1_value = args.opt1
opt2_value = args.opt2

print(opt1_value)
print(opt2_value)