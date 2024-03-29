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
        ast, path = self.getEbnf()

        #This directive's result
        children = []

        comments = []
        for node in ast.root:
            if isinstance(node, ASTCommentNode): comments.append(node)
            elif isinstance(node, ASTProductNode):
                text = ''
                for comment in comments:
                    text += self.commentToText(comment)

                #TODO: Better way to do this? This is copied from the include
                #directive's code
                document = utils.new_document(path, self.state.document.settings)

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

    def getEbnf(self):
        ast = AST()
        path = ''

        if(len(self.arguments) == 0):
            path = self.state.document.current_source

            self.assert_has_content()

            ebnf = io.StringIO('\n'.join(self.content))

            try:
                ast.parse(ebnf.read)
            finally:
                ebnf.close()
        else:
            path = self.arguments[0]

            try:
                ebnf = open(self.arguments[0], 'r')
            except OSError as error:
                self.severe(f'{self.name}: Could not read {self.arguments[0]}.')
            else:
                self.state.document.settings.record_dependencies.add(self.arguments[0])

            try:
                ast.parse(ebnf.read)
            except SyntaxError as error:
                self.error(f'{self.name}: Syntax error in EBNF, {error}')
            finally:
                ebnf.close()

        return ast, path

    def commentToText(self, comment):
        if comment.startLine == comment.endLine:
            return comment.data.strip() + '\n'
        else:
            lines = comment.data.split('\n')
            for rawline in lines:
                line = rawline.expandtabs(self.state.document.settings.tab_width)
                if len(line.strip()) != 0:
                    indent = len(line) - len(line.lstrip())
                    break

            text = ''
            for rawline in lines:
                #TODO: Add warning or error if a line is indented less than the
                #first one. In such a case the comment's text would be lost
                text += f'{rawline[indent:]}\n'
            return text
