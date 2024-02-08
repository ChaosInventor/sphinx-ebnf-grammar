# SPDX-FileCopyrightText: 2024-present ChaosInventor <chaosinventor@yandex.com>
#
# SPDX-License-Identifier: MIT

from sphinx_ebnf_grammar import directives


def setup(app):
    app.add_directive("ebnfgrammar", directives.EBNFGrammar)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
