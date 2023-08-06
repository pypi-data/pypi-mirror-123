Object.defineProperty(exports, "__esModule", { value: true });
exports.commonInitialization = void 0;
const tslib_1 = require("tslib");
require("focus-visible");
const constants_1 = require("app/constants");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const matchMedia_1 = require("app/utils/matchMedia");
function commonInitialization(config) {
    if (constants_1.NODE_ENV === 'development') {
        Promise.resolve().then(() => (0, tslib_1.__importStar)(require(/* webpackMode: "eager" */ 'app/utils/silence-react-unsafe-warnings')));
    }
    configStore_1.default.loadInitialData(config);
    // setup darkmode + favicon
    (0, matchMedia_1.setupColorScheme)();
}
exports.commonInitialization = commonInitialization;
//# sourceMappingURL=commonInitialization.jsx.map