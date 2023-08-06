Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const confirmDelete_1 = (0, tslib_1.__importDefault)(require("app/components/confirmDelete"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const ActionButtons = ({ org, app, showPublish, showDelete, onPublish, onDelete, disablePublishReason, disableDeleteReason, }) => {
    const appDashboardButton = (<StyledButton size="small" icon={<icons_1.IconStats />} to={`/settings/${org.slug}/developer-settings/${app.slug}/dashboard/`}>
      {(0, locale_1.t)('Dashboard')}
    </StyledButton>);
    const publishRequestButton = showPublish ? (<StyledButton disabled={!!disablePublishReason} title={disablePublishReason} icon={<icons_1.IconUpgrade />} size="small" onClick={onPublish}>
      {(0, locale_1.t)('Publish')}
    </StyledButton>) : null;
    const deleteConfirmMessage = (0, locale_1.t)(`Deleting ${app.slug} will also delete any and all of its installations. \
         This is a permanent action. Do you wish to continue?`);
    const deleteButton = showDelete ? (disableDeleteReason ? (<StyledButton disabled title={disableDeleteReason} size="small" icon={<icons_1.IconDelete />} label="Delete"/>) : (onDelete && (<confirmDelete_1.default message={deleteConfirmMessage} confirmInput={app.slug} priority="danger" onConfirm={() => onDelete(app)}>
          <StyledButton size="small" icon={<icons_1.IconDelete />} label="Delete"/>
        </confirmDelete_1.default>))) : null;
    return (<ButtonHolder>
      {appDashboardButton}
      {publishRequestButton}
      {deleteButton}
    </ButtonHolder>);
};
const ButtonHolder = (0, styled_1.default)('div') `
  flex-direction: row;
  display: flex;
  & > * {
    margin-left: ${(0, space_1.default)(0.5)};
  }
`;
const StyledButton = (0, styled_1.default)(button_1.default) `
  color: ${p => p.theme.subText};
`;
exports.default = ActionButtons;
//# sourceMappingURL=actionButtons.jsx.map