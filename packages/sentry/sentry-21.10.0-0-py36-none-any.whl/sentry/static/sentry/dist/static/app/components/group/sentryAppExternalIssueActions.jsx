Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const modal_1 = require("app/actionCreators/modal");
const platformExternalIssues_1 = require("app/actionCreators/platformExternalIssues");
const issueSyncListElement_1 = require("app/components/issueSyncListElement");
const sentryAppIcon_1 = require("app/components/sentryAppIcon");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const recordSentryAppInteraction_1 = require("app/utils/recordSentryAppInteraction");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const sentryAppExternalIssueModal_1 = (0, tslib_1.__importDefault)(require("./sentryAppExternalIssueModal"));
class SentryAppExternalIssueActions extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            action: 'create',
            externalIssue: this.props.externalIssue,
        };
        this.doOpenModal = (e) => {
            // Only show the modal when we don't have a linked issue
            if (this.state.externalIssue) {
                return;
            }
            const { group, event, sentryAppComponent, sentryAppInstallation } = this.props;
            (0, recordSentryAppInteraction_1.recordInteraction)(sentryAppComponent.sentryApp.slug, 'sentry_app_component_interacted', {
                componentType: 'issue-link',
            });
            e === null || e === void 0 ? void 0 : e.preventDefault();
            (0, modal_1.openModal)(deps => (<sentryAppExternalIssueModal_1.default {...deps} {...{ group, event, sentryAppComponent, sentryAppInstallation }} onSubmitSuccess={this.onSubmitSuccess}/>), { allowClickClose: false });
        };
        this.deleteIssue = () => {
            const { api, group } = this.props;
            const { externalIssue } = this.state;
            externalIssue &&
                (0, platformExternalIssues_1.deleteExternalIssue)(api, group.id, externalIssue.id)
                    .then(_data => {
                    this.setState({ externalIssue: undefined });
                    (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Successfully unlinked issue.'));
                })
                    .catch(_error => {
                    (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to unlink issue.'));
                });
        };
        this.onAddRemoveClick = () => {
            const { externalIssue } = this.state;
            if (!externalIssue) {
                this.doOpenModal();
            }
            else {
                this.deleteIssue();
            }
        };
        this.onSubmitSuccess = (externalIssue) => {
            this.setState({ externalIssue });
        };
    }
    componentDidUpdate(prevProps) {
        if (this.props.externalIssue !== prevProps.externalIssue) {
            this.updateExternalIssue(this.props.externalIssue);
        }
    }
    updateExternalIssue(externalIssue) {
        this.setState({ externalIssue });
    }
    render() {
        const { sentryAppComponent } = this.props;
        const { externalIssue } = this.state;
        const name = sentryAppComponent.sentryApp.name;
        let url = '#';
        let displayName = (0, locale_1.tct)('Link [name] Issue', { name });
        if (externalIssue) {
            url = externalIssue.webUrl;
            displayName = externalIssue.displayName;
        }
        return (<IssueLinkContainer>
        <IssueLink>
          <StyledSentryAppIcon slug={sentryAppComponent.sentryApp.slug}/>
          <issueSyncListElement_1.IntegrationLink onClick={this.doOpenModal} href={url}>
            {displayName}
          </issueSyncListElement_1.IntegrationLink>
        </IssueLink>
        <StyledIcon onClick={this.onAddRemoveClick}>
          {!!externalIssue ? <icons_1.IconClose /> : <icons_1.IconAdd />}
        </StyledIcon>
      </IssueLinkContainer>);
    }
}
const StyledSentryAppIcon = (0, styled_1.default)(sentryAppIcon_1.SentryAppIcon) `
  color: ${p => p.theme.textColor};
  width: ${(0, space_1.default)(3)};
  height: ${(0, space_1.default)(3)};
  cursor: pointer;
  flex-shrink: 0;
`;
const IssueLink = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  min-width: 0;
`;
const IssueLinkContainer = (0, styled_1.default)('div') `
  line-height: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
`;
const StyledIcon = (0, styled_1.default)('span') `
  color: ${p => p.theme.textColor};
  cursor: pointer;
`;
exports.default = (0, withApi_1.default)(SentryAppExternalIssueActions);
//# sourceMappingURL=sentryAppExternalIssueActions.jsx.map