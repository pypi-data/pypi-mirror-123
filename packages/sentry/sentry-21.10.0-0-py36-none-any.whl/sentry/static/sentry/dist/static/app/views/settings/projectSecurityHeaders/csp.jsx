Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const access_1 = (0, tslib_1.__importDefault)(require("app/components/acl/access"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const panels_1 = require("app/components/panels");
const previewFeature_1 = (0, tslib_1.__importDefault)(require("app/components/previewFeature"));
const cspReports_1 = (0, tslib_1.__importDefault)(require("app/data/forms/cspReports"));
const locale_1 = require("app/locale");
const routeTitle_1 = (0, tslib_1.__importDefault)(require("app/utils/routeTitle"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const jsonForm_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/jsonForm"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const reportUri_1 = (0, tslib_1.__importStar)(require("app/views/settings/projectSecurityHeaders/reportUri"));
class ProjectCspReports extends asyncView_1.default {
    getEndpoints() {
        const { orgId, projectId } = this.props.params;
        return [
            ['keyList', `/projects/${orgId}/${projectId}/keys/`],
            ['project', `/projects/${orgId}/${projectId}/`],
        ];
    }
    getTitle() {
        const { projectId } = this.props.params;
        return (0, routeTitle_1.default)((0, locale_1.t)('Content Security Policy (CSP)'), projectId, false);
    }
    getInstructions(keyList) {
        return ('def middleware(request, response):\n' +
            "    response['Content-Security-Policy'] = \\\n" +
            '        "default-src *; " \\\n' +
            "        \"script-src 'self' 'unsafe-eval' 'unsafe-inline' cdn.example.com cdn.ravenjs.com; \" \\\n" +
            "        \"style-src 'self' 'unsafe-inline' cdn.example.com; \" \\\n" +
            '        "img-src * data:; " \\\n' +
            '        "report-uri ' +
            (0, reportUri_1.getSecurityDsn)(keyList) +
            '"\n' +
            '    return response\n');
    }
    getReportOnlyInstructions(keyList) {
        return ('def middleware(request, response):\n' +
            "    response['Content-Security-Policy-Report-Only'] = \\\n" +
            '        "default-src \'self\'; " \\\n' +
            '        "report-uri ' +
            (0, reportUri_1.getSecurityDsn)(keyList) +
            '"\n' +
            '    return response\n');
    }
    renderBody() {
        const { orgId, projectId } = this.props.params;
        const { project, keyList } = this.state;
        if (!keyList || !project) {
            return null;
        }
        return (<div>
        <settingsPageHeader_1.default title={(0, locale_1.t)('Content Security Policy')}/>

        <previewFeature_1.default />

        <reportUri_1.default keyList={keyList} orgId={orgId} projectId={projectId}/>

        <form_1.default saveOnBlur apiMethod="PUT" initialData={project.options} apiEndpoint={`/projects/${orgId}/${projectId}/`}>
          <access_1.default access={['project:write']}>
            {({ hasAccess }) => <jsonForm_1.default disabled={!hasAccess} forms={cspReports_1.default}/>}
          </access_1.default>
        </form_1.default>

        <panels_1.Panel>
          <panels_1.PanelHeader>{(0, locale_1.t)('About')}</panels_1.PanelHeader>

          <panels_1.PanelBody withPadding>
            <p>
              {(0, locale_1.tct)(`[link:Content Security Policy]
            (CSP) is a security standard which helps prevent cross-site scripting (XSS),
            clickjacking and other code injection attacks resulting from execution of
            malicious content in the trusted web page context. It's enforced by browser
            vendors, and Sentry supports capturing CSP violations using the standard
            reporting hooks.`, {
                link: (<externalLink_1.default href="https://en.wikipedia.org/wiki/Content_Security_Policy"/>),
            })}
            </p>

            <p>
              {(0, locale_1.tct)(`To configure [csp:CSP] reports
              in Sentry, you'll need to send a header from your server describing your
              policy, as well specifying the authenticated Sentry endpoint.`, {
                csp: <abbr title="Content Security Policy"/>,
            })}
            </p>

            <p>
              {(0, locale_1.t)('For example, in Python you might achieve this via a simple web middleware')}
            </p>
            <pre>{this.getInstructions(keyList)}</pre>

            <p>
              {(0, locale_1.t)(`Alternatively you can setup CSP reports to simply send reports rather than
              actually enforcing the policy`)}
            </p>
            <pre>{this.getReportOnlyInstructions(keyList)}</pre>

            <p>
              {(0, locale_1.tct)(`We recommend setting this up to only run on a percentage of requests, as
              otherwise you may find that you've quickly exhausted your quota. For more
              information, take a look at [link:the article on html5rocks.com].`, {
                link: (<a href="http://www.html5rocks.com/en/tutorials/security/content-security-policy/"/>),
            })}
            </p>
          </panels_1.PanelBody>
        </panels_1.Panel>
      </div>);
    }
}
exports.default = ProjectCspReports;
//# sourceMappingURL=csp.jsx.map