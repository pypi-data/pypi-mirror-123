Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const sprintf_js_1 = require("sprintf-js");
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const defaultProps = {
    label: (0, locale_1.t)('Ignore this issue until \u2026'),
};
class CustomIgnoreDurationModal extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            dateWarning: false,
        };
        this.snoozeDateInputRef = (0, react_1.createRef)();
        this.snoozeTimeInputRef = (0, react_1.createRef)();
        this.selectedIgnoreMinutes = () => {
            var _a, _b;
            const dateStr = (_a = this.snoozeDateInputRef.current) === null || _a === void 0 ? void 0 : _a.value; // YYYY-MM-DD
            const timeStr = (_b = this.snoozeTimeInputRef.current) === null || _b === void 0 ? void 0 : _b.value; // HH:MM
            if (dateStr && timeStr) {
                const selectedDate = moment_1.default.utc(dateStr + ' ' + timeStr);
                if (selectedDate.isValid()) {
                    const now = moment_1.default.utc();
                    return selectedDate.diff(now, 'minutes');
                }
            }
            return 0;
        };
        this.snoozeClicked = () => {
            const minutes = this.selectedIgnoreMinutes();
            this.setState({
                dateWarning: minutes <= 0,
            });
            if (minutes > 0) {
                this.props.onSelected({ ignoreDuration: minutes });
            }
            this.props.closeModal();
        };
    }
    render() {
        // Give the user a sane starting point to select a date
        // (prettier than the empty date/time inputs):
        const defaultDate = new Date();
        defaultDate.setDate(defaultDate.getDate() + 14);
        defaultDate.setSeconds(0);
        defaultDate.setMilliseconds(0);
        const defaultDateVal = (0, sprintf_js_1.sprintf)('%d-%02d-%02d', defaultDate.getUTCFullYear(), defaultDate.getUTCMonth() + 1, defaultDate.getUTCDate());
        const defaultTimeVal = (0, sprintf_js_1.sprintf)('%02d:00', defaultDate.getUTCHours());
        const { Header, Body, Footer, label } = this.props;
        return (<react_1.Fragment>
        <Header>{label}</Header>
        <Body>
          <form className="form-horizontal">
            <div className="control-group">
              <h6 className="nav-header">{(0, locale_1.t)('Date')}</h6>
              <input className="form-control" type="date" id="snooze-until-date" defaultValue={defaultDateVal} ref={this.snoozeDateInputRef} required style={{ padding: '0 10px' }}/>
            </div>
            <div className="control-group m-b-1">
              <h6 className="nav-header">{(0, locale_1.t)('Time (UTC)')}</h6>
              <input className="form-control" type="time" id="snooze-until-time" defaultValue={defaultTimeVal} ref={this.snoozeTimeInputRef} style={{ padding: '0 10px' }} required/>
            </div>
          </form>
        </Body>
        {this.state.dateWarning && (<alert_1.default icon={<icons_1.IconWarning size="md"/>} type="error">
            {(0, locale_1.t)('Please enter a valid date in the future')}
          </alert_1.default>)}
        <Footer>
          <buttonBar_1.default gap={1}>
            <button_1.default type="button" priority="default" onClick={this.props.closeModal}>
              {(0, locale_1.t)('Cancel')}
            </button_1.default>
            <button_1.default type="button" priority="primary" onClick={this.snoozeClicked}>
              {(0, locale_1.t)('Ignore')}
            </button_1.default>
          </buttonBar_1.default>
        </Footer>
      </react_1.Fragment>);
    }
}
exports.default = CustomIgnoreDurationModal;
CustomIgnoreDurationModal.defaultProps = defaultProps;
//# sourceMappingURL=customIgnoreDurationModal.jsx.map