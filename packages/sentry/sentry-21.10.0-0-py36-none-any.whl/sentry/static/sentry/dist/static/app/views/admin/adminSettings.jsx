Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const isUndefined_1 = (0, tslib_1.__importDefault)(require("lodash/isUndefined"));
const panels_1 = require("app/components/panels");
const locale_1 = require("app/locale");
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const forms_1 = require("app/views/settings/components/forms");
const options_1 = require("./options");
const optionsAvailable = [
    'system.url-prefix',
    'system.admin-email',
    'system.support-email',
    'system.security-email',
    'system.rate-limit',
    'auth.allow-registration',
    'auth.ip-rate-limit',
    'auth.user-rate-limit',
    'api.rate-limit.org-create',
    'beacon.anonymous',
];
class AdminSettings extends asyncView_1.default {
    get endpoint() {
        return '/internal/options/';
    }
    getEndpoints() {
        return [['data', this.endpoint]];
    }
    renderBody() {
        var _a;
        const { data } = this.state;
        const initialData = {};
        const fields = {};
        for (const key of optionsAvailable) {
            // TODO(dcramer): we should not be mutating options
            const option = (_a = data[key]) !== null && _a !== void 0 ? _a : { field: {}, value: undefined };
            if ((0, isUndefined_1.default)(option.value) || option.value === '') {
                const defn = (0, options_1.getOption)(key);
                initialData[key] = defn.defaultValue ? defn.defaultValue() : '';
            }
            else {
                initialData[key] = option.value;
            }
            fields[key] = (0, options_1.getOptionField)(key, option.field);
        }
        return (<div>
        <h3>{(0, locale_1.t)('Settings')}</h3>

        <forms_1.Form apiMethod="PUT" apiEndpoint={this.endpoint} initialData={initialData} saveOnBlur>
          <panels_1.Panel>
            <panels_1.PanelHeader>General</panels_1.PanelHeader>
            {fields['system.url-prefix']}
            {fields['system.admin-email']}
            {fields['system.support-email']}
            {fields['system.security-email']}
            {fields['system.rate-limit']}
          </panels_1.Panel>

          <panels_1.Panel>
            <panels_1.PanelHeader>Security & Abuse</panels_1.PanelHeader>
            {fields['auth.allow-registration']}
            {fields['auth.ip-rate-limit']}
            {fields['auth.user-rate-limit']}
            {fields['api.rate-limit.org-create']}
          </panels_1.Panel>

          <panels_1.Panel>
            <panels_1.PanelHeader>Beacon</panels_1.PanelHeader>
            {fields['beacon.anonymous']}
          </panels_1.Panel>
        </forms_1.Form>
      </div>);
    }
}
exports.default = AdminSettings;
//# sourceMappingURL=adminSettings.jsx.map