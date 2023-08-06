Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const modal_1 = require("app/actionCreators/modal");
const issueSyncListElement_1 = (0, tslib_1.__importDefault)(require("app/components/issueSyncListElement"));
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const integrationItem_1 = (0, tslib_1.__importDefault)(require("app/views/organizationIntegrations/integrationItem"));
const externalIssueForm_1 = (0, tslib_1.__importDefault)(require("./externalIssueForm"));
const ExternalIssueActions = ({ configurations, group, onChange, api }) => {
    const { linked, unlinked } = configurations
        .sort((a, b) => a.name.toLowerCase().localeCompare(b.name.toLowerCase()))
        .reduce((acc, curr) => {
        if (curr.externalIssues.length) {
            acc.linked.push(curr);
        }
        else {
            acc.unlinked.push(curr);
        }
        return acc;
    }, { linked: [], unlinked: [] });
    const deleteIssue = (integration) => {
        const { externalIssues } = integration;
        // Currently we do not support a case where there is multiple external issues.
        // For example, we shouldn't have more than 1 jira ticket created for an issue for each jira configuration.
        const issue = externalIssues[0];
        const { id } = issue;
        const endpoint = `/groups/${group.id}/integrations/${integration.id}/?externalIssue=${id}`;
        api.request(endpoint, {
            method: 'DELETE',
            success: () => {
                onChange(() => (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Successfully unlinked issue.')), () => (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to unlink issue.')));
            },
            error: () => {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to unlink issue.'));
            },
        });
    };
    const doOpenModal = (integration) => (0, modal_1.openModal)(deps => <externalIssueForm_1.default {...deps} {...{ group, onChange, integration }}/>, { allowClickClose: false });
    return (<react_1.Fragment>
      {linked.map(config => {
            const { provider, externalIssues } = config;
            const issue = externalIssues[0];
            return (<issueSyncListElement_1.default key={issue.id} externalIssueLink={issue.url} externalIssueId={issue.id} externalIssueKey={issue.key} externalIssueDisplayName={issue.displayName} onClose={() => deleteIssue(config)} integrationType={provider.key} hoverCardHeader={(0, locale_1.t)('Linked %s Integration', provider.name)} hoverCardBody={<div>
                <IssueTitle>{issue.title}</IssueTitle>
                {issue.description && (<IssueDescription>{issue.description}</IssueDescription>)}
              </div>}/>);
        })}

      {unlinked.length > 0 && (<issueSyncListElement_1.default integrationType={unlinked[0].provider.key} hoverCardHeader={(0, locale_1.t)('Linked %s Integration', unlinked[0].provider.name)} hoverCardBody={<Container>
              {unlinked.map(config => (<Wrapper onClick={() => doOpenModal(config)} key={config.id}>
                  <integrationItem_1.default integration={config}/>
                </Wrapper>))}
            </Container>} onOpen={unlinked.length === 1 ? () => doOpenModal(unlinked[0]) : undefined}/>)}
    </react_1.Fragment>);
};
const IssueTitle = (0, styled_1.default)('div') `
  font-size: 1.1em;
  font-weight: 600;
  ${overflowEllipsis_1.default};
`;
const IssueDescription = (0, styled_1.default)('div') `
  margin-top: ${(0, space_1.default)(1)};
  ${overflowEllipsis_1.default};
`;
const Wrapper = (0, styled_1.default)('div') `
  margin-bottom: ${(0, space_1.default)(2)};
  cursor: pointer;
`;
const Container = (0, styled_1.default)('div') `
  & > div:last-child {
    margin-bottom: ${(0, space_1.default)(1)};
  }
`;
exports.default = (0, withApi_1.default)(ExternalIssueActions);
//# sourceMappingURL=externalIssueActions.jsx.map