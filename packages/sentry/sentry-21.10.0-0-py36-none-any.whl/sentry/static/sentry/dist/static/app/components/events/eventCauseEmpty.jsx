Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const codesworth_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/spot/codesworth.svg"));
const prompts_1 = require("app/actionCreators/prompts");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const commitRow_1 = (0, tslib_1.__importDefault)(require("app/components/commitRow"));
const styles_1 = require("app/components/events/styles");
const panels_1 = require("app/components/panels");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const types_1 = require("app/types");
const trackAdvancedAnalyticsEvent_1 = (0, tslib_1.__importDefault)(require("app/utils/analytics/trackAdvancedAnalyticsEvent"));
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const promptIsDismissed_1 = require("app/utils/promptIsDismissed");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const EXAMPLE_COMMITS = ['dec0de', 'de1e7e', '5ca1ed'];
const DUMMY_COMMIT = {
    id: (0, getDynamicText_1.default)({
        value: EXAMPLE_COMMITS[Math.floor(Math.random() * EXAMPLE_COMMITS.length)],
        fixed: '5ca1ed',
    }),
    author: {
        id: '',
        name: 'codesworth',
        username: '',
        email: 'codesworth@example.com',
        ip_address: '',
        lastSeen: '',
        lastLogin: '',
        isSuperuser: false,
        isAuthenticated: false,
        emails: [],
        isManaged: false,
        lastActive: '',
        isStaff: false,
        identities: [],
        isActive: true,
        has2fa: false,
        canReset2fa: false,
        authenticators: [],
        dateJoined: '',
        options: {
            theme: 'system',
            timezone: '',
            stacktraceOrder: 1,
            language: '',
            clock24Hours: false,
            avatarType: 'letter_avatar',
        },
        flags: { newsletter_consent_prompt: false },
        hasPasswordAuth: true,
        permissions: new Set([]),
        experiments: {},
    },
    dateCreated: (0, moment_1.default)().subtract(3, 'day').format(),
    repository: {
        id: '',
        integrationId: '',
        name: '',
        externalSlug: '',
        url: '',
        provider: {
            id: 'integrations:github',
            name: 'GitHub',
        },
        dateCreated: '',
        status: types_1.RepositoryStatus.ACTIVE,
    },
    releases: [],
    message: (0, locale_1.t)('This example commit broke something'),
};
const SUSPECT_COMMITS_FEATURE = 'suspect_commits';
class EventCauseEmpty extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            shouldShow: undefined,
        };
    }
    componentDidMount() {
        this.fetchData();
    }
    componentDidUpdate(_prevProps, prevState) {
        const { shouldShow } = this.state;
        if (!prevState.shouldShow && shouldShow) {
            this.trackAnalytics('event_cause.viewed');
        }
    }
    fetchData() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, event, project, organization } = this.props;
            if (!(0, promptIsDismissed_1.promptCanShow)(SUSPECT_COMMITS_FEATURE, event.eventID)) {
                this.setState({ shouldShow: false });
                return;
            }
            const data = yield (0, prompts_1.promptsCheck)(api, {
                projectId: project.id,
                organizationId: organization.id,
                feature: SUSPECT_COMMITS_FEATURE,
            });
            this.setState({ shouldShow: !(0, promptIsDismissed_1.promptIsDismissed)(data !== null && data !== void 0 ? data : {}, 7) });
        });
    }
    handleClick({ action, eventKey }) {
        const { api, project, organization } = this.props;
        const data = {
            projectId: project.id,
            organizationId: organization.id,
            feature: SUSPECT_COMMITS_FEATURE,
            status: action,
        };
        (0, prompts_1.promptsUpdate)(api, data).then(() => this.setState({ shouldShow: false }));
        this.trackAnalytics(eventKey);
    }
    trackAnalytics(eventKey) {
        const { project, organization } = this.props;
        (0, trackAdvancedAnalyticsEvent_1.default)(eventKey, {
            project_id: project.id,
            platform: project.platform,
            organization,
        });
    }
    render() {
        const { shouldShow } = this.state;
        if (!shouldShow) {
            return null;
        }
        return (<styles_1.DataSection data-test-id="loaded-event-cause-empty">
        <StyledPanel dashedBorder>
          <BoxHeader>
            <Description>
              <h3>{(0, locale_1.t)('Configure Suspect Commits')}</h3>
              <p>{(0, locale_1.t)('To identify which commit caused this issue')}</p>
            </Description>
            <ButtonList>
              <DocsButton size="small" priority="primary" href="https://docs.sentry.io/product/releases/setup/" onClick={() => this.trackAnalytics('event_cause.docs_clicked')}>
                {(0, locale_1.t)('Read the docs')}
              </DocsButton>

              <div>
                <SnoozeButton title={(0, locale_1.t)('Remind me next week')} size="small" onClick={() => this.handleClick({
                action: 'snoozed',
                eventKey: 'event_cause.snoozed',
            })}>
                  {(0, locale_1.t)('Snooze')}
                </SnoozeButton>
                <DismissButton title={(0, locale_1.t)('Dismiss for this project')} size="small" onClick={() => this.handleClick({
                action: 'dismissed',
                eventKey: 'event_cause.dismissed',
            })}>
                  {(0, locale_1.t)('Dismiss')}
                </DismissButton>
              </div>
            </ButtonList>
          </BoxHeader>
          <ExampleCommitPanel>
            <commitRow_1.default key={DUMMY_COMMIT.id} commit={DUMMY_COMMIT} customAvatar={<CustomAvatar src={codesworth_svg_1.default}/>}/>
          </ExampleCommitPanel>
        </StyledPanel>
      </styles_1.DataSection>);
    }
}
const StyledPanel = (0, styled_1.default)(panels_1.Panel) `
  padding: ${(0, space_1.default)(3)};
  padding-bottom: 0;
  background: none;
`;
const Description = (0, styled_1.default)('div') `
  h3 {
    font-size: 14px;
    text-transform: uppercase;
    margin-bottom: ${(0, space_1.default)(0.25)};
    color: ${p => p.theme.gray300};
  }

  p {
    font-size: 13px;
    font-weight: bold;
    color: ${p => p.theme.textColor};
    margin-bottom: ${(0, space_1.default)(1.5)};
  }
`;
const ButtonList = (0, styled_1.default)('div') `
  display: inline-grid;
  grid-auto-flow: column;
  grid-gap: ${(0, space_1.default)(1)};
  align-items: center;
  justify-self: end;
  margin-bottom: 16px;
`;
const DocsButton = (0, styled_1.default)(button_1.default) `
  &:focus {
    color: ${p => p.theme.white};
  }
`;
const SnoozeButton = (0, styled_1.default)(button_1.default) `
  border-right: 0;
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
`;
const DismissButton = (0, styled_1.default)(button_1.default) `
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
`;
const ExampleCommitPanel = (0, styled_1.default)(panels_1.Panel) `
  overflow: hidden;
  pointer-events: none;
  position: relative;
  padding-right: ${(0, space_1.default)(3)};

  &:after {
    display: block;
    content: 'Example';
    position: absolute;
    top: 16px;
    right: -24px;
    text-transform: uppercase;
    background: #e46187;
    padding: 4px 26px;
    line-height: 11px;
    font-size: 11px;
    color: ${p => p.theme.white};
    transform: rotate(45deg);
  }
`;
const CustomAvatar = (0, styled_1.default)('img') `
  height: 48px;
  padding-right: 12px;
  margin: -6px 0px -6px -2px;
`;
const BoxHeader = (0, styled_1.default)('div') `
  display: grid;
  align-items: start;
  grid-template-columns: repeat(auto-fit, minmax(256px, 1fr));
`;
exports.default = (0, withApi_1.default)(EventCauseEmpty);
//# sourceMappingURL=eventCauseEmpty.jsx.map