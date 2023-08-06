Object.defineProperty(exports, "__esModule", { value: true });
exports.PluginActions = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const indicator_1 = require("app/actionCreators/indicator");
const modal_1 = require("app/actionCreators/modal");
const issueSyncListElement_1 = (0, tslib_1.__importDefault)(require("app/components/issueSyncListElement"));
const navTabs_1 = (0, tslib_1.__importDefault)(require("app/components/navTabs"));
const locale_1 = require("app/locale");
const plugins_1 = (0, tslib_1.__importDefault)(require("app/plugins"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
class PluginActions extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            issue: null,
            pluginLoading: false,
        };
        this.deleteIssue = () => {
            const plugin = Object.assign(Object.assign({}, this.props.plugin), { issue: null });
            // override plugin.issue so that 'create/link' Modal
            // doesn't think the plugin still has an issue linked
            const endpoint = `/issues/${this.props.group.id}/plugins/${plugin.slug}/unlink/`;
            this.props.api.request(endpoint, {
                success: () => {
                    this.loadPlugin(plugin);
                    (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Successfully unlinked issue.'));
                },
                error: () => {
                    (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to unlink issue'));
                },
            });
        };
        this.loadPlugin = (data) => {
            this.setState({
                pluginLoading: true,
            }, () => {
                plugins_1.default.load(data, () => {
                    const issue = data.issue || null;
                    this.setState({ pluginLoading: false, issue });
                });
            });
        };
        this.handleModalClose = (data) => this.setState({
            issue: (data === null || data === void 0 ? void 0 : data.id) && (data === null || data === void 0 ? void 0 : data.link)
                ? { issue_id: data.id, url: data.link, label: data.label }
                : null,
        });
        this.openModal = () => {
            const { issue } = this.state;
            const { project, group, organization } = this.props;
            const plugin = Object.assign(Object.assign({}, this.props.plugin), { issue });
            (0, modal_1.openModal)(deps => (<PluginActionsModal {...deps} project={project} group={group} organization={organization} plugin={plugin} onSuccess={this.handleModalClose}/>), { onClose: this.handleModalClose });
        };
    }
    componentDidMount() {
        this.loadPlugin(this.props.plugin);
    }
    UNSAFE_componentWillReceiveProps(nextProps) {
        if (this.props.plugin.id !== nextProps.plugin.id) {
            this.loadPlugin(nextProps.plugin);
        }
    }
    render() {
        const { issue } = this.state;
        const plugin = Object.assign(Object.assign({}, this.props.plugin), { issue });
        return (<issueSyncListElement_1.default onOpen={this.openModal} externalIssueDisplayName={issue ? issue.label : null} externalIssueId={issue ? issue.issue_id : null} externalIssueLink={issue ? issue.url : null} onClose={this.deleteIssue} integrationType={plugin.id}/>);
    }
}
exports.PluginActions = PluginActions;
class PluginActionsModal extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            actionType: 'create',
        };
    }
    render() {
        const { Header, Body, group, project, organization, plugin, onSuccess } = this.props;
        const { actionType } = this.state;
        return (<react_1.Fragment>
        <Header closeButton>
          {(0, locale_1.tct)('[name] Issue', { name: plugin.name || plugin.title })}
        </Header>
        <navTabs_1.default underlined>
          <li className={actionType === 'create' ? 'active' : ''}>
            <a onClick={() => this.setState({ actionType: 'create' })}>{(0, locale_1.t)('Create')}</a>
          </li>
          <li className={actionType === 'link' ? 'active' : ''}>
            <a onClick={() => this.setState({ actionType: 'link' })}>{(0, locale_1.t)('Link')}</a>
          </li>
        </navTabs_1.default>
        {actionType && (
            // need the key here so React will re-render
            // with new action prop
            <Body key={actionType}>
            {plugins_1.default.get(plugin).renderGroupActions({
                    plugin,
                    group,
                    project,
                    organization,
                    actionType,
                    onSuccess,
                })}
          </Body>)}
      </react_1.Fragment>);
    }
}
exports.default = (0, withApi_1.default)((0, withOrganization_1.default)(PluginActions));
//# sourceMappingURL=pluginActions.jsx.map