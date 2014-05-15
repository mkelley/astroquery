#!/usr/bin/python
import xml.etree.ElementTree as ET
import urllib
import gzip
import io
import os
from utils import Number

oec_server_url = "https://github.com/OpenExoplanetCatalogue/oec_gzip/raw/master/systems.xml.gz"

__all__ = ['xml_element_to_dict','findvalue', 'get_catalogue']

def get_catalogue(filepath=None):
    """
    Parameters
    -----------
    filepath: str or None
        if no filepath is given, remote source is used.

    Returns
    -------
    An Element Tree containing the open exoplanet catalogue
    """

    if filepath is None:
        oec = ET.parse(gzip.GzipFile(fileobj=io.BytesIO(urllib.urlopen(oec_server_url).read())))
    else:
        oec = ET.parse(gzip.GzipFile(filepath)) 
    return oec

def xml_element_to_dict(e):
    """ 
    Parameters
    ----------
    e: str
        str of an xml tree

    Returns
    -------
    A dictionary of the given xml tree
    """

    d = {}
    for c in e.getchildren():
        d[c.tag] = c.text
    return d

def findvalue( element, searchstring):
    """ (str) -> Number
    Find the tag given by searchstring and return its data as a Number object.
    """
    """
    Parameters
    ----------
    element: Element
        Element from the ElementTree module.
    searchstring: str
        name of the tag to look for in element

    Returns
    -------
    None if tag does not exist.
    str if the tag cannot be expressed as a float.
    Number if the tag is a numerical value
    """

    res = element.find(searchstring)
    if res is None:
        return None
    try:
        float(res.text)
    except:
        if res.text is not None:
            return res.text
    if len(res.attrib) == 0:
       return Number(res.text) 
    tempnum = Number(res.text)
    if res.attrib.has_key("errorminus"):
        tempnum.errorminus = res.attrib["errorminus"]
    if res.attrib.has_key("errorplus"):
        tempnum.errorplus = res.attrib["errorplus"]
    if res.attrib.has_key("upperlimit"):
        tempnum.upperlimit = res.attrib["upperlimit"]
    if res.attrib.has_key("lowerlimit"):
        tempnum.lowerlimit = res.attrib["lowerlimit"]
    return tempnum 
