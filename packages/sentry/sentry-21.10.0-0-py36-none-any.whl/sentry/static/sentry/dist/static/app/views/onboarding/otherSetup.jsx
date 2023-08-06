Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
require("prism-sentry/index.css");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const framer_motion_1 = require("framer-motion");
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const locale_1 = require("app/locale");
const trackAdvancedAnalyticsEvent_1 = (0, tslib_1.__importDefault)(require("app/utils/analytics/trackAdvancedAnalyticsEvent"));
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const firstEventFooter_1 = (0, tslib_1.__importDefault)(require("./components/firstEventFooter"));
const fullIntroduction_1 = (0, tslib_1.__importDefault)(require("./components/fullIntroduction"));
class OtherSetup extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.handleFullDocsClick = () => {
            const { organization } = this.props;
            (0, trackAdvancedAnalyticsEvent_1.default)('growth.onboarding_view_full_docs', { organization });
        };
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { keyList: null });
    }
    getEndpoints() {
        const { organization, project } = this.props;
        return [['keyList', `/projects/${organization.slug}/${project === null || project === void 0 ? void 0 : project.slug}/keys/`]];
    }
    render() {
        const { organization, project } = this.props;
        const { keyList } = this.state;
        const currentPlatform = 'other';
        const blurb = (<React.Fragment>
        <p>
          {(0, locale_1.tct)(`Prepare the SDK for your language following this [docsLink:guide].`, {
                docsLink: <externalLink_1.default href="https://develop.sentry.dev/sdk/overview/"/>,
            })}
        </p>

        <p>
          {(0, locale_1.t)('Once your SDK is set up, use the following DSN and send your first event!')}
        </p>

        <p>{(0, locale_1.tct)('Here is the DSN: [DSN]', { DSN: <b> {keyList === null || keyList === void 0 ? void 0 : keyList[0].dsn.public}</b> })}</p>
      </React.Fragment>);
        const docs = (<DocsWrapper>
        {blurb}
        {project && (<firstEventFooter_1.default project={project} organization={organization} docsLink="https://develop.sentry.dev/sdk" docsOnClick={this.handleFullDocsClick}/>)}
      </DocsWrapper>);
        const testOnlyAlert = (<alert_1.default type="warning">
        Platform documentation is not rendered in for tests in CI
      </alert_1.default>);
        return (<React.Fragment>
        <fullIntroduction_1.default currentPlatform={currentPlatform}/>
        {(0, getDynamicText_1.default)({
                value: docs,
                fixed: testOnlyAlert,
            })}
      </React.Fragment>);
    }
}
const DocsWrapper = (0, styled_1.default)(framer_motion_1.motion.div) ``;
DocsWrapper.defaultProps = {
    initial: { opacity: 0, y: 40 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0 },
};
exports.default = (0, withOrganization_1.default)((0, withApi_1.default)(OtherSetup));
//# sourceMappingURL=otherSetup.jsx.map