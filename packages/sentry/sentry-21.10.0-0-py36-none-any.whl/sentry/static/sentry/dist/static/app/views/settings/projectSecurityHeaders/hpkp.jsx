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
class ProjectHpkpReports extends asyncView_1.default {
    getEndpoints() {
        const { orgId, projectId } = this.props.params;
        return [['keyList', `/projects/${orgId}/${projectId}/keys/`]];
    }
    getTitle() {
        const { projectId } = this.props.params;
        return (0, routeTitle_1.default)((0, locale_1.t)('HTTP Public Key Pinning (HPKP)'), projectId, false);
    }
    getInstructions(keyList) {
        return ('def middleware(request, response):\n' +
            "    response['Public-Key-Pins'] = \\\n" +
            '        \'pin-sha256="cUPcTAZWKaASuYWhhneDttWpY3oBAkE3h2+soZS7sWs="; \' \\\n' +
            '        \'pin-sha256="M8HztCzM3elUxkcjR2S5P4hhyBNf6lHkmjAHKhpGPWE="; \' \\\n' +
            "        'max-age=5184000; includeSubDomains; ' \\\n" +
            `        \'report-uri="${(0, reportUri_1.getSecurityDsn)(keyList)}"\' \n` +
            '    return response\n');
    }
    getReportOnlyInstructions(keyList) {
        return ('def middleware(request, response):\n' +
            "    response['Public-Key-Pins-Report-Only'] = \\\n" +
            '        \'pin-sha256="cUPcTAZWKaASuYWhhneDttWpY3oBAkE3h2+soZS7sWs="; \' \\\n' +
            '        \'pin-sha256="M8HztCzM3elUxkcjR2S5P4hhyBNf6lHkmjAHKhpGPWE="; \' \\\n' +
            "        'max-age=5184000; includeSubDomains; ' \\\n" +
            `        \'report-uri="${(0, reportUri_1.getSecurityDsn)(keyList)}"\' \n` +
            '    return response\n');
    }
    renderBody() {
        const { params } = this.props;
        const { keyList } = this.state;
        if (!keyList) {
            return null;
        }
        return (<div>
        <settingsPageHeader_1.default title={(0, locale_1.t)('HTTP Public Key Pinning')}/>

        <previewFeature_1.default />

        <reportUri_1.default keyList={keyList} orgId={params.orgId} projectId={params.projectId}/>

        <panels_1.Panel>
          <panels_1.PanelHeader>{(0, locale_1.t)('About')}</panels_1.PanelHeader>

          <panels_1.PanelBody withPadding>
            <p>
              {(0, locale_1.tct)(`[link:HTTP Public Key Pinning]
              (HPKP) is a security feature that tells a web client to associate a specific
              cryptographic public key with a certain web server to decrease the risk of MITM
              attacks with forged certificates. It's enforced by browser vendors, and Sentry
              supports capturing violations using the standard reporting hooks.`, {
                link: (<externalLink_1.default href="https://en.wikipedia.org/wiki/HTTP_Public_Key_Pinning"/>),
            })}
            </p>

            <p>
              {(0, locale_1.t)(`To configure HPKP reports
              in Sentry, you'll need to send a header from your server describing your
              policy, as well specifying the authenticated Sentry endpoint.`)}
            </p>

            <p>
              {(0, locale_1.t)('For example, in Python you might achieve this via a simple web middleware')}
            </p>
            <pre>{this.getInstructions(keyList)}</pre>

            <p>
              {(0, locale_1.t)(`Alternatively you can setup HPKP reports to simply send reports rather than
              actually enforcing the policy`)}
            </p>
            <pre>{this.getReportOnlyInstructions(keyList)}</pre>

            <p>
              {(0, locale_1.tct)(`We recommend setting this up to only run on a percentage of requests, as
              otherwise you may find that you've quickly exhausted your quota. For more
              information, take a look at [link:the documentation on MDN].`, {
                link: (<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Public_Key_Pinning"/>),
            })}
            </p>
          </panels_1.PanelBody>
        </panels_1.Panel>
      </div>);
    }
}
exports.default = ProjectHpkpReports;
//# sourceMappingURL=hpkp.jsx.map