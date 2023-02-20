import os
import logging
import warnings
import unittest
from test.pp_test import PreProcessTest
from test.aly_test import AnalyzeTest
from test.cut_test import CutTest
from test.cho_test import ChooseTest
from test.red_test import RenderTest

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'
    warnings.simplefilter('ignore')
    load_case = unittest.TestLoader().loadTestsFromTestCase
    pp_suite = load_case(PreProcessTest)
    aly_suite = load_case(AnalyzeTest)
    cut_suite = load_case(CutTest)
    cho_suite = load_case(ChooseTest)
    red_suite = load_case(RenderTest)
    alltests = unittest.TestSuite([pp_suite, aly_suite, cut_suite, cho_suite, red_suite])
    runner = unittest.TextTestRunner(verbosity=1)
    runner.run(red_suite)
    # unittest.main()