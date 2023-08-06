Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const timeSince_1 = (0, tslib_1.__importDefault)(require("app/components/timeSince"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
function ProcessingIssueHint({ orgId, projectId, issue, showProject }) {
    const link = `/settings/${orgId}/projects/${projectId}/processing-issues/`;
    let showButton = false;
    let text = '';
    let lastEvent = null;
    let icon = null;
    let alertType = 'error';
    let project = null;
    if (showProject) {
        project = (<React.Fragment>
        <strong>{projectId}</strong> &mdash;{' '}
      </React.Fragment>);
    }
    if (issue.numIssues > 0) {
        icon = <icons_1.IconWarning size="sm" color="red300"/>;
        text = (0, locale_1.tn)('There is %s issue blocking event processing', 'There are %s issues blocking event processing', issue.numIssues);
        lastEvent = (<React.Fragment>
        (
        {(0, locale_1.tct)('last event from [ago]', {
                ago: <timeSince_1.default date={issue.lastSeen}/>,
            })}
        )
      </React.Fragment>);
        alertType = 'error';
        showButton = true;
    }
    else if (issue.issuesProcessing > 0) {
        icon = <icons_1.IconSettings size="sm" color="blue300"/>;
        alertType = 'info';
        text = (0, locale_1.tn)('Reprocessing %s event …', 'Reprocessing %s events …', issue.issuesProcessing);
    }
    else if (issue.resolveableIssues > 0) {
        icon = <icons_1.IconSettings size="sm" color="yellow300"/>;
        alertType = 'warning';
        text = (0, locale_1.tn)('There is %s event pending reprocessing.', 'There are %s events pending reprocessing.', issue.resolveableIssues);
        showButton = true;
    }
    else {
        /* we should not go here but what do we know */
        return null;
    }
    return (<StyledAlert type={alertType} icon={icon}>
      <Wrapper>
        <div>
          {project} <strong>{text}</strong> {lastEvent}
        </div>
        {showButton && (<div>
            <StyledButton size="xsmall" to={link}>
              {(0, locale_1.t)('Show details')}
            </StyledButton>
          </div>)}
      </Wrapper>
    </StyledAlert>);
}
exports.default = ProcessingIssueHint;
const StyledAlert = (0, styled_1.default)(alert_1.default) `
  border-width: 1px 0;
  border-radius: 0;
  margin: 0;
  font-size: ${p => p.theme.fontSizeMedium};
`;
const Wrapper = (0, styled_1.default)('div') `
  display: flex;
  justify-content: space-between;
`;
const StyledButton = (0, styled_1.default)(button_1.default) `
  white-space: nowrap;
  margin-left: ${(0, space_1.default)(1)};
`;
//# sourceMappingURL=processingIssueHint.jsx.map