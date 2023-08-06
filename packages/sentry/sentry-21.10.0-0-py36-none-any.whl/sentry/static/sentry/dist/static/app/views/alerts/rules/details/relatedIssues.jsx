Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const styles_1 = require("app/components/charts/styles");
const emptyStateWarning_1 = (0, tslib_1.__importDefault)(require("app/components/emptyStateWarning"));
const groupList_1 = (0, tslib_1.__importDefault)(require("app/components/issues/groupList"));
const panels_1 = require("app/components/panels");
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
class RelatedIssues extends react_1.Component {
    constructor() {
        super(...arguments);
        this.renderEmptyMessage = () => {
            return (<panels_1.Panel>
        <panels_1.PanelBody>
          <emptyStateWarning_1.default small withIcon={false}>
            {(0, locale_1.t)('No issues for this alert rule')}
          </emptyStateWarning_1.default>
        </panels_1.PanelBody>
      </panels_1.Panel>);
        };
    }
    render() {
        const { rule, projects, organization, timePeriod, query } = this.props;
        const { start, end } = timePeriod;
        const path = `/organizations/${organization.slug}/issues/`;
        const queryParams = Object.assign(Object.assign({ start,
            end, groupStatsPeriod: 'auto', limit: 5 }, (rule.environment ? { environment: rule.environment } : {})), { sort: rule.aggregate === 'count_unique(user)' ? 'user' : 'freq', query, project: projects.map(project => project.id) });
        const issueSearch = {
            pathname: `/organizations/${organization.slug}/issues/`,
            query: queryParams,
        };
        return (<react_1.Fragment>
        <ControlsWrapper>
          <StyledSectionHeading>
            {(0, locale_1.t)('Related Issues')}
            <tooltip_1.default title={(0, locale_1.t)('Top issues containing events matching the metric.')}>
              <icons_1.IconInfo size="xs" color="gray200"/>
            </tooltip_1.default>
          </StyledSectionHeading>
          <button_1.default data-test-id="issues-open" size="small" to={issueSearch}>
            {(0, locale_1.t)('Open in Issues')}
          </button_1.default>
        </ControlsWrapper>

        <TableWrapper>
          <groupList_1.default orgId={organization.slug} endpointPath={path} queryParams={queryParams} query={`start=${start}&end=${end}&groupStatsPeriod=auto`} canSelectGroups={false} renderEmptyMessage={this.renderEmptyMessage} withChart withPagination={false} useFilteredStats customStatsPeriod={timePeriod} useTintRow={false}/>
        </TableWrapper>
      </react_1.Fragment>);
    }
}
const StyledSectionHeading = (0, styled_1.default)(styles_1.SectionHeading) `
  display: flex;
  align-items: center;
`;
const ControlsWrapper = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: ${(0, space_1.default)(1)};
`;
const TableWrapper = (0, styled_1.default)('div') `
  margin-bottom: ${(0, space_1.default)(4)};
  ${panels_1.Panel} {
    /* smaller space between table and pagination */
    margin-bottom: -${(0, space_1.default)(1)};
  }
`;
exports.default = RelatedIssues;
//# sourceMappingURL=relatedIssues.jsx.map