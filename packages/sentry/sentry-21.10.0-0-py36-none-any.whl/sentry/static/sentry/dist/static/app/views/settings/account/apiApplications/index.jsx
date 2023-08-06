Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const indicator_1 = require("app/actionCreators/indicator");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const panels_1 = require("app/components/panels");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const row_1 = (0, tslib_1.__importDefault)(require("app/views/settings/account/apiApplications/row"));
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const ROUTE_PREFIX = '/settings/account/api/';
class ApiApplications extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.handleCreateApplication = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            (0, indicator_1.addLoadingMessage)();
            try {
                const app = yield this.api.requestPromise('/api-applications/', {
                    method: 'POST',
                });
                (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Created a new API Application'));
                this.props.router.push(`${ROUTE_PREFIX}applications/${app.id}/`);
            }
            catch (_err) {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to remove application. Please try again.'));
            }
        });
        this.handleRemoveApplication = (app) => {
            this.setState({
                appList: this.state.appList.filter(a => a.id !== app.id),
            });
        };
    }
    getEndpoints() {
        return [['appList', '/api-applications/']];
    }
    getTitle() {
        return (0, locale_1.t)('API Applications');
    }
    renderBody() {
        const action = (<button_1.default priority="primary" size="small" onClick={this.handleCreateApplication} icon={<icons_1.IconAdd size="xs" isCircled/>}>
        {(0, locale_1.t)('Create New Application')}
      </button_1.default>);
        const isEmpty = this.state.appList.length === 0;
        return (<div>
        <settingsPageHeader_1.default title="API Applications" action={action}/>

        <panels_1.Panel>
          <panels_1.PanelHeader>{(0, locale_1.t)('Application Name')}</panels_1.PanelHeader>

          <panels_1.PanelBody>
            {!isEmpty ? (this.state.appList.map(app => (<row_1.default api={this.api} key={app.id} app={app} onRemove={this.handleRemoveApplication}/>))) : (<emptyMessage_1.default>
                {(0, locale_1.t)("You haven't created any applications yet.")}
              </emptyMessage_1.default>)}
          </panels_1.PanelBody>
        </panels_1.Panel>
      </div>);
    }
}
exports.default = ApiApplications;
//# sourceMappingURL=index.jsx.map