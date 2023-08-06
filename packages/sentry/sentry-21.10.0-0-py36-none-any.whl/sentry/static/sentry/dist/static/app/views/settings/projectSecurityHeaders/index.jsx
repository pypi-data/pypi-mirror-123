Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const panels_1 = require("app/components/panels");
const locale_1 = require("app/locale");
const recreateRoute_1 = (0, tslib_1.__importDefault)(require("app/utils/recreateRoute"));
const routeTitle_1 = (0, tslib_1.__importDefault)(require("app/utils/routeTitle"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const textBlock_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/text/textBlock"));
const reportUri_1 = (0, tslib_1.__importDefault)(require("app/views/settings/projectSecurityHeaders/reportUri"));
class ProjectSecurityHeaders extends asyncView_1.default {
    getEndpoints() {
        const { orgId, projectId } = this.props.params;
        return [['keyList', `/projects/${orgId}/${projectId}/keys/`]];
    }
    getTitle() {
        const { projectId } = this.props.params;
        return (0, routeTitle_1.default)((0, locale_1.t)('Security Headers'), projectId, false);
    }
    getReports() {
        return [
            {
                name: 'Content Security Policy (CSP)',
                url: (0, recreateRoute_1.default)('csp/', this.props),
            },
            {
                name: 'Certificate Transparency (Expect-CT)',
                url: (0, recreateRoute_1.default)('expect-ct/', this.props),
            },
            {
                name: 'HTTP Public Key Pinning (HPKP)',
                url: (0, recreateRoute_1.default)('hpkp/', this.props),
            },
        ];
    }
    renderBody() {
        const { params } = this.props;
        const { keyList } = this.state;
        if (keyList === null) {
            return null;
        }
        return (<div>
        <settingsPageHeader_1.default title={(0, locale_1.t)('Security Header Reports')}/>

        <reportUri_1.default keyList={keyList} projectId={params.projectId} orgId={params.orgId}/>

        <panels_1.Panel>
          <panels_1.PanelHeader>{(0, locale_1.t)('Additional Configuration')}</panels_1.PanelHeader>
          <panels_1.PanelBody withPadding>
            <textBlock_1.default style={{ marginBottom: 20 }}>
              {(0, locale_1.tct)('In addition to the [key_param] parameter, you may also pass the following within the querystring for the report URI:', {
                key_param: <code>sentry_key</code>,
            })}
            </textBlock_1.default>
            <table className="table" style={{ marginBottom: 0 }}>
              <tbody>
                <tr>
                  <th style={{ padding: '8px 5px' }}>sentry_environment</th>
                  <td style={{ padding: '8px 5px' }}>
                    {(0, locale_1.t)('The environment name (e.g. production)')}.
                  </td>
                </tr>
                <tr>
                  <th style={{ padding: '8px 5px' }}>sentry_release</th>
                  <td style={{ padding: '8px 5px' }}>
                    {(0, locale_1.t)('The version of the application.')}
                  </td>
                </tr>
              </tbody>
            </table>
          </panels_1.PanelBody>
        </panels_1.Panel>

        <panels_1.Panel>
          <panels_1.PanelHeader>{(0, locale_1.t)('Supported Formats')}</panels_1.PanelHeader>
          <panels_1.PanelBody>
            {this.getReports().map(({ name, url }) => (<ReportItem key={url}>
                <HeaderName>{name}</HeaderName>
                <button_1.default to={url} priority="primary">
                  {(0, locale_1.t)('Instructions')}
                </button_1.default>
              </ReportItem>))}
          </panels_1.PanelBody>
        </panels_1.Panel>
      </div>);
    }
}
exports.default = ProjectSecurityHeaders;
const ReportItem = (0, styled_1.default)(panels_1.PanelItem) `
  align-items: center;
  justify-content: space-between;
`;
const HeaderName = (0, styled_1.default)('span') `
  font-size: 1.2em;
`;
//# sourceMappingURL=index.jsx.map