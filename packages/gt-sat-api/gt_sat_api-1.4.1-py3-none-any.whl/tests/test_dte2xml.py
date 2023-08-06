from gt_sat_api.parsers import dte_to_xml


def test_dte2xml(dte, xml_example):
    """Test XML generated matched the examples"""
    xml_generated = dte_to_xml(dte)
    assert xml_generated == xml_example
