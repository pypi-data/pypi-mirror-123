Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const clipboard_1 = (0, tslib_1.__importDefault)(require("app/components/clipboard"));
const confirmDelete_1 = (0, tslib_1.__importDefault)(require("app/components/confirmDelete"));
const dateTime_1 = (0, tslib_1.__importDefault)(require("app/components/dateTime"));
const questionTooltip_1 = (0, tslib_1.__importDefault)(require("app/components/questionTooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const CardHeader = ({ publicKey, name, description, created, disabled, onEdit, onDelete, }) => {
    const deleteButton = (<button_1.default size="small" icon={<icons_1.IconDelete />} label={(0, locale_1.t)('Delete Key')} disabled={disabled} title={disabled ? (0, locale_1.t)('You do not have permission to delete keys') : undefined}/>);
    return (<Header>
      <KeyName>
        {name}
        {description && <questionTooltip_1.default position="top" size="sm" title={description}/>}
      </KeyName>
      <DateCreated>
        {(0, locale_1.tct)('Created on [date]', { date: <dateTime_1.default date={created} timeAndDate/> })}
      </DateCreated>
      <StyledButtonBar gap={1}>
        <clipboard_1.default value={publicKey}>
          <button_1.default size="small" icon={<icons_1.IconCopy />}>
            {(0, locale_1.t)('Copy Key')}
          </button_1.default>
        </clipboard_1.default>
        <button_1.default size="small" onClick={onEdit(publicKey)} icon={<icons_1.IconEdit />} label={(0, locale_1.t)('Edit Key')} disabled={disabled} title={disabled ? (0, locale_1.t)('You do not have permission to edit keys') : undefined}/>
        {disabled ? (deleteButton) : (<confirmDelete_1.default message={(0, locale_1.t)('After removing this Public Key, your Relay will no longer be able to communicate with Sentry and events will be dropped.')} onConfirm={onDelete(publicKey)} confirmInput={name}>
            {deleteButton}
          </confirmDelete_1.default>)}
      </StyledButtonBar>
    </Header>);
};
exports.default = CardHeader;
const KeyName = (0, styled_1.default)('div') `
  grid-row: 1/2;
  display: grid;
  grid-template-columns: repeat(2, max-content);
  grid-column-gap: ${(0, space_1.default)(0.5)};
`;
const DateCreated = (0, styled_1.default)('div') `
  grid-row: 2/3;
  color: ${p => p.theme.gray300};
  font-size: ${p => p.theme.fontSizeMedium};
`;
const StyledButtonBar = (0, styled_1.default)(buttonBar_1.default) `
  @media (min-width: ${p => p.theme.breakpoints[1]}) {
    grid-row: 1/3;
  }
`;
const Header = (0, styled_1.default)('div') `
  display: grid;
  grid-row-gap: ${(0, space_1.default)(1)};
  margin-bottom: ${(0, space_1.default)(1)};

  @media (min-width: ${p => p.theme.breakpoints[1]}) {
    grid-template-columns: 1fr max-content;
    grid-template-rows: repeat(2, max-content);
  }
`;
//# sourceMappingURL=cardHeader.jsx.map