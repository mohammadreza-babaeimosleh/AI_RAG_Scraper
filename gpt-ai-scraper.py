import pandas as pd
from datetime import datetime

import requests
import ast
from bs4 import BeautifulSoup
import json
from pathlib import Path
import sys
from loguru import logger
from pprint import pprint
import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
import time
import os

import requests
import urllib

from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

import openai
from openai import OpenAI
client = OpenAI(api_key="Place your Key")

from pydantic import BaseModel, ValidationError, validator
from typing import Any, Dict, List, Optional


html_content = """ <div class="ee213fa0"><script type="application/ld+json">{"@context":"https://schema.org","@type":"ItemPage","mainEntity":{"@type":"Product","name":"VACANT | BURJ AL ARAB VIEW | HIGH FLOOR | CALL NOW","url":"https://www.bayut.com/property/details-9332112.html","alternateName":"1 Bedroom Apartment For Sale in Orchid Residence","description":"welcome to this stunning 1-bedroom apartment for sale in orchid residence, located in the prestigious dubai science park. this spacious 812 sqft apartment is priced at aed 950,000 and comes unfurnished, allowing you to personalize it to your taste. the apartment features 2 bathrooms and offers a beautiful community view. the amenities of this property include: - built-in wardrobes,- a balcony- walk-in closet- landmark view- open kitchen- a fitness centre. residents can also enjoy the shared gym and pool within the building. this brand new apartment is perfect for investors looking for a lucrative property in a prime location. presented by f m Properties, the largest real estate agency in dubai with over 700 agents operating from 24 locations. with over 9,200 satisfied clients giving a 4.9-star rating, f m Properties is the most trusted real estate company in dubai. don't miss out on this amazing opportunity to own a piece of luxury in dubai. contact us today to schedule a viewing of this investment property developed by a private owner. ¶ Property Features: ✅ Built In Wardrobes✅ Balcony✅ Walk-In Closet✅ Landmark view✅ Brand new✅ Investment Property✅ Open Kitchen✅ Fitness Centre✅ Shared Gym✅ Shared Pool♣fam Properties  Contact Us - [redacted phone number]  Toll free: 800fam[redacted phone number]  Email: [redacted email address] Visit our website: famproperties. com  Office Registration no: 1858  RERA Broker ID: 8976  Permit No:[redacted phone number]","image":"https://images.bayut.com/thumbnails/730839532-800x600.jpeg","offers":[{"@type":"Offer","priceCurrency":"AED","url":"https://www.bayut.com/property/details-9332112.html","priceSpecification":{"@type":"UnitPriceSpecification","price":950000,"priceCurrency":"AED"},"offeredBy":{"@type":"RealEstateAgent","name":"Momin Mehmood","image":"https://images.bayut.com/thumbnails/96047125-240x180.jpeg","parentOrganization":{"@type":"Organization","name":"fäm Properties - Branch 7","url":"https://www.bayut.com/companies/fam-properties-branch-7-9954/"}}}]}}</script><script type="application/ld+json">{"@context":"https://schema.org","@type":"Apartment","name":"VACANT | BURJ AL ARAB VIEW | HIGH FLOOR | CALL NOW","url":"https://www.bayut.com/property/details-9332112.html","alternateName":"1 Bedroom Apartment For Sale in Orchid Residence","geo":{"@type":"GeoCoordinates","latitude":25.073861,"longitude":55.248326},"floorSize":{"@type":"QuantitativeValue","value":"812","unitText":"SQFT"},"numberOfRooms":{"@type":"QuantitativeValue","name":"Bedroom(s)","value":"1"},"numberOfBathroomsTotal":"2","image":"https://images.bayut.com/thumbnails/730839532-800x600.jpeg","address":{"@type":"PostalAddress","addressCountry":"UAE","addressRegion":"Dubai","addressLocality":"Dubai Science Park"},"containedInPlace":{"@type":"Place","name":"Dubai Science Park","url":"https://www.bayut.com/for-sale/apartments/dubai/dubai-science-park/"}}</script><h2 class="_143094e6">Property Information</h2><ul class="_3dc8d08d" style="columns:2" aria-label="Property details"><li><span class="ed0db22a">Type</span><span class="_2fdf7fc5" aria-label="Type">Apartment</span></li><li><span class="ed0db22a">Purpose</span><span class="_2fdf7fc5" aria-label="Purpose">For Sale</span></li><li><span class="ed0db22a">Reference no.</span><span class="_2fdf7fc5" aria-label="Reference">Bayut - B-AS-113898</span></li><li aria-label="Property completion status"><span class="ed0db22a">Completion</span><span class="_2fdf7fc5" aria-label="Completion status">Ready</span></li><li aria-label="Property TruCheck verification date"><div class="bcf923bd ed0db22a"><span class="aa17eb01">on</span><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60.92 13.76" class="_0e4c1c3e"><g style="isolation:isolate"><text transform="translate(0 10.34)" style="isolation:isolate" font-family="Lato-Medium,Lato" font-size="12" font-weight="500"><tspan letter-spacing="-.11em">T</tspan><tspan x="5.83" y="0">ru</tspan></text><text transform="translate(16.93 10.34)" style="isolation:isolate" font-family="Lato-Bold,Lato" font-size="12" font-weight="700">Check</text><text transform="translate(50.24 6.34)" style="isolation:isolate" font-family="Lato-Medium,Lato" font-size="7" font-weight="500">TM</text></g></svg><span class="_31005c6b">on</span></div><span class="_2fdf7fc5" aria-label="Trucheck date">9 August 2024</span><div class="ea1f54ef"><div><div class="d9150e01"><svg class="_361e75c4"><use xlink:href="/assets/iconInfo_noinline.4760bc9ed0d7c2d8d2d81110e34fe439.svg#info"></use></svg></div></div></div></li><li><div class="bcf923bd ed0db22a">Average Rent</div><span class="_2fdf7fc5" aria-label="Average Rent">Not available</span><div class="a5152284"><div><div class="d9150e01"><svg class="_361e75c4"><use xlink:href="/assets/iconInfo_noinline.4760bc9ed0d7c2d8d2d81110e34fe439.svg#info"></use></svg></div></div><div class="_52908f50 tether-target tether-element-attached-bottom tether-element-attached-center tether-target-attached-top tether-target-attached-center"></div></div></li><li><span class="ed0db22a">Added on</span><span class="_2fdf7fc5" aria-label="Reactivated date">15 July 2024</span></li><li><span class="ed0db22a">Service charges</span><span class="_2fdf7fc5" aria-label="Service charges"><div class="f1fcc55a"><div class="a77b266c"><div class="_7ce0b17e"><div class="f1fcc55a"><div class="_2923a568">AED<span class="_9e0180f9"></span>16.69</div><span class="_7ce0b17e">/ sqft</span></div></div></div><div class="a5152284"><div><div class="_948d9e0a"><svg class="a28a49b2"><use xlink:href="/assets/iconInfo_noinline.4760bc9ed0d7c2d8d2d81110e34fe439.svg#info"></use></svg></div></div></div></div></span></li></ul></div> """
html_content2 = """<div class="c6f9dffc"><h2 class="_461e7694">Features / Amenities</h2><div class="_91c991df"><div class="e3c6da98"><div class="_6499ab17"><svg class="_063ae78a"><use xlink:href="/assets/iconAmenities_noinline.cbb4ef6d5688dfc77d5e9dfa9c789898.svg#balcony-or-terrace"></use></svg></div><div class="_01ade828"><span class="_7181e5ac">Balcony or Terrace</span></div></div><div class="e3c6da98"><div class="_6499ab17"><svg class="_063ae78a"><use xlink:href="/assets/iconAmenities_noinline.cbb4ef6d5688dfc77d5e9dfa9c789898.svg#swimming-pool"></use></svg></div><div class="_01ade828"><span class="_7181e5ac">Swimming Pool</span></div></div><div class="e3c6da98"><div class="_6499ab17"><svg class="_063ae78a"><use xlink:href="/assets/iconAmenities_noinline.cbb4ef6d5688dfc77d5e9dfa9c789898.svg#shared-gym"></use></svg></div><div class="_01ade828"><span class="_7181e5ac">Gym or Health Club</span></div></div></div></div>"""


