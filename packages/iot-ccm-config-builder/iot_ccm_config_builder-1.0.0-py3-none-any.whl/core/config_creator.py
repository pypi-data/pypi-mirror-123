import json
from core import utils

choices = ["support_capability", "network_interface_capability", "application_interface_capability",
           "human_user_interface_capability", "sensing_capability", "actuating_capability", "storing_capability",
           "transferring_capability", "processing_capability", "latent_capability"]

third_choice = ["support_capability", "human_user_interface_capability", "sensing_capability",
                "actuating_capability", "storing_capability", "transferring_capability", "processing_capability",
                "latent_capability"]


def get_mandatory_modules(capability_type):
    if capability_type == "network_interface_capability":
        module_choices = ["mqtt", "websocket"]
    elif capability_type == "application_interface_capability":
        module_choices = ["data", "control"]
    elif capability_type == "support_capability":
        module_choices = ["configure", "authentication"]
    else:
        module_choices = None

    return module_choices


def set_optional_capabilities():
    optional_capabilities = {}
    boolean = True
    while boolean:
        boolean = utils.create_boolean_question("Would you like to add another capability?")
        if boolean:
            capability_type = utils.create_string_question("Choose any capability among: ", choices)
            module_choices = get_mandatory_modules(capability_type)
            capability_info = set_capability_info(module_choices)
            capability = {capability_type: capability_info}
            optional_capabilities.update(capability)

    return optional_capabilities


def set_capability_info(module_name=None):
    capability = {}

    if module_name:
        utils.create_json_question("Describe the module " + module_name + " using JSON format: ")

    capability_name = utils.create_string_question("Capability name: ")
    capability.update({"capability_name": capability_name})
    capability_id = utils.create_string_question("Capability id: ")
    capability.update({"capability_id": capability_id})
    boolean = utils.create_boolean_question("Would like to add more elements to the capability? ")
    if boolean:
        module = utils.create_json_question("Describe the capability's elements using JSON format: ")
        capability.update({"module": module})

    return capability


def set_mandatory_capabilities():
    mandatory_capabilities = {}

    mandatory_cap1_module = utils.create_string_question("Mandatory capability 1/3 - Network capability: ",
                                                         ["mqtt", "websocket"])
    mandatory_cap1_info = set_capability_info(mandatory_cap1_module)
    mandatory_cap1 = {"network_interface_capability": mandatory_cap1_info}
    mandatory_capabilities.update(mandatory_cap1)

    mandatory_cap2_module = utils.create_string_question(
        "Mandatory capability 2/3 - Application Interface capability name: ",
        ["data", "control"])
    mandatory_cap2_info = set_capability_info(mandatory_cap2_module)
    mandatory_cap2 = {"application_interface_capability": mandatory_cap2_info}
    mandatory_capabilities.update(mandatory_cap2)

    mandatory_cap3_type = utils.create_string_question("Mandatory capability 3/3 - Choose any capability among: ",
                                                       third_choice)
    mandatory_cap3_module = get_mandatory_modules(mandatory_cap3_type)
    mandatory_cap3_info = set_capability_info(mandatory_cap3_module)
    mandatory_cap3 = {mandatory_cap3_type: mandatory_cap3_info}
    mandatory_capabilities.update(mandatory_cap3)

    return mandatory_capabilities


def set_component_capabilities():
    capabilities = {}

    mandatory_capabilities = set_mandatory_capabilities()
    capabilities['mandatory_capabilities'] = mandatory_capabilities

    optional_capabilities = set_optional_capabilities()
    capabilities['optional_capabilities'] = optional_capabilities

    return capabilities


def set_component_location():
    location_json = {}
    location_id = utils.create_string_question("Location id: ")
    location_json['location_id'] = location_id

    location_module = utils.create_json_question("Describe the location using JSON format:")
    location_module['module'] = location_module

    return location_json


def init_config():
    component = {}
    component_name = utils.create_string_question("Component name: ")
    component['component_name'] = component_name
    component_id = utils.create_string_question("Component id: ")
    component['component_id'] = component_id
    component_description = utils.create_string_question("Component description: ")
    component['component_description'] = component_description
    component_location = set_component_location()
    component['component_location'] = component_location
    component_capabilities = set_component_capabilities()
    component['capabilities'] = component_capabilities

    return component


def create_config():
    """ Initializes the request for the creation of a configuration file

    Returns:

    """
    create_bool = utils.create_boolean_question("Create a new config file?")
    if create_bool:
        filename = utils.create_string_question("Name the configurations file: ")
        with open('docs/' + filename + '.json', 'w') as outfile:
            config_json = init_config()
            json.dump(config_json, outfile)
        print("Configurations file successfully created!")
    else:
        print("Configurations file hasn't been created..")
