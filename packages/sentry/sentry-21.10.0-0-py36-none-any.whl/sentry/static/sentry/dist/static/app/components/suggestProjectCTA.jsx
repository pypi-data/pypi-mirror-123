Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const modal_1 = require("app/actionCreators/modal");
const prompts_1 = require("app/actionCreators/prompts");
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const suggestProjectModal_1 = (0, tslib_1.__importDefault)(require("app/components/modals/suggestProjectModal"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const trackAdvancedAnalyticsEvent_1 = (0, tslib_1.__importDefault)(require("app/utils/analytics/trackAdvancedAnalyticsEvent"));
const promptIsDismissed_1 = require("app/utils/promptIsDismissed");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
const MOBILE_PLATFORMS = [
    'react-native',
    'android',
    'cordova',
    'cocoa',
    'cocoa-swift',
    'apple-ios',
    'swift',
    'flutter',
    'xamarin',
    'dotnet-xamarin',
];
const MOBILE_USER_AGENTS = ['okhttp', 'CFNetwork', 'Alamofire', 'Dalvik'];
class SuggestProjectCTA extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {};
        this.handleCTAClose = () => {
            const { api, organization } = this.props;
            (0, trackAdvancedAnalyticsEvent_1.default)('growth.dismissed_mobile_prompt_banner', {
                matchedUserAgentString: this.matchedUserAgentString,
                organization,
            });
            (0, prompts_1.promptsUpdate)(api, {
                organizationId: organization.id,
                feature: 'suggest_mobile_project',
                status: 'dismissed',
            });
            this.setState({ isDismissed: true });
        };
        this.openModal = () => {
            (0, trackAdvancedAnalyticsEvent_1.default)('growth.opened_mobile_project_suggest_modal', {
                matchedUserAgentString: this.matchedUserAgentString,
                organization: this.props.organization,
            });
            (0, modal_1.openModal)(deps => (<suggestProjectModal_1.default organization={this.props.organization} matchedUserAgentString={this.matchedUserAgentString} {...deps}/>));
        };
    }
    componentDidMount() {
        this.fetchData();
    }
    // Returns the matched user agent string
    // otherwise, returns an empty string
    get matchedUserAgentString() {
        var _a, _b, _c, _d;
        const { entries } = this.props.event;
        const requestEntry = entries.find(item => item.type === 'request');
        if (!requestEntry) {
            return '';
        }
        // find the user agent header out of our list of headers
        const userAgent = (_c = (_b = (_a = requestEntry) === null || _a === void 0 ? void 0 : _a.data) === null || _b === void 0 ? void 0 : _b.headers) === null || _c === void 0 ? void 0 : _c.find(item => (item === null || item === void 0 ? void 0 : item[0].toLowerCase()) === 'user-agent');
        if (!userAgent) {
            return '';
        }
        // check if any of our mobile agent headers matches the event mobile agent
        return ((_d = MOBILE_USER_AGENTS.find(mobileAgent => { var _a; return (_a = userAgent[1]) === null || _a === void 0 ? void 0 : _a.toLowerCase().includes(mobileAgent.toLowerCase()); })) !== null && _d !== void 0 ? _d : '');
    }
    // check our projects to see if there is a mobile project
    get hasMobileProject() {
        return this.props.projects.some(project => MOBILE_PLATFORMS.includes(project.platform || ''));
    }
    // returns true if the current event is mobile from the user agent
    // or if we found a mobile event with the API
    get hasMobileEvent() {
        const { mobileEventResult } = this.state;
        return !!this.matchedUserAgentString || !!mobileEventResult;
    }
    /**
     * conditions to show prompt:
     * 1. Have a mobile event
     * 2. No mobile project
     * 3. CTA is not dimissed
     * 4. We've loaded the data from the backend for the prompt
     */
    get showCTA() {
        const { loaded, isDismissed } = this.state;
        return !!(this.hasMobileEvent && !this.hasMobileProject && !isDismissed && loaded);
    }
    fetchData() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            // no need to catch error since we have error boundary wrapping
            const [isDismissed, mobileEventResult] = yield Promise.all([
                this.checkMobilePrompt(),
                this.checkOrgHasMobileEvent(),
            ]);
            // set the new state
            this.setState({
                isDismissed,
                mobileEventResult,
                loaded: true,
            }, () => {
                const matchedUserAgentString = this.matchedUserAgentString;
                if (this.showCTA) {
                    // now record the results
                    (0, trackAdvancedAnalyticsEvent_1.default)('growth.show_mobile_prompt_banner', {
                        matchedUserAgentString,
                        mobileEventBrowserName: (mobileEventResult === null || mobileEventResult === void 0 ? void 0 : mobileEventResult.browserName) || '',
                        mobileEventClientOsName: (mobileEventResult === null || mobileEventResult === void 0 ? void 0 : mobileEventResult.clientOsName) || '',
                        organization: this.props.organization,
                    }, { startSession: true });
                }
            });
        });
    }
    checkOrgHasMobileEvent() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, organization } = this.props;
            return api.requestPromise(`/organizations/${organization.slug}/has-mobile-app-events/`, {
                query: {
                    userAgents: MOBILE_USER_AGENTS,
                },
            });
        });
    }
    checkMobilePrompt() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, organization } = this.props;
            // check our prompt backend
            const promptData = yield (0, prompts_1.promptsCheck)(api, {
                organizationId: organization.id,
                feature: 'suggest_mobile_project',
            });
            return (0, promptIsDismissed_1.promptIsDismissed)(promptData);
        });
    }
    renderCTA() {
        return (<alert_1.default type="info">
        <Content>
          <span>
            {(0, locale_1.tct)('We have a sneaking suspicion you have a mobile app that doesn’t use Sentry. [link:Start Monitoring]', { link: <a onClick={this.openModal}/> })}
          </span>
          <StyledIconClose onClick={this.handleCTAClose}/>
        </Content>
      </alert_1.default>);
    }
    render() {
        return this.showCTA ? this.renderCTA() : null;
    }
}
exports.default = (0, withApi_1.default)((0, withProjects_1.default)(SuggestProjectCTA));
const Content = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: 1fr max-content;
  grid-gap: ${(0, space_1.default)(1)};
`;
const StyledIconClose = (0, styled_1.default)(icons_1.IconClose) `
  margin: auto;
  cursor: pointer;
`;
//# sourceMappingURL=suggestProjectCTA.jsx.map