# SPDX-FileCopyrightText: 2024-present ChaosInventor <chaosinventor@yandex.com>
#
# SPDX-License-Identifier: MIT

from docutils import nodes
from docutils.parsers.rst import Directive


class EBNFGrammar(Directive):
    def run(self):
        paragraph_node = nodes.paragraph(text="Hello World!")

        return [paragraph_node]
