import os
import yamlifier
import unittest


TESTDATA = os.path.normpath(os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "..",
    "testdata"))
TEMPLATE = os.path.join(TESTDATA, "template.yaml")
OUTPUT = os.path.join(TESTDATA, "generated.yaml")
OUTPUT_CORRECT = os.path.join(TESTDATA, "generated-correct.yaml")
SUBSTITUTE = {
    "VARIABLE1": "funny person"
}


class TestYamlifier(unittest.TestCase):
    def test_generate(self):
        yamlifier.generate(
            TEMPLATE,
            OUTPUT,
            TESTDATA,
            SUBSTITUTE,
            force=True,
            large=False
        )

        output, output_error = yamlifier.read_file(OUTPUT)
        correct, correct_error = yamlifier.read_file(OUTPUT_CORRECT)

        # tar archive compresses files in different order so output
        # is not binary equivalent.
        self.assertEqual(correct_error, output_error)
        self.assertEqual(len(correct), len(output))

if __name__ == '__main__':
    unittest.main()
