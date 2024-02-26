# SPDX-FileCopyrightText: 2024-present ChaosInventor <chaosinventor@yandex.com>
#
# SPDX-License-Identifier: MIT

import io
from docutils import nodes, statemachine, utils, parsers
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

            ebnf = io.StringIO('\n'.join(self.content))

            ast.parse(ebnf.read)
            ebnf.close()
        else:
            try:
                ebnf = open(self.arguments[0], 'r')
            except OSError as error:
                self.severe(f'{self.name}: Could not read {self.arguments[0]}.')
            else:
                self.state.document.settings.record_dependencies.add(self.arguments[0])

            ast.parse(ebnf.read)
            ebnf.close()

        children = []

        comments = []
        for node in ast.root:
            if isinstance(node, ASTCommentNode): comments.append(node)
            elif isinstance(node, ASTProductNode):
                #TODO: Handle indention in comments and white space in general better
                text = ''
                for comment in comments:
                    text += comment.data.strip() + '\n'

                #TODO: Better way to do this? This is copied from the include
                #directive's code
                document = utils.new_document('', self.state.document.settings)

                parser = parsers.rst.Parser()
                parser.parse(text, document)

                document.transformer.populate_from_components((parser,))
                document.transformer.apply_transforms()

                for child in document.children:
                    children.append(child)

                comments.clear()

                #TODO: Fancier rule rendering and white space handling
                children.append(nodes.literal(text=repr(node)))
            else: self.error(f"Unknown node type at root {node}") #TODO: More descriptive errors

        return children
