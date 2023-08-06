Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const prompts_1 = require("app/actionCreators/prompts");
const sidebarPanelActions_1 = (0, tslib_1.__importDefault)(require("app/actions/sidebarPanelActions"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
const promptIsDismissed_1 = require("app/utils/promptIsDismissed");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withGlobalSelection_1 = (0, tslib_1.__importDefault)(require("app/utils/withGlobalSelection"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const withSdkUpdates_1 = (0, tslib_1.__importDefault)(require("app/utils/withSdkUpdates"));
const types_1 = require("./sidebar/types");
const button_1 = (0, tslib_1.__importDefault)(require("./button"));
const recordAnalyticsSeen = ({ organization }) => (0, analytics_1.trackAnalyticsEvent)({
    eventKey: 'sdk_updates.seen',
    eventName: 'SDK Updates: Seen',
    organization_id: organization.id,
});
const recordAnalyticsSnoozed = ({ organization }) => (0, analytics_1.trackAnalyticsEvent)({
    eventKey: 'sdk_updates.snoozed',
    eventName: 'SDK Updates: Snoozed',
    organization_id: organization.id,
});
const recordAnalyticsClicked = ({ organization }) => (0, analytics_1.trackAnalyticsEvent)({
    eventKey: 'sdk_updates.clicked',
    eventName: 'SDK Updates: Clicked',
    organization_id: organization.id,
});
const flattenSuggestions = (list) => list.reduce((suggestions, sdk) => [...suggestions, ...sdk.suggestions], []);
class InnerGlobalSdkSuggestions extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            isDismissed: null,
        };
        this.snoozePrompt = () => {
            const { api, organization } = this.props;
            (0, prompts_1.promptsUpdate)(api, {
                organizationId: organization.id,
                feature: 'sdk_updates',
                status: 'snoozed',
            });
            this.setState({ isDismissed: true });
            recordAnalyticsSnoozed({ organization: this.props.organization });
        };
    }
    componentDidMount() {
        this.promptsCheck();
        recordAnalyticsSeen({ organization: this.props.organization });
    }
    promptsCheck() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, organization } = this.props;
            const prompt = yield (0, prompts_1.promptsCheck)(api, {
                organizationId: organization.id,
                feature: 'sdk_updates',
            });
            this.setState({
                isDismissed: (0, promptIsDismissed_1.promptIsDismissed)(prompt),
            });
        });
    }
    render() {
        const _a = this.props, { api: _api, selection, sdkUpdates, organization, Wrapper } = _a, props = (0, tslib_1.__rest)(_a, ["api", "selection", "sdkUpdates", "organization", "Wrapper"]);
        const { isDismissed } = this.state;
        if (!sdkUpdates || isDismissed === null || isDismissed) {
            return null;
        }
        // withSdkUpdates explicitly only queries My Projects. This means that when
        // looking at any projects outside of My Projects (like All Projects), this
        // will only show the updates relevant to the to user.
        const projectSpecificUpdates = (selection === null || selection === void 0 ? void 0 : selection.projects.length) === 0 || (selection === null || selection === void 0 ? void 0 : selection.projects) === [globalSelectionHeader_1.ALL_ACCESS_PROJECTS]
            ? sdkUpdates
            : sdkUpdates.filter(update => { var _a; return (_a = selection === null || selection === void 0 ? void 0 : selection.projects) === null || _a === void 0 ? void 0 : _a.includes(parseInt(update.projectId, 10)); });
        // Are there any updates?
        if (flattenSuggestions(projectSpecificUpdates).length === 0) {
            return null;
        }
        const showBroadcastsPanel = (<button_1.default priority="link" onClick={() => {
                sidebarPanelActions_1.default.activatePanel(types_1.SidebarPanelKey.Broadcasts);
                recordAnalyticsClicked({ organization });
            }}>
        {(0, locale_1.t)('Review updates')}
      </button_1.default>);
        const notice = (<alert_1.default type="info" icon={<icons_1.IconUpgrade />} {...props}>
        <Content>
          {(0, locale_1.t)(`You have outdated SDKs in your projects. Update them for important fixes and features.`)}
          <Actions>
            <button_1.default priority="link" title={(0, locale_1.t)('Dismiss for the next two weeks')} onClick={this.snoozePrompt}>
              {(0, locale_1.t)('Remind me later')}
            </button_1.default>
            |{showBroadcastsPanel}
          </Actions>
        </Content>
      </alert_1.default>);
        return Wrapper ? <Wrapper>{notice}</Wrapper> : notice;
    }
}
const Content = (0, styled_1.default)('div') `
  display: flex;
  flex-wrap: wrap;

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    justify-content: space-between;
  }
`;
const Actions = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: repeat(3, max-content);
  grid-gap: ${(0, space_1.default)(1)};
`;
const GlobalSdkSuggestions = (0, withOrganization_1.default)((0, withSdkUpdates_1.default)((0, withGlobalSelection_1.default)((0, withApi_1.default)(InnerGlobalSdkSuggestions))));
exports.default = GlobalSdkSuggestions;
//# sourceMappingURL=globalSdkUpdateAlert.jsx.map