Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const modal_1 = require("app/actionCreators/modal");
const role_1 = (0, tslib_1.__importDefault)(require("app/components/acl/role"));
const menuItemActionLink_1 = (0, tslib_1.__importDefault)(require("app/components/actions/menuItemActionLink"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const dropdownLink_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownLink"));
const panels_1 = require("app/components/panels");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const dataSection_1 = (0, tslib_1.__importDefault)(require("../dataSection"));
const imageVisualization_1 = (0, tslib_1.__importDefault)(require("./imageVisualization"));
const modal_2 = (0, tslib_1.__importStar)(require("./modal"));
function Screenshot({ event, organization, screenshot, projectSlug, onDelete }) {
    const orgSlug = organization.slug;
    function handleOpenVisualizationModal(eventAttachment, downloadUrl) {
        (0, modal_1.openModal)(modalProps => (<modal_2.default {...modalProps} event={event} orgSlug={orgSlug} projectSlug={projectSlug} eventAttachment={eventAttachment} downloadUrl={downloadUrl} onDelete={() => onDelete(eventAttachment.id)}/>), { modalCss: modal_2.modalCss });
    }
    function renderContent(screenshotAttachment) {
        const downloadUrl = `/api/0/projects/${organization.slug}/${projectSlug}/events/${event.id}/attachments/${screenshotAttachment.id}/`;
        return (<react_1.Fragment>
        <StyledPanelBody>
          <StyledImageVisualization attachment={screenshotAttachment} orgId={orgSlug} projectId={projectSlug} event={event}/>
        </StyledPanelBody>
        <StyledPanelFooter>
          <StyledButtonbar gap={1}>
            <button_1.default size="xsmall" onClick={() => handleOpenVisualizationModal(screenshotAttachment, `${downloadUrl}?download=1`)}>
              {(0, locale_1.t)('View screenshot')}
            </button_1.default>
            <dropdownLink_1.default caret={false} customTitle={<button_1.default label={(0, locale_1.t)('Actions')} size="xsmall" icon={<icons_1.IconEllipsis size="xs"/>}/>} anchorRight>
              <menuItemActionLink_1.default shouldConfirm={false} title={(0, locale_1.t)('Download')} href={`${downloadUrl}?download=1`}>
                {(0, locale_1.t)('Download')}
              </menuItemActionLink_1.default>
              <menuItemActionLink_1.default shouldConfirm title={(0, locale_1.t)('Delete')} onAction={() => onDelete(screenshotAttachment.id)} header={(0, locale_1.t)('Screenshots help identify what the user saw when the event happened')} message={(0, locale_1.t)('Are you sure you wish to delete this screenshot?')}>
                {(0, locale_1.t)('Delete')}
              </menuItemActionLink_1.default>
            </dropdownLink_1.default>
          </StyledButtonbar>
        </StyledPanelFooter>
      </react_1.Fragment>);
    }
    return (<role_1.default organization={organization} role={organization.attachmentsRole}>
      {({ hasRole }) => {
            if (!hasRole) {
                return null;
            }
            return (<dataSection_1.default title={(0, locale_1.t)('Screenshot')} description={(0, locale_1.t)('Screenshot help identify what the user saw when the event happened')}>
            <StyledPanel>{renderContent(screenshot)}</StyledPanel>
          </dataSection_1.default>);
        }}
    </role_1.default>);
}
exports.default = Screenshot;
const StyledPanel = (0, styled_1.default)(panels_1.Panel) `
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin-bottom: 0;
  min-height: 200px;
  min-width: 175px;
  height: 100%;
`;
const StyledPanelBody = (0, styled_1.default)(panels_1.PanelBody) `
  min-height: 175px;
  height: 100%;
  overflow: hidden;
  border: 1px solid ${p => p.theme.border};
  border-radius: ${p => p.theme.borderRadius};
  margin: -1px;
  width: calc(100% + 2px);
  border-bottom-left-radius: 0;
  border-bottom-right-radius: 0;
  position: relative;
`;
const StyledPanelFooter = (0, styled_1.default)(panels_1.PanelFooter) `
  padding: ${(0, space_1.default)(1)};
  width: 100%;
`;
const StyledImageVisualization = (0, styled_1.default)(imageVisualization_1.default) `
  position: absolute;
  width: 100%;
`;
const StyledButtonbar = (0, styled_1.default)(buttonBar_1.default) `
  justify-content: space-between;
  .dropdown {
    height: 24px;
  }
`;
//# sourceMappingURL=index.jsx.map