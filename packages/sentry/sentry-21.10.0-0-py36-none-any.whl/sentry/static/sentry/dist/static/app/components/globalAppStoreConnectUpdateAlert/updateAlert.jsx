Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const prompts_1 = require("app/actionCreators/prompts");
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const appStoreConnectContext_1 = (0, tslib_1.__importDefault)(require("app/components/projects/appStoreConnectContext"));
const utils_1 = require("app/components/projects/appStoreConnectContext/utils");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const promptIsDismissed_1 = require("app/utils/promptIsDismissed");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const APP_STORE_CONNECT_UPDATES = 'app_store_connect_updates';
function UpdateAlert({ api, Wrapper, isCompact, project, organization, className }) {
    const appStoreConnectContext = (0, react_1.useContext)(appStoreConnectContext_1.default);
    const [isDismissed, setIsDismissed] = (0, react_1.useState)(false);
    (0, react_1.useEffect)(() => {
        checkPrompt();
    }, []);
    function checkPrompt() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            if (!project ||
                !appStoreConnectContext ||
                !appStoreConnectContext.updateAlertMessage ||
                isDismissed) {
                return;
            }
            const prompt = yield (0, prompts_1.promptsCheck)(api, {
                organizationId: organization.id,
                projectId: project.id,
                feature: APP_STORE_CONNECT_UPDATES,
            });
            setIsDismissed((0, promptIsDismissed_1.promptIsDismissed)(prompt));
        });
    }
    function handleDismiss() {
        if (!project) {
            return;
        }
        (0, prompts_1.promptsUpdate)(api, {
            organizationId: organization.id,
            projectId: project.id,
            feature: APP_STORE_CONNECT_UPDATES,
            status: 'dismissed',
        });
        setIsDismissed(true);
    }
    function renderMessage(appStoreConnectValidationData, projectSettingsLink) {
        if (!appStoreConnectValidationData.updateAlertMessage) {
            return null;
        }
        const { updateAlertMessage } = appStoreConnectValidationData;
        return (<div>
        {updateAlertMessage}
        {isCompact && (<react_1.Fragment>
            &nbsp;
            <link_1.default to={updateAlertMessage ===
                    utils_1.appStoreConnectAlertMessage.appStoreCredentialsInvalid
                    ? projectSettingsLink
                    : `${projectSettingsLink}&revalidateItunesSession=true`}>
              {(0, locale_1.t)('Update it in the project settings to reconnect')}
            </link_1.default>
          </react_1.Fragment>)}
      </div>);
    }
    function renderActions(projectSettingsLink) {
        if (isCompact) {
            return (<ButtonClose priority="link" title={(0, locale_1.t)('Dismiss')} label={(0, locale_1.t)('Dismiss')} onClick={handleDismiss} icon={<icons_1.IconClose />}/>);
        }
        return (<Actions>
        <button_1.default priority="link" onClick={handleDismiss}>
          {(0, locale_1.t)('Dismiss')}
        </button_1.default>
        |
        <button_1.default priority="link" to={`${projectSettingsLink}&revalidateItunesSession=true`}>
          {(0, locale_1.t)('Update session')}
        </button_1.default>
      </Actions>);
    }
    if (!project ||
        !appStoreConnectContext ||
        !appStoreConnectContext.updateAlertMessage ||
        isDismissed) {
        return null;
    }
    const projectSettingsLink = `/settings/${organization.slug}/projects/${project.slug}/debug-symbols/?customRepository=${appStoreConnectContext.id}`;
    const notice = (<alert_1.default type="warning" icon={<icons_1.IconRefresh />} className={className}>
      <Content>
        {renderMessage(appStoreConnectContext, projectSettingsLink)}
        {renderActions(projectSettingsLink)}
      </Content>
    </alert_1.default>);
    return Wrapper ? <Wrapper>{notice}</Wrapper> : notice;
}
exports.default = (0, withApi_1.default)(UpdateAlert);
const Actions = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: repeat(3, max-content);
  grid-gap: ${(0, space_1.default)(1)};
  align-items: center;
`;
const Content = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: 1fr max-content;
  grid-gap: ${(0, space_1.default)(1)};
`;
const ButtonClose = (0, styled_1.default)(button_1.default) `
  color: ${p => p.theme.textColor};
  /* Give the button an explicit height so that it lines up with the icon */
  height: 22px;
`;
//# sourceMappingURL=updateAlert.jsx.map