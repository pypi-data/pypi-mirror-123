#!/usr/bin/env python3

import io
import os
import sys
import tempfile
from shutil import copyfile
from unittest import TestCase, main

from basic_test_case import BasicTestCase

from readalongs.app import app
from readalongs.cli import prepare, tokenize
from readalongs.log import LOGGER


class TestTokenizeCli(BasicTestCase):
    def setUp(self):
        super().setUp()

        self.xmlfile = os.path.join(self.tempdir, "fra.xml")
        _ = self.runner.invoke(
            prepare, ["-l", "fra", os.path.join(self.data_dir, "fra.txt"), self.xmlfile]
        )

    def test_invoke_tok(self):
        results = self.runner.invoke(
            tokenize, [self.xmlfile, os.path.join(self.tempdir, "delme")]
        )
        self.assertEqual(results.exit_code, 0)
        self.assertTrue(os.path.exists(os.path.join(self.tempdir, "delme.xml")))

    def test_generate_output_name(self):
        results = self.runner.invoke(tokenize, ["--debug", self.xmlfile])
        self.assertEqual(results.exit_code, 0)
        self.assertTrue(os.path.exists(os.path.join(self.tempdir, "fra.tokenized.xml")))

    def test_with_stdin(self):
        with io.open(self.xmlfile) as f:
            inputtext = f.read()
        results = self.runner.invoke(tokenize, "-", input=inputtext)
        self.assertEqual(results.exit_code, 0)
        self.assertIn(
            "<s><w>Ceci</w> <w>est</w> <w>une</w> <w>phrase</w>", results.output
        )

    def test_file_already_exists(self):
        results = self.runner.invoke(tokenize, [self.xmlfile, self.xmlfile])
        self.assertNotEqual(results.exit_code, 0)
        self.assertIn("use -f to overwrite", results.output)

    def test_bad_input(self):
        results = self.runner.invoke(tokenize, "- -", input="this is not XML!")
        self.assertNotEqual(results.exit_code, 0)
        self.assertIn("Error parsing", results.output)
        # LOGGER.warning("Output: {}".format(results.output))
        # LOGGER.warning("Exception: {}".format(results.exception))


if __name__ == "__main__":
    main()
