Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/actions/button"));
const menuItemActionLink_1 = (0, tslib_1.__importDefault)(require("app/components/actions/menuItemActionLink"));
const button_2 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const confirmDelete_1 = (0, tslib_1.__importDefault)(require("app/components/confirmDelete"));
const dropdownButton_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownButton"));
const dropdownLink_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownLink"));
const iconEllipsis_1 = require("app/icons/iconEllipsis");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const debugFiles_1 = require("app/types/debugFiles");
const textBlock_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/text/textBlock"));
function Actions({ repositoryName, repositoryType, isDetailsExpanded, isDetailsDisabled, onToggleDetails, onEdit, onDelete, showDetails, }) {
    function renderConfirmDelete(element) {
        return (<confirmDelete_1.default confirmText={(0, locale_1.t)('Delete Repository')} message={repositoryType === debugFiles_1.CustomRepoType.APP_STORE_CONNECT ? (<react_1.Fragment>
              <textBlock_1.default>
                <strong>
                  {(0, locale_1.t)('Removing App Store Connect symbol source does not remove current dSYMs.')}
                </strong>
              </textBlock_1.default>
              <textBlock_1.default>
                {(0, locale_1.t)('The App Store Connect symbol source periodically imports dSYMs into the "Uploaded debug information files". Removing this symbol source does not delete those files and they will remain available for symbolication until deleted directly.')}
              </textBlock_1.default>
            </react_1.Fragment>) : (<react_1.Fragment>
              <textBlock_1.default>
                <strong>
                  {(0, locale_1.t)('Removing this repository applies instantly to new events.')}
                </strong>
              </textBlock_1.default>
              <textBlock_1.default>
                {(0, locale_1.t)('Debug files from this repository will not be used to symbolicate future events. This may create new issues and alert members in your organization.')}
              </textBlock_1.default>
            </react_1.Fragment>)} confirmInput={repositoryName} priority="danger" onConfirm={onDelete}>
        {element}
      </confirmDelete_1.default>);
    }
    return (<StyledButtonBar gap={1}>
      {showDetails && (<StyledDropdownButton isOpen={isDetailsExpanded} size="small" onClick={isDetailsDisabled ? undefined : onToggleDetails} hideBottomBorder={false} disabled={isDetailsDisabled}>
          {(0, locale_1.t)('Details')}
        </StyledDropdownButton>)}
      <StyledButton onClick={onEdit} size="small">
        {(0, locale_1.t)('Configure')}
      </StyledButton>
      {renderConfirmDelete(<StyledButton size="small">{(0, locale_1.t)('Delete')}</StyledButton>)}
      <DropDownWrapper>
        <dropdownLink_1.default caret={false} customTitle={<StyledActionButton label={(0, locale_1.t)('Actions')} icon={<iconEllipsis_1.IconEllipsis />}/>} anchorRight>
          <menuItemActionLink_1.default title={(0, locale_1.t)('Configure')} onClick={onEdit}>
            {(0, locale_1.t)('Configure')}
          </menuItemActionLink_1.default>
          {renderConfirmDelete(<menuItemActionLink_1.default title={(0, locale_1.t)('Delete')}>{(0, locale_1.t)('Delete')}</menuItemActionLink_1.default>)}
        </dropdownLink_1.default>
      </DropDownWrapper>
    </StyledButtonBar>);
}
exports.default = Actions;
const StyledActionButton = (0, styled_1.default)(button_1.default) `
  height: 32px;
`;
const StyledDropdownButton = (0, styled_1.default)(dropdownButton_1.default) `
  border-bottom-right-radius: ${p => p.theme.borderRadius};
  border-bottom-left-radius: ${p => p.theme.borderRadius};
`;
const StyledButtonBar = (0, styled_1.default)(buttonBar_1.default) `
  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    grid-row: 1 / 3;
  }

  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    grid-auto-flow: row;
    grid-gap: ${(0, space_1.default)(1)};
    margin-top: ${(0, space_1.default)(0.5)};
  }
`;
const StyledButton = (0, styled_1.default)(button_2.default) `
  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    display: none;
  }
`;
const DropDownWrapper = (0, styled_1.default)('div') `
  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    display: none;
  }
`;
//# sourceMappingURL=actions.jsx.map