# SPDX-FileCopyrightText: 2024-present ChaosInventor <chaosinventor@yandex.com>
#
# SPDX-License-Identifier: MIT

from docutils import nodes, statemachine
from docutils.parsers.rst import Directive, directives
from parse_ebnf import AST, ASTCommentNode, ASTProductNode


class EBNFGrammar(Directive):
    require_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True

    #TODO: More options and handle them
    option_spec = {
            'title': directives.unchanged,
            }

    has_content = True

    def run(self):
        ast = AST()

        if(len(self.arguments) == 0):
            self.assert_has_content()
            #TODO: Turn content into IO string and parse
        else:
            #TODO: Make file a dependence so that output is regenerated when
            #it is changed
            ebnf = open(self.arguments[0], 'r')
            ast.parse(ebnf.read)
            ebnf.close()

        comments = []
        for node in ast.root:
            if isinstance(node, ASTCommentNode): comments.append(node)
            elif isinstance(node, ASTProductNode):
                #TODO: Handle indention in comments and white space in general better
                text = ''
                for comment in comments:
                    text += comment.data.strip() + '\n'

                #TODO: Fancier rule rendering
                text += '\n``' + repr(node) + '``'

                #FIXME: Use better recursive parsing, this puts the rules in reverse
                #order
                lines = statemachine.string2lines(text, self.state.document.settings.tab_width)
                self.state_machine.insert_input(lines, self.arguments[0] if len(self.arguments) > 0 else '')

                comments.clear()
            else: self.error(f"Unknown node type at root {node}") #TODO: More descriptive errors

        return []
