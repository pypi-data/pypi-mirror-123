Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const autoSelectText_1 = (0, tslib_1.__importDefault)(require("app/components/autoSelectText"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const platformPicker_1 = (0, tslib_1.__importDefault)(require("app/components/platformPicker"));
const sentryDocumentTitle_1 = (0, tslib_1.__importDefault)(require("app/components/sentryDocumentTitle"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const recreateRoute_1 = (0, tslib_1.__importDefault)(require("app/utils/recreateRoute"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const textBlock_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/text/textBlock"));
class ProjectInstallOverview extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.redirectToDocs = (platform) => {
            const { orgId, projectId } = this.props.params;
            const installUrl = this.isGettingStarted
                ? `/organizations/${orgId}/projects/${projectId}/getting-started/${platform}/`
                : (0, recreateRoute_1.default)(`${platform}/`, Object.assign(Object.assign({}, this.props), { stepBack: -1 }));
            react_router_1.browserHistory.push(installUrl);
        };
        this.toggleDsn = () => {
            this.setState(state => ({ showDsn: !state.showDsn }));
        };
    }
    get isGettingStarted() {
        return window.location.href.indexOf('getting-started') > 0;
    }
    getEndpoints() {
        const { orgId, projectId } = this.props.params;
        return [['keyList', `/projects/${orgId}/${projectId}/keys/`]];
    }
    render() {
        const { orgId, projectId } = this.props.params;
        const { keyList, showDsn } = this.state;
        const issueStreamLink = `/organizations/${orgId}/issues/#welcome`;
        return (<div>
        <sentryDocumentTitle_1.default title={(0, locale_1.t)('Instrumentation')} projectSlug={projectId}/>
        <settingsPageHeader_1.default title={(0, locale_1.t)('Configure your application')}/>
        <textBlock_1.default>
          {(0, locale_1.t)('Get started by selecting the platform or language that powers your application.')}
        </textBlock_1.default>

        {showDsn ? (<DsnInfo>
            <DsnContainer>
              <strong>{(0, locale_1.t)('DSN')}</strong>
              <DsnValue>{keyList === null || keyList === void 0 ? void 0 : keyList[0].dsn.public}</DsnValue>
            </DsnContainer>

            <button_1.default priority="primary" to={issueStreamLink}>
              {(0, locale_1.t)('Got it! Take me to the Issue Stream.')}
            </button_1.default>
          </DsnInfo>) : (<p>
            <small>
              {(0, locale_1.tct)('Already have things setup? [link:Get your DSN]', {
                    link: <button_1.default priority="link" onClick={this.toggleDsn}/>,
                })}
              .
            </small>
          </p>)}
        <platformPicker_1.default setPlatform={this.redirectToDocs} showOther={false} organization={this.props.organization}/>
        <p>
          {(0, locale_1.tct)(`For a complete list of client integrations, please see
             [docLink:our in-depth documentation].`, { docLink: <externalLink_1.default href="https://docs.sentry.io"/> })}
        </p>
      </div>);
    }
}
const DsnValue = (0, styled_1.default)(p => (<code {...p}>
    <autoSelectText_1.default>{p.children}</autoSelectText_1.default>
  </code>)) `
  overflow: hidden;
`;
const DsnInfo = (0, styled_1.default)('div') `
  margin-bottom: ${(0, space_1.default)(3)};
`;
const DsnContainer = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: max-content 1fr;
  grid-gap: ${(0, space_1.default)(1.5)} ${(0, space_1.default)(2)};
  align-items: center;
  margin-bottom: ${(0, space_1.default)(2)};
`;
exports.default = (0, withOrganization_1.default)(ProjectInstallOverview);
//# sourceMappingURL=overview.jsx.map