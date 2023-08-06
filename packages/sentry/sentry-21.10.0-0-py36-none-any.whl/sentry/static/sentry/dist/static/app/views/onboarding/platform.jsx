Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const framer_motion_1 = require("framer-motion");
const indicator_1 = require("app/actionCreators/indicator");
const projects_1 = require("app/actionCreators/projects");
const projectActions_1 = (0, tslib_1.__importDefault)(require("app/actions/projectActions"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const platformPicker_1 = (0, tslib_1.__importDefault)(require("app/components/platformPicker"));
const locale_1 = require("app/locale");
const trackAdvancedAnalyticsEvent_1 = (0, tslib_1.__importDefault)(require("app/utils/analytics/trackAdvancedAnalyticsEvent"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withTeams_1 = (0, tslib_1.__importDefault)(require("app/utils/withTeams"));
const stepHeading_1 = (0, tslib_1.__importDefault)(require("./components/stepHeading"));
class OnboardingPlatform extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            firstProjectCreated: false,
            progressing: false,
        };
        this.handleSetPlatform = (platform) => this.props.onUpdate({ platform });
        this.handleContinue = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            var _a;
            this.setState({ progressing: true });
            const { platform } = this.props;
            if (platform === null) {
                return;
            }
            (0, trackAdvancedAnalyticsEvent_1.default)('growth.onboarding_set_up_your_project', {
                platform,
                organization: (_a = this.props.organization) !== null && _a !== void 0 ? _a : null,
            });
            // Create their first project if they don't already have one. This is a
            // no-op if they already have a project.
            yield this.createFirstProject(platform);
            this.props.onComplete({});
        });
    }
    componentDidMount() {
        var _a;
        (0, trackAdvancedAnalyticsEvent_1.default)('growth.onboarding_load_choose_platform', {
            organization: (_a = this.props.organization) !== null && _a !== void 0 ? _a : null,
        });
    }
    componentDidUpdate(prevProps) {
        if (prevProps.active && !this.props.active) {
            // eslint-disable-next-line react/no-did-update-set-state
            this.setState({ progressing: false });
        }
    }
    get hasFirstProject() {
        return this.props.project || this.state.firstProjectCreated;
    }
    get continueButtonLabel() {
        if (this.state.progressing) {
            return (0, locale_1.t)('Creating Project...');
        }
        if (!this.hasFirstProject) {
            return (0, locale_1.t)('Create Project');
        }
        if (!this.props.active) {
            return (0, locale_1.t)('Project Created');
        }
        return (0, locale_1.t)('Set Up Your Project');
    }
    createFirstProject(platform) {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, orgId, teams } = this.props;
            if (this.hasFirstProject) {
                return;
            }
            if (teams.length < 1) {
                return;
            }
            this.setState({ firstProjectCreated: true });
            try {
                const data = yield (0, projects_1.createProject)(api, orgId, teams[0].slug, orgId, platform, {
                    defaultRules: false,
                });
                projectActions_1.default.createSuccess(data);
            }
            catch (error) {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Failed to create project'));
                throw error;
            }
        });
    }
    render() {
        const { active, project, platform } = this.props;
        const selectedPlatform = platform || (project && project.platform);
        const continueDisabled = this.state.progressing || (this.hasFirstProject && !active);
        return (<div>
        <stepHeading_1.default step={1}>Choose your project’s platform</stepHeading_1.default>
        <framer_motion_1.motion.div variants={{
                initial: { y: 30, opacity: 0 },
                animate: { y: 0, opacity: 1 },
                exit: { opacity: 0 },
            }}>
          <p>
            {(0, locale_1.tct)(`Variety is the spice of application monitoring. Sentry SDKs integrate
             with most languages and platforms your developer heart desires.
             [link:View the full list].`, { link: <externalLink_1.default href="https://docs.sentry.io/platforms/"/> })}
          </p>
          <platformPicker_1.default noAutoFilter platform={selectedPlatform} setPlatform={this.handleSetPlatform} source="Onboarding" organization={this.props.organization}/>
          <p>
            {(0, locale_1.tct)(`Don't see your platform-of-choice? Fear not. Select
               [otherPlatformLink:other platform] when using a [communityClient:community client].
               Need help? Learn more in [docs:our docs].`, {
                otherPlatformLink: (<button_1.default priority="link" onClick={() => this.handleSetPlatform('other')}/>),
                communityClient: (<externalLink_1.default href="https://docs.sentry.io/platforms/#community-supported"/>),
                docs: <externalLink_1.default href="https://docs.sentry.io/platforms/"/>,
            })}
          </p>
          {selectedPlatform && (<button_1.default data-test-id="platform-select-next" priority="primary" disabled={continueDisabled} onClick={this.handleContinue}>
              {this.continueButtonLabel}
            </button_1.default>)}
        </framer_motion_1.motion.div>
      </div>);
    }
}
exports.default = (0, withApi_1.default)((0, withTeams_1.default)(OnboardingPlatform));
//# sourceMappingURL=platform.jsx.map