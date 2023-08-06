Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const qs = (0, tslib_1.__importStar)(require("query-string"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const featureBadge_1 = (0, tslib_1.__importDefault)(require("app/components/featureBadge"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
const pageHeading_1 = (0, tslib_1.__importDefault)(require("app/components/pageHeading"));
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const panels_1 = require("app/components/panels");
const searchBar_1 = (0, tslib_1.__importDefault)(require("app/components/searchBar"));
const timeSince_1 = (0, tslib_1.__importDefault)(require("app/components/timeSince"));
const locale_1 = require("app/locale");
const organization_1 = require("app/styles/organization");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const queryString_1 = require("app/utils/queryString");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const monitorIcon_1 = (0, tslib_1.__importDefault)(require("./monitorIcon"));
class Monitors extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.handleSearch = (query) => {
            const { location, router } = this.props;
            router.push({
                pathname: location.pathname,
                query: (0, getParams_1.getParams)(Object.assign(Object.assign({}, (location.query || {})), { query })),
            });
        };
    }
    getEndpoints() {
        const { params, location } = this.props;
        return [
            [
                'monitorList',
                `/organizations/${params.orgId}/monitors/`,
                {
                    query: location.query,
                },
            ],
        ];
    }
    getTitle() {
        return `Monitors - ${this.props.params.orgId}`;
    }
    renderBody() {
        var _a;
        const { monitorList, monitorListPageLinks } = this.state;
        const { organization } = this.props;
        return (<react_1.Fragment>
        <organization_1.PageHeader>
          <HeaderTitle>
            <div>
              {(0, locale_1.t)('Monitors')} <featureBadge_1.default type="beta"/>
            </div>
            <NewMonitorButton to={`/organizations/${organization.slug}/monitors/create/`} priority="primary" size="xsmall">
              {(0, locale_1.t)('New Monitor')}
            </NewMonitorButton>
          </HeaderTitle>
          <StyledSearchBar query={(0, queryString_1.decodeScalar)((_a = qs.parse(location.search)) === null || _a === void 0 ? void 0 : _a.query, '')} placeholder={(0, locale_1.t)('Search for monitors.')} onSearch={this.handleSearch}/>
        </organization_1.PageHeader>
        <panels_1.Panel>
          <panels_1.PanelBody>
            {monitorList === null || monitorList === void 0 ? void 0 : monitorList.map(monitor => (<PanelItemCentered key={monitor.id}>
                <monitorIcon_1.default status={monitor.status} size={16}/>
                <StyledLink to={`/organizations/${organization.slug}/monitors/${monitor.id}/`}>
                  {monitor.name}
                </StyledLink>
                {monitor.nextCheckIn ? (<StyledTimeSince date={monitor.lastCheckIn}/>) : ((0, locale_1.t)('n/a'))}
              </PanelItemCentered>))}
          </panels_1.PanelBody>
        </panels_1.Panel>
        {monitorListPageLinks && (<pagination_1.default pageLinks={monitorListPageLinks} {...this.props}/>)}
      </react_1.Fragment>);
    }
}
const HeaderTitle = (0, styled_1.default)(pageHeading_1.default) `
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex: 1;
`;
const StyledSearchBar = (0, styled_1.default)(searchBar_1.default) `
  flex: 1;
`;
const NewMonitorButton = (0, styled_1.default)(button_1.default) `
  margin-right: ${(0, space_1.default)(2)};
`;
const PanelItemCentered = (0, styled_1.default)(panels_1.PanelItem) `
  align-items: center;
  padding: 0;
  padding-left: ${(0, space_1.default)(2)};
  padding-right: ${(0, space_1.default)(2)};
`;
const StyledLink = (0, styled_1.default)(link_1.default) `
  flex: 1;
  padding: ${(0, space_1.default)(2)};
`;
const StyledTimeSince = (0, styled_1.default)(timeSince_1.default) `
  font-variant-numeric: tabular-nums;
`;
exports.default = (0, react_router_1.withRouter)((0, withOrganization_1.default)(Monitors));
//# sourceMappingURL=monitors.jsx.map