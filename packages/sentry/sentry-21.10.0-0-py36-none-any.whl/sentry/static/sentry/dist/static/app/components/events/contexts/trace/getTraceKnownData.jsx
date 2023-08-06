Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const metaProxy_1 = require("app/components/events/meta/metaProxy");
const utils_1 = require("app/utils");
const getTraceKnownDataDetails_1 = (0, tslib_1.__importDefault)(require("./getTraceKnownDataDetails"));
const types_1 = require("./types");
function getTraceKnownData(data, traceKnownDataValues, event, organization) {
    const knownData = [];
    const dataKeys = traceKnownDataValues.filter(traceKnownDataValue => {
        if (traceKnownDataValue === types_1.TraceKnownDataType.TRANSACTION_NAME) {
            return event === null || event === void 0 ? void 0 : event.tags.find(tag => {
                return tag.key === 'transaction';
            });
        }
        return data[traceKnownDataValue];
    });
    for (const key of dataKeys) {
        const knownDataDetails = (0, getTraceKnownDataDetails_1.default)(data, key, event, organization);
        if ((knownDataDetails && !(0, utils_1.defined)(knownDataDetails.value)) || !knownDataDetails) {
            continue;
        }
        knownData.push(Object.assign(Object.assign({ key }, knownDataDetails), { meta: (0, metaProxy_1.getMeta)(data, key), subjectDataTestId: `trace-context-${key.toLowerCase()}-value` }));
    }
    return knownData;
}
exports.default = getTraceKnownData;
//# sourceMappingURL=getTraceKnownData.jsx.map