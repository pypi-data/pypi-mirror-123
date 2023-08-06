Object.defineProperty(exports, "__esModule", { value: true });
const locale_1 = require("app/locale");
const types_1 = require("./types");
const getEventExtraDataKnownDataDetails = (data, key) => {
    switch (key) {
        case types_1.EventExtraDataType.CRASHED_PROCESS:
            return {
                subject: (0, locale_1.t)('Crashed Process'),
                value: data[key],
            };
        default:
            return {
                subject: key,
                value: data[key],
            };
    }
};
exports.default = getEventExtraDataKnownDataDetails;
//# sourceMappingURL=getEventExtraDataKnownDataDetails.jsx.map