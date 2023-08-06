Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_router_1 = require("react-router");
const locale_1 = require("app/locale");
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const permissionAlert_1 = (0, tslib_1.__importDefault)(require("app/views/settings/project/permissionAlert"));
const keySettings_1 = (0, tslib_1.__importDefault)(require("app/views/settings/project/projectKeys/details/keySettings"));
const keyStats_1 = (0, tslib_1.__importDefault)(require("app/views/settings/project/projectKeys/details/keyStats"));
class ProjectKeyDetails extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.handleRemove = () => {
            const { orgId, projectId } = this.props.params;
            react_router_1.browserHistory.push(`/${orgId}/${projectId}/settings/keys/`);
        };
    }
    getTitle() {
        return (0, locale_1.t)('Key Details');
    }
    getEndpoints() {
        const { keyId, orgId, projectId } = this.props.params;
        return [['data', `/projects/${orgId}/${projectId}/keys/${keyId}/`]];
    }
    renderBody() {
        const { data } = this.state;
        const { params } = this.props;
        return (<div data-test-id="key-details">
        <settingsPageHeader_1.default title={(0, locale_1.t)('Key Details')}/>
        <permissionAlert_1.default />

        <keyStats_1.default api={this.api} params={params}/>

        <keySettings_1.default api={this.api} params={params} data={data} onRemove={this.handleRemove}/>
      </div>);
    }
}
exports.default = ProjectKeyDetails;
//# sourceMappingURL=index.jsx.map