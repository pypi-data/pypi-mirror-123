Object.defineProperty(exports, "__esModule", { value: true });
const locale_1 = require("app/locale");
const utils_1 = require("../utils");
const types_1 = require("./types");
function getAppKnownDataDetails(event, data, type) {
    switch (type) {
        case types_1.AppKnownDataType.ID:
            return {
                subject: (0, locale_1.t)('ID'),
                value: data.app_id,
            };
        case types_1.AppKnownDataType.START_TIME:
            return {
                subject: (0, locale_1.t)('Start Time'),
                value: (0, utils_1.getRelativeTimeFromEventDateCreated)(event.dateCreated ? event.dateCreated : event.dateReceived, data.app_start_time),
            };
        case types_1.AppKnownDataType.DEVICE_HASH:
            return {
                subject: (0, locale_1.t)('Device'),
                value: data.device_app_hash,
            };
        case types_1.AppKnownDataType.TYPE:
            return {
                subject: (0, locale_1.t)('Build Type'),
                value: data.build_type,
            };
        case types_1.AppKnownDataType.IDENTIFIER:
            return {
                subject: (0, locale_1.t)('Build ID'),
                value: data.app_identifier,
            };
        case types_1.AppKnownDataType.NAME:
            return {
                subject: (0, locale_1.t)('Build Name'),
                value: data.app_name,
            };
        case types_1.AppKnownDataType.VERSION:
            return {
                subject: (0, locale_1.t)('Version'),
                value: data.app_version,
            };
        case types_1.AppKnownDataType.BUILD:
            return {
                subject: (0, locale_1.t)('App Build'),
                value: data.app_build,
            };
        default:
            return {
                subject: type,
                value: data[type],
            };
    }
}
exports.default = getAppKnownDataDetails;
//# sourceMappingURL=getAppKnownDataDetails.jsx.map