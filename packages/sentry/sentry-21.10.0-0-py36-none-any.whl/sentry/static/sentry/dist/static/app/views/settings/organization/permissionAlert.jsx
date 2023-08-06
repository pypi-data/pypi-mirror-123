Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const access_1 = (0, tslib_1.__importDefault)(require("app/components/acl/access"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const PermissionAlert = (_a) => {
    var { access = ['org:write'] } = _a, props = (0, tslib_1.__rest)(_a, ["access"]);
    return (<access_1.default access={access}>
    {({ hasAccess }) => !hasAccess && (<alert_1.default type="warning" icon={<icons_1.IconWarning size="sm"/>} {...props}>
          {(0, locale_1.t)('These settings can only be edited by users with the organization owner or manager role.')}
        </alert_1.default>)}
  </access_1.default>);
};
exports.default = PermissionAlert;
//# sourceMappingURL=permissionAlert.jsx.map