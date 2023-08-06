Object.defineProperty(exports, "__esModule", { value: true });
exports.createFuzzySearch = exports.loadFuzzySearch = void 0;
const tslib_1 = require("tslib");
const constants_1 = require("app/constants");
function loadFuzzySearch() {
    return Promise.resolve().then(() => (0, tslib_1.__importStar)(require('fuse.js')));
}
exports.loadFuzzySearch = loadFuzzySearch;
function createFuzzySearch(objects, options) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        if (!options.keys) {
            throw new Error('You need to define `options.keys`');
        }
        const { default: Fuse } = yield loadFuzzySearch();
        const opts = Object.assign(Object.assign({}, constants_1.DEFAULT_FUSE_OPTIONS), options);
        return new Fuse(objects, opts);
    });
}
exports.createFuzzySearch = createFuzzySearch;
//# sourceMappingURL=createFuzzySearch.jsx.map