Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const hookOrDefault_1 = (0, tslib_1.__importDefault)(require("app/components/hookOrDefault"));
const locale_1 = require("app/locale");
const animations_1 = require("app/styles/animations");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
class SkipConfirm extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            showConfirmation: false,
        };
        this.toggleConfirm = (e) => {
            e.stopPropagation();
            this.setState(state => ({ showConfirmation: !state.showConfirmation }));
        };
        this.handleSkip = (e) => {
            e.stopPropagation();
            this.props.onSkip();
        };
    }
    render() {
        const { children } = this.props;
        return (<React.Fragment>
        {children({ skip: this.toggleConfirm })}
        <Confirmation visible={this.state.showConfirmation} onSkip={this.handleSkip} onDismiss={this.toggleConfirm}/>
      </React.Fragment>);
    }
}
exports.default = SkipConfirm;
const SkipHelp = (0, hookOrDefault_1.default)({
    hookName: 'onboarding-wizard:skip-help',
    defaultComponent: () => (<button_1.default priority="primary" size="xsmall" to="https://forum.sentry.io/" external>
      {(0, locale_1.t)('Community Forum')}
    </button_1.default>),
});
const Confirmation = (0, styled_1.default)((_a) => {
    var { onDismiss, onSkip, visible: _ } = _a, props = (0, tslib_1.__rest)(_a, ["onDismiss", "onSkip", "visible"]);
    return (<div onClick={onDismiss} {...props}>
    <p>{(0, locale_1.t)("Not sure what to do? We're here for you!")}</p>
    <buttonBar_1.default gap={1}>
      <SkipHelp />
      <button_1.default size="xsmall" onClick={onSkip}>
        {(0, locale_1.t)('Just skip')}
      </button_1.default>
    </buttonBar_1.default>
  </div>);
}) `
  display: ${p => (p.visible ? 'flex' : 'none')};
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  padding: 0 ${(0, space_1.default)(3)};
  border-radius: ${p => p.theme.borderRadius};
  align-items: center;
  flex-direction: column;
  justify-content: center;
  background: rgba(255, 255, 255, 0.9);
  animation: ${animations_1.fadeIn} 200ms normal forwards;
  font-size: ${p => p.theme.fontSizeMedium};

  p {
    margin-bottom: ${(0, space_1.default)(1)};
  }
`;
//# sourceMappingURL=skipConfirm.jsx.map