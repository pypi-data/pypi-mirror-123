Object.defineProperty(exports, "__esModule", { value: true });
exports.GuideAnchor = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const guides_1 = require("app/actionCreators/guides");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const hovercard_1 = (0, tslib_1.__importStar)(require("app/components/hovercard"));
const locale_1 = require("app/locale");
const guideStore_1 = (0, tslib_1.__importDefault)(require("app/stores/guideStore"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
/**
 * A GuideAnchor puts an informative hovercard around an element.
 * Guide anchors register with the GuideStore, which uses registrations
 * from one or more anchors on the page to determine which guides can
 * be shown on the page.
 */
class GuideAnchor extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            active: false,
            step: 0,
            orgId: null,
        };
        this.unsubscribe = guideStore_1.default.listen((data) => this.onGuideStateChange(data), undefined);
        this.containerElement = React.createRef();
        /**
         * Terminology:
         *
         *  - A guide can be FINISHED by clicking one of the buttons in the last step
         *  - A guide can be DISMISSED by x-ing out of it at any step except the last (where there is no x)
         *  - In both cases we consider it CLOSED
         */
        this.handleFinish = (e) => {
            e.stopPropagation();
            const { onFinish } = this.props;
            if (onFinish) {
                onFinish();
            }
            const { currentGuide, orgId } = this.state;
            if (currentGuide) {
                (0, guides_1.recordFinish)(currentGuide.guide, orgId);
            }
            (0, guides_1.closeGuide)();
        };
        this.handleNextStep = (e) => {
            e.stopPropagation();
            (0, guides_1.nextStep)();
        };
        this.handleDismiss = (e) => {
            e.stopPropagation();
            const { currentGuide, step, orgId } = this.state;
            if (currentGuide) {
                (0, guides_1.dismissGuide)(currentGuide.guide, step, orgId);
            }
        };
    }
    componentDidMount() {
        const { target } = this.props;
        target && (0, guides_1.registerAnchor)(target);
    }
    componentDidUpdate(_prevProps, prevState) {
        if (this.containerElement.current && !prevState.active && this.state.active) {
            try {
                const { top } = this.containerElement.current.getBoundingClientRect();
                const scrollTop = window.pageYOffset;
                const centerElement = top + scrollTop - window.innerHeight / 2;
                window.scrollTo({ top: centerElement });
            }
            catch (err) {
                Sentry.captureException(err);
            }
        }
    }
    componentWillUnmount() {
        const { target } = this.props;
        target && (0, guides_1.unregisterAnchor)(target);
        this.unsubscribe();
    }
    onGuideStateChange(data) {
        var _a, _b, _c, _d;
        const active = (_c = ((_b = (_a = data.currentGuide) === null || _a === void 0 ? void 0 : _a.steps[data.currentStep]) === null || _b === void 0 ? void 0 : _b.target) === this.props.target) !== null && _c !== void 0 ? _c : false;
        this.setState({
            active,
            currentGuide: (_d = data.currentGuide) !== null && _d !== void 0 ? _d : undefined,
            step: data.currentStep,
            orgId: data.orgId,
        });
    }
    getHovercardBody() {
        const { to } = this.props;
        const { currentGuide, step } = this.state;
        if (!currentGuide) {
            return null;
        }
        const totalStepCount = currentGuide.steps.length;
        const currentStepCount = step + 1;
        const currentStep = currentGuide.steps[step];
        const lastStep = currentStepCount === totalStepCount;
        const hasManySteps = totalStepCount > 1;
        // to clear `#assistant` from the url
        const href = window.location.hash === '#assistant' ? '#' : '';
        const dismissButton = (<DismissButton size="small" href={href} onClick={this.handleDismiss} priority="link">
        {currentStep.dismissText || (0, locale_1.t)('Dismiss')}
      </DismissButton>);
        return (<GuideContainer>
        <GuideContent>
          {currentStep.title && <GuideTitle>{currentStep.title}</GuideTitle>}
          <GuideDescription>{currentStep.description}</GuideDescription>
        </GuideContent>
        <GuideAction>
          <div>
            {lastStep ? (<React.Fragment>
                <StyledButton size="small" to={to} onClick={this.handleFinish}>
                  {currentStep.nextText ||
                    (hasManySteps ? (0, locale_1.t)('Enough Already') : (0, locale_1.t)('Got It'))}
                </StyledButton>
                {currentStep.hasNextGuide && dismissButton}
              </React.Fragment>) : (<React.Fragment>
                <StyledButton size="small" onClick={this.handleNextStep} to={to}>
                  {currentStep.nextText || (0, locale_1.t)('Next')}
                </StyledButton>
                {!currentStep.cantDismiss && dismissButton}
              </React.Fragment>)}
          </div>

          {hasManySteps && (<StepCount>
              {(0, locale_1.tct)('[currentStepCount] of [totalStepCount]', {
                    currentStepCount,
                    totalStepCount,
                })}
            </StepCount>)}
        </GuideAction>
      </GuideContainer>);
    }
    render() {
        const { children, position, offset, containerClassName } = this.props;
        const { active } = this.state;
        if (!active) {
            return children ? children : null;
        }
        return (<StyledHovercard show body={this.getHovercardBody()} tipColor={theme_1.default.purple300} position={position} offset={offset} containerClassName={containerClassName}>
        <span ref={this.containerElement}>{children}</span>
      </StyledHovercard>);
    }
}
exports.GuideAnchor = GuideAnchor;
class GuideAnchorWrapper extends React.Component {
    render() {
        const _a = this.props, { disabled, children } = _a, rest = (0, tslib_1.__rest)(_a, ["disabled", "children"]);
        if (disabled || window.localStorage.getItem('hide_anchors') === '1') {
            return children || null;
        }
        return <GuideAnchor {...rest}>{children}</GuideAnchor>;
    }
}
exports.default = GuideAnchorWrapper;
const GuideContainer = (0, styled_1.default)('div') `
  display: grid;
  grid-template-rows: repeat(2, auto);
  grid-gap: ${(0, space_1.default)(2)};
  text-align: center;
  line-height: 1.5;
  background-color: ${p => p.theme.purple300};
  border-color: ${p => p.theme.purple300};
  color: ${p => p.theme.white};
`;
const GuideContent = (0, styled_1.default)('div') `
  display: grid;
  grid-template-rows: repeat(2, auto);
  grid-gap: ${(0, space_1.default)(1)};

  a {
    color: ${p => p.theme.white};
    text-decoration: underline;
  }
`;
const GuideTitle = (0, styled_1.default)('div') `
  font-weight: bold;
  font-size: ${p => p.theme.fontSizeExtraLarge};
`;
const GuideDescription = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeMedium};
`;
const GuideAction = (0, styled_1.default)('div') `
  display: grid;
  grid-template-rows: repeat(2, auto);
  grid-gap: ${(0, space_1.default)(1)};
`;
const StyledButton = (0, styled_1.default)(button_1.default) `
  font-size: ${p => p.theme.fontSizeMedium};
  min-width: 40%;
`;
const DismissButton = (0, styled_1.default)(StyledButton) `
  margin-left: ${(0, space_1.default)(1)};

  &:hover,
  &:focus,
  &:active {
    color: ${p => p.theme.white};
  }
  color: ${p => p.theme.white};
`;
const StepCount = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeSmall};
  font-weight: bold;
  text-transform: uppercase;
`;
const StyledHovercard = (0, styled_1.default)(hovercard_1.default) `
  ${hovercard_1.Body} {
    background-color: ${theme_1.default.purple300};
    margin: -1px;
    border-radius: ${theme_1.default.borderRadius};
    width: 300px;
  }
`;
//# sourceMappingURL=guideAnchor.jsx.map