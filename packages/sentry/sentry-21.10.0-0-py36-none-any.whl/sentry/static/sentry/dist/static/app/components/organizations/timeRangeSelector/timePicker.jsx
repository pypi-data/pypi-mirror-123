Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const classnames_1 = (0, tslib_1.__importDefault)(require("classnames"));
const TimePicker = (0, styled_1.default)(class TimePicker extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            focused: false,
        };
        this.handleFocus = () => {
            this.setState({ focused: true });
        };
        this.handleBlur = () => {
            this.setState({ focused: false });
        };
    }
    shouldComponentUpdate() {
        // This is necessary because when a change event happens,
        // the change is propagated up to the dropdown. This causes
        // a re-render of this component which in turn causes the
        // input element to lose focus. To get around losing focus,
        // we prevent the component from updating when one of the
        // inputs has focus. This is okay because the inputs will
        // keep track of their own values so we do not have to keep
        // track of it.
        return !this.state.focused;
    }
    render() {
        const { className, start, end, disabled, onChangeStart, onChangeEnd } = this.props;
        return (<div className={(0, classnames_1.default)(className, 'rdrDateDisplay')}>
          <div>
            <Input type="time" key={start} defaultValue={start} className="rdrDateDisplayItem" data-test-id="startTime" disabled={disabled} onFocus={this.handleFocus} onBlur={this.handleBlur} onChange={onChangeStart}/>
          </div>

          <div>
            <Input type="time" defaultValue={end} key={end} className="rdrDateDisplayItem" data-test-id="endTime" disabled={disabled} onFocus={this.handleFocus} onBlur={this.handleBlur} onChange={onChangeEnd}/>
          </div>
        </div>);
    }
}) `
  &.rdrDateDisplay {
    display: grid;
    background: transparent;
    grid-template-columns: 48% 48%;
    grid-column-gap: 4%;
    align-items: center;
    font-size: 0.875em;
    color: ${p => p.theme.subText};
    width: 70%;
    padding: 0;
  }
`;
const Input = (0, styled_1.default)('input') `
  &.rdrDateDisplayItem {
    width: 100%;
    padding-left: 5%;
    background: ${p => p.theme.backgroundSecondary};
    border: 1px solid ${p => p.theme.border};
    color: ${p => p.theme.gray300};
    box-shadow: none;
  }
`;
exports.default = TimePicker;
//# sourceMappingURL=timePicker.jsx.map