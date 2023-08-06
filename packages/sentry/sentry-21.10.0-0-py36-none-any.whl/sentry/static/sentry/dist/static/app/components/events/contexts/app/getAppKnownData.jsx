Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const metaProxy_1 = require("app/components/events/meta/metaProxy");
const utils_1 = require("app/utils");
const getAppKnownDataDetails_1 = (0, tslib_1.__importDefault)(require("./getAppKnownDataDetails"));
function getAppKnownData(event, data, appKnownDataValues) {
    const knownData = [];
    const dataKeys = appKnownDataValues.filter(appKnownDataValue => (0, utils_1.defined)(data[appKnownDataValue]));
    for (const key of dataKeys) {
        const knownDataDetails = (0, getAppKnownDataDetails_1.default)(event, data, key);
        knownData.push(Object.assign(Object.assign({ key }, knownDataDetails), { meta: (0, metaProxy_1.getMeta)(data, key) }));
    }
    return knownData;
}
exports.default = getAppKnownData;
//# sourceMappingURL=getAppKnownData.jsx.map