Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const omit_1 = (0, tslib_1.__importDefault)(require("lodash/omit"));
const pick_1 = (0, tslib_1.__importDefault)(require("lodash/pick"));
const guideAnchor_1 = (0, tslib_1.__importDefault)(require("app/components/assistant/guideAnchor"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const errorBoundary_1 = (0, tslib_1.__importDefault)(require("app/components/errorBoundary"));
const eventDataSection_1 = (0, tslib_1.__importDefault)(require("app/components/events/eventDataSection"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const breadcrumbs_1 = require("app/types/breadcrumbs");
const event_1 = require("app/types/event");
const utils_1 = require("app/utils");
const searchBarAction_1 = (0, tslib_1.__importDefault)(require("../searchBarAction"));
const searchBarActionFilter_1 = (0, tslib_1.__importDefault)(require("../searchBarAction/searchBarActionFilter"));
const level_1 = (0, tslib_1.__importDefault)(require("./breadcrumb/level"));
const type_1 = (0, tslib_1.__importDefault)(require("./breadcrumb/type"));
const breadcrumbs_2 = (0, tslib_1.__importDefault)(require("./breadcrumbs"));
const utils_2 = require("./utils");
function BreadcrumbsContainer({ data, event, organization, type: eventType, route, router, }) {
    const [state, setState] = (0, react_1.useState)({
        searchTerm: '',
        breadcrumbs: [],
        filteredByFilter: [],
        filteredBySearch: [],
        filterOptions: {},
        displayRelativeTime: false,
    });
    const { filterOptions, breadcrumbs, searchTerm, filteredBySearch, displayRelativeTime, relativeTime, filteredByFilter, } = state;
    (0, react_1.useEffect)(() => {
        loadBreadcrumbs();
    }, []);
    function loadBreadcrumbs() {
        let crumbs = data.values;
        // Add the (virtual) breadcrumb based on the error or message event if possible.
        const virtualCrumb = getVirtualCrumb();
        if (virtualCrumb) {
            crumbs = [...crumbs, virtualCrumb];
        }
        const transformedCrumbs = (0, utils_2.transformCrumbs)(crumbs);
        setState(Object.assign(Object.assign({}, state), { relativeTime: transformedCrumbs[transformedCrumbs.length - 1].timestamp, breadcrumbs: transformedCrumbs, filteredByFilter: transformedCrumbs, filteredBySearch: transformedCrumbs, filterOptions: getFilterOptions(transformedCrumbs) }));
    }
    function getFilterOptions(crumbs) {
        const typeOptions = getFilterTypes(crumbs);
        const levels = getFilterLevels(typeOptions);
        const options = {};
        if (!!typeOptions.length) {
            options[(0, locale_1.t)('Types')] = typeOptions.map(typeOption => (0, omit_1.default)(typeOption, 'levels'));
        }
        if (!!levels.length) {
            options[(0, locale_1.t)('Levels')] = levels;
        }
        return options;
    }
    function getFilterTypes(crumbs) {
        const filterTypes = [];
        for (const index in crumbs) {
            const breadcrumb = crumbs[index];
            const foundFilterType = filterTypes.findIndex(f => f.id === breadcrumb.type);
            if (foundFilterType === -1) {
                filterTypes.push({
                    id: breadcrumb.type,
                    symbol: <type_1.default type={breadcrumb.type} color={breadcrumb.color}/>,
                    isChecked: false,
                    description: breadcrumb.description,
                    levels: (breadcrumb === null || breadcrumb === void 0 ? void 0 : breadcrumb.level) ? [breadcrumb.level] : [],
                });
                continue;
            }
            if ((breadcrumb === null || breadcrumb === void 0 ? void 0 : breadcrumb.level) &&
                !filterTypes[foundFilterType].levels.includes(breadcrumb.level)) {
                filterTypes[foundFilterType].levels.push(breadcrumb.level);
            }
        }
        return filterTypes;
    }
    function getFilterLevels(types) {
        const filterLevels = [];
        for (const indexType in types) {
            for (const indexLevel in types[indexType].levels) {
                const level = types[indexType].levels[indexLevel];
                if (filterLevels.some(f => f.id === level)) {
                    continue;
                }
                filterLevels.push({
                    id: level,
                    symbol: <level_1.default level={level}/>,
                    isChecked: false,
                });
            }
        }
        return filterLevels;
    }
    function filterBySearch(newSearchTerm, crumbs) {
        if (!newSearchTerm.trim()) {
            return crumbs;
        }
        // Slightly hacky, but it works
        // the string is being `stringfy`d here in order to match exactly the same `stringfy`d string of the loop
        const searchFor = JSON.stringify(newSearchTerm)
            // it replaces double backslash generate by JSON.stringfy with single backslash
            .replace(/((^")|("$))/g, '')
            .toLocaleLowerCase();
        return crumbs.filter(obj => Object.keys((0, pick_1.default)(obj, ['type', 'category', 'message', 'level', 'timestamp', 'data'])).some(key => {
            const info = obj[key];
            if (!(0, utils_1.defined)(info) || !String(info).trim()) {
                return false;
            }
            return JSON.stringify(info)
                .replace(/((^")|("$))/g, '')
                .toLocaleLowerCase()
                .trim()
                .includes(searchFor);
        }));
    }
    function getFilteredCrumbsByFilter(newfilterOptions) {
        const checkedTypeOptions = new Set(Object.values(newfilterOptions)[0]
            .filter(filterOption => filterOption.isChecked)
            .map(option => option.id));
        const checkedLevelOptions = new Set(Object.values(newfilterOptions)[1]
            .filter(filterOption => filterOption.isChecked)
            .map(option => option.id));
        if (!![...checkedTypeOptions].length && !![...checkedLevelOptions].length) {
            return breadcrumbs.filter(filteredCrumb => checkedTypeOptions.has(filteredCrumb.type) &&
                checkedLevelOptions.has(filteredCrumb.level));
        }
        if (!![...checkedTypeOptions].length) {
            return breadcrumbs.filter(filteredCrumb => checkedTypeOptions.has(filteredCrumb.type));
        }
        if (!![...checkedLevelOptions].length) {
            return breadcrumbs.filter(filteredCrumb => checkedLevelOptions.has(filteredCrumb.level));
        }
        return breadcrumbs;
    }
    function moduleToCategory(module) {
        if (!module) {
            return undefined;
        }
        const match = module.match(/^.*\/(.*?)(:\d+)/);
        if (!match) {
            return module.split(/./)[0];
        }
        return match[1];
    }
    function getVirtualCrumb() {
        const exception = event.entries.find(entry => entry.type === event_1.EntryType.EXCEPTION);
        if (!exception && !event.message) {
            return undefined;
        }
        const timestamp = event.dateCreated;
        if (exception) {
            const { type, value, module: mdl } = exception.data.values[0];
            return {
                type: breadcrumbs_1.BreadcrumbType.ERROR,
                level: breadcrumbs_1.BreadcrumbLevelType.ERROR,
                category: moduleToCategory(mdl) || 'exception',
                data: {
                    type,
                    value,
                },
                timestamp,
            };
        }
        const levelTag = (event.tags || []).find(tag => tag.key === 'level');
        return {
            type: breadcrumbs_1.BreadcrumbType.INFO,
            level: (levelTag === null || levelTag === void 0 ? void 0 : levelTag.value) || breadcrumbs_1.BreadcrumbLevelType.UNDEFINED,
            category: 'message',
            message: event.message,
            timestamp,
        };
    }
    function handleSearch(value) {
        setState(Object.assign(Object.assign({}, state), { searchTerm: value, filteredBySearch: filterBySearch(value, filteredByFilter) }));
    }
    function handleFilter(newfilterOptions) {
        const newfilteredByFilter = getFilteredCrumbsByFilter(newfilterOptions);
        setState(Object.assign(Object.assign({}, state), { filterOptions: newfilterOptions, filteredByFilter: newfilteredByFilter, filteredBySearch: filterBySearch(searchTerm, newfilteredByFilter) }));
    }
    function handleSwitchTimeFormat() {
        setState(Object.assign(Object.assign({}, state), { displayRelativeTime: !displayRelativeTime }));
    }
    function handleResetFilter() {
        setState(Object.assign(Object.assign({}, state), { filteredByFilter: breadcrumbs, filterOptions: Object.keys(filterOptions).reduce((accumulator, currentValue) => {
                accumulator[currentValue] = filterOptions[currentValue].map(filterOption => (Object.assign(Object.assign({}, filterOption), { isChecked: false })));
                return accumulator;
            }, {}), filteredBySearch: filterBySearch(searchTerm, breadcrumbs) }));
    }
    function handleResetSearchBar() {
        setState(Object.assign(Object.assign({}, state), { searchTerm: '', filteredBySearch: breadcrumbs }));
    }
    function getEmptyMessage() {
        if (!!filteredBySearch.length) {
            return {};
        }
        if (searchTerm && !filteredBySearch.length) {
            const hasActiveFilter = Object.values(filterOptions)
                .flatMap(filterOption => filterOption)
                .find(filterOption => filterOption.isChecked);
            return {
                emptyMessage: (0, locale_1.t)('Sorry, no breadcrumbs match your search query'),
                emptyAction: hasActiveFilter ? (<button_1.default onClick={handleResetFilter} priority="primary">
            {(0, locale_1.t)('Reset filter')}
          </button_1.default>) : (<button_1.default onClick={handleResetSearchBar} priority="primary">
            {(0, locale_1.t)('Clear search bar')}
          </button_1.default>),
            };
        }
        return {
            emptyMessage: (0, locale_1.t)('There are no breadcrumbs to be displayed'),
        };
    }
    return (<StyledEventDataSection type={eventType} title={<guideAnchor_1.default target="breadcrumbs" position="right">
          <h3>{(0, locale_1.t)('Breadcrumbs')}</h3>
        </guideAnchor_1.default>} actions={<StyledSearchBarAction placeholder={(0, locale_1.t)('Search breadcrumbs')} onChange={handleSearch} query={searchTerm} filter={<searchBarActionFilter_1.default onChange={handleFilter} options={filterOptions}/>}/>} wrapTitle={false} isCentered>
      <errorBoundary_1.default>
        <breadcrumbs_2.default router={router} route={route} emptyMessage={getEmptyMessage()} breadcrumbs={filteredBySearch} event={event} organization={organization} onSwitchTimeFormat={handleSwitchTimeFormat} displayRelativeTime={displayRelativeTime} searchTerm={searchTerm} relativeTime={relativeTime} // relativeTime has to be always available, as the last item timestamp is the event created time
    />
      </errorBoundary_1.default>
    </StyledEventDataSection>);
}
exports.default = BreadcrumbsContainer;
const StyledEventDataSection = (0, styled_1.default)(eventDataSection_1.default) `
  margin-bottom: ${(0, space_1.default)(3)};
`;
const StyledSearchBarAction = (0, styled_1.default)(searchBarAction_1.default) `
  z-index: 2;
`;
//# sourceMappingURL=index.jsx.map