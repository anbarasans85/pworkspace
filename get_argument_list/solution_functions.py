from collections import Iterable


def config_to_string_list(configuration_dictionary):
    """ Constructs a dictionary to be passed as an argument to pyBAS API

    Recursive function to construct argument list for pyBAS API.

    Args:
        * configuration_dictionary (dict): DUT configurations

    Returns:
        * dict: Result dictionary
        * list: List of dictionaries

    Author:
        Anbarasan Shenbagaraj <ashenbag@brocade.com>

    Modifications(user-date-reason) :
    """
    if not isinstance(configuration_dictionary, dict):
        print('*** ERROR INPUT: {0} ***'.format(configuration_dictionary))
        return dict()
    result_dict = dict()
    result_list = list()
    for key, value in configuration_dictionary.items():
        if isinstance(value, list):
            temp_list = list()
            for litem in value:
                temp_list.append(config_to_string_list({key: litem}))
            if result_list:
                temp2_list = list()
                for litem in temp_list:
                    temp2_list.append(multiply_two_dicts(litem, result_list))
                result_list = list(temp2_list)
            else:
                result_list = list(temp_list)
            result_list = list(flatten(result_list))
    for key, value in configuration_dictionary.items():
        if isinstance(value, dict):
            result_dict = merge_two_dicts(result_dict, {key: value.keys()[0]})
            if isinstance(value.values()[0], dict):
                result = config_to_string_list(value.values()[0])
                if isinstance(result, dict):
                    result_dict = merge_two_dicts(result_dict, result)
                elif isinstance(result, list):
                    if not result_list:
                        result_list = multiply_two_dicts(result_dict, result)
                    else:
                        temp_list3 = multiply_two_dicts(result_dict, result)
                        temp_list4 = list()
                        for litem in result_list:
                            temp_list4.append(multiply_two_dicts(litem, temp_list3))
                        result_list = list(temp_list4)
                        result_list = list(flatten(result_list))
            elif isinstance(value.values()[0], list):
                for llitem in value.values()[0]:
                    result = config_to_string_list(llitem)
                    result_list.append(multiply_two_dicts(result_dict, result))
    result_list = multiply_two_dicts(result_dict, result_list)
    for key, value in configuration_dictionary.items():
        if isinstance(value, str) or isinstance(value, int):
            result_dict = merge_two_dicts(result_dict, {key: value})
    result_list = multiply_two_dicts(result_dict, result_list)
    if result_list:
        return result_list
    else:
        return result_dict


def merge_two_dicts(x, y):
    """ Merges two dictionaries
    Example:
    x = {'neighbor': '2.2.2.1'}
    y = {'INTF': 'loopback 1', 'REMOTEAS': 101, 'UPDATESRC': 1}
    result = {'UPDATESRC': 1, 'INTF': 'loopback 1', 'REMOTEAS': 101,
    'neighbor': '2.2.2.1'}

    Args:
        * x (dict): first dictionary
        * y (dict): second dictionary

    Returns:
        * dict: Merged result dictionary

    Author:
        Anbarasan Shenbagaraj <ashenbag@brocade.com>

    Modifications(user-date-reason) :
    """
    z = x.copy()
    z.update(y)
    return z


def multiply_two_dicts(x, y):
    """ Multiply two dictionaries and returns a list or dict

    Examples:
    1.
    x = {'ADDRFAMILY': 'ipv4'}
    y = [{'neighbor': '2.2.2.1', 'INTF': 'loopback 1',
    'FAMILY_TYPE': 'unicast', 'REMOTEAS': 101, 'UPDATESRC': 1}]
    #
    result_list = [[{'INTF': 'loopback 1', 'UPDATESRC': 1,
    'neighbor': '2.2.2.1', 'ADDRFAMILY': 'ipv4', 'FAMILY_TYPE': 'unicast',
    'REMOTEAS': 101}]]

    2.
    x = {'VRFNAME': 'default-vrf'}
    y = [{'ADDRFAMILY': 'l2vpn', 'FAMILY_TYPE': 'evpn', 'neighbor': '2.2.2.1',
    'ACTIVATE': 1}]
    #
    result_list = [[[{'INTF': 'loopback 1', 'VRFNAME': 'default-vrf',
    'neighbor': '2.2.2.1', 'UPDATESRC': 1, 'ADDRFAMILY': 'ipv4',
    'FAMILY_TYPE': 'unicast',
    'REMOTEAS': 101}]], [[{'FAMILY_TYPE': 'evpn', 'ADDRFAMILY': 'l2vpn',
    'VRFNAME': 'default-vrf', 'ACTIVATE': 1, 'neighbor': '2.2.2.1'}]]]

    Args:
        * x (dict): first dictionary
        * y (list): mostly a list; could be a dictionary

    Returns:
        * dict: Merged result dictionary

    Author:
        Anbarasan Shenbagaraj <ashenbag@brocade.com>

    Modifications(user-date-reason) :
    """
    if isinstance(y, dict):
        return merge_two_dicts(x, y)
    elif all(isinstance(element, list) for element in y):
        result_list = list()
        for y_element in y:
            result_list.append(multiply_two_dicts(x, y_element))
        return result_list
    elif isinstance(y, list):
        output = []
        for item in y:
            z = x.copy()
            z.update(item)
            output.append(z)
        return output


def get_argument_list(configuration_dictionary):
    """ Constructs a dictionary to be passed as an argument to pyBAS API

    Reads configuration dictionary (which is read from YAML file) and
    constructs a list of dictionaries to be passed as an argument to pyBAS
    API

    pyBAS APIs expect input values to be tuple of mandatory arguments and
    dictionary of optional arguments
    To convert the YAML configuration, verification dictionaries to the format
    expected by pyBAS APIs, this function get_argument_list is used.
    Please note that YAML dictionary mostly contains nested dictionary with
    list elements.

    result_list in below examples will be iterated through in the RF keyword
    implementation functions such as Configure BGP Neighbor, Configure VRF.
    List elements may be edited (like adding module name) and passed to
    respective pyBAS API.

    Examples:
    1.
    input_dict = {'ADDRFAMILY': [{'ipv4': {'MAXROUTE': 700}}, {'ipv6':
    {'MAXROUTE': 800}}], 'RD': '1:1'}
    #
    result_list = [{'RD': '1:1', 'ADDRFAMILY': 'ipv4', 'MAXROUTE': 700},
    {'RD': '1:1', 'ADDRFAMILY': 'ipv6', 'MAXROUTE': 800}]

    2.
    input_dict = {'VRFNAME': [{'default-vrf': {'ADDRFAMILY': [
    {'ipv4': {'FAMILY_TYPE': [{'unicast': {'neighbor': [{'2.2.2.1':
    {'INTF': 'loopback 1', 'REMOTEAS': 101, 'UPDATESRC': 1}}]}}]}},
    {'l2vpn': {'FAMILY_TYPE': [{'evpn': {'neighbor': [{'2.2.2.1':
    {'ACTIVATE': 1}}]}}]}}]}}]}
    #
    result_list = [{'INTF': 'loopback 1', 'VRFNAME': 'default-vrf',
    'neighbor': '2.2.2.1', 'UPDATESRC': 1, 'ADDRFAMILY': 'ipv4',
    'FAMILY_TYPE': 'unicast', 'REMOTEAS': 101},
    {'FAMILY_TYPE': 'evpn', 'ADDRFAMILY': 'l2vpn', 'VRFNAME': 'default-vrf',
    'ACTIVATE': 1, 'neighbor': '2.2.2.1'}]

    3.
    input_dict = {'VRF': [{'L3VPN_VRF_01': {'ADDRFAMILY': [{'ipv4':
    {'FAMILY_TYPE': [{'unicast': {'network': ['101.1.1.0/24']}}]}}]}},
         {'L3VPN_VRF_02': {'ADDRFAMILY': [{'ipv4': {'FAMILY_TYPE': [
         {'unicast': {'network': ['101.1.1.0/24']}}]}}]}}]}
    #
    result_list = [{'ADDRFAMILY': 'ipv4', 'FAMILY_TYPE': 'unicast',
    'VRF': 'L3VPN_VRF_01', 'network': '101.1.1.0/24'},
    {'ADDRFAMILY': 'ipv4', 'FAMILY_TYPE': 'unicast', 'VRF': 'L3VPN_VRF_02',
    'network': '101.1.1.0/24'}]

    Args:
        * configuration_dictionary (dict): DUT configurations

    Returns:
        * list: List of dictionaries

    Author:
        Anbarasan Shenbagaraj <ashenbag@brocade.com>

    Modifications(user-date-reason) :
    """
    result_list = get_argument_list2(configuration_dictionary)
    return list(flatten(result_list))


def get_argument_list2(configuration_dictionary):
    """ Helper function for get_argument_list

    Calls the main config_to_string_list function to get constructed
    dictionary and list

    Args:
        * configuration_dictionary (dict): DUT configurations

    Returns:
        * list: List of dictionaries

    Author:
        Anbarasan Shenbagaraj <ashenbag@brocade.com>

    Modifications(user-date-reason) :
    """
    result = config_to_string_list(configuration_dictionary)
    if not isinstance(result, list):
        return [result]
    if any(isinstance(element, list) for element in result):
        return [item for sublist in result for item in sublist]
    else:
        return result


def flatten(input_list):
    """ Flatten input list
    (Copied from Internet)

    Args:
       * input_list (list): Input list to flatten

    Returns:
       (generator object): Generator object

    Author:
       Anbarasan Shenbagaraj <ashenbag@brocade.com>

    Modifications(user-date-reason) :
    """
    for i in input_list:
        if isinstance(i, Iterable) and not isinstance(i, str) \
                and not isinstance(i, dict):
            for subc in flatten(i):
                yield subc
        else:
            yield i
