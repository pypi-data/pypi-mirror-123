Object.defineProperty(exports, "__esModule", { value: true });
const utils_1 = require("app/components/smartSearchBar/utils");
describe('addSpace()', function () {
    it('should add a space when there is no trailing space', function () {
        expect((0, utils_1.addSpace)('one')).toEqual('one ');
    });
    it('should not add another space when there is already one', function () {
        expect((0, utils_1.addSpace)('one ')).toEqual('one ');
    });
    it('should leave the empty string alone', function () {
        expect((0, utils_1.addSpace)('')).toEqual('');
    });
});
describe('removeSpace()', function () {
    it('should remove a trailing space', function () {
        expect((0, utils_1.removeSpace)('one ')).toEqual('one');
    });
    it('should not remove the last character if it is not a space', function () {
        expect((0, utils_1.removeSpace)('one')).toEqual('one');
    });
    it('should leave the empty string alone', function () {
        expect((0, utils_1.removeSpace)('')).toEqual('');
    });
});
describe('getQueryTerms()', function () {
    it('should extract query terms from a query string', function () {
        let query = 'tagname: ';
        expect((0, utils_1.getQueryTerms)(query, query.length)).toEqual(['tagname:']);
        query = 'tagname:derp browser:';
        expect((0, utils_1.getQueryTerms)(query, query.length)).toEqual(['tagname:derp', 'browser:']);
        query = '   browser:"Chrome 33.0"    ';
        expect((0, utils_1.getQueryTerms)(query, query.length)).toEqual(['browser:"Chrome 33.0"']);
    });
});
describe('getLastTermIndex()', function () {
    it('should provide the index of the last query term, given cursor index', function () {
        let query = 'tagname:';
        expect((0, utils_1.getLastTermIndex)(query, 0)).toEqual(8);
        query = 'tagname:foo'; // 'f' (index 9)
        expect((0, utils_1.getLastTermIndex)(query, 9)).toEqual(11);
        query = 'tagname:foo anothertag:bar'; // 'f' (index 9)
        expect((0, utils_1.getLastTermIndex)(query, 9)).toEqual(11);
    });
});
//# sourceMappingURL=utils.spec.jsx.map