# ------------------------------------------------------------------------------------------------------------------------------------

class IntegerType(BaseModel):
    value: Optional[int]  # Accepts int or None

class StringType(BaseModel):
    value: Optional[str]  # Accepts str or None

class FloatType(BaseModel):
    value: Optional[float]  # Accepts float or None

class BooleanType(BaseModel):
    value: Optional[bool]  # Accepts bool or None

class ListType(BaseModel):
    value: Optional[List[Any]]  # Accepts List or None

class DateTimeType(BaseModel):
    value: Optional[str]  # Accepts datetime string or None

    # Validator to ensure the string is in a correct datetime format
    @validator('value')
    def check_datetime_format(cls, v):
        try:
            # Attempt to parse the datetime; adjust the format string as necessary
            datetime.strptime(v, '%d-%m-%Y')
        except ValueError:
            if v == 'None':
                return True
            else:
                raise ValueError(f"String '{v}' is not in a valid datetime format")
        return v

# Define a mapping of type names to Pydantic models
type_mapping_for_validation = {
    'integer': IntegerType,
    'string': StringType,
    'float': FloatType,
    'boolian': BooleanType,
    'list': ListType,
    'datetime': DateTimeType
}

type_mapping_for_instruction = {
    'integer': 'integer',
    'string': 'string',
    'float': 'float',
    'boolian': 'boolean',
    'list': 'list',
    'datetime': "datetime.strptime('%d-%m-%Y')"
}

type_mapping_for_tool_call = {
    'integer': 'integer',
    'string': 'string',
    'float': 'float',
    'boolian': 'boolean',
    'list': 'array',
    'datetime': 'string'
}

# ------------------------------------------------------------------------------------------------------------------------------------

def fetch_data():
    data = [
        (("Price", 'integer') ,html_content), 
        (("Building Name", 'string') ,html_content),
        (("Added on", "datetime"), html_content), 
        (("Unit images", 'string'), html_content),
        (("Type", 'string'), html_content),
        (("Reference no.", 'string'), html_content),
        (("Completion", 'string'), html_content),
        (("TruCheck TM on", 'datetime'), html_content),
        (("Average Rent", 'string'), html_content),
        (("Handover date", 'datetime'), html_content),
        (("Property Description", 'string'), html_content),
        (("Service charges", 'string'), html_content),
        (("Year of Completion", 'integer'), html_content),
        (("Total Floors", 'integer'), html_content),
        (("Elevators", 'integer'), html_content),
        (("Features / Amenities", 'list'), html_content2),
    ]

    return data

def fetch_expected_types(data):
    return {item[0][0]: item[0][1] for item in data}

# ------------------------------------------------------------------------------------------------------------------------------------

def validate_entry(entry: Dict[str, Any], expected_types: Dict[str, str]) -> Dict[str, Any]:
    """
    Validate the values in the entry against the expected types.

    :param entry: The dictionary containing variable names and values
    :param expected_types: A dictionary specifying the expected types for each variable
    :return: A dictionary with validation results (True if valid, error message if not)
    """
    validation_results = {}
    for var_name, value in entry.items():
        expected_type = expected_types.get(var_name)
        if expected_type not in type_mapping_for_validation:
            validation_results[var_name] = f"Unknown expected type: {expected_type}"
            continue

        model = type_mapping_for_validation[expected_type]
        try:
            model(value=value)
            validation_results[var_name] = True
        except ValidationError as e:
            validation_results[var_name] = str(e)

    return validation_results

# ------------------------------------------------------------------------------------------------------------------------------------

def build_instructions(data):
  instructions = """Hi GPT, I have HTML content for a webpage about different information of a unit and you are a scraping assisstant.
Extract all the required information completely and with the correct mentioned data type.
if a field does not exist, put "None" in its place (not anything else like '0', 'Null').
The required information are:
  """
  for item in data:
    instructions += f"""\n- Required information: {item[0][0]} , type: {type_mapping_for_instruction[item[0][1]]} or 'None' """

  instructions+= """\n\nIt is extremely important not to miss any part of each required answer.
Do not make up any response and give the exact detail based on the HTML file.
Convert answers into a human-readable form (do not return HTML).
after extracting the required data, to return the answer, you MUST return extracted information each by it's proper given `return_information` tool_choice.
  """
  return instructions

# ------------------------------------------------------------------------------------------------------------------------------------

def build_html_content(data):
    agregated_html = '\n'.join([item[1] for item in data])
    return agregated_html

# ------------------------------------------------------------------------------------------------------------------------------------

def return_information(*args):
    for arg in args:
        print(arg)

# ------------------------------------------------------------------------------------------------------------------------------------

def build_fucntion_tools(data):
    tools = []
    tool = {}
    properties = {}
    for item in data:
        if item[0][1] != 'list':
            instance_property = {
                f'{item[0][0]}': {
                    'type': f'{type_mapping_for_tool_call[item[0][1]]}',
                    'description': f'Required information: {item[0][0]}'
                }
            }
        else:
            instance_property = {
                f'{item[0][0]}': {
                    'type': f'{type_mapping_for_tool_call[item[0][1]]}',
                    'items': {
                        'type': "string"
                    },
                    'description': f'Required information: {item[0][0]}'
                }
            }

        properties.update(instance_property)

    parameters = {
                'type': 'object',
                'properties': properties,
                'required': [f"{item[0][0]}" for item in data],
                "additionalProperties": False
            }

    tool["function"] = {
        'name': "return_information",
        'description': f"Returns extracted information in a proper format to the server",
        'parameters': parameters,
        # 'strict': True,
    }

    tool["type"] = "function"

    tools.append(tool)

    return tools

# ------------------------------------------------------------------------------------------------------------------------------------

def extract_information():

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": f"The HTML conetent that you need to analyse is as follows:\n{html_content}"}
            ],
        temperature = 0,
        tools = tools,
        tool_choice = {"type": "function", "function": {"name": "return_information"}}
        )

    return completion

# ------------------------------------------------------------------------------------------------------------------------------------



# ------------------------------------------------------------------------------------------------------------------------------------

data = fetch_data()
instructions = build_instructions(data)
tools = build_fucntion_tools(data)
expected_types = fetch_expected_types(data)
html_content = build_html_content(data)

from pprint import pprint

info = extract_information()

tool_calls = info.choices[0].message.tool_calls[0]
function_name = tool_calls.function.name
function_arguments = json.loads(tool_calls.function.arguments)
logger.info("Returned Arguments are as follows:")
pprint(function_arguments)

if function_name == "return_information":
    logger.info("GPT used the function")
    # result = return_information(function_arguments.values())
    # print(result)

validation_results = validate_entry(function_arguments, expected_types)
pprint(validation_results)

# ------------------------------------------------------------------------------------------------------------------------------------


