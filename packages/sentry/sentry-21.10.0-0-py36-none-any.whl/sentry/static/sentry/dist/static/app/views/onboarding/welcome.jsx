Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const framer_motion_1 = require("framer-motion");
const platformicons_1 = require("platformicons");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const trackAdvancedAnalyticsEvent_1 = (0, tslib_1.__importDefault)(require("app/utils/analytics/trackAdvancedAnalyticsEvent"));
const testableTransition_1 = (0, tslib_1.__importDefault)(require("app/utils/testableTransition"));
const fallingError_1 = (0, tslib_1.__importDefault)(require("./components/fallingError"));
const welcomeBackground_1 = (0, tslib_1.__importDefault)(require("./components/welcomeBackground"));
const easterEggText = [
    (0, locale_1.t)('Be careful. She’s barely hanging on as it is.'),
    (0, locale_1.t)("You know this error's not real, right?"),
    (0, locale_1.t)("It's that big button, right up there."),
    (0, locale_1.t)('You could do this all day. But you really shouldn’t.'),
    (0, locale_1.tct)("Ok, really, that's enough. Click [ready:I'm Ready].", { ready: <em /> }),
    (0, locale_1.tct)("Next time you do that, [bold:we're starting].", { bold: <strong /> }),
    (0, locale_1.t)("We weren't kidding, let's get going."),
];
const fadeAway = {
    variants: {
        initial: { opacity: 0 },
        animate: { opacity: 1, filter: 'blur(0px)' },
        exit: { opacity: 0, filter: 'blur(1px)' },
    },
    transition: (0, testableTransition_1.default)({ duration: 0.8 }),
};
class OnboardingWelcome extends react_1.Component {
    componentDidMount() {
        var _a;
        // Next step will render the platform picker (using both large and small
        // icons). Keep things smooth by prefetching them. Preload a bit late to
        // avoid jank on welcome animations.
        setTimeout(platformicons_1.preloadIcons, 1500);
        (0, trackAdvancedAnalyticsEvent_1.default)('growth.onboarding_start_onboarding', {
            organization: (_a = this.props.organization) !== null && _a !== void 0 ? _a : null,
        });
    }
    render() {
        const { onComplete, active } = this.props;
        return (<fallingError_1.default onFall={fallCount => fallCount >= easterEggText.length && onComplete({})}>
        {({ fallingError, fallCount, triggerFall }) => (<Wrapper>
            <welcomeBackground_1.default />
            <framer_motion_1.motion.h1 {...fadeAway}>{(0, locale_1.t)('Welcome to Sentry')}</framer_motion_1.motion.h1>
            <framer_motion_1.motion.p {...fadeAway}>
              {(0, locale_1.t)('Find the errors and performance slowdowns that keep you up at night. In two steps.')}
            </framer_motion_1.motion.p>
            <CTAContainer {...fadeAway}>
              <button_1.default data-test-id="welcome-next" disabled={!active} priority="primary" onClick={() => {
                    triggerFall();
                    onComplete({});
                }}>
                {(0, locale_1.t)("I'm Ready")}
              </button_1.default>
              <PositionedFallingError>{fallingError}</PositionedFallingError>
            </CTAContainer>
            <SecondaryAction {...fadeAway}>
              {fallCount > 0 ? easterEggText[fallCount - 1] : <br />}
            </SecondaryAction>
          </Wrapper>)}
      </fallingError_1.default>);
    }
}
const CTAContainer = (0, styled_1.default)(framer_motion_1.motion.div) `
  margin-bottom: ${(0, space_1.default)(2)};
  position: relative;

  button {
    position: relative;
    z-index: 2;
  }
`;
const PositionedFallingError = (0, styled_1.default)('span') `
  display: block;
  position: absolute;
  top: 30px;
  right: -5px;
  z-index: 0;
`;
const SecondaryAction = (0, styled_1.default)(framer_motion_1.motion.small) `
  color: ${p => p.theme.subText};
  margin-top: 100px;
`;
const Wrapper = (0, styled_1.default)(framer_motion_1.motion.div) `
  max-width: 400px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding-top: 100px;

  h1 {
    font-size: 42px;
  }
`;
Wrapper.defaultProps = {
    variants: { exit: { x: 0 } },
    transition: (0, testableTransition_1.default)({
        staggerChildren: 0.2,
    }),
};
exports.default = OnboardingWelcome;
//# sourceMappingURL=welcome.jsx.map