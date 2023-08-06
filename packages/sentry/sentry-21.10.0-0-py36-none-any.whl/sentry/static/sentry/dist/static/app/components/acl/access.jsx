Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const isRenderFunc_1 = require("app/utils/isRenderFunc");
const withConfig_1 = (0, tslib_1.__importDefault)(require("app/utils/withConfig"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const DEFAULT_NO_ACCESS_MESSAGE = (<alert_1.default type="error" icon={<icons_1.IconInfo size="md"/>}>
    {(0, locale_1.t)('You do not have sufficient permissions to access this.')}
  </alert_1.default>);
const defaultProps = {
    renderNoAccessMessage: false,
    isSuperuser: false,
    requireAll: true,
    access: [],
};
/**
 * Component to handle access restrictions.
 */
class Access extends React.Component {
    render() {
        const { organization, config, access, requireAll, isSuperuser, renderNoAccessMessage, children, } = this.props;
        const { access: orgAccess } = organization || { access: [] };
        const method = requireAll ? 'every' : 'some';
        const hasAccess = !access || access[method](acc => orgAccess.includes(acc));
        const hasSuperuser = !!(config.user && config.user.isSuperuser);
        const renderProps = {
            hasAccess,
            hasSuperuser,
        };
        const render = hasAccess && (!isSuperuser || hasSuperuser);
        if (!render && typeof renderNoAccessMessage === 'function') {
            return renderNoAccessMessage(renderProps);
        }
        else if (!render && renderNoAccessMessage) {
            return DEFAULT_NO_ACCESS_MESSAGE;
        }
        if ((0, isRenderFunc_1.isRenderFunc)(children)) {
            return children(renderProps);
        }
        return render ? children : null;
    }
}
Access.defaultProps = defaultProps;
exports.default = (0, withOrganization_1.default)((0, withConfig_1.default)(Access));
//# sourceMappingURL=access.jsx.map