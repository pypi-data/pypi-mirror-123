Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const locale_1 = require("app/locale");
function NoStackTraceMessage({ message }) {
    return <alert_1.default type="error">{message !== null && message !== void 0 ? message : (0, locale_1.t)('No or unknown stacktrace')}</alert_1.default>;
}
exports.default = NoStackTraceMessage;
//# sourceMappingURL=noStackTraceMessage.jsx.map