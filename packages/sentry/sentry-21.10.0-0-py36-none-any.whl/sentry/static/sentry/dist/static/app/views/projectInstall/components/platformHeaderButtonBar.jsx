Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const locale_1 = require("app/locale");
function PlatformHeaderButtonBar({ gettingStartedLink, docsLink }) {
    return (<buttonBar_1.default gap={1}>
      <button_1.default size="small" to={gettingStartedLink}>
        {(0, locale_1.t)('< Back')}
      </button_1.default>
      <button_1.default size="small" href={docsLink} external>
        {(0, locale_1.t)('Full Documentation')}
      </button_1.default>
    </buttonBar_1.default>);
}
exports.default = PlatformHeaderButtonBar;
//# sourceMappingURL=platformHeaderButtonBar.jsx.map