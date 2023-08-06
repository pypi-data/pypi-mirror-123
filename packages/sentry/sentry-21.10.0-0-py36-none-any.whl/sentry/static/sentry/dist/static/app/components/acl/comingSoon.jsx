Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const ComingSoon = () => (<alert_1.default type="info" icon={<icons_1.IconInfo size="md"/>}>
    {(0, locale_1.t)('This feature is coming soon!')}
  </alert_1.default>);
exports.default = ComingSoon;
//# sourceMappingURL=comingSoon.jsx.map