Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const input_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/input"));
const field_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field"));
const types_1 = require("../../types");
const utils_1 = require("../utils");
const eventIdFieldStatusIcon_1 = (0, tslib_1.__importDefault)(require("./eventIdFieldStatusIcon"));
class EventIdField extends React.Component {
    constructor() {
        super(...arguments);
        this.state = Object.assign({}, this.props.eventId);
        this.handleChange = (event) => {
            const eventId = event.target.value.replace(/-/g, '').trim();
            if (eventId !== this.state.value) {
                this.setState({
                    value: eventId,
                    status: types_1.EventIdStatus.UNDEFINED,
                });
            }
        };
        this.handleBlur = (event) => {
            event.preventDefault();
            if (this.isEventIdValid()) {
                this.props.onUpdateEventId(this.state.value);
            }
        };
        this.handleKeyDown = (event) => {
            const { keyCode } = event;
            if (keyCode === 13 && this.isEventIdValid()) {
                this.props.onUpdateEventId(this.state.value);
            }
        };
        this.handleClickIconClose = () => {
            this.setState({
                value: '',
                status: types_1.EventIdStatus.UNDEFINED,
            });
        };
    }
    componentDidUpdate(prevProps) {
        if (!(0, isEqual_1.default)(prevProps.eventId, this.props.eventId)) {
            this.loadState();
        }
    }
    loadState() {
        this.setState(Object.assign({}, this.props.eventId));
    }
    getErrorMessage() {
        const { status } = this.state;
        switch (status) {
            case types_1.EventIdStatus.INVALID:
                return (0, locale_1.t)('This event ID is invalid.');
            case types_1.EventIdStatus.ERROR:
                return (0, locale_1.t)('An error occurred while fetching the suggestions based on this event ID.');
            case types_1.EventIdStatus.NOT_FOUND:
                return (0, locale_1.t)('The chosen event ID was not found in projects you have access to.');
            default:
                return undefined;
        }
    }
    isEventIdValid() {
        const { value, status } = this.state;
        if (value && value.length !== 32) {
            if (status !== types_1.EventIdStatus.INVALID) {
                (0, utils_1.saveToSourceGroupData)({ value, status });
                this.setState({ status: types_1.EventIdStatus.INVALID });
            }
            return false;
        }
        return true;
    }
    render() {
        const { disabled } = this.props;
        const { value, status } = this.state;
        return (<field_1.default data-test-id="event-id-field" label={(0, locale_1.t)('Event ID (Optional)')} help={(0, locale_1.t)('Providing an event ID will automatically provide you a list of suggested sources')} inline={false} error={this.getErrorMessage()} flexibleControlStateSize stacked showHelpInTooltip>
        <FieldWrapper>
          <StyledInput type="text" name="eventId" disabled={disabled} value={value} placeholder={(0, locale_1.t)('XXXXXXXXXXXXXX')} onChange={this.handleChange} onKeyDown={this.handleKeyDown} onBlur={this.handleBlur}/>
          <Status>
            <eventIdFieldStatusIcon_1.default onClickIconClose={this.handleClickIconClose} status={status}/>
          </Status>
        </FieldWrapper>
      </field_1.default>);
    }
}
exports.default = EventIdField;
const StyledInput = (0, styled_1.default)(input_1.default) `
  flex: 1;
  font-weight: 400;
  input {
    padding-right: ${(0, space_1.default)(1.5)};
  }
  margin-bottom: 0;
`;
const Status = (0, styled_1.default)('div') `
  height: 40px;
  position: absolute;
  right: ${(0, space_1.default)(1.5)};
  top: 0;
  display: flex;
  align-items: center;
`;
const FieldWrapper = (0, styled_1.default)('div') `
  position: relative;
  display: flex;
  align-items: center;
`;
//# sourceMappingURL=eventIdField.jsx.map