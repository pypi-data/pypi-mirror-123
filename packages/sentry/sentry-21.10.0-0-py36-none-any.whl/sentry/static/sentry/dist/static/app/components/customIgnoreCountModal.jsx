Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const locale_1 = require("app/locale");
const inputField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/inputField"));
const selectField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/selectField"));
class CustomIgnoreCountModal extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            count: 100,
            window: null,
        };
        this.handleSubmit = () => {
            const { count, window } = this.state;
            const { countName, windowName } = this.props;
            const statusDetails = { [countName]: count };
            if (window) {
                statusDetails[windowName] = window;
            }
            this.props.onSelected(statusDetails);
            this.props.closeModal();
        };
        this.handleChange = (name, value) => {
            this.setState({ [name]: value });
        };
    }
    render() {
        const { Header, Footer, Body, countLabel, label, closeModal, windowOptions } = this.props;
        const { count, window } = this.state;
        return (<react_1.Fragment>
        <Header>
          <h4>{label}</h4>
        </Header>
        <Body>
          <inputField_1.default inline={false} flexibleControlStateSize stacked label={countLabel} name="count" type="number" value={count} onChange={val => this.handleChange('count', Number(val))} required placeholder={(0, locale_1.t)('e.g. 100')}/>
          <selectField_1.default inline={false} flexibleControlStateSize stacked label={(0, locale_1.t)('Time window')} value={window} name="window" onChange={val => this.handleChange('window', val)} options={windowOptions} placeholder={(0, locale_1.t)('e.g. per hour')} allowClear help={(0, locale_1.t)('(Optional) If supplied, this rule will apply as a rate of change.')}/>
        </Body>
        <Footer>
          <buttonBar_1.default gap={1}>
            <button_1.default type="button" onClick={closeModal}>
              {(0, locale_1.t)('Cancel')}
            </button_1.default>
            <button_1.default type="button" priority="primary" onClick={this.handleSubmit}>
              {(0, locale_1.t)('Ignore')}
            </button_1.default>
          </buttonBar_1.default>
        </Footer>
      </react_1.Fragment>);
    }
}
exports.default = CustomIgnoreCountModal;
//# sourceMappingURL=customIgnoreCountModal.jsx.map