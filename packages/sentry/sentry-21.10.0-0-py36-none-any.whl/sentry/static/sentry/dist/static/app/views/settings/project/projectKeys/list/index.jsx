Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const indicator_1 = require("app/actionCreators/indicator");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const panels_1 = require("app/components/panels");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const routeTitle_1 = (0, tslib_1.__importDefault)(require("app/utils/routeTitle"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const textBlock_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/text/textBlock"));
const keyRow_1 = (0, tslib_1.__importDefault)(require("./keyRow"));
class ProjectKeys extends asyncView_1.default {
    constructor() {
        super(...arguments);
        /**
         * Optimistically remove key
         */
        this.handleRemoveKey = (data) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const oldKeyList = [...this.state.keyList];
            (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Revoking key\u2026'));
            this.setState(state => ({
                keyList: state.keyList.filter(key => key.id !== data.id),
            }));
            const { orgId, projectId } = this.props.params;
            try {
                yield this.api.requestPromise(`/projects/${orgId}/${projectId}/keys/${data.id}/`, {
                    method: 'DELETE',
                });
                (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Revoked key'));
            }
            catch (_err) {
                this.setState({
                    keyList: oldKeyList,
                });
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to revoke key'));
            }
        });
        this.handleToggleKey = (isActive, data) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const oldKeyList = [...this.state.keyList];
            (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Saving changes\u2026'));
            this.setState(state => {
                const keyList = state.keyList.map(key => {
                    if (key.id === data.id) {
                        return Object.assign(Object.assign({}, key), { isActive: !data.isActive });
                    }
                    return key;
                });
                return { keyList };
            });
            const { orgId, projectId } = this.props.params;
            try {
                yield this.api.requestPromise(`/projects/${orgId}/${projectId}/keys/${data.id}/`, {
                    method: 'PUT',
                    data: { isActive },
                });
                (0, indicator_1.addSuccessMessage)(isActive ? (0, locale_1.t)('Enabled key') : (0, locale_1.t)('Disabled key'));
            }
            catch (_err) {
                (0, indicator_1.addErrorMessage)(isActive ? (0, locale_1.t)('Error enabling key') : (0, locale_1.t)('Error disabling key'));
                this.setState({ keyList: oldKeyList });
            }
        });
        this.handleCreateKey = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { orgId, projectId } = this.props.params;
            try {
                const data = yield this.api.requestPromise(`/projects/${orgId}/${projectId}/keys/`, {
                    method: 'POST',
                });
                this.setState(state => ({
                    keyList: [...state.keyList, data],
                }));
                (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Created a new key.'));
            }
            catch (_err) {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to create new key. Please try again.'));
            }
        });
    }
    getTitle() {
        const { projectId } = this.props.params;
        return (0, routeTitle_1.default)((0, locale_1.t)('Client Keys'), projectId, false);
    }
    getEndpoints() {
        const { orgId, projectId } = this.props.params;
        return [['keyList', `/projects/${orgId}/${projectId}/keys/`]];
    }
    renderEmpty() {
        return (<panels_1.Panel>
        <emptyMessage_1.default icon={<icons_1.IconFlag size="xl"/>} description={(0, locale_1.t)('There are no keys active for this project.')}/>
      </panels_1.Panel>);
    }
    renderResults() {
        const { location, organization, routes, params } = this.props;
        const { orgId, projectId } = params;
        const access = new Set(organization.access);
        return (<react_1.Fragment>
        {this.state.keyList.map(key => (<keyRow_1.default api={this.api} access={access} key={key.id} orgId={orgId} projectId={`${projectId}`} data={key} onToggle={this.handleToggleKey} onRemove={this.handleRemoveKey} routes={routes} location={location} params={params}/>))}
        <pagination_1.default pageLinks={this.state.keyListPageLinks}/>
      </react_1.Fragment>);
    }
    renderBody() {
        const access = new Set(this.props.organization.access);
        const isEmpty = !this.state.keyList.length;
        return (<div data-test-id="project-keys">
        <settingsPageHeader_1.default title={(0, locale_1.t)('Client Keys')} action={access.has('project:write') ? (<button_1.default onClick={this.handleCreateKey} size="small" priority="primary" icon={<icons_1.IconAdd size="xs" isCircled/>}>
                {(0, locale_1.t)('Generate New Key')}
              </button_1.default>) : null}/>
        <textBlock_1.default>
          {(0, locale_1.tct)(`To send data to Sentry you will need to configure an SDK with a client key
          (usually referred to as the [code:SENTRY_DSN] value). For more
          information on integrating Sentry with your application take a look at our
          [link:documentation].`, {
                link: <externalLink_1.default href="https://docs.sentry.io/"/>,
                code: <code />,
            })}
        </textBlock_1.default>

        {isEmpty ? this.renderEmpty() : this.renderResults()}
      </div>);
    }
}
exports.default = (0, withOrganization_1.default)(ProjectKeys);
//# sourceMappingURL=index.jsx.map