Object.defineProperty(exports, "__esModule", { value: true });
exports.TourImage = exports.TourText = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const modal_1 = require("app/actionCreators/modal");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const callIfFunction_1 = require("app/utils/callIfFunction");
const defaultProps = {
    doneText: (0, locale_1.t)('Done'),
};
/**
 * Provide a showModal action to the child function that lets
 * a tour be triggered.
 *
 * Once active this component will track when the tour was started and keep
 * a last known step state. Ideally the state would live entirely in this component.
 * However, once the modal has been opened state changes in this component don't
 * trigger re-renders in the modal contents. This requires a bit of duplicate state
 * to be managed around the current step.
 */
class FeatureTourModal extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            openedAt: 0,
            current: 0,
        };
        // Record the step change and call the callback this component was given.
        this.handleAdvance = (current, duration) => {
            this.setState({ current });
            (0, callIfFunction_1.callIfFunction)(this.props.onAdvance, current, duration);
        };
        this.handleShow = () => {
            this.setState({ openedAt: Date.now() }, () => {
                const modalProps = {
                    steps: this.props.steps,
                    onAdvance: this.handleAdvance,
                    openedAt: this.state.openedAt,
                    doneText: this.props.doneText,
                    doneUrl: this.props.doneUrl,
                };
                (0, modal_1.openModal)(deps => <ModalContents {...deps} {...modalProps}/>, {
                    onClose: this.handleClose,
                });
            });
        };
        this.handleClose = () => {
            // The bootstrap modal and modal store both call this callback.
            // We use the state flag to deduplicate actions to upstream components.
            if (this.state.openedAt === 0) {
                return;
            }
            const { onCloseModal } = this.props;
            const duration = Date.now() - this.state.openedAt;
            (0, callIfFunction_1.callIfFunction)(onCloseModal, this.state.current, duration);
            // Reset the state now that the modal is closed, used to deduplicate close actions.
            this.setState({ openedAt: 0, current: 0 });
        };
    }
    render() {
        const { children } = this.props;
        return <React.Fragment>{children({ showModal: this.handleShow })}</React.Fragment>;
    }
}
FeatureTourModal.defaultProps = defaultProps;
exports.default = FeatureTourModal;
class ModalContents extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            current: 0,
            openedAt: Date.now(),
        };
        this.handleAdvance = () => {
            const { onAdvance, openedAt } = this.props;
            this.setState(prevState => ({ current: prevState.current + 1 }), () => {
                const duration = Date.now() - openedAt;
                (0, callIfFunction_1.callIfFunction)(onAdvance, this.state.current, duration);
            });
        };
    }
    render() {
        const { Body, steps, doneText, doneUrl, closeModal } = this.props;
        const { current } = this.state;
        const step = steps[current] !== undefined ? steps[current] : steps[steps.length - 1];
        const hasNext = steps[current + 1] !== undefined;
        return (<Body>
        <CloseButton borderless size="zero" onClick={closeModal} icon={<icons_1.IconClose />}/>
        <TourContent>
          {step.image}
          <TourHeader>{step.title}</TourHeader>
          {step.body}
          <TourButtonBar gap={1}>
            {step.actions && step.actions}
            {hasNext && (<button_1.default data-test-id="next-step" priority="primary" onClick={this.handleAdvance}>
                {(0, locale_1.t)('Next')}
              </button_1.default>)}
            {!hasNext && (<button_1.default external href={doneUrl} data-test-id="complete-tour" onClick={closeModal} priority="primary">
                {doneText}
              </button_1.default>)}
          </TourButtonBar>
          <StepCounter>{(0, locale_1.t)('%s of %s', current + 1, steps.length)}</StepCounter>
        </TourContent>
      </Body>);
    }
}
ModalContents.defaultProps = defaultProps;
const CloseButton = (0, styled_1.default)(button_1.default) `
  position: absolute;
  top: -${(0, space_1.default)(2)};
  right: -${(0, space_1.default)(1)};
`;
const TourContent = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: ${(0, space_1.default)(3)} ${(0, space_1.default)(4)} ${(0, space_1.default)(1)} ${(0, space_1.default)(4)};
`;
const TourHeader = (0, styled_1.default)('h4') `
  margin-bottom: ${(0, space_1.default)(1)};
`;
const TourButtonBar = (0, styled_1.default)(buttonBar_1.default) `
  margin-bottom: ${(0, space_1.default)(3)};
`;
const StepCounter = (0, styled_1.default)('div') `
  text-transform: uppercase;
  font-size: ${p => p.theme.fontSizeSmall};
  font-weight: bold;
  color: ${p => p.theme.gray300};
`;
// Styled components that can be used to build tour content.
exports.TourText = (0, styled_1.default)('p') `
  text-align: center;
  margin-bottom: ${(0, space_1.default)(4)};
`;
exports.TourImage = (0, styled_1.default)('img') `
  height: 200px;
  margin-bottom: ${(0, space_1.default)(4)};

  /** override styles in less files */
  max-width: 380px !important;
  box-shadow: none !important;
  border: 0 !important;
  border-radius: 0 !important;
`;
//# sourceMappingURL=featureTourModal.jsx.map