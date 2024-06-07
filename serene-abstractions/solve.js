#!/usr/bin/env -S deno run --allow-read=tree

// We have the AST (and we have the source code of the program that
// generated it), so we just have to figure out how to execute it.
// In this script, which was painstakingly written by hand, I read
// the tree, parse it, and then attempt to convert it back to JS.
// Once we have the recovered source code, it can trivially be
// executed to yield the flag.

// For the record, this script is of dubious quality. I threw it
// together extremely quickly and it implements only what is
// necessary to execute the provided tree, and nothing else.
// It's also filled with bugs, but it works in this case.

const dump = Deno.readTextFileSync('tree').trim().split('\n')

class Node {
    constructor(name, depth, parent) {
        this.name = name
        this.depth = depth
        this.parent = parent
        this.children = []
        this.properties = {}
    }
}

const processors = {
    'Function': (node, effectiveContent) => {
        if (node.name === 'FunctionBody') {
            return
        }

        node.properties.functionName = effectiveContent[1].replaceAll('\'', '')
    },
    'MemberExpression': node => {
        const isComputed = node.name.split('=')[1].replace(')', '') === 'true'

        node.name = 'MemberExpression'
        node.properties.computed = isComputed
    },
    'Identifier': (node, effectiveContent) => {
        node.properties.string = effectiveContent[1].replaceAll('"', '')

        const remainder = effectiveContent.slice(2).map(value => {
            const [start, end] = value.split('=')
            return [{
                'is_global': 'isGlobal',
                'is_local': 'isLocal',
            }[start] ?? start, JSON.parse(end.replace(/\(|\)/g, ''))]
        })

        Object.assign(node.properties, Object.fromEntries(remainder))
    },
    'NumericLiteral': (node, effectiveContent) => {
        node.properties.value = Number(effectiveContent[1])
    },
    'StringLiteral': (node, effectiveContent) => {
        node.properties.value = effectiveContent[1].replaceAll('"', '')
    },
    'BooleanLiteral': (node, effectiveContent) => {
        node.properties.value = effectiveContent[1] === 'true'
    },
    'CatchClause': (node, effectiveContent) => {
        node.properties.parameter = effectiveContent[1]
    },
    'Var': node => {
        if (node.name !== 'Var') {
            return
        }

        node.properties.skip = true
        node.parent.properties.type = 'var'
    },
    'Const': node => {
        node.properties.skip = true
        node.parent.properties.type = 'const'
    },
    'Let': node => {
        node.properties.skip = true
        node.parent.properties.type = 'let'
    },
    '++': node => {
        node.properties.skip = true
        node.parent.properties.op = '++'
    },
    '--': node => {
        node.properties.skip = true
        node.parent.properties.op = '++'
    }
}

const binaryExpressions = {
    '+': 'Addition',
    '-': 'Subtraction',
    '**': 'Exponentiation',
    '*': 'Multiplication',
    '/': 'Division',
    '%': 'Modulo',
    '===': 'StrictlyEquals',
    '!==': 'StrictlyInequals',
    '==': 'LooselyEquals',
    '!=': 'LooselyInequals',
    '>=': 'GreaterThanEquals',
    '<=': 'LessThanEquals',
    '>': 'GreaterThan',
    '<': 'LessThan',
    '&': 'BitwiseAnd',
    '|': 'BitwiseOr',
    '^': 'BitwiseXor',
    '~': 'BitwiseNot',
    '<<': 'LeftShift',
    '>>>': 'UnsignedRightShift',
    '>>': 'RightShift',
    'instanceof': 'InstanceOf',
    'in': 'In'
}

for (const [operator, name] of Object.entries(binaryExpressions)) {
    processors[operator] = node => {
        if (node.parent.name === 'UnaryExpression') {
            node.parent.properties.op = operator
            node.properties.skip = true
            return
        }

        node.name = 'BinaryExpression'
        node.properties.op = name
    }
}

const rootNode = new Node(Symbol('rootNode'), -1, null, 0)

let lastNode = rootNode

for (const [index, line] of dump.entries()) {
    const depth = (line.match(/ {2}/g) ?? []).length

    const effectiveContent = line.trim().split(' ')

    let node = new Node(effectiveContent[0], depth, null)

    if (node.name.startsWith('(') && node.name.endsWith(')')) {
        node.properties.skip = true
    }

    while (depth < lastNode.depth) { // ascend
        lastNode = lastNode.parent
    }

    if (depth === lastNode.depth) { // sibling
        lastNode.parent.children.push(node)
        node.parent = lastNode.parent
    } else if (depth > lastNode.depth) { // descend
        lastNode.children.push(node)
        node.parent = lastNode
    }

    // very hackish way of accomplishing this
    if (node.parent.name === 'AssignmentExpression' && node.name.endsWith('=')) {
        node.parent.properties.op = node.name
        node.properties.skip = true
    } else {
        for (const nameStart of Object.keys(processors)) {
            if (node.name.startsWith(nameStart)) {
                processors[nameStart](node, effectiveContent)
                break
            }
        }
    }

    // i think this is a bug in LibJS (or it might not be idk)
    if (node.name === 'TryStatement') {
        dump[index + 1] = dump[index + 1].replace('(Block)', 'Try')
        node.properties.skip = true
    }

    lastNode = node
}

const dumpNode = (node, skipped = 0) => {
    // do not dump the root or imaginary nodes
    if (node !== rootNode && !node.properties.skip) {
        let properties = []

        for (const [property, value] of Object.entries(node.properties)) {
            properties.push(`${property} = ${JSON.stringify(value)}`)
        }

        properties = properties.length ? ` (${properties.join('; ')})` : ''

        const indent = '  '.repeat(node.depth - skipped)

        if (Object.hasOwn(node, 'code')) { // the node was transformed
            console.log(indent + node.code)
        } else { // just dump the AST entry for now
            console.log(indent + node.name + properties)
        }
    }

    if (node.properties.skip) {
        skipped++
    }

    for (const child of node.children) {
        dumpNode(child, skipped)
    }
}

const execNode = node => {
    for (const child of node.children) {
        execNode(child) // go from the bottom up
    }

    if (node !== rootNode && !node.properties.skip) {
        switch (node.name) {
            case 'Program':
            case 'ForStatement':
            case 'WhileStatement':
            case 'IfStatement':
                node.code = ' '
                break
            case 'Identifier':
                node.code = node.properties.string
                node.children = []
                break
            case 'BinaryExpression':
                if (node.properties.op) {
                    const [op] = Object.entries(binaryExpressions)
                        .find(([, name]) => name === node.properties.op)
                    node.code = op
                    node.children = []
                } else {
                    node.code = `(${node.children.map(child => child.code).join(' ')})`
                    node.children = []
                }

                break
            case 'VariableDeclaration':
                node.code = node.properties.type + ' ' + node.children[1].code
                node.children = []
                break
            case 'StringLiteral':
                node.code = `\`${node.properties.value}\``
                break
            case 'NumericLiteral':
            case 'BooleanLiteral':
                node.code = String(node.properties.value)
                break
            case 'VariableDeclarator':
                node.code = node.children[0].code
                if (node.children[1]) {
                    node.code += ' = ' + node.children[1].code
                }
                node.children = []
                break
            case 'ReturnStatement':
                node.code = `return ${node.children[0].code}`
                break
            case 'FunctionExpression':
            case 'FunctionDeclaration': {
                let body = node.children[0]

                let parameters = []

                if (body.name === '(Parameters)') {
                    parameters = body.children.map(param => param.code)
                    body = node.children[1]
                }

                node.code = `function ${node.properties.functionName}(`+
                    `${parameters.join(', ')}) {\n` +
                    body.children.map(child => child.code).join('\n') + '\n}'
                node.children = []

                if (node.name === 'FunctionExpression') {
                    node.code = `(${node.code})`
                }

                break
            }
            case 'FunctionBody':
                node.code = node.children[0].children.map(child => child.code).join(';\n')
                break
            case 'MemberExpression':
                if (node.properties.computed) {
                    node.code = `${node.children[0].code}[${node.children[1].code}]`
                } else {
                    node.code = `${node.children[0].code}.${node.children[1].code}`
                }
                node.children = []
                break
            case 'CallExpression':
                node.code = node.children[0].code + '('

                const parameters = []

                for (const child of node.children.slice(1)) {
                    parameters.push(child.code)
                }

                node.code = node.code + parameters.join(', ') + ')'

                node.children = []

                break
            case 'ArrayExpression':
                node.code = `[${node.children.map(child => child.code).join(', ')}]`
                node.children = []
                break
            case 'ExpressionStatement':
                node.code = node.children[0].code + ';'
                node.children = []
                break
            case 'For':
                node.code = 'for ('
                node.code += node.children[0].code
                node.code += '; ' + node.children[1].code
                node.code += '; ' + node.children[2].code
                node.code += ')'
                node.code += node.children[3].code
                node.children = []
                break
            case 'UpdateExpression':
                node.code = node.children[0].code + node.properties.op
                node.children = []
                break
            case 'BlockStatement':
                node.code = '{\n'
                node.code += node.children[0].children.map(child => child.code).join('\n')
                node.code += '\n}'
                break
            case 'AssignmentExpression':
                node.code = '(' + node.children[1].code
                node.code += ` ${node.properties.op} `
                node.code += node.children[2].code + ')'
                node.children = []
                break
            case 'UnaryExpression':
                node.code = node.properties.op + node.children[1].code
                node.children = []
                break
            case 'SpreadExpression':
                node.code = '...' + node.children[0].code
                node.children = []
                break
            case 'If':
                node.code = `if (${node.children[0].code}) `
                node.code += node.children[1].code
                node.children = []
                break
            case 'Else':
                node.code = 'else ' + node.children[0].code
                node.children = []
                break
            case 'Try':
                node.code = 'try ' + node.children[0].code
                break
            case 'CatchClause':
                node.code = ' catch ' + node.properties.parameter
                node.code += node.children[0].code
                node.parent.name = 'CatchParent'
                node.parent.properties.skip = false
                break
            case 'CatchParent':
                node.code = node.children[0].code
                break
            case 'BreakStatement':
                node.code = 'break'
                break
            case 'ConditionalExpression':
                node.code = node.children[0].children[0].code + ' ? '
                node.code += node.children[1].children[0].code + ' : '
                node.code += node.children[2].children[0].code
                node.children = []
                break
            case 'While':
                node.code = 'while (' + node.children[0].code + ')'
                node.code += node.children[1].code
                node.children = []
                break
            default:
                console.warn('TODO', node.name)
                break
        }
    }
}

execNode(rootNode)
dumpNode(rootNode)
