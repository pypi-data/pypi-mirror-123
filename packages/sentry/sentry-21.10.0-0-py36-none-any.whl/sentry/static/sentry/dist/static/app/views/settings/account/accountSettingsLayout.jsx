Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const organizations_1 = require("app/actionCreators/organizations");
const sentryTypes_1 = (0, tslib_1.__importDefault)(require("app/sentryTypes"));
const withLatestContext_1 = (0, tslib_1.__importDefault)(require("app/utils/withLatestContext"));
const accountSettingsNavigation_1 = (0, tslib_1.__importDefault)(require("app/views/settings/account/accountSettingsNavigation"));
const settingsLayout_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsLayout"));
class AccountSettingsLayout extends React.Component {
    getChildContext() {
        return {
            organization: this.props.organization,
        };
    }
    componentDidUpdate(prevProps) {
        const { organization } = this.props;
        if (prevProps.organization === organization) {
            return;
        }
        // if there is no org in context, SidebarDropdown uses an org from `withLatestContext`
        // (which queries the org index endpoint instead of org details)
        // and does not have `access` info
        if (organization && typeof organization.access === 'undefined') {
            (0, organizations_1.fetchOrganizationDetails)(organization.slug, {
                setActive: true,
                loadProjects: true,
            });
        }
    }
    render() {
        const { organization } = this.props;
        return (<settingsLayout_1.default {...this.props} renderNavigation={() => <accountSettingsNavigation_1.default organization={organization}/>}>
        {this.props.children}
      </settingsLayout_1.default>);
    }
}
AccountSettingsLayout.childContextTypes = {
    organization: sentryTypes_1.default.Organization,
};
exports.default = (0, withLatestContext_1.default)(AccountSettingsLayout);
//# sourceMappingURL=accountSettingsLayout.jsx.map