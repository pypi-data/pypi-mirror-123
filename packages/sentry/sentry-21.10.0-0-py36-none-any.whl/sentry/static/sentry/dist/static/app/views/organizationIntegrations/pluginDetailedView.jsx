Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const modal = (0, tslib_1.__importStar)(require("app/actionCreators/modal"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const contextPickerModal_1 = (0, tslib_1.__importDefault)(require("app/components/contextPickerModal"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const abstractIntegrationDetailedView_1 = (0, tslib_1.__importDefault)(require("./abstractIntegrationDetailedView"));
const installedPlugin_1 = (0, tslib_1.__importDefault)(require("./installedPlugin"));
const pluginDeprecationAlert_1 = (0, tslib_1.__importDefault)(require("./pluginDeprecationAlert"));
class PluginDetailedView extends abstractIntegrationDetailedView_1.default {
    constructor() {
        super(...arguments);
        this.handleResetConfiguration = (projectId) => {
            // make a copy of our project list
            const projectList = this.plugin.projectList.slice();
            // find the index of the project
            const index = projectList.findIndex(item => item.projectId === projectId);
            // should match but quit if it doesn't
            if (index < 0) {
                return;
            }
            // remove from array
            projectList.splice(index, 1);
            // update state
            this.setState({
                plugins: [Object.assign(Object.assign({}, this.state.plugins[0]), { projectList })],
            });
        };
        this.handlePluginEnableStatus = (projectId, enable = true) => {
            // make a copy of our project list
            const projectList = this.plugin.projectList.slice();
            // find the index of the project
            const index = projectList.findIndex(item => item.projectId === projectId);
            // should match but quit if it doesn't
            if (index < 0) {
                return;
            }
            // update item in array
            projectList[index] = Object.assign(Object.assign({}, projectList[index]), { enabled: enable });
            // update state
            this.setState({
                plugins: [Object.assign(Object.assign({}, this.state.plugins[0]), { projectList })],
            });
        };
        this.handleAddToProject = () => {
            const plugin = this.plugin;
            const { organization, router } = this.props;
            this.trackIntegrationAnalytics('integrations.plugin_add_to_project_clicked');
            modal.openModal(modalProps => (<contextPickerModal_1.default {...modalProps} nextPath={`/settings/${organization.slug}/projects/:projectId/plugins/${plugin.id}/`} needProject needOrg={false} onFinish={path => {
                    modalProps.closeModal();
                    router.push(path);
                }}/>), { allowClickClose: false });
        };
    }
    getEndpoints() {
        const { orgId, integrationSlug } = this.props.params;
        return [
            ['plugins', `/organizations/${orgId}/plugins/configs/?plugins=${integrationSlug}`],
        ];
    }
    get integrationType() {
        return 'plugin';
    }
    get plugin() {
        return this.state.plugins[0];
    }
    get description() {
        return this.plugin.description || '';
    }
    get author() {
        var _a;
        return (_a = this.plugin.author) === null || _a === void 0 ? void 0 : _a.name;
    }
    get resourceLinks() {
        return this.plugin.resourceLinks || [];
    }
    get installationStatus() {
        return this.plugin.projectList.length > 0 ? 'Installed' : 'Not Installed';
    }
    get integrationName() {
        return `${this.plugin.name}${this.plugin.isHidden ? ' (Legacy)' : ''}`;
    }
    get featureData() {
        return this.plugin.featureDescriptions;
    }
    getTabDisplay(tab) {
        // we want to show project configurations to make it more clear
        if (tab === 'configurations') {
            return 'project configurations';
        }
        return 'overview';
    }
    renderTopButton(disabledFromFeatures, userHasAccess) {
        if (userHasAccess) {
            return (<AddButton data-test-id="install-button" disabled={disabledFromFeatures} onClick={this.handleAddToProject} size="small" priority="primary">
          {(0, locale_1.t)('Add to Project')}
        </AddButton>);
        }
        return this.renderRequestIntegrationButton();
    }
    renderConfigurations() {
        const plugin = this.plugin;
        const { organization } = this.props;
        if (plugin.projectList.length) {
            return (<react_1.Fragment>
          <pluginDeprecationAlert_1.default organization={organization} plugin={plugin}/>
          <div>
            {plugin.projectList.map((projectItem) => (<installedPlugin_1.default key={projectItem.projectId} organization={organization} plugin={plugin} projectItem={projectItem} onResetConfiguration={this.handleResetConfiguration} onPluginEnableStatusChange={this.handlePluginEnableStatus} trackIntegrationAnalytics={this.trackIntegrationAnalytics}/>))}
          </div>
        </react_1.Fragment>);
        }
        return this.renderEmptyConfigurations();
    }
}
const AddButton = (0, styled_1.default)(button_1.default) `
  margin-bottom: ${(0, space_1.default)(1)};
`;
exports.default = (0, withOrganization_1.default)(PluginDetailedView);
//# sourceMappingURL=pluginDetailedView.jsx.map