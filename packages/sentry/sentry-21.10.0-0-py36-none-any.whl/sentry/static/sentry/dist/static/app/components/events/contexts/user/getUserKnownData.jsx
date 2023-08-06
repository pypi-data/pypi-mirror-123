Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const metaProxy_1 = require("app/components/events/meta/metaProxy");
const utils_1 = require("app/utils");
const getUserKnownDataDetails_1 = (0, tslib_1.__importDefault)(require("./getUserKnownDataDetails"));
function getUserKnownData(data, userKnownDataValues) {
    const knownData = [];
    const dataKeys = userKnownDataValues.filter(userKnownDataValue => (0, utils_1.defined)(data[userKnownDataValue]));
    for (const key of dataKeys) {
        const knownDataDetails = (0, getUserKnownDataDetails_1.default)(data, key);
        if ((knownDataDetails && !(0, utils_1.defined)(knownDataDetails.value)) || !knownDataDetails) {
            continue;
        }
        knownData.push(Object.assign(Object.assign({ key }, knownDataDetails), { meta: (0, metaProxy_1.getMeta)(data, key), subjectDataTestId: `user-context-${key.toLowerCase()}-value` }));
    }
    return knownData;
}
exports.default = getUserKnownData;
//# sourceMappingURL=getUserKnownData.jsx.map