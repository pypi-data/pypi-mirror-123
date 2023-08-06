Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const hookStore_1 = (0, tslib_1.__importDefault)(require("app/stores/hookStore"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const settingsNavigation_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsNavigation"));
const navigationConfiguration_1 = (0, tslib_1.__importDefault)(require("app/views/settings/organization/navigationConfiguration"));
class OrganizationSettingsNavigation extends React.Component {
    constructor() {
        super(...arguments);
        this.state = this.getHooks();
        /**
         * TODO(epurkhiser): Becase the settings organization navigation hooks
         * do not conform to a normal component style hook, and take a single
         * parameter 'organization', we cannot use the `Hook` component here,
         * and must resort to using listening to the HookStore to retrieve hook data.
         *
         * We should update the hook interface for the two hooks used here
         */
        this.unsubscribe = hookStore_1.default.listen((hookName, hooks) => {
            this.handleHooks(hookName, hooks);
        }, undefined);
    }
    componentDidMount() {
        // eslint-disable-next-line react/no-did-mount-set-state
        this.setState(this.getHooks());
    }
    componentWillUnmount() {
        this.unsubscribe();
    }
    getHooks() {
        // Allow injection via getsentry et all
        const { organization } = this.props;
        return {
            hookConfigs: hookStore_1.default.get('settings:organization-navigation-config').map(cb => cb(organization)),
            hooks: hookStore_1.default.get('settings:organization-navigation').map(cb => cb(organization)),
        };
    }
    handleHooks(name, hooks) {
        const org = this.props.organization;
        if (name !== 'settings:organization-navigation-config') {
            return;
        }
        this.setState({ hookConfigs: hooks.map(cb => cb(org)) });
    }
    render() {
        const { hooks, hookConfigs } = this.state;
        const { organization } = this.props;
        const access = new Set(organization.access);
        const features = new Set(organization.features);
        return (<settingsNavigation_1.default navigationObjects={navigationConfiguration_1.default} access={access} features={features} organization={organization} hooks={hooks} hookConfigs={hookConfigs}/>);
    }
}
exports.default = (0, withOrganization_1.default)(OrganizationSettingsNavigation);
//# sourceMappingURL=organizationSettingsNavigation.jsx.map