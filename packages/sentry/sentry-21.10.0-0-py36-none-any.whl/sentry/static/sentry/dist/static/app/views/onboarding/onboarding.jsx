Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_document_title_1 = (0, tslib_1.__importDefault)(require("react-document-title"));
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const framer_motion_1 = require("framer-motion");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const hook_1 = (0, tslib_1.__importDefault)(require("app/components/hook"));
const logoSentry_1 = (0, tslib_1.__importDefault)(require("app/components/logoSentry"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const testableTransition_1 = (0, tslib_1.__importDefault)(require("app/utils/testableTransition"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
const pageCorners_1 = (0, tslib_1.__importDefault)(require("./components/pageCorners"));
const platform_1 = (0, tslib_1.__importDefault)(require("./platform"));
const sdkConfiguration_1 = (0, tslib_1.__importDefault)(require("./sdkConfiguration"));
const welcome_1 = (0, tslib_1.__importDefault)(require("./welcome"));
const ONBOARDING_STEPS = [
    {
        id: 'welcome',
        title: (0, locale_1.t)('Welcome to Sentry'),
        Component: welcome_1.default,
        centered: true,
    },
    {
        id: 'select-platform',
        title: (0, locale_1.t)('Select a platform'),
        Component: platform_1.default,
    },
    {
        id: 'get-started',
        title: (0, locale_1.t)('Install the Sentry SDK'),
        Component: sdkConfiguration_1.default,
    },
];
class Onboarding extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {};
        this.handleUpdate = (data) => {
            this.setState(data);
        };
        this.handleGoBack = () => {
            const previousStep = this.props.steps[this.activeStepIndex - 1];
            react_router_1.browserHistory.replace(`/onboarding/${this.props.params.orgId}/${previousStep.id}/`);
        };
        this.Contents = () => {
            const cornerVariantControl = (0, framer_motion_1.useAnimation)();
            const updateCornerVariant = () => {
                cornerVariantControl.start(this.activeStepIndex === 0 ? 'top-right' : 'top-left');
            };
            // XXX(epurkhiser): We're using a react hook here becuase there's no other
            // way to create framer-motion controls than by using the `useAnimation`
            // hook.
            React.useEffect(updateCornerVariant, []);
            return (<Container>
        <Back animate={this.activeStepIndex > 0 ? 'visible' : 'hidden'} onClick={this.handleGoBack}/>
        <framer_motion_1.AnimatePresence exitBeforeEnter onExitComplete={updateCornerVariant}>
          {this.renderOnboardingStep()}
        </framer_motion_1.AnimatePresence>
        <pageCorners_1.default animateVariant={cornerVariantControl}/>
      </Container>);
        };
    }
    componentDidMount() {
        this.validateActiveStep();
    }
    componentDidUpdate() {
        this.validateActiveStep();
    }
    validateActiveStep() {
        if (this.activeStepIndex === -1) {
            const firstStep = this.props.steps[0].id;
            react_router_1.browserHistory.replace(`/onboarding/${this.props.params.orgId}/${firstStep}/`);
        }
    }
    get activeStepIndex() {
        return this.props.steps.findIndex(({ id }) => this.props.params.step === id);
    }
    get activeStep() {
        return this.props.steps[this.activeStepIndex];
    }
    get firstProject() {
        const sortedProjects = this.props.projects.sort((a, b) => new Date(a.dateCreated).getTime() - new Date(b.dateCreated).getTime());
        return sortedProjects.length > 0 ? sortedProjects[0] : null;
    }
    get projectPlatform() {
        var _a, _b, _c;
        return (_c = (_a = this.state.platform) !== null && _a !== void 0 ? _a : (_b = this.firstProject) === null || _b === void 0 ? void 0 : _b.platform) !== null && _c !== void 0 ? _c : null;
    }
    handleNextStep(step, data) {
        this.handleUpdate(data);
        if (step !== this.activeStep) {
            return;
        }
        const { orgId } = this.props.params;
        const nextStep = this.props.steps[this.activeStepIndex + 1];
        react_router_1.browserHistory.push(`/onboarding/${orgId}/${nextStep.id}/`);
    }
    renderProgressBar() {
        const activeStepIndex = this.activeStepIndex;
        return (<ProgressBar>
        {this.props.steps.map((step, index) => (<ProgressStep active={activeStepIndex === index} key={step.id}/>))}
      </ProgressBar>);
    }
    renderOnboardingStep() {
        const { orgId } = this.props.params;
        const step = this.activeStep;
        return (<OnboardingStep centered={step.centered} key={step.id} data-test-id={`onboarding-step-${step.id}`}>
        <step.Component active orgId={orgId} project={this.firstProject} platform={this.projectPlatform} onComplete={data => this.handleNextStep(step, data)} onUpdate={this.handleUpdate} organization={this.props.organization}/>
      </OnboardingStep>);
    }
    render() {
        if (this.activeStepIndex === -1) {
            return null;
        }
        return (<OnboardingWrapper>
        <react_document_title_1.default title={this.activeStep.title}/>
        <Header>
          <LogoSvg />
          <HeaderRight>
            {this.renderProgressBar()}
            <hook_1.default name="onboarding:extra-chrome"/>
          </HeaderRight>
        </Header>
        <this.Contents />
      </OnboardingWrapper>);
    }
}
Onboarding.defaultProps = {
    steps: ONBOARDING_STEPS,
};
const OnboardingWrapper = (0, styled_1.default)('main') `
  overflow: hidden;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
`;
const Container = (0, styled_1.default)('div') `
  display: flex;
  justify-content: center;
  position: relative;
  background: ${p => p.theme.background};
  padding: 120px ${(0, space_1.default)(3)};
  padding-top: 12vh;
  width: 100%;
  margin: 0 auto;
  flex-grow: 1;
`;
const Header = (0, styled_1.default)('header') `
  background: ${p => p.theme.background};
  padding: ${(0, space_1.default)(4)};
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.05);
  display: flex;
  justify-content: space-between;
`;
const LogoSvg = (0, styled_1.default)(logoSentry_1.default) `
  width: 130px;
  height: 30px;
  color: ${p => p.theme.textColor};
`;
const ProgressBar = (0, styled_1.default)('div') `
  margin: 0 ${(0, space_1.default)(4)};
  position: relative;
  display: flex;
  align-items: center;
  min-width: 120px;
  justify-content: space-between;

  &:before {
    position: absolute;
    display: block;
    content: '';
    height: 4px;
    background: ${p => p.theme.inactive};
    left: 2px;
    right: 2px;
    top: 50%;
    margin-top: -2px;
  }
`;
const ProgressStep = (0, styled_1.default)('div') `
  position: relative;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  border: 4px solid ${p => (p.active ? p.theme.active : p.theme.inactive)};
  background: ${p => p.theme.background};
`;
const ProgressStatus = (0, styled_1.default)(framer_motion_1.motion.div) `
  color: ${p => p.theme.subText};
  font-size: ${p => p.theme.fontSizeMedium};
  text-align: right;
  grid-column: 3;
  grid-row: 1;
`;
const HeaderRight = (0, styled_1.default)('div') `
  display: grid;
  grid-auto-flow: column;
  grid-auto-columns: max-content;
  grid-gap: ${(0, space_1.default)(1)};
`;
ProgressStatus.defaultProps = {
    initial: { opacity: 0, y: -10 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0, y: 10 },
    transition: (0, testableTransition_1.default)(),
};
const Back = (0, styled_1.default)((_a) => {
    var { className, animate } = _a, props = (0, tslib_1.__rest)(_a, ["className", "animate"]);
    return (<framer_motion_1.motion.div className={className} animate={animate} transition={(0, testableTransition_1.default)()} variants={{
            initial: { opacity: 0 },
            visible: { opacity: 1, transition: (0, testableTransition_1.default)({ delay: 1 }) },
            hidden: { opacity: 0 },
        }}>
    <button_1.default {...props} icon={<icons_1.IconChevron direction="left" size="sm"/>} priority="link">
      {(0, locale_1.t)('Go back')}
    </button_1.default>
  </framer_motion_1.motion.div>);
}) `
  position: absolute;
  top: 40px;
  left: 20px;

  button {
    font-size: ${p => p.theme.fontSizeSmall};
    color: ${p => p.theme.subText};
  }
`;
const OnboardingStep = (0, styled_1.default)(framer_motion_1.motion.div) `
  width: 850px;
  display: flex;
  flex-direction: column;
  ${p => p.centered &&
    `justify-content: center;
     align-items: center;`};
`;
OnboardingStep.defaultProps = {
    initial: 'initial',
    animate: 'animate',
    exit: 'exit',
    variants: { animate: {} },
    transition: (0, testableTransition_1.default)({
        staggerChildren: 0.2,
    }),
};
exports.default = (0, withOrganization_1.default)((0, withProjects_1.default)(Onboarding));
//# sourceMappingURL=onboarding.jsx.map