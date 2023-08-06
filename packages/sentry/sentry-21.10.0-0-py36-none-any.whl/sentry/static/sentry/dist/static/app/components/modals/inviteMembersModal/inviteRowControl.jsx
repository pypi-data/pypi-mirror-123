Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@emotion/react");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const selectControl_1 = (0, tslib_1.__importDefault)(require("app/components/forms/selectControl"));
const teamSelector_1 = (0, tslib_1.__importDefault)(require("app/components/forms/teamSelector"));
const roleSelectControl_1 = (0, tslib_1.__importDefault)(require("app/components/roleSelectControl"));
const iconClose_1 = require("app/icons/iconClose");
const locale_1 = require("app/locale");
const renderEmailValue_1 = (0, tslib_1.__importDefault)(require("./renderEmailValue"));
function ValueComponent(props, inviteStatus) {
    return (0, renderEmailValue_1.default)(inviteStatus[props.data.value], props);
}
function mapToOptions(values) {
    return values.map(value => ({ value, label: value }));
}
class InviteRowControl extends React.Component {
    constructor() {
        super(...arguments);
        this.state = { inputValue: '' };
        this.handleInputChange = (inputValue) => {
            this.setState({ inputValue });
        };
        this.handleKeyDown = (event) => {
            const { onChangeEmails, emails } = this.props;
            const { inputValue } = this.state;
            switch (event.key) {
                case 'Enter':
                case ',':
                case ' ':
                    onChangeEmails([...mapToOptions(emails), { label: inputValue, value: inputValue }]);
                    this.setState({ inputValue: '' });
                    event.preventDefault();
                    break;
                default:
                // do nothing.
            }
        };
    }
    render() {
        const { className, disabled, emails, role, teams, roleOptions, roleDisabledUnallowed, inviteStatus, onRemove, onChangeEmails, onChangeRole, onChangeTeams, disableRemove, theme, } = this.props;
        return (<div className={className}>
        <selectControl_1.default data-test-id="select-emails" disabled={disabled} placeholder={(0, locale_1.t)('Enter one or more emails')} inputValue={this.state.inputValue} value={emails} components={{
                MultiValue: props => ValueComponent(props, inviteStatus),
                DropdownIndicator: () => null,
            }} options={mapToOptions(emails)} onBlur={(e) => e.target.value &&
                onChangeEmails([
                    ...mapToOptions(emails),
                    { label: e.target.value, value: e.target.value },
                ])} styles={getStyles(theme, inviteStatus)} onInputChange={this.handleInputChange} onKeyDown={this.handleKeyDown} onChange={onChangeEmails} multiple creatable clearable menuIsOpen={false}/>
        <roleSelectControl_1.default data-test-id="select-role" disabled={disabled} value={role} roles={roleOptions} disableUnallowed={roleDisabledUnallowed} onChange={onChangeRole}/>
        <teamSelector_1.default data-test-id="select-teams" disabled={disabled} placeholder={(0, locale_1.t)('Add to teams\u2026')} value={teams} onChange={onChangeTeams} multiple clearable/>
        <button_1.default borderless icon={<iconClose_1.IconClose />} size="zero" onClick={onRemove} disabled={disableRemove}/>
      </div>);
    }
}
/**
 * The email select control has custom selected item states as items
 * show their delivery status after the form is submitted.
 */
function getStyles(theme, inviteStatus) {
    return {
        multiValue: (provided, { data }) => {
            const status = inviteStatus[data.value];
            return Object.assign(Object.assign({}, provided), ((status === null || status === void 0 ? void 0 : status.error)
                ? {
                    color: theme.red300,
                    border: `1px solid ${theme.red300}`,
                    backgroundColor: theme.red100,
                }
                : {}));
        },
        multiValueLabel: (provided, { data }) => {
            const status = inviteStatus[data.value];
            return Object.assign(Object.assign(Object.assign({}, provided), { pointerEvents: 'all' }), ((status === null || status === void 0 ? void 0 : status.error) ? { color: theme.red300 } : {}));
        },
        multiValueRemove: (provided, { data }) => {
            const status = inviteStatus[data.value];
            return Object.assign(Object.assign({}, provided), ((status === null || status === void 0 ? void 0 : status.error)
                ? {
                    borderLeft: `1px solid ${theme.red300}`,
                    ':hover': { backgroundColor: theme.red100, color: theme.red300 },
                }
                : {}));
        },
    };
}
exports.default = (0, react_1.withTheme)(InviteRowControl);
//# sourceMappingURL=inviteRowControl.jsx.map