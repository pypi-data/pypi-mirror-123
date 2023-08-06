Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const metaProxy_1 = require("app/components/events/meta/metaProxy");
const getEventExtraDataKnownDataDetails_1 = (0, tslib_1.__importDefault)(require("./getEventExtraDataKnownDataDetails"));
function getEventExtraDataKnownData(data) {
    const knownData = [];
    const dataKeys = Object.keys(data);
    for (const key of dataKeys) {
        const knownDataDetails = (0, getEventExtraDataKnownDataDetails_1.default)(data, key);
        knownData.push(Object.assign(Object.assign({ key }, knownDataDetails), { meta: (0, metaProxy_1.getMeta)(data, key) }));
    }
    return knownData;
}
exports.default = getEventExtraDataKnownData;
//# sourceMappingURL=getEventExtraDataKnownData.jsx.map