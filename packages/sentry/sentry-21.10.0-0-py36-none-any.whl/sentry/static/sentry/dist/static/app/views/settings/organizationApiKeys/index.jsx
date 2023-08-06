Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_router_1 = require("react-router");
const indicator_1 = require("app/actionCreators/indicator");
const locale_1 = require("app/locale");
const recreateRoute_1 = (0, tslib_1.__importDefault)(require("app/utils/recreateRoute"));
const routeTitle_1 = (0, tslib_1.__importDefault)(require("app/utils/routeTitle"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const organizationApiKeysList_1 = (0, tslib_1.__importDefault)(require("./organizationApiKeysList"));
/**
 * API Keys are deprecated, but there may be some legacy customers that still use it
 */
class OrganizationApiKeys extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.handleRemove = (id) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const oldKeys = [...this.state.keys];
            this.setState(state => ({
                keys: state.keys.filter(({ id: existingId }) => existingId !== id),
            }));
            try {
                yield this.api.requestPromise(`/organizations/${this.props.params.orgId}/api-keys/${id}/`, {
                    method: 'DELETE',
                    data: {},
                });
            }
            catch (_a) {
                this.setState({ keys: oldKeys, busy: false });
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Error removing key'));
            }
        });
        this.handleAddApiKey = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            this.setState({
                busy: true,
            });
            try {
                const data = yield this.api.requestPromise(`/organizations/${this.props.params.orgId}/api-keys/`, {
                    method: 'POST',
                    data: {},
                });
                if (data) {
                    this.setState({ busy: false });
                    react_router_1.browserHistory.push((0, recreateRoute_1.default)(`${data.id}/`, {
                        params: this.props.params,
                        routes: this.props.routes,
                    }));
                    (0, indicator_1.addSuccessMessage)((0, locale_1.t)(`Created a new API key "${data.label}"`));
                }
            }
            catch (_b) {
                this.setState({ busy: false });
            }
        });
    }
    getEndpoints() {
        return [['keys', `/organizations/${this.props.params.orgId}/api-keys/`]];
    }
    getTitle() {
        return (0, routeTitle_1.default)((0, locale_1.t)('API Keys'), this.props.organization.slug, false);
    }
    renderLoading() {
        return this.renderBody();
    }
    renderBody() {
        return (<organizationApiKeysList_1.default loading={this.state.loading} busy={this.state.busy} keys={this.state.keys} onRemove={this.handleRemove} onAddApiKey={this.handleAddApiKey} {...this.props}/>);
    }
}
exports.default = (0, withOrganization_1.default)(OrganizationApiKeys);
//# sourceMappingURL=index.jsx.map