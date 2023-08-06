Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const react_1 = require("@sentry/react");
const omit_1 = (0, tslib_1.__importDefault)(require("lodash/omit"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const userFeedback_1 = (0, tslib_1.__importDefault)(require("app/components/events/userFeedback"));
const compactIssue_1 = (0, tslib_1.__importDefault)(require("app/components/issues/compactIssue"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const noProjectMessage_1 = (0, tslib_1.__importDefault)(require("app/components/noProjectMessage"));
const globalSelectionHeader_1 = (0, tslib_1.__importDefault)(require("app/components/organizations/globalSelectionHeader"));
const pageHeading_1 = (0, tslib_1.__importDefault)(require("app/components/pageHeading"));
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const panels_1 = require("app/components/panels");
const locale_1 = require("app/locale");
const organization_1 = require("app/styles/organization");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const userFeedbackEmpty_1 = (0, tslib_1.__importDefault)(require("./userFeedbackEmpty"));
const utils_1 = require("./utils");
class OrganizationUserFeedback extends asyncView_1.default {
    getEndpoints() {
        const { organization, location: { search }, } = this.props;
        return [
            [
                'reportList',
                `/organizations/${organization.slug}/user-feedback/`,
                {
                    query: (0, utils_1.getQuery)(search),
                },
            ],
        ];
    }
    getTitle() {
        return `${(0, locale_1.t)('User Feedback')} - ${this.props.organization.slug}`;
    }
    get projectIds() {
        const { project } = this.props.location.query;
        return Array.isArray(project)
            ? project
            : typeof project === 'string'
                ? [project]
                : [];
    }
    renderResults() {
        const { orgId } = this.props.params;
        return (<panels_1.Panel className="issue-list" data-test-id="user-feedback-list">
        {this.state.reportList.map(item => {
                const issue = item.issue;
                return (<compactIssue_1.default key={item.id} id={issue.id} data={issue} eventId={item.eventID}>
              <StyledEventUserFeedback report={item} orgId={orgId} issueId={issue.id}/>
            </compactIssue_1.default>);
            })}
      </panels_1.Panel>);
    }
    renderEmpty() {
        return <userFeedbackEmpty_1.default projectIds={this.projectIds}/>;
    }
    renderLoading() {
        return this.renderBody();
    }
    renderStreamBody() {
        const { loading, reportList } = this.state;
        if (loading) {
            return (<panels_1.Panel>
          <loadingIndicator_1.default />
        </panels_1.Panel>);
        }
        if (!reportList.length) {
            return this.renderEmpty();
        }
        return this.renderResults();
    }
    renderBody() {
        const { organization } = this.props;
        const { location } = this.props;
        const { pathname, search, query } = location;
        const { status } = (0, utils_1.getQuery)(search);
        const { reportListPageLinks } = this.state;
        const unresolvedQuery = (0, omit_1.default)(query, 'status');
        const allIssuesQuery = Object.assign(Object.assign({}, query), { status: '' });
        return (<globalSelectionHeader_1.default>
        <organization_1.PageContent>
          <noProjectMessage_1.default organization={organization}>
            <div data-test-id="user-feedback">
              <Header>
                <pageHeading_1.default>{(0, locale_1.t)('User Feedback')}</pageHeading_1.default>
                <buttonBar_1.default active={!Array.isArray(status) ? status || '' : ''} merged>
                  <button_1.default size="small" barId="unresolved" to={{ pathname, query: unresolvedQuery }}>
                    {(0, locale_1.t)('Unresolved')}
                  </button_1.default>
                  <button_1.default size="small" barId="" to={{ pathname, query: allIssuesQuery }}>
                    {(0, locale_1.t)('All Issues')}
                  </button_1.default>
                </buttonBar_1.default>
              </Header>
              {this.renderStreamBody()}
              <pagination_1.default pageLinks={reportListPageLinks}/>
            </div>
          </noProjectMessage_1.default>
        </organization_1.PageContent>
      </globalSelectionHeader_1.default>);
    }
}
exports.default = (0, withOrganization_1.default)((0, react_1.withProfiler)(OrganizationUserFeedback));
const Header = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: ${(0, space_1.default)(2)};
`;
const StyledEventUserFeedback = (0, styled_1.default)(userFeedback_1.default) `
  margin: ${(0, space_1.default)(2)} 0 0;
`;
//# sourceMappingURL=index.jsx.map