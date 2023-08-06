Object.defineProperty(exports, "__esModule", { value: true });
exports.getQuery = void 0;
const tslib_1 = require("tslib");
const pick_1 = (0, tslib_1.__importDefault)(require("lodash/pick"));
const qs = (0, tslib_1.__importStar)(require("query-string"));
const globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
const DEFAULT_STATUS = 'unresolved';
/**
 * Get query for API given the current location.search string
 */
function getQuery(search) {
    const query = qs.parse(search);
    const status = typeof query.status !== 'undefined' ? query.status : DEFAULT_STATUS;
    const queryParams = Object.assign({ status }, (0, pick_1.default)(query, ['cursor', ...Object.values(globalSelectionHeader_1.URL_PARAM)]));
    return queryParams;
}
exports.getQuery = getQuery;
//# sourceMappingURL=utils.jsx.map