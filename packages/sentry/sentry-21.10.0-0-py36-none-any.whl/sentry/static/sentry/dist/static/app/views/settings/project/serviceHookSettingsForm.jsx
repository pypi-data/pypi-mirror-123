Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const panels_1 = require("app/components/panels");
const locale_1 = require("app/locale");
const apiForm_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/apiForm"));
const booleanField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/booleanField"));
const multipleCheckbox_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/multipleCheckbox"));
const formField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/formField"));
const textField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/textField"));
const EVENT_CHOICES = ['event.alert', 'event.created'].map(e => [e, e]);
class ServiceHookSettingsForm extends react_1.Component {
    constructor() {
        super(...arguments);
        this.onSubmitSuccess = () => {
            const { orgId, projectId } = this.props;
            react_router_1.browserHistory.push(`/settings/${orgId}/projects/${projectId}/hooks/`);
        };
    }
    render() {
        const { initialData, orgId, projectId, hookId } = this.props;
        const endpoint = hookId
            ? `/projects/${orgId}/${projectId}/hooks/${hookId}/`
            : `/projects/${orgId}/${projectId}/hooks/`;
        return (<panels_1.Panel>
        <apiForm_1.default apiMethod={hookId ? 'PUT' : 'POST'} apiEndpoint={endpoint} initialData={initialData} onSubmitSuccess={this.onSubmitSuccess} footerStyle={{
                marginTop: 0,
                paddingRight: 20,
            }} submitLabel={hookId ? (0, locale_1.t)('Save Changes') : (0, locale_1.t)('Create Hook')}>
          <panels_1.PanelHeader>{(0, locale_1.t)('Hook Configuration')}</panels_1.PanelHeader>
          <panels_1.PanelBody>
            <booleanField_1.default name="isActive" label={(0, locale_1.t)('Active')}/>
            <textField_1.default name="url" label={(0, locale_1.t)('URL')} required help={(0, locale_1.t)('The URL which will receive events.')}/>
            <formField_1.default name="events" label={(0, locale_1.t)('Events')} inline={false} help={(0, locale_1.t)('The event types you wish to subscribe to.')}>
              {({ value, onChange }) => (<multipleCheckbox_1.default onChange={onChange} value={value} choices={EVENT_CHOICES}/>)}
            </formField_1.default>
          </panels_1.PanelBody>
        </apiForm_1.default>
      </panels_1.Panel>);
    }
}
exports.default = ServiceHookSettingsForm;
//# sourceMappingURL=serviceHookSettingsForm.jsx.map