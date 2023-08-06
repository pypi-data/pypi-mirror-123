Object.defineProperty(exports, "__esModule", { value: true });
exports.getSecurityDsn = void 0;
const tslib_1 = require("tslib");
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const panels_1 = require("app/components/panels");
const locale_1 = require("app/locale");
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const field_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field"));
const textCopyInput_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/textCopyInput"));
const DEFAULT_ENDPOINT = 'https://sentry.example.com/api/security-report/';
function getSecurityDsn(keyList) {
    const endpoint = keyList.length ? keyList[0].dsn.security : DEFAULT_ENDPOINT;
    return (0, getDynamicText_1.default)({
        value: endpoint,
        fixed: DEFAULT_ENDPOINT,
    });
}
exports.getSecurityDsn = getSecurityDsn;
function ReportUri({ keyList, orgId, projectId }) {
    return (<panels_1.Panel>
      <panels_1.PanelHeader>{(0, locale_1.t)('Report URI')}</panels_1.PanelHeader>
      <panels_1.PanelBody>
        <panels_1.PanelAlert type="info">
          {(0, locale_1.tct)("We've automatically pulled these credentials from your available [link:Client Keys]", {
            link: <link_1.default to={`/settings/${orgId}/projects/${projectId}/keys/`}/>,
        })}
        </panels_1.PanelAlert>
        <field_1.default inline={false} flexibleControlStateSize>
          <textCopyInput_1.default>{getSecurityDsn(keyList)}</textCopyInput_1.default>
        </field_1.default>
      </panels_1.PanelBody>
    </panels_1.Panel>);
}
exports.default = ReportUri;
//# sourceMappingURL=reportUri.jsx.map