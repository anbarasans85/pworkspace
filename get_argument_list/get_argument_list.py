import pprint
import yaml
from solution_functions import *

yaml_file_name = 'config.yaml'
input_configuration_dictionary = dict()
yaml_file = open(yaml_file_name).read()
input_configuration_dictionary.update(yaml.load(yaml_file).get('INPUT'))


def print_simple(rresult_input):
    for ritem in rresult_input:
        print ritem


def print_sorted(rresult_input):
    for ritem in rresult_input:
        for i, rkey in enumerate(sorted(ritem)):
            if i != (len(ritem) - 1):
                print('{0}: {1},'.format(rkey, ritem[rkey])),
            else:
                print('{0}: {1}'.format(rkey, ritem[rkey])),
        print('')

print('YAML Contents')
pprint.pprint(input_configuration_dictionary)
print('Result')
rresult = get_argument_list(input_configuration_dictionary)
print_sorted(rresult)
