Object.defineProperty(exports, "__esModule", { value: true });
const loadFixtures_1 = require("sentry-test/loadFixtures");
const parser_1 = require("app/components/searchSyntax/parser");
const utils_1 = require("app/components/searchSyntax/utils");
/**
 * Normalize results to match the json test cases
 */
const normalizeResult = (tokens) => (0, utils_1.treeTransformer)({
    tree: tokens,
    transform: token => {
        // XXX: This attempts to keep the test data simple, only including keys
        // that are really needed to validate functionality.
        // @ts-ignore
        delete token.location;
        // @ts-ignore
        delete token.text;
        // @ts-ignore
        delete token.config;
        if (token.type === parser_1.Token.Filter && token.invalid === null) {
            // @ts-ignore
            delete token.invalid;
        }
        if (token.type === parser_1.Token.ValueIso8601Date) {
            // Date values are represented as ISO strings in the test case json
            return Object.assign(Object.assign({}, token), { value: token.value.toISOString() });
        }
        return token;
    },
});
describe('searchSyntax/parser', function () {
    const testData = (0, loadFixtures_1.loadFixtures)('search-syntax');
    const registerTestCase = (testCase) => it(`handles ${testCase.query}`, () => {
        const result = (0, parser_1.parseSearch)(testCase.query);
        // Handle errors
        if (testCase.raisesError) {
            expect(result).toBeNull();
            return;
        }
        if (result === null) {
            throw new Error('Parsed result as null without raiseError true');
        }
        expect(normalizeResult(result)).toEqual(testCase.result);
    });
    Object.entries(testData).map(([name, cases]) => describe(`${name}`, () => {
        cases.map(registerTestCase);
    }));
});
//# sourceMappingURL=parser.spec.jsx.map