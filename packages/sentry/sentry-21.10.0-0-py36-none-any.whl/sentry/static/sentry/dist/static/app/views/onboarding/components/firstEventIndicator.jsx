Object.defineProperty(exports, "__esModule", { value: true });
exports.Indicator = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const framer_motion_1 = require("framer-motion");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const pulsingIndicator_1 = (0, tslib_1.__importDefault)(require("app/styles/pulsingIndicator"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const trackAdvancedAnalyticsEvent_1 = (0, tslib_1.__importDefault)(require("app/utils/analytics/trackAdvancedAnalyticsEvent"));
const eventWaiter_1 = (0, tslib_1.__importDefault)(require("app/utils/eventWaiter"));
const testableTransition_1 = (0, tslib_1.__importDefault)(require("app/utils/testableTransition"));
const FirstEventIndicator = (_a) => {
    var { children } = _a, props = (0, tslib_1.__rest)(_a, ["children"]);
    return (<eventWaiter_1.default {...props}>
    {({ firstIssue }) => children({
            indicator: <Indicator firstIssue={firstIssue} {...props}/>,
            firstEventButton: (<button_1.default title={(0, locale_1.t)("You'll need to send your first error to continue")} tooltipProps={{ disabled: !!firstIssue }} disabled={!firstIssue} priority="primary" onClick={() => (0, trackAdvancedAnalyticsEvent_1.default)('growth.onboarding_take_to_error', {
                    organization: props.organization,
                })} to={`/organizations/${props.organization.slug}/issues/${firstIssue !== true && firstIssue !== null ? `${firstIssue.id}/` : ''}`}>
            {(0, locale_1.t)('Take me to my error')}
          </button_1.default>),
        })}
  </eventWaiter_1.default>);
};
const Indicator = ({ firstIssue }) => (<Container>
    <framer_motion_1.AnimatePresence>
      {!firstIssue ? <Waiting key="waiting"/> : <Success key="received"/>}
    </framer_motion_1.AnimatePresence>
  </Container>);
exports.Indicator = Indicator;
const Container = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: 1fr;
  justify-content: right;
`;
const StatusWrapper = (0, styled_1.default)(framer_motion_1.motion.div) `
  display: grid;
  grid-template-columns: 1fr max-content;
  grid-gap: ${(0, space_1.default)(1)};
  align-items: center;
  font-size: ${p => p.theme.fontSizeMedium};
  /* Keep the wrapper in the parent grids first cell for transitions */
  grid-column: 1;
  grid-row: 1;
`;
StatusWrapper.defaultProps = {
    initial: 'initial',
    animate: 'animate',
    exit: 'exit',
    variants: {
        initial: { opacity: 0, y: -10 },
        animate: {
            opacity: 1,
            y: 0,
            transition: (0, testableTransition_1.default)({ when: 'beforeChildren', staggerChildren: 0.35 }),
        },
        exit: { opacity: 0, y: 10 },
    },
};
const Waiting = (props) => (<StatusWrapper {...props}>
    <AnimatedText>{(0, locale_1.t)('Waiting to receive first event to continue')}</AnimatedText>
    <WaitingIndicator />
  </StatusWrapper>);
const Success = (props) => (<StatusWrapper {...props}>
    <AnimatedText>{(0, locale_1.t)('Event was received!')}</AnimatedText>
    <ReceivedIndicator />
  </StatusWrapper>);
const indicatorAnimation = {
    initial: { opacity: 0, y: -10 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0, y: 10 },
};
const AnimatedText = (0, styled_1.default)(framer_motion_1.motion.div) ``;
AnimatedText.defaultProps = {
    variants: indicatorAnimation,
    transition: (0, testableTransition_1.default)(),
};
const WaitingIndicator = (0, styled_1.default)(framer_motion_1.motion.div) `
  margin: 0 6px;
  ${pulsingIndicator_1.default};
`;
WaitingIndicator.defaultProps = {
    variants: indicatorAnimation,
    transition: (0, testableTransition_1.default)(),
};
const ReceivedIndicator = (0, styled_1.default)(icons_1.IconCheckmark) `
  color: #fff;
  background: ${p => p.theme.green300};
  border-radius: 50%;
  padding: 3px;
  margin: 0 ${(0, space_1.default)(0.25)};
`;
ReceivedIndicator.defaultProps = {
    size: 'sm',
};
exports.default = FirstEventIndicator;
//# sourceMappingURL=firstEventIndicator.jsx.map