Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const panels_1 = require("app/components/panels");
const locale_1 = require("app/locale");
const consolidatedScopes_1 = require("app/utils/consolidatedScopes");
const permissionSelection_1 = (0, tslib_1.__importDefault)(require("app/views/settings/organizationDeveloperSettings/permissionSelection"));
const resourceSubscriptions_1 = (0, tslib_1.__importDefault)(require("app/views/settings/organizationDeveloperSettings/resourceSubscriptions"));
class PermissionsObserver extends react_1.Component {
    constructor(props) {
        super(props);
        this.onPermissionChange = (permissions) => {
            this.setState({ permissions });
        };
        this.onEventChange = (events) => {
            this.setState({ events });
        };
        this.state = {
            permissions: this.scopeListToPermissionState(),
            events: this.props.events,
        };
    }
    /**
     * Converts the list of raw API scopes passed in to an object that can
     * before stored and used via `state`. This object is structured by
     * resource and holds "Permission" values. For example:
     *
     *    {
     *      'Project': 'read',
     *      ...,
     *    }
     *
     */
    scopeListToPermissionState() {
        return (0, consolidatedScopes_1.toResourcePermissions)(this.props.scopes);
    }
    render() {
        const { permissions, events } = this.state;
        return (<react_1.Fragment>
        <panels_1.Panel>
          <panels_1.PanelHeader>{(0, locale_1.t)('Permissions')}</panels_1.PanelHeader>
          <panels_1.PanelBody>
            <permissionSelection_1.default permissions={permissions} onChange={this.onPermissionChange} appPublished={this.props.appPublished}/>
          </panels_1.PanelBody>
        </panels_1.Panel>
        <panels_1.Panel>
          <panels_1.PanelHeader>{(0, locale_1.t)('Webhooks')}</panels_1.PanelHeader>
          <panels_1.PanelBody>
            <resourceSubscriptions_1.default permissions={permissions} events={events} onChange={this.onEventChange} webhookDisabled={this.props.webhookDisabled}/>
          </panels_1.PanelBody>
        </panels_1.Panel>
      </react_1.Fragment>);
    }
}
exports.default = PermissionsObserver;
PermissionsObserver.defaultProps = {
    webhookDisabled: false,
    appPublished: false,
};
//# sourceMappingURL=permissionsObserver.jsx.map