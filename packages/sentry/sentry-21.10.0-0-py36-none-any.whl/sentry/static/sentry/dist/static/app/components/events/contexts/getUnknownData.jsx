Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const startCase_1 = (0, tslib_1.__importDefault)(require("lodash/startCase"));
const metaProxy_1 = require("app/components/events/meta/metaProxy");
function getUnknownData(allData, knownKeys) {
    return Object.entries(allData)
        .filter(([key]) => key !== 'type' && key !== 'title')
        .filter(([key]) => !knownKeys.includes(key))
        .map(([key, value]) => ({
        key,
        value,
        subject: (0, startCase_1.default)(key),
        meta: (0, metaProxy_1.getMeta)(allData, key),
    }));
}
exports.default = getUnknownData;
//# sourceMappingURL=getUnknownData.jsx.map