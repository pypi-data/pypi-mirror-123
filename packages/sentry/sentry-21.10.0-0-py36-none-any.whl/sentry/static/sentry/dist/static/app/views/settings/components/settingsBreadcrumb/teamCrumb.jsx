Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = (0, tslib_1.__importDefault)(require("react"));
const react_router_1 = require("react-router");
const debounce_1 = (0, tslib_1.__importDefault)(require("lodash/debounce"));
const idBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge"));
const constants_1 = require("app/constants");
const recreateRoute_1 = (0, tslib_1.__importDefault)(require("app/utils/recreateRoute"));
const useTeams_1 = (0, tslib_1.__importDefault)(require("app/utils/useTeams"));
const breadcrumbDropdown_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsBreadcrumb/breadcrumbDropdown"));
const menuItem_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsBreadcrumb/menuItem"));
const _1 = require(".");
const TeamCrumb = (_a) => {
    var { params, routes, route } = _a, props = (0, tslib_1.__rest)(_a, ["params", "routes", "route"]);
    const { teams, onSearch, fetching } = (0, useTeams_1.default)();
    const team = teams.find(({ slug }) => slug === params.teamId);
    const hasMenu = teams.length > 1;
    const handleSearchChange = (e) => {
        onSearch(e.target.value);
    };
    const debouncedHandleSearch = (0, debounce_1.default)(handleSearchChange, constants_1.DEFAULT_DEBOUNCE_DURATION);
    if (!team) {
        return null;
    }
    return (<breadcrumbDropdown_1.default name={<_1.CrumbLink to={(0, recreateRoute_1.default)(route, {
                routes,
                params: Object.assign(Object.assign({}, params), { teamId: team.slug }),
            })}>
          <idBadge_1.default avatarSize={18} team={team}/>
        </_1.CrumbLink>} onSelect={item => {
            react_router_1.browserHistory.push((0, recreateRoute_1.default)('', {
                routes,
                params: Object.assign(Object.assign({}, params), { teamId: item.value }),
            }));
        }} hasMenu={hasMenu} route={route} items={teams.map((teamItem, index) => ({
            index,
            value: teamItem.slug,
            label: (<menuItem_1.default>
            <idBadge_1.default team={teamItem}/>
          </menuItem_1.default>),
        }))} onChange={debouncedHandleSearch} busyItemsStillVisible={fetching} {...props}/>);
};
exports.default = TeamCrumb;
//# sourceMappingURL=teamCrumb.jsx.map