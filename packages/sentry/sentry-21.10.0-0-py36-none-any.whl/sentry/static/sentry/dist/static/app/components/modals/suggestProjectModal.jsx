Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const qs = (0, tslib_1.__importStar)(require("query-string"));
const mobile_hero_jpg_1 = (0, tslib_1.__importDefault)(require("sentry-images/spot/mobile-hero.jpg"));
const indicator_1 = require("app/actionCreators/indicator");
const access_1 = (0, tslib_1.__importDefault)(require("app/components/acl/access"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const list_1 = (0, tslib_1.__importDefault)(require("app/components/list"));
const listItem_1 = (0, tslib_1.__importDefault)(require("app/components/list/listItem"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const trackAdvancedAnalyticsEvent_1 = (0, tslib_1.__importDefault)(require("app/utils/analytics/trackAdvancedAnalyticsEvent"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const emailField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/emailField"));
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
class SuggestProjectModal extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            askTeammate: false,
        };
        this.handleGetStartedClick = () => {
            const { matchedUserAgentString, organization } = this.props;
            (0, trackAdvancedAnalyticsEvent_1.default)('growth.clicked_mobile_prompt_setup_project', {
                matchedUserAgentString,
                organization,
            });
        };
        this.handleAskTeammate = () => {
            const { matchedUserAgentString, organization } = this.props;
            this.setState({ askTeammate: true });
            (0, trackAdvancedAnalyticsEvent_1.default)('growth.clicked_mobile_prompt_ask_teammate', {
                matchedUserAgentString,
                organization,
            });
        };
        this.goBack = () => {
            this.setState({ askTeammate: false });
        };
        this.handleSubmitSuccess = () => {
            const { matchedUserAgentString, organization, closeModal } = this.props;
            (0, indicator_1.addSuccessMessage)('Notified teammate successfully');
            (0, trackAdvancedAnalyticsEvent_1.default)('growth.submitted_mobile_prompt_ask_teammate', {
                matchedUserAgentString,
                organization,
            });
            closeModal();
        };
        this.handlePreSubmit = () => {
            (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Submitting\u2026'));
        };
        this.handleSubmitError = () => {
            (0, indicator_1.addErrorMessage)((0, locale_1.t)('Error notifying teammate'));
        };
    }
    renderAskTeammate() {
        const { Body, organization } = this.props;
        return (<Body>
        <form_1.default apiEndpoint={`/organizations/${organization.slug}/request-project-creation/`} apiMethod="POST" submitLabel={(0, locale_1.t)('Send')} onSubmitSuccess={this.handleSubmitSuccess} onSubmitError={this.handleSubmitError} onPreSubmit={this.handlePreSubmit} extraButton={<BackWrapper>
              <StyledBackButton onClick={this.goBack}>{(0, locale_1.t)('Back')}</StyledBackButton>
            </BackWrapper>}>
          <p>
            {(0, locale_1.t)('Let the right folks know about Sentry Mobile Application Monitoring.')}
          </p>
          <emailField_1.default required name="targetUserEmail" inline={false} label={(0, locale_1.t)('Email Address')} placeholder="name@example.com" stacked/>
        </form_1.default>
      </Body>);
    }
    renderMain() {
        const { Body, Footer, organization } = this.props;
        const paramString = qs.stringify({
            referrer: 'suggest_project',
            category: 'mobile',
        });
        const newProjectLink = `/organizations/${organization.slug}/projects/new/?${paramString}`;
        return (<react_1.Fragment>
        <Body>
          <ModalContainer>
            <SmallP>
              {(0, locale_1.t)("Sentry for Mobile shows a holistic overview of your application's health in real time. So you can correlate errors with releases, tags, and devices to solve problems quickly, decrease churn, and improve user retention.")}
            </SmallP>

            <StyledList symbol="bullet">
              <listItem_1.default>
                {(0, locale_1.tct)('[see:See] session data, version adoption, and user impact by every release.', {
                see: <strong />,
            })}
              </listItem_1.default>
              <listItem_1.default>
                {(0, locale_1.tct)('[solve:Solve] issues quickly with full context: contextualized stack traces, events that lead to the error, client, hardware information, and the very commit that introduced the error.', {
                solve: <strong />,
            })}
              </listItem_1.default>
              <listItem_1.default>
                {(0, locale_1.tct)('[learn:Learn] and analyze event data to reduce regressions and ultimately improve user adoption and engagement.', {
                learn: <strong />,
            })}
              </listItem_1.default>
            </StyledList>

            <SmallP>{(0, locale_1.t)('And guess what? Setup takes less than five minutes.')}</SmallP>
          </ModalContainer>
        </Body>
        <Footer>
          <access_1.default organization={organization} access={['project:write']}>
            {({ hasAccess }) => (<buttonBar_1.default gap={1}>
                <button_1.default priority={hasAccess ? 'default' : 'primary'} onClick={this.handleAskTeammate}>
                  {(0, locale_1.t)('Tell a Teammate')}
                </button_1.default>
                {hasAccess && (<button_1.default href={newProjectLink} onClick={this.handleGetStartedClick} priority="primary">
                    {(0, locale_1.t)('Get Started')}
                  </button_1.default>)}
              </buttonBar_1.default>)}
          </access_1.default>
        </Footer>
      </react_1.Fragment>);
    }
    render() {
        const { Header } = this.props;
        const { askTeammate } = this.state;
        const header = askTeammate ? (0, locale_1.t)('Tell a Teammate') : (0, locale_1.t)('Try Sentry for Mobile');
        return (<react_1.Fragment>
        <Header>
          <PatternHeader />
          <Title>{header}</Title>
        </Header>
        {this.state.askTeammate ? this.renderAskTeammate() : this.renderMain()}
      </react_1.Fragment>);
    }
}
const ModalContainer = (0, styled_1.default)('div') `
  display: grid;
  grid-gap: ${(0, space_1.default)(3)};

  code {
    word-break: break-word;
  }
`;
const Title = (0, styled_1.default)('h3') `
  margin-top: ${(0, space_1.default)(2)};
  margin-bottom: ${(0, space_1.default)(3)};
`;
const SmallP = (0, styled_1.default)('p') `
  margin: 0;
`;
const PatternHeader = (0, styled_1.default)('div') `
  margin: -${(0, space_1.default)(4)} -${(0, space_1.default)(4)} 0 -${(0, space_1.default)(4)};
  border-radius: 7px 7px 0 0;
  background-image: url(${mobile_hero_jpg_1.default});
  background-size: 475px;
  background-color: black;
  background-repeat: no-repeat;
  overflow: hidden;
  background-position: center bottom;
  height: 156px;
`;
const StyledList = (0, styled_1.default)(list_1.default) `
  li {
    padding-left: ${(0, space_1.default)(3)};
  }
`;
const BackWrapper = (0, styled_1.default)('div') `
  width: 100%;
  margin-right: ${(0, space_1.default)(1)};
`;
const StyledBackButton = (0, styled_1.default)(button_1.default) `
  float: right;
`;
exports.default = (0, withApi_1.default)(SuggestProjectModal);
//# sourceMappingURL=suggestProjectModal.jsx.map