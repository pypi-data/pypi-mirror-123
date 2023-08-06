Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const metaProxy_1 = require("app/components/events/meta/metaProxy");
const utils_1 = require("app/utils");
const getOperatingSystemKnownDataDetails_1 = (0, tslib_1.__importDefault)(require("./getOperatingSystemKnownDataDetails"));
function getOperatingSystemKnownData(data, operatingSystemKnownDataValues) {
    const knownData = [];
    const dataKeys = operatingSystemKnownDataValues.filter(operatingSystemKnownDataValue => (0, utils_1.defined)(data[operatingSystemKnownDataValue]));
    for (const key of dataKeys) {
        const knownDataDetails = (0, getOperatingSystemKnownDataDetails_1.default)(data, key);
        knownData.push(Object.assign(Object.assign({ key }, knownDataDetails), { meta: (0, metaProxy_1.getMeta)(data, key) }));
    }
    return knownData;
}
exports.default = getOperatingSystemKnownData;
//# sourceMappingURL=getOperatingSystemKnownData.jsx.map