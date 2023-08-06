Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const panels_1 = require("app/components/panels");
const previewFeature_1 = (0, tslib_1.__importDefault)(require("app/components/previewFeature"));
const locale_1 = require("app/locale");
const routeTitle_1 = (0, tslib_1.__importDefault)(require("app/utils/routeTitle"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const reportUri_1 = (0, tslib_1.__importStar)(require("app/views/settings/projectSecurityHeaders/reportUri"));
class ProjectExpectCtReports extends asyncView_1.default {
    getEndpoints() {
        const { orgId, projectId } = this.props.params;
        return [['keyList', `/projects/${orgId}/${projectId}/keys/`]];
    }
    getTitle() {
        const { projectId } = this.props.params;
        return (0, routeTitle_1.default)((0, locale_1.t)('Certificate Transparency (Expect-CT)'), projectId, false);
    }
    getInstructions(keyList) {
        return `Expect-CT: report-uri="${(0, reportUri_1.getSecurityDsn)(keyList)}"`;
    }
    renderBody() {
        const { params } = this.props;
        const { keyList } = this.state;
        if (!keyList) {
            return null;
        }
        return (<div>
        <settingsPageHeader_1.default title={(0, locale_1.t)('Certificate Transparency')}/>

        <previewFeature_1.default />

        <reportUri_1.default keyList={keyList} orgId={params.orgId} projectId={params.orgId}/>

        <panels_1.Panel>
          <panels_1.PanelHeader>{'About'}</panels_1.PanelHeader>
          <panels_1.PanelBody withPadding>
            <p>
              {(0, locale_1.tct)(`[link:Certificate Transparency]
      (CT) is a security standard which helps track and identify valid certificates, allowing identification of maliciously issued certificates`, {
                link: (<externalLink_1.default href="https://en.wikipedia.org/wiki/Certificate_Transparency"/>),
            })}
            </p>
            <p>
              {(0, locale_1.tct)("To configure reports in Sentry, you'll need to configure the [header] a header from your server:", {
                header: <code>Expect-CT</code>,
            })}
            </p>

            <pre>{this.getInstructions(keyList)}</pre>

            <p>
              {(0, locale_1.tct)('For more information, see [link:the article on MDN].', {
                link: (<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Expect-CT"/>),
            })}
            </p>
          </panels_1.PanelBody>
        </panels_1.Panel>
      </div>);
    }
}
exports.default = ProjectExpectCtReports;
//# sourceMappingURL=expectCt.jsx.map