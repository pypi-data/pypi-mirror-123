Object.defineProperty(exports, "__esModule", { value: true });
const parser_1 = require("app/components/arithmeticInput/parser");
describe('arithmeticInput/parser', function () {
    it('errors on too many operators', () => {
        expect((0, parser_1.parseArithmetic)('1+1+1+1+1+1+1+1+1+1+1+1').error).toEqual('Maximum operators exceeded');
    });
    it('errors on divide by 0', () => {
        expect((0, parser_1.parseArithmetic)('1/0').error).toEqual('Division by 0 is not allowed');
    });
    it('handles one term', () => {
        expect((0, parser_1.parseArithmetic)('1').result).toStrictEqual('1');
    });
    it('handles some addition', () => {
        expect((0, parser_1.parseArithmetic)('1 + 2').result).toStrictEqual(new parser_1.Operation({
            operator: 'plus',
            lhs: '1',
            rhs: '2',
        }));
    });
    it('handles three term addition', () => {
        expect((0, parser_1.parseArithmetic)('1 + 2 + 3').result).toStrictEqual(new parser_1.Operation({
            operator: 'plus',
            lhs: new parser_1.Operation({
                operator: 'plus',
                lhs: '1',
                rhs: '2',
            }),
            rhs: '3',
        }));
    });
    it('handles some multiplication', () => {
        expect((0, parser_1.parseArithmetic)('1 * 2').result).toStrictEqual(new parser_1.Operation({
            operator: 'multiply',
            lhs: '1',
            rhs: '2',
        }));
    });
    it('handles three term multiplication', () => {
        expect((0, parser_1.parseArithmetic)('1 * 2 * 3').result).toStrictEqual(new parser_1.Operation({
            operator: 'multiply',
            lhs: new parser_1.Operation({
                operator: 'multiply',
                lhs: '1',
                rhs: '2',
            }),
            rhs: '3',
        }));
    });
    it('handles brackets', () => {
        expect((0, parser_1.parseArithmetic)('1 * (2 + 3)').result).toStrictEqual(new parser_1.Operation({
            operator: 'multiply',
            lhs: '1',
            rhs: new parser_1.Operation({
                operator: 'plus',
                lhs: '2',
                rhs: '3',
            }),
        }));
        expect((0, parser_1.parseArithmetic)('(1 + 2) / 3').result).toStrictEqual(new parser_1.Operation({
            operator: 'divide',
            lhs: new parser_1.Operation({
                operator: 'plus',
                lhs: '1',
                rhs: '2',
            }),
            rhs: '3',
        }));
    });
    it('handles order of operations', () => {
        expect((0, parser_1.parseArithmetic)('1 + 2 * 3').result).toStrictEqual(new parser_1.Operation({
            operator: 'plus',
            lhs: '1',
            rhs: new parser_1.Operation({
                operator: 'multiply',
                lhs: '2',
                rhs: '3',
            }),
        }));
        expect((0, parser_1.parseArithmetic)('1 / 2 - 3').result).toStrictEqual(new parser_1.Operation({
            operator: 'minus',
            lhs: new parser_1.Operation({
                operator: 'divide',
                lhs: '1',
                rhs: '2',
            }),
            rhs: '3',
        }));
    });
    it('handles fields and functions', () => {
        expect((0, parser_1.parseArithmetic)('spans.db + measurements.lcp').result).toStrictEqual(new parser_1.Operation({
            operator: 'plus',
            lhs: 'spans.db',
            rhs: 'measurements.lcp',
        }));
        expect((0, parser_1.parseArithmetic)('failure_count() + count_unique(user)').result).toStrictEqual(new parser_1.Operation({
            operator: 'plus',
            lhs: 'failure_count()',
            rhs: 'count_unique(user)',
        }));
    });
});
//# sourceMappingURL=parser.spec.jsx.map