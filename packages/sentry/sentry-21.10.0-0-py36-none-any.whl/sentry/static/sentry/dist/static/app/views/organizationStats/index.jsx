Object.defineProperty(exports, "__esModule", { value: true });
exports.OrganizationStats = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const omit_1 = (0, tslib_1.__importDefault)(require("lodash/omit"));
const pick_1 = (0, tslib_1.__importDefault)(require("lodash/pick"));
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const dropdownControl_1 = (0, tslib_1.__importStar)(require("app/components/dropdownControl"));
const errorBoundary_1 = (0, tslib_1.__importDefault)(require("app/components/errorBoundary"));
const getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
const pageHeading_1 = (0, tslib_1.__importDefault)(require("app/components/pageHeading"));
const pageTimeRangeSelector_1 = (0, tslib_1.__importDefault)(require("app/components/pageTimeRangeSelector"));
const sentryDocumentTitle_1 = (0, tslib_1.__importDefault)(require("app/components/sentryDocumentTitle"));
const constants_1 = require("app/constants");
const locale_1 = require("app/locale");
const organization_1 = require("app/styles/organization");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const types_1 = require("app/types");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const usageChart_1 = require("./usageChart");
const usageStatsOrg_1 = (0, tslib_1.__importDefault)(require("./usageStatsOrg"));
const usageStatsProjects_1 = (0, tslib_1.__importDefault)(require("./usageStatsProjects"));
const PAGE_QUERY_PARAMS = [
    'pageStatsPeriod',
    'pageStart',
    'pageEnd',
    'pageUtc',
    'dataCategory',
    'transform',
    'sort',
    'query',
    'cursor',
];
class OrganizationStats extends react_1.Component {
    constructor() {
        super(...arguments);
        this.getNextLocations = (project) => {
            const { location, organization } = this.props;
            const nextLocation = Object.assign(Object.assign({}, location), { query: Object.assign(Object.assign({}, location.query), { project: project.id }) });
            // Do not leak out page-specific keys
            nextLocation.query = (0, omit_1.default)(nextLocation.query, PAGE_QUERY_PARAMS);
            return {
                performance: Object.assign(Object.assign({}, nextLocation), { pathname: `/organizations/${organization.slug}/performance/` }),
                projectDetail: Object.assign(Object.assign({}, nextLocation), { pathname: `/organizations/${organization.slug}/projects/${project.slug}/` }),
                issueList: Object.assign(Object.assign({}, nextLocation), { pathname: `/organizations/${organization.slug}/issues/` }),
                settings: {
                    pathname: `/settings/${organization.slug}/projects/${project.slug}/`,
                },
            };
        };
        this.handleUpdateDatetime = (datetime) => {
            const { start, end, relative, utc } = datetime;
            if (start && end) {
                const parser = utc ? moment_1.default.utc : moment_1.default;
                return this.setStateOnUrl({
                    pageStatsPeriod: undefined,
                    pageStart: parser(start).format(),
                    pageEnd: parser(end).format(),
                    pageUtc: utc !== null && utc !== void 0 ? utc : undefined,
                });
            }
            return this.setStateOnUrl({
                pageStatsPeriod: relative || undefined,
                pageStart: undefined,
                pageEnd: undefined,
                pageUtc: undefined,
            });
        };
        /**
         * TODO: Enable user to set dateStart/dateEnd
         *
         * See PAGE_QUERY_PARAMS for list of accepted keys on nextState
         */
        this.setStateOnUrl = (nextState, options = {
            willUpdateRouter: true,
        }) => {
            const { location, router } = this.props;
            const nextQueryParams = (0, pick_1.default)(nextState, PAGE_QUERY_PARAMS);
            const nextLocation = Object.assign(Object.assign({}, location), { query: Object.assign(Object.assign({}, location === null || location === void 0 ? void 0 : location.query), nextQueryParams) });
            if (options.willUpdateRouter) {
                router.push(nextLocation);
            }
            return nextLocation;
        };
        this.renderPageControl = () => {
            const { organization } = this.props;
            const { start, end, period, utc } = this.dataDatetime;
            return (<react_1.Fragment>
        <StyledPageTimeRangeSelector organization={organization} relative={period !== null && period !== void 0 ? period : ''} start={start !== null && start !== void 0 ? start : null} end={end !== null && end !== void 0 ? end : null} utc={utc !== null && utc !== void 0 ? utc : null} onUpdate={this.handleUpdateDatetime} relativeOptions={(0, omit_1.default)(constants_1.DEFAULT_RELATIVE_PERIODS, ['1h'])}/>

        <DropdownDataCategory label={<DropdownLabel>
              <span>{(0, locale_1.t)('Event Type: ')}</span>
              <span>{this.dataCategoryName}</span>
            </DropdownLabel>}>
          {usageChart_1.CHART_OPTIONS_DATACATEGORY.map(option => (<dropdownControl_1.DropdownItem key={option.value} eventKey={option.value} onSelect={(val) => this.setStateOnUrl({ dataCategory: val })}>
              {option.label}
            </dropdownControl_1.DropdownItem>))}
        </DropdownDataCategory>
      </react_1.Fragment>);
        };
    }
    get dataCategory() {
        var _a, _b;
        const dataCategory = (_b = (_a = this.props.location) === null || _a === void 0 ? void 0 : _a.query) === null || _b === void 0 ? void 0 : _b.dataCategory;
        switch (dataCategory) {
            case types_1.DataCategory.ERRORS:
            case types_1.DataCategory.TRANSACTIONS:
            case types_1.DataCategory.ATTACHMENTS:
                return dataCategory;
            default:
                return types_1.DataCategory.ERRORS;
        }
    }
    get dataCategoryName() {
        var _a;
        const dataCategory = this.dataCategory;
        return (_a = types_1.DataCategoryName[dataCategory]) !== null && _a !== void 0 ? _a : (0, locale_1.t)('Unknown Data Category');
    }
    get dataDatetime() {
        var _a, _b;
        const query = (_b = (_a = this.props.location) === null || _a === void 0 ? void 0 : _a.query) !== null && _b !== void 0 ? _b : {};
        const { start, end, statsPeriod, utc: utcString, } = (0, getParams_1.getParams)(query, {
            allowEmptyPeriod: true,
            allowAbsoluteDatetime: true,
            allowAbsolutePageDatetime: true,
        });
        if (!statsPeriod && !start && !end) {
            return { period: constants_1.DEFAULT_STATS_PERIOD };
        }
        // Following getParams, statsPeriod will take priority over start/end
        if (statsPeriod) {
            return { period: statsPeriod };
        }
        const utc = utcString === 'true';
        if (start && end) {
            return utc
                ? {
                    start: moment_1.default.utc(start).format(),
                    end: moment_1.default.utc(end).format(),
                    utc,
                }
                : {
                    start: (0, moment_1.default)(start).utc().format(),
                    end: (0, moment_1.default)(end).utc().format(),
                    utc,
                };
        }
        return { period: constants_1.DEFAULT_STATS_PERIOD };
    }
    // Validation and type-casting should be handled by chart
    get chartTransform() {
        var _a, _b;
        return (_b = (_a = this.props.location) === null || _a === void 0 ? void 0 : _a.query) === null || _b === void 0 ? void 0 : _b.transform;
    }
    // Validation and type-casting should be handled by table
    get tableSort() {
        var _a, _b;
        return (_b = (_a = this.props.location) === null || _a === void 0 ? void 0 : _a.query) === null || _b === void 0 ? void 0 : _b.sort;
    }
    get tableQuery() {
        var _a, _b;
        return (_b = (_a = this.props.location) === null || _a === void 0 ? void 0 : _a.query) === null || _b === void 0 ? void 0 : _b.query;
    }
    get tableCursor() {
        var _a, _b;
        return (_b = (_a = this.props.location) === null || _a === void 0 ? void 0 : _a.query) === null || _b === void 0 ? void 0 : _b.cursor;
    }
    render() {
        const { organization } = this.props;
        return (<sentryDocumentTitle_1.default title="Usage Stats">
        <organization_1.PageContent>
          <organization_1.PageHeader>
            <pageHeading_1.default>{(0, locale_1.t)('Organization Usage Stats')}</pageHeading_1.default>
          </organization_1.PageHeader>

          <p>
            {(0, locale_1.t)('We collect usage metrics on three types of events: errors, transactions, and attachments. The charts below reflect events that Sentry has received across your entire organization. You can also find them broken down by project in the table.')}
          </p>

          <PageGrid>
            {this.renderPageControl()}

            <errorBoundary_1.default mini>
              <usageStatsOrg_1.default organization={organization} dataCategory={this.dataCategory} dataCategoryName={this.dataCategoryName} dataDatetime={this.dataDatetime} chartTransform={this.chartTransform} handleChangeState={this.setStateOnUrl}/>
            </errorBoundary_1.default>
            <errorBoundary_1.default mini>
              <usageStatsProjects_1.default organization={organization} dataCategory={this.dataCategory} dataCategoryName={this.dataCategoryName} dataDatetime={this.dataDatetime} tableSort={this.tableSort} tableQuery={this.tableQuery} tableCursor={this.tableCursor} handleChangeState={this.setStateOnUrl} getNextLocations={this.getNextLocations}/>
            </errorBoundary_1.default>
          </PageGrid>
        </organization_1.PageContent>
      </sentryDocumentTitle_1.default>);
    }
}
exports.OrganizationStats = OrganizationStats;
exports.default = (0, withOrganization_1.default)(OrganizationStats);
const PageGrid = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: 1fr;
  grid-gap: ${(0, space_1.default)(2)};

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    grid-template-columns: repeat(2, 1fr);
  }
  @media (min-width: ${p => p.theme.breakpoints[2]}) {
    grid-template-columns: repeat(4, 1fr);
  }
`;
const DropdownDataCategory = (0, styled_1.default)(dropdownControl_1.default) `
  height: 42px;
  grid-column: auto / span 1;
  justify-self: stretch;
  align-self: stretch;
  z-index: ${p => p.theme.zIndex.orgStats.dataCategory};

  button {
    width: 100%;
    height: 100%;

    > span {
      display: flex;
      justify-content: space-between;
    }
  }

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    grid-column: auto / span 2;
  }
  @media (min-width: ${p => p.theme.breakpoints[2]}) {
    grid-column: auto / span 1;
  }
`;
const StyledPageTimeRangeSelector = (0, styled_1.default)(pageTimeRangeSelector_1.default) `
  grid-column: auto / span 1;
  z-index: ${p => p.theme.zIndex.orgStats.timeRange};

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    grid-column: auto / span 2;
  }
  @media (min-width: ${p => p.theme.breakpoints[2]}) {
    grid-column: auto / span 3;
  }
`;
const DropdownLabel = (0, styled_1.default)('span') `
  text-align: left;
  font-weight: 600;
  color: ${p => p.theme.textColor};

  > span:last-child {
    font-weight: 400;
  }
`;
//# sourceMappingURL=index.jsx.map