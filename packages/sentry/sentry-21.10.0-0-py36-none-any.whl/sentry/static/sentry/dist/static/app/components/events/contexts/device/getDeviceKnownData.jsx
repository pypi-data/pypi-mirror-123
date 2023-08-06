Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const metaProxy_1 = require("app/components/events/meta/metaProxy");
const utils_1 = require("app/utils");
const getDeviceKnownDataDetails_1 = (0, tslib_1.__importDefault)(require("./getDeviceKnownDataDetails"));
function getDeviceKnownData(event, data, deviceKnownDataValues) {
    const knownData = [];
    const dataKeys = deviceKnownDataValues.filter(deviceKnownDataValue => (0, utils_1.defined)(data[deviceKnownDataValue]));
    for (const key of dataKeys) {
        const knownDataDetails = (0, getDeviceKnownDataDetails_1.default)(event, data, key);
        knownData.push(Object.assign(Object.assign({ key }, knownDataDetails), { meta: (0, metaProxy_1.getMeta)(data, key), subjectDataTestId: `device-context-${key.toLowerCase()}-value` }));
    }
    return knownData;
}
exports.default = getDeviceKnownData;
//# sourceMappingURL=getDeviceKnownData.jsx.map