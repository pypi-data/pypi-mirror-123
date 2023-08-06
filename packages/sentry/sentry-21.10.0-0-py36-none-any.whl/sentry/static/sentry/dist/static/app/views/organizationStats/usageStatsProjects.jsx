Object.defineProperty(exports, "__esModule", { value: true });
exports.SortBy = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const utils_1 = require("app/components/charts/utils");
const sortLink_1 = (0, tslib_1.__importDefault)(require("app/components/gridEditable/sortLink"));
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const searchBar_1 = (0, tslib_1.__importDefault)(require("app/components/searchBar"));
const constants_1 = require("app/constants");
const locale_1 = require("app/locale");
const types_1 = require("app/types");
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
const types_2 = require("./types");
const usageTable_1 = (0, tslib_1.__importStar)(require("./usageTable"));
var SortBy;
(function (SortBy) {
    SortBy["PROJECT"] = "project";
    SortBy["TOTAL"] = "total";
    SortBy["ACCEPTED"] = "accepted";
    SortBy["FILTERED"] = "filtered";
    SortBy["DROPPED"] = "dropped";
    SortBy["INVALID"] = "invalid";
    SortBy["RATE_LIMITED"] = "rate_limited";
})(SortBy = exports.SortBy || (exports.SortBy = {}));
class UsageStatsProjects extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.handleChangeSort = (nextKey) => {
            const { handleChangeState } = this.props;
            const { key, direction } = this.tableSort;
            let nextDirection = 1; // Default to descending
            if (key === nextKey) {
                nextDirection = direction * -1; // Toggle if clicking on the same column
            }
            else if (nextKey === SortBy.PROJECT) {
                nextDirection = -1; // Default PROJECT to ascending
            }
            // The header uses SortLink, which takes a LocationDescriptor and pushes
            // that to the router. As such, we do not need to update the router in
            // handleChangeState
            return handleChangeState({ sort: `${nextDirection > 0 ? '-' : ''}${nextKey}` }, { willUpdateRouter: false });
        };
        this.handleSearch = (query) => {
            const { handleChangeState, tableQuery } = this.props;
            if (query === tableQuery) {
                return;
            }
            if (!query) {
                handleChangeState({ query: undefined, cursor: undefined });
                return;
            }
            handleChangeState({ query, cursor: undefined });
        };
    }
    componentDidUpdate(prevProps) {
        const { dataDatetime: prevDateTime, dataCategory: prevDataCategory } = prevProps;
        const { dataDatetime: currDateTime, dataCategory: currDataCategory } = this.props;
        if (prevDateTime.start !== currDateTime.start ||
            prevDateTime.end !== currDateTime.end ||
            prevDateTime.period !== currDateTime.period ||
            prevDateTime.utc !== currDateTime.utc ||
            currDataCategory !== prevDataCategory) {
            this.reloadData();
        }
    }
    getEndpoints() {
        return [['projectStats', this.endpointPath, { query: this.endpointQuery }]];
    }
    get endpointPath() {
        const { organization } = this.props;
        return `/organizations/${organization.slug}/stats_v2/`;
    }
    get endpointQuery() {
        const { dataDatetime, dataCategory } = this.props;
        const queryDatetime = dataDatetime.start && dataDatetime.end
            ? {
                start: dataDatetime.start,
                end: dataDatetime.end,
                utc: dataDatetime.utc,
            }
            : {
                statsPeriod: dataDatetime.period || constants_1.DEFAULT_STATS_PERIOD,
            };
        // We do not need more granularity in the data so interval is '1d'
        return Object.assign(Object.assign({}, queryDatetime), { interval: (0, utils_1.getSeriesApiInterval)(dataDatetime), groupBy: ['outcome', 'project'], field: ['sum(quantity)'], project: '-1', category: dataCategory.slice(0, -1) });
    }
    get tableData() {
        const { projectStats } = this.state;
        return Object.assign({ headers: this.tableHeader }, this.mapSeriesToTable(projectStats));
    }
    get tableSort() {
        const { tableSort } = this.props;
        if (!tableSort) {
            return {
                key: SortBy.TOTAL,
                direction: 1,
            };
        }
        let key = tableSort;
        let direction = -1;
        if (tableSort.charAt(0) === '-') {
            key = key.slice(1);
            direction = 1;
        }
        switch (key) {
            case SortBy.PROJECT:
            case SortBy.TOTAL:
            case SortBy.ACCEPTED:
            case SortBy.FILTERED:
            case SortBy.DROPPED:
                return { key, direction };
            default:
                return { key: SortBy.ACCEPTED, direction: -1 };
        }
    }
    get tableCursor() {
        const { tableCursor } = this.props;
        const offset = Number(tableCursor === null || tableCursor === void 0 ? void 0 : tableCursor.split(':')[1]);
        return isNaN(offset) ? 0 : offset;
    }
    /**
     * OrganizationStatsEndpointV2 does not have any performance issues. We use
     * client-side pagination to limit the number of rows on the table so the
     * page doesn't scroll too deeply for organizations with a lot of projects
     */
    get pageLink() {
        const numRows = this.filteredProjects.length;
        const offset = this.tableCursor;
        const prevOffset = offset - UsageStatsProjects.MAX_ROWS_USAGE_TABLE;
        const nextOffset = offset + UsageStatsProjects.MAX_ROWS_USAGE_TABLE;
        return `<link>; rel="previous"; results="${prevOffset >= 0}"; cursor="0:${Math.max(0, prevOffset)}:1", <link>; rel="next"; results="${nextOffset < numRows}"; cursor="0:${nextOffset}:0"`;
    }
    /**
     * Filter projects if there's a query
     */
    get filteredProjects() {
        const { projects, tableQuery } = this.props;
        return tableQuery
            ? projects.filter(p => p.slug.includes(tableQuery) && p.hasAccess)
            : projects.filter(p => p.hasAccess);
    }
    get tableHeader() {
        const { key, direction } = this.tableSort;
        const getArrowDirection = (linkKey) => {
            if (linkKey !== key) {
                return undefined;
            }
            return direction > 0 ? 'desc' : 'asc';
        };
        return [
            {
                key: SortBy.PROJECT,
                title: (0, locale_1.t)('Project'),
                align: 'left',
                direction: getArrowDirection(SortBy.PROJECT),
                onClick: () => this.handleChangeSort(SortBy.PROJECT),
            },
            {
                key: SortBy.TOTAL,
                title: (0, locale_1.t)('Total'),
                align: 'right',
                direction: getArrowDirection(SortBy.TOTAL),
                onClick: () => this.handleChangeSort(SortBy.TOTAL),
            },
            {
                key: SortBy.ACCEPTED,
                title: (0, locale_1.t)('Accepted'),
                align: 'right',
                direction: getArrowDirection(SortBy.ACCEPTED),
                onClick: () => this.handleChangeSort(SortBy.ACCEPTED),
            },
            {
                key: SortBy.FILTERED,
                title: (0, locale_1.t)('Filtered'),
                align: 'right',
                direction: getArrowDirection(SortBy.FILTERED),
                onClick: () => this.handleChangeSort(SortBy.FILTERED),
            },
            {
                key: SortBy.DROPPED,
                title: (0, locale_1.t)('Dropped'),
                align: 'right',
                direction: getArrowDirection(SortBy.DROPPED),
                onClick: () => this.handleChangeSort(SortBy.DROPPED),
            },
        ].map(h => {
            const Cell = h.key === SortBy.PROJECT ? usageTable_1.CellProject : usageTable_1.CellStat;
            return (<Cell key={h.key}>
          <sortLink_1.default canSort title={h.title} align={h.align} direction={h.direction} generateSortLink={h.onClick}/>
        </Cell>);
        });
    }
    getProjectLink(project) {
        const { dataCategory, getNextLocations, organization } = this.props;
        const { performance, projectDetail, settings } = getNextLocations(project);
        if (dataCategory === types_1.DataCategory.TRANSACTIONS &&
            organization.features.includes('performance-view')) {
            return {
                projectLink: performance,
                projectSettingsLink: settings,
            };
        }
        return {
            projectLink: projectDetail,
            projectSettingsLink: settings,
        };
    }
    mapSeriesToTable(projectStats) {
        if (!projectStats) {
            return { tableStats: [] };
        }
        const stats = {};
        try {
            const baseStat = {
                [SortBy.TOTAL]: 0,
                [SortBy.ACCEPTED]: 0,
                [SortBy.FILTERED]: 0,
                [SortBy.DROPPED]: 0,
            };
            const projectList = this.filteredProjects;
            const projectSet = new Set(projectList.map(p => p.id));
            projectStats.groups.forEach(group => {
                const { outcome, project: projectId } = group.by;
                // Backend enum is singlar. Frontend enum is plural.
                if (!projectSet.has(projectId.toString())) {
                    return;
                }
                if (!stats[projectId]) {
                    stats[projectId] = Object.assign({}, baseStat);
                }
                if (outcome !== types_2.Outcome.CLIENT_DISCARD) {
                    stats[projectId].total += group.totals['sum(quantity)'];
                }
                if (outcome === types_2.Outcome.ACCEPTED || outcome === types_2.Outcome.FILTERED) {
                    stats[projectId][outcome] += group.totals['sum(quantity)'];
                }
                else if (outcome === types_2.Outcome.RATE_LIMITED ||
                    outcome === types_2.Outcome.INVALID ||
                    outcome === types_2.Outcome.DROPPED) {
                    stats[projectId][SortBy.DROPPED] += group.totals['sum(quantity)'];
                }
            });
            // For projects without stats, fill in with zero
            const tableStats = projectList.map(proj => {
                var _a;
                const stat = (_a = stats[proj.id]) !== null && _a !== void 0 ? _a : Object.assign({}, baseStat);
                return Object.assign(Object.assign({ project: Object.assign({}, proj) }, this.getProjectLink(proj)), stat);
            });
            const { key, direction } = this.tableSort;
            tableStats.sort((a, b) => {
                if (key === SortBy.PROJECT) {
                    return b.project.slug.localeCompare(a.project.slug) * direction;
                }
                return a[key] !== b[key]
                    ? (b[key] - a[key]) * direction
                    : a.project.slug.localeCompare(b.project.slug);
            });
            const offset = this.tableCursor;
            return {
                tableStats: tableStats.slice(offset, offset + UsageStatsProjects.MAX_ROWS_USAGE_TABLE),
            };
        }
        catch (err) {
            Sentry.withScope(scope => {
                scope.setContext('query', this.endpointQuery);
                scope.setContext('body', projectStats);
                Sentry.captureException(err);
            });
            return {
                tableStats: [],
                error: err,
            };
        }
    }
    renderComponent() {
        const { error, errors, loading } = this.state;
        const { dataCategory, loadingProjects, tableQuery } = this.props;
        const { headers, tableStats } = this.tableData;
        return (<react_1.Fragment>
        <GridRow>
          <searchBar_1.default defaultQuery="" query={tableQuery} placeholder={(0, locale_1.t)('Filter your projects')} onSearch={this.handleSearch}/>
        </GridRow>

        <GridRow>
          <usageTable_1.default isLoading={loading || loadingProjects} isError={error} errors={errors} // TODO(ts)
         isEmpty={tableStats.length === 0} headers={headers} dataCategory={dataCategory} usageStats={tableStats}/>
          <pagination_1.default pageLinks={this.pageLink}/>
        </GridRow>
      </react_1.Fragment>);
    }
}
UsageStatsProjects.MAX_ROWS_USAGE_TABLE = 25;
exports.default = (0, withProjects_1.default)(UsageStatsProjects);
const GridRow = (0, styled_1.default)('div') `
  grid-column: 1 / -1;
`;
//# sourceMappingURL=usageStatsProjects.jsx.map