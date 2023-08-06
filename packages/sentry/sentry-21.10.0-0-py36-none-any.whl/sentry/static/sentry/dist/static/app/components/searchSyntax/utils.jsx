Object.defineProperty(exports, "__esModule", { value: true });
exports.isWithinToken = exports.getKeyName = exports.treeTransformer = exports.treeResultLocator = void 0;
const parser_1 = require("./parser");
/**
 * Used internally within treeResultLocator to stop recursion once we've
 * located a matched result.
 */
class TokenResultFound extends Error {
    constructor(result) {
        super();
        this.result = result;
    }
}
/**
 * Used as the marker to skip token traversal in treeResultLocator
 */
const skipTokenMarker = Symbol('Returned to skip visiting a token');
/**
 * Utility function to visit every Token node within an AST tree (in DFS order)
 * and apply a test method that may choose to return some value from that node.
 *
 * You must call the `returnValue` method for a result to be returned.
 *
 * When returnValue is never called and all nodes of the search tree have been
 * visited the noResultValue will be returned.
 */
function treeResultLocator({ tree, visitorTest, noResultValue, }) {
    const returnResult = (result) => new TokenResultFound(result);
    const nodeVisitor = (token) => {
        if (token === null) {
            return;
        }
        const result = visitorTest({ token, returnResult, skipToken: skipTokenMarker });
        // Bubble the result back up.
        //
        // XXX: Using a throw here is a bit easier than threading the return value
        // back up through the recursive call tree.
        if (result instanceof TokenResultFound) {
            throw result;
        }
        // Don't traverse into any nested tokens
        if (result === skipTokenMarker) {
            return;
        }
        switch (token.type) {
            case parser_1.Token.Filter:
                nodeVisitor(token.key);
                nodeVisitor(token.value);
                break;
            case parser_1.Token.KeyExplicitTag:
                nodeVisitor(token.key);
                break;
            case parser_1.Token.KeyAggregate:
                nodeVisitor(token.name);
                token.args && nodeVisitor(token.args);
                nodeVisitor(token.argsSpaceBefore);
                nodeVisitor(token.argsSpaceAfter);
                break;
            case parser_1.Token.LogicGroup:
                token.inner.forEach(nodeVisitor);
                break;
            case parser_1.Token.KeyAggregateArgs:
                token.args.forEach(v => nodeVisitor(v.value));
                break;
            case parser_1.Token.ValueNumberList:
            case parser_1.Token.ValueTextList:
                token.items.forEach((v) => nodeVisitor(v.value));
                break;
            default:
        }
    };
    try {
        tree.forEach(nodeVisitor);
    }
    catch (error) {
        if (error instanceof TokenResultFound) {
            return error.result;
        }
        throw error;
    }
    return noResultValue;
}
exports.treeResultLocator = treeResultLocator;
/**
 * Utility function to visit every Token node within an AST tree and apply
 * a transform to those nodes.
 */
function treeTransformer({ tree, transform }) {
    const nodeVisitor = (token) => {
        if (token === null) {
            return null;
        }
        switch (token.type) {
            case parser_1.Token.Filter:
                return transform(Object.assign(Object.assign({}, token), { key: nodeVisitor(token.key), value: nodeVisitor(token.value) }));
            case parser_1.Token.KeyExplicitTag:
                return transform(Object.assign(Object.assign({}, token), { key: nodeVisitor(token.key) }));
            case parser_1.Token.KeyAggregate:
                return transform(Object.assign(Object.assign({}, token), { name: nodeVisitor(token.name), args: token.args ? nodeVisitor(token.args) : token.args, argsSpaceBefore: nodeVisitor(token.argsSpaceBefore), argsSpaceAfter: nodeVisitor(token.argsSpaceAfter) }));
            case parser_1.Token.LogicGroup:
                return transform(Object.assign(Object.assign({}, token), { inner: token.inner.map(nodeVisitor) }));
            case parser_1.Token.KeyAggregateArgs:
                return transform(Object.assign(Object.assign({}, token), { args: token.args.map(v => (Object.assign(Object.assign({}, v), { value: nodeVisitor(v.value) }))) }));
            case parser_1.Token.ValueNumberList:
            case parser_1.Token.ValueTextList:
                return transform(Object.assign(Object.assign({}, token), { 
                    // TODO(ts): Not sure why `v` cannot be inferred here
                    items: token.items.map((v) => (Object.assign(Object.assign({}, v), { value: nodeVisitor(v.value) }))) }));
            default:
                return transform(token);
        }
    };
    return tree.map(nodeVisitor);
}
exports.treeTransformer = treeTransformer;
/**
 * Utility to get the string name of any type of key.
 */
const getKeyName = (key, options = {}) => {
    const { aggregateWithArgs } = options;
    switch (key.type) {
        case parser_1.Token.KeySimple:
            return key.value;
        case parser_1.Token.KeyExplicitTag:
            return key.key.value;
        case parser_1.Token.KeyAggregate:
            return aggregateWithArgs
                ? `${key.name.value}(${key.args ? key.args.text : ''})`
                : key.name.value;
        default:
            return '';
    }
};
exports.getKeyName = getKeyName;
function isWithinToken(node, position) {
    return position >= node.location.start.offset && position <= node.location.end.offset;
}
exports.isWithinToken = isWithinToken;
//# sourceMappingURL=utils.jsx.map