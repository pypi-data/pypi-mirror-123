Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const debounce_1 = (0, tslib_1.__importDefault)(require("lodash/debounce"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const pick_1 = (0, tslib_1.__importDefault)(require("lodash/pick"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const panelTable_1 = (0, tslib_1.__importDefault)(require("app/components/panels/panelTable"));
const questionTooltip_1 = (0, tslib_1.__importDefault)(require("app/components/questionTooltip"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const debugImage_1 = require("app/types/debugImage");
const utils_1 = require("app/utils");
const searchBarAction_1 = (0, tslib_1.__importDefault)(require("../../searchBarAction"));
const searchBarActionFilter_1 = (0, tslib_1.__importDefault)(require("../../searchBarAction/searchBarActionFilter"));
const status_1 = (0, tslib_1.__importDefault)(require("./candidate/status"));
const candidate_1 = (0, tslib_1.__importDefault)(require("./candidate"));
const utils_2 = require("./utils");
const filterOptionCategories = {
    status: (0, locale_1.t)('Status'),
    source: (0, locale_1.t)('Source'),
};
class Candidates extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            searchTerm: '',
            filterOptions: {},
            filteredCandidatesBySearch: [],
            filteredCandidatesByFilter: [],
        };
        this.doSearch = (0, debounce_1.default)(this.filterCandidatesBySearch, 300);
        this.handleChangeSearchTerm = (searchTerm = '') => {
            this.setState({ searchTerm });
        };
        this.handleChangeFilter = (filterOptions) => {
            const { filteredCandidatesBySearch } = this.state;
            const filteredCandidatesByFilter = this.getFilteredCandidatedByFilter(filteredCandidatesBySearch, filterOptions);
            this.setState({ filterOptions, filteredCandidatesByFilter });
        };
        this.handleResetFilter = () => {
            const { filterOptions } = this.state;
            this.setState({
                filterOptions: Object.keys(filterOptions).reduce((accumulator, currentValue) => {
                    accumulator[currentValue] = filterOptions[currentValue].map(filterOption => (Object.assign(Object.assign({}, filterOption), { isChecked: false })));
                    return accumulator;
                }, {}),
            }, this.filterCandidatesBySearch);
        };
        this.handleResetSearchBar = () => {
            const { candidates } = this.props;
            this.setState({
                searchTerm: '',
                filteredCandidatesByFilter: candidates,
                filteredCandidatesBySearch: candidates,
            });
        };
    }
    componentDidMount() {
        this.getFilters();
    }
    componentDidUpdate(prevProps, prevState) {
        if (!(0, isEqual_1.default)(prevProps.candidates, this.props.candidates)) {
            this.getFilters();
            return;
        }
        if (prevState.searchTerm !== this.state.searchTerm) {
            this.doSearch();
        }
    }
    filterCandidatesBySearch() {
        const { searchTerm, filterOptions } = this.state;
        const { candidates } = this.props;
        if (!searchTerm.trim()) {
            const filteredCandidatesByFilter = this.getFilteredCandidatedByFilter(candidates, filterOptions);
            this.setState({
                filteredCandidatesBySearch: candidates,
                filteredCandidatesByFilter,
            });
            return;
        }
        // Slightly hacky, but it works
        // the string is being `stringfy`d here in order to match exactly the same `stringfy`d string of the loop
        const searchFor = JSON.stringify(searchTerm)
            // it replaces double backslash generate by JSON.stringfy with single backslash
            .replace(/((^")|("$))/g, '')
            .toLocaleLowerCase();
        const filteredCandidatesBySearch = candidates.filter(obj => Object.keys((0, pick_1.default)(obj, ['source_name', 'location'])).some(key => {
            const info = obj[key];
            if (key === 'location' && typeof Number(info) === 'number') {
                return false;
            }
            if (!(0, utils_1.defined)(info) || !String(info).trim()) {
                return false;
            }
            return JSON.stringify(info)
                .replace(/((^")|("$))/g, '')
                .toLocaleLowerCase()
                .trim()
                .includes(searchFor);
        }));
        const filteredCandidatesByFilter = this.getFilteredCandidatedByFilter(filteredCandidatesBySearch, filterOptions);
        this.setState({
            filteredCandidatesBySearch,
            filteredCandidatesByFilter,
        });
    }
    getFilters() {
        const candidates = [...this.props.candidates];
        const filterOptions = this.getFilterOptions(candidates);
        this.setState({
            filterOptions,
            filteredCandidatesBySearch: candidates,
            filteredCandidatesByFilter: this.getFilteredCandidatedByFilter(candidates, filterOptions),
        });
    }
    getFilterOptions(candidates) {
        const { imageStatus } = this.props;
        const filterOptions = {};
        const candidateStatus = [
            ...new Set(candidates.map(candidate => candidate.download.status)),
        ];
        if (candidateStatus.length > 1) {
            filterOptions[filterOptionCategories.status] = candidateStatus.map(status => ({
                id: status,
                symbol: <status_1.default status={status}/>,
                isChecked: status !== debugImage_1.CandidateDownloadStatus.NOT_FOUND ||
                    imageStatus === debugImage_1.ImageStatus.MISSING,
            }));
        }
        const candidateSources = [
            ...new Set(candidates.map(candidate => { var _a; return (_a = candidate.source_name) !== null && _a !== void 0 ? _a : (0, locale_1.t)('Unknown'); })),
        ];
        if (candidateSources.length > 1) {
            filterOptions[filterOptionCategories.source] = candidateSources.map(sourceName => ({
                id: sourceName,
                symbol: sourceName,
                isChecked: false,
            }));
        }
        return filterOptions;
    }
    getFilteredCandidatedByFilter(candidates, filterOptions) {
        var _a, _b;
        const checkedStatusOptions = new Set((_a = filterOptions[filterOptionCategories.status]) === null || _a === void 0 ? void 0 : _a.filter(filterOption => filterOption.isChecked).map(option => option.id));
        const checkedSourceOptions = new Set((_b = filterOptions[filterOptionCategories.source]) === null || _b === void 0 ? void 0 : _b.filter(filterOption => filterOption.isChecked).map(option => option.id));
        if (checkedStatusOptions.size === 0 && checkedSourceOptions.size === 0) {
            return candidates;
        }
        if (checkedStatusOptions.size > 0) {
            const filteredByStatus = candidates.filter(candidate => checkedStatusOptions.has(candidate.download.status));
            if (checkedSourceOptions.size === 0) {
                return filteredByStatus;
            }
            return filteredByStatus.filter(candidate => { var _a; return checkedSourceOptions.has((_a = candidate === null || candidate === void 0 ? void 0 : candidate.source_name) !== null && _a !== void 0 ? _a : ''); });
        }
        return candidates.filter(candidate => { var _a; return checkedSourceOptions.has((_a = candidate === null || candidate === void 0 ? void 0 : candidate.source_name) !== null && _a !== void 0 ? _a : ''); });
    }
    getEmptyMessage() {
        const { searchTerm, filteredCandidatesByFilter: images, filterOptions } = this.state;
        if (!!images.length) {
            return {};
        }
        const hasActiveFilter = Object.values(filterOptions)
            .flatMap(filterOption => filterOption)
            .find(filterOption => filterOption.isChecked);
        if (searchTerm || hasActiveFilter) {
            return {
                emptyMessage: (0, locale_1.t)('Sorry, no debug files match your search query'),
                emptyAction: hasActiveFilter ? (<button_1.default onClick={this.handleResetFilter} priority="primary">
            {(0, locale_1.t)('Reset filter')}
          </button_1.default>) : (<button_1.default onClick={this.handleResetSearchBar} priority="primary">
            {(0, locale_1.t)('Clear search bar')}
          </button_1.default>),
            };
        }
        return {
            emptyMessage: (0, locale_1.t)('There are no debug files to be displayed'),
        };
    }
    render() {
        const { organization, projSlug, baseUrl, onDelete, isLoading, candidates, eventDateReceived, hasReprocessWarning, } = this.props;
        const { searchTerm, filterOptions, filteredCandidatesByFilter } = this.state;
        const haveCandidatesOkOrDeletedDebugFile = candidates.some(candidate => (candidate.download.status === debugImage_1.CandidateDownloadStatus.OK &&
            candidate.source === utils_2.INTERNAL_SOURCE) ||
            candidate.download.status === debugImage_1.CandidateDownloadStatus.DELETED);
        const haveCandidatesAtLeastOneAction = haveCandidatesOkOrDeletedDebugFile || hasReprocessWarning;
        return (<Wrapper>
        <Header>
          <Title>
            {(0, locale_1.t)('Debug File Candidates')}
            <questionTooltip_1.default title={(0, locale_1.tct)('These are the Debug Information Files (DIFs) corresponding to this image which have been looked up on [docLink:symbol servers] during the processing of the stacktrace.', {
                docLink: (<externalLink_1.default href="https://docs.sentry.io/platforms/native/data-management/debug-files/symbol-servers/"/>),
            })} size="xs" position="top" isHoverable/>
          </Title>
          {!!candidates.length && (<StyledSearchBarAction query={searchTerm} onChange={value => this.handleChangeSearchTerm(value)} placeholder={(0, locale_1.t)('Search debug file candidates')} filter={<searchBarActionFilter_1.default options={filterOptions} onChange={this.handleChangeFilter}/>}/>)}
        </Header>
        <StyledPanelTable headers={haveCandidatesAtLeastOneAction
                ? [(0, locale_1.t)('Status'), (0, locale_1.t)('Information'), '']
                : [(0, locale_1.t)('Status'), (0, locale_1.t)('Information')]} isEmpty={!filteredCandidatesByFilter.length} isLoading={isLoading} {...this.getEmptyMessage()}>
          {filteredCandidatesByFilter.map((candidate, index) => (<candidate_1.default key={index} candidate={candidate} organization={organization} baseUrl={baseUrl} projSlug={projSlug} eventDateReceived={eventDateReceived} hasReprocessWarning={hasReprocessWarning} haveCandidatesAtLeastOneAction={haveCandidatesAtLeastOneAction} onDelete={onDelete}/>))}
        </StyledPanelTable>
      </Wrapper>);
    }
}
exports.default = Candidates;
const Wrapper = (0, styled_1.default)('div') `
  display: grid;
`;
const Header = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: column;
  @media (min-width: ${props => props.theme.breakpoints[0]}) {
    flex-wrap: wrap;
    flex-direction: row;
  }
`;
const Title = (0, styled_1.default)('div') `
  padding-right: ${(0, space_1.default)(4)};
  display: grid;
  grid-gap: ${(0, space_1.default)(0.5)};
  grid-template-columns: repeat(2, max-content);
  align-items: center;
  font-weight: 600;
  color: ${p => p.theme.gray400};
  height: 32px;
  flex: 1;

  @media (min-width: ${props => props.theme.breakpoints[0]}) {
    margin-bottom: ${(0, space_1.default)(1)};
  }
`;
const StyledPanelTable = (0, styled_1.default)(panelTable_1.default) `
  grid-template-columns: ${p => p.headers.length === 3 ? 'max-content 1fr max-content' : 'max-content 1fr'};

  height: 100%;

  @media (min-width: ${props => props.theme.breakpoints[4]}) {
    overflow: visible;
  }
`;
const StyledSearchBarAction = (0, styled_1.default)(searchBarAction_1.default) `
  margin-bottom: ${(0, space_1.default)(1.5)};
`;
//# sourceMappingURL=candidates.jsx.map