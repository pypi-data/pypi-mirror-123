Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const types_1 = require("./types");
const EMAIL_REGEX = /[^@]+@[^\.]+\..+/;
function getUserKnownDataDetails(data, type) {
    switch (type) {
        case types_1.UserKnownDataType.NAME:
            return {
                subject: (0, locale_1.t)('Name'),
                value: data.name,
            };
        case types_1.UserKnownDataType.USERNAME:
            return {
                subject: (0, locale_1.t)('Username'),
                value: data.username,
            };
        case types_1.UserKnownDataType.ID:
            return {
                subject: (0, locale_1.t)('ID'),
                value: data.id,
            };
        case types_1.UserKnownDataType.IP_ADDRESS:
            return {
                subject: (0, locale_1.t)('IP Address'),
                value: data.ip_address,
            };
        case types_1.UserKnownDataType.EMAIL:
            return {
                subject: (0, locale_1.t)('Email'),
                value: data.email,
                subjectIcon: EMAIL_REGEX.test(data.email) && (<externalLink_1.default href={`mailto:${data.email}`} className="external-icon">
            <icons_1.IconMail size="xs"/>
          </externalLink_1.default>),
            };
        default:
            return undefined;
    }
}
exports.default = getUserKnownDataDetails;
//# sourceMappingURL=getUserKnownDataDetails.jsx.map