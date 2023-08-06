Object.defineProperty(exports, "__esModule", { value: true });
const locale_1 = require("app/locale");
const types_1 = require("./types");
function getRuntimeKnownDataDetails(data, type) {
    switch (type) {
        case types_1.RuntimeKnownDataType.NAME:
            return {
                subject: (0, locale_1.t)('Name'),
                value: data.name,
            };
        case types_1.RuntimeKnownDataType.VERSION:
            return {
                subject: (0, locale_1.t)('Version'),
                value: `${data.version}${data.build ? `(${data.build})` : ''}`,
            };
        default:
            return {
                subject: type,
                value: data[type],
            };
    }
}
exports.default = getRuntimeKnownDataDetails;
//# sourceMappingURL=getRuntimeKnownDataDetails.jsx.map