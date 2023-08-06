Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const access_1 = (0, tslib_1.__importDefault)(require("app/components/acl/access"));
const role_1 = (0, tslib_1.__importDefault)(require("app/components/acl/role"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/actions/button"));
const menuItemActionLink_1 = (0, tslib_1.__importDefault)(require("app/components/actions/menuItemActionLink"));
const button_2 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const dropdownLink_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownLink"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const debugImage_1 = require("app/types/debugImage");
const noPermissionToDownloadDebugFilesInfo = (0, locale_1.t)('You do not have permission to download debug files');
const noPermissionToDeleteDebugFilesInfo = (0, locale_1.t)('You do not have permission to delete debug files');
const debugFileDeleteConfirmationInfo = (0, locale_1.t)('Are you sure you wish to delete this file?');
function Actions({ candidate, organization, isInternalSource, baseUrl, projSlug, onDelete, }) {
    const { download, location: debugFileId } = candidate;
    const { status } = download;
    if (!debugFileId || !isInternalSource) {
        return null;
    }
    const deleted = status === debugImage_1.CandidateDownloadStatus.DELETED;
    const downloadUrl = `${baseUrl}/projects/${organization.slug}/${projSlug}/files/dsyms/?id=${debugFileId}`;
    const actions = (<role_1.default role={organization.debugFilesRole} organization={organization}>
      {({ hasRole }) => (<access_1.default access={['project:write']} organization={organization}>
          {({ hasAccess }) => (<react_1.Fragment>
              <StyledDropdownLink caret={false} customTitle={<button_1.default label={(0, locale_1.t)('Actions')} disabled={deleted} icon={<icons_1.IconEllipsis size="sm"/>}/>} anchorRight>
                <tooltip_1.default disabled={hasRole} title={noPermissionToDownloadDebugFilesInfo}>
                  <menuItemActionLink_1.default shouldConfirm={false} icon={<icons_1.IconDownload size="xs"/>} title={(0, locale_1.t)('Download')} href={downloadUrl} onClick={event => {
                    if (deleted) {
                        event.preventDefault();
                    }
                }} disabled={!hasRole || deleted}>
                    {(0, locale_1.t)('Download')}
                  </menuItemActionLink_1.default>
                </tooltip_1.default>
                <tooltip_1.default disabled={hasAccess} title={noPermissionToDeleteDebugFilesInfo}>
                  <menuItemActionLink_1.default onAction={() => onDelete(debugFileId)} message={debugFileDeleteConfirmationInfo} title={(0, locale_1.t)('Delete')} disabled={!hasAccess || deleted} shouldConfirm>
                    {(0, locale_1.t)('Delete')}
                  </menuItemActionLink_1.default>
                </tooltip_1.default>
              </StyledDropdownLink>
              <StyledButtonBar gap={1}>
                <tooltip_1.default disabled={hasRole} title={noPermissionToDownloadDebugFilesInfo}>
                  <button_2.default size="xsmall" icon={<icons_1.IconDownload size="xs"/>} href={downloadUrl} disabled={!hasRole}>
                    {(0, locale_1.t)('Download')}
                  </button_2.default>
                </tooltip_1.default>
                <tooltip_1.default disabled={hasAccess} title={noPermissionToDeleteDebugFilesInfo}>
                  <confirm_1.default confirmText={(0, locale_1.t)('Delete')} message={debugFileDeleteConfirmationInfo} onConfirm={() => onDelete(debugFileId)} disabled={!hasAccess}>
                    <button_2.default priority="danger" icon={<icons_1.IconDelete size="xs"/>} size="xsmall" disabled={!hasAccess}/>
                  </confirm_1.default>
                </tooltip_1.default>
              </StyledButtonBar>
            </react_1.Fragment>)}
        </access_1.default>)}
    </role_1.default>);
    if (!deleted) {
        return actions;
    }
    return (<tooltip_1.default title={(0, locale_1.t)('Actions not available because this debug file was deleted')}>
      {actions}
    </tooltip_1.default>);
}
exports.default = Actions;
const StyledDropdownLink = (0, styled_1.default)(dropdownLink_1.default) `
  display: none;

  @media (min-width: ${props => props.theme.breakpoints[4]}) {
    display: flex;
    align-items: center;
    transition: none;
  }
`;
const StyledButtonBar = (0, styled_1.default)(buttonBar_1.default) `
  @media (min-width: ${props => props.theme.breakpoints[4]}) {
    display: none;
  }
`;
//# sourceMappingURL=actions.jsx.map