Object.defineProperty(exports, "__esModule", { value: true });
exports.parseArithmetic = exports.TokenConverter = exports.Operation = void 0;
const tslib_1 = require("tslib");
const locale_1 = require("app/locale");
const grammar_pegjs_1 = (0, tslib_1.__importDefault)(require("./grammar.pegjs"));
// This constant should stay in sync with the backend parser
const MAX_OPERATORS = 10;
const MAX_OPERATOR_MESSAGE = (0, locale_1.t)('Maximum operators exceeded');
class Operation {
    constructor({ operator, lhs = null, rhs }) {
        this.operator = operator;
        this.lhs = lhs;
        this.rhs = rhs;
    }
}
exports.Operation = Operation;
class Term {
    constructor({ term, location }) {
        this.term = term;
        this.location = location;
    }
}
class TokenConverter {
    constructor() {
        this.tokenTerm = (maybeFactor, remainingAdds) => {
            if (remainingAdds.length > 0) {
                remainingAdds[0].lhs = maybeFactor;
                return flatten(remainingAdds);
            }
            else {
                return maybeFactor;
            }
        };
        this.tokenOperation = (operator, rhs) => {
            this.numOperations += 1;
            if (this.numOperations > MAX_OPERATORS &&
                !this.errors.includes(MAX_OPERATOR_MESSAGE)) {
                this.errors.push(MAX_OPERATOR_MESSAGE);
            }
            if (operator === 'divide' && rhs === '0') {
                this.errors.push((0, locale_1.t)('Division by 0 is not allowed'));
            }
            return new Operation({ operator, rhs });
        };
        this.tokenFactor = (primary, remaining) => {
            remaining[0].lhs = primary;
            return flatten(remaining);
        };
        this.tokenField = (term, location) => {
            const field = new Term({ term, location });
            this.fields.push(field);
            return term;
        };
        this.tokenFunction = (term, location) => {
            const func = new Term({ term, location });
            this.functions.push(func);
            return term;
        };
        this.numOperations = 0;
        this.errors = [];
        this.fields = [];
        this.functions = [];
    }
}
exports.TokenConverter = TokenConverter;
// Assumes an array with at least one element
function flatten(remaining) {
    let term = remaining.shift();
    while (remaining.length > 0) {
        const nextTerm = remaining.shift();
        if (nextTerm && term && nextTerm.lhs === null) {
            nextTerm.lhs = term;
        }
        term = nextTerm;
    }
    // Shouldn't happen, tokenTerm checks remaining and tokenFactor should have at least 1 item
    // This is just to help ts out
    if (term === undefined) {
        throw new Error('Unable to parse arithmetic');
    }
    return term;
}
function parseArithmetic(query) {
    const tc = new TokenConverter();
    try {
        const result = grammar_pegjs_1.default.parse(query, { tc });
        return { result, error: tc.errors[0], tc };
    }
    catch (error) {
        return { result: null, error: error.message, tc };
    }
}
exports.parseArithmetic = parseArithmetic;
//# sourceMappingURL=parser.jsx.map