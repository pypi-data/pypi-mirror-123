Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const menuItemActionLink_1 = (0, tslib_1.__importDefault)(require("app/components/actions/menuItemActionLink"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const dropdownLink_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownLink"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const deleteRuleConfirmMessage = (0, locale_1.t)('Are you sure you wish to delete this dynamic sampling rule?');
const deleteRuleMessage = (0, locale_1.t)('You do not have permission to delete dynamic sampling rules.');
const editRuleMessage = (0, locale_1.t)('You do not have permission to edit dynamic sampling rules.');
function Actions({ disabled, onEditRule, onDeleteRule, onOpenMenuActions, isMenuActionsOpen, }) {
    return (<react_1.Fragment>
      <StyledButtonbar gap={1}>
        <button_1.default label={(0, locale_1.t)('Edit Rule')} size="small" onClick={onEditRule} icon={<icons_1.IconEdit />} disabled={disabled} title={disabled ? editRuleMessage : undefined}/>
        <confirm_1.default priority="danger" message={deleteRuleConfirmMessage} onConfirm={onDeleteRule} disabled={disabled}>
          <button_1.default label={(0, locale_1.t)('Delete Rule')} size="small" icon={<icons_1.IconDelete />} title={disabled ? deleteRuleMessage : undefined}/>
        </confirm_1.default>
      </StyledButtonbar>
      <StyledDropdownLink caret={false} customTitle={<button_1.default label={(0, locale_1.t)('Actions')} icon={<icons_1.IconEllipsis size="sm"/>} size="xsmall" onClick={onOpenMenuActions}/>} isOpen={isMenuActionsOpen} anchorRight>
        <menuItemActionLink_1.default shouldConfirm={false} icon={<icons_1.IconDownload size="xs"/>} title={(0, locale_1.t)('Edit')} onClick={!disabled
            ? onEditRule
            : event => {
                event === null || event === void 0 ? void 0 : event.stopPropagation();
            }} disabled={disabled}>
          <tooltip_1.default disabled={!disabled} title={editRuleMessage} containerDisplayMode="block">
            {(0, locale_1.t)('Edit')}
          </tooltip_1.default>
        </menuItemActionLink_1.default>
        <menuItemActionLink_1.default onAction={onDeleteRule} message={deleteRuleConfirmMessage} icon={<icons_1.IconDownload size="xs"/>} title={(0, locale_1.t)('Delete')} disabled={disabled} priority="danger" shouldConfirm>
          <tooltip_1.default disabled={!disabled} title={deleteRuleMessage} containerDisplayMode="block">
            {(0, locale_1.t)('Delete')}
          </tooltip_1.default>
        </menuItemActionLink_1.default>
      </StyledDropdownLink>
    </react_1.Fragment>);
}
exports.default = Actions;
const StyledButtonbar = (0, styled_1.default)(buttonBar_1.default) `
  justify-content: flex-end;
  flex: 1;
  display: none;
  @media (min-width: ${p => p.theme.breakpoints[2]}) {
    display: grid;
  }
`;
const StyledDropdownLink = (0, styled_1.default)(dropdownLink_1.default) `
  display: flex;
  align-items: center;
  transition: none;
  @media (min-width: ${p => p.theme.breakpoints[2]}) {
    display: none;
  }
`;
//# sourceMappingURL=actions.jsx.map