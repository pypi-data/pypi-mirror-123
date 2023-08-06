Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const debounce_1 = (0, tslib_1.__importDefault)(require("lodash/debounce"));
const indicator_1 = require("app/actionCreators/indicator");
const navigation_1 = require("app/actionCreators/navigation");
const autoComplete_1 = (0, tslib_1.__importDefault)(require("app/components/autoComplete"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const searchResult_1 = (0, tslib_1.__importDefault)(require("app/components/search/searchResult"));
const searchResultWrapper_1 = (0, tslib_1.__importDefault)(require("app/components/search/searchResultWrapper"));
const sources_1 = (0, tslib_1.__importDefault)(require("app/components/search/sources"));
const apiSource_1 = (0, tslib_1.__importDefault)(require("app/components/search/sources/apiSource"));
const commandSource_1 = (0, tslib_1.__importDefault)(require("app/components/search/sources/commandSource"));
const formSource_1 = (0, tslib_1.__importDefault)(require("app/components/search/sources/formSource"));
const routeSource_1 = (0, tslib_1.__importDefault)(require("app/components/search/sources/routeSource"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
const replaceRouterParams_1 = (0, tslib_1.__importDefault)(require("app/utils/replaceRouterParams"));
// Not using typeof defaultProps because of the wrapping HOC which
// causes defaultProp magic to fall off.
const defaultProps = {
    renderItem: ({ item, matches, itemProps, highlighted, }) => (<searchResultWrapper_1.default {...itemProps} highlighted={highlighted}>
      <searchResult_1.default highlighted={highlighted} item={item} matches={matches}/>
    </searchResultWrapper_1.default>),
    sources: [apiSource_1.default, formSource_1.default, routeSource_1.default, commandSource_1.default],
    closeOnSelect: true,
};
// "Omni" search
class Search extends React.Component {
    constructor() {
        super(...arguments);
        this.handleSelect = (item, state) => {
            if (!item) {
                return;
            }
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: `${this.props.entryPoint}.select`,
                eventName: `${this.props.entryPoint} Select`,
                query: state && state.inputValue,
                result_type: item.resultType,
                source_type: item.sourceType,
                organization_id: null,
            });
            const { to, action, configUrl } = item;
            // `action` refers to a callback function while
            // `to` is a react-router route
            if (action) {
                action(item, state);
                return;
            }
            if (!to) {
                return;
            }
            if (to.startsWith('http')) {
                const open = window.open();
                if (open === null) {
                    (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to open search result (a popup blocker may have caused this).'));
                    return;
                }
                open.opener = null;
                open.location.href = to;
                return;
            }
            const { params, router } = this.props;
            const nextPath = (0, replaceRouterParams_1.default)(to, params);
            (0, navigation_1.navigateTo)(nextPath, router, configUrl);
        };
        this.saveQueryMetrics = (0, debounce_1.default)(query => {
            if (!query) {
                return;
            }
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: `${this.props.entryPoint}.query`,
                eventName: `${this.props.entryPoint} Query`,
                query,
                organization_id: null,
            });
        }, 200);
        this.renderItem = ({ resultObj, index, highlightedIndex, getItemProps }) => {
            // resultObj is a fuse.js result object with {item, matches, score}
            const { renderItem } = this.props;
            const highlighted = index === highlightedIndex;
            const { item, matches } = resultObj;
            const key = `${item.title}-${index}`;
            const itemProps = Object.assign({}, getItemProps({ item, index }));
            if (typeof renderItem !== 'function') {
                throw new Error('Invalid `renderItem`');
            }
            const renderedItem = renderItem({
                item,
                matches,
                index,
                highlighted,
                itemProps,
            });
            return React.cloneElement(renderedItem, { key });
        };
    }
    componentDidMount() {
        (0, analytics_1.trackAnalyticsEvent)({
            eventKey: `${this.props.entryPoint}.open`,
            eventName: `${this.props.entryPoint} Open`,
            organization_id: null,
        });
    }
    render() {
        const { params, dropdownStyle, searchOptions, minSearch, maxResults, renderInput, sources, closeOnSelect, resultFooter, } = this.props;
        return (<autoComplete_1.default defaultHighlightedIndex={0} onSelect={this.handleSelect} closeOnSelect={closeOnSelect}>
        {({ getInputProps, getItemProps, isOpen, inputValue, highlightedIndex }) => {
                const searchQuery = inputValue.toLowerCase().trim();
                const isValidSearch = inputValue.length >= minSearch;
                this.saveQueryMetrics(searchQuery);
                return (<SearchWrapper>
              {renderInput({ getInputProps })}

              {isValidSearch && isOpen ? (<sources_1.default searchOptions={searchOptions} query={searchQuery} params={params} sources={sources !== null && sources !== void 0 ? sources : defaultProps.sources}>
                  {({ isLoading, results, hasAnyResults }) => (<DropdownBox className={dropdownStyle}>
                      {isLoading && (<LoadingWrapper>
                          <loadingIndicator_1.default mini hideMessage relative/>
                        </LoadingWrapper>)}
                      {!isLoading &&
                                results.slice(0, maxResults).map((resultObj, index) => this.renderItem({
                                    resultObj,
                                    index,
                                    highlightedIndex,
                                    getItemProps,
                                }))}
                      {!isLoading && !hasAnyResults && (<EmptyItem>{(0, locale_1.t)('No results found')}</EmptyItem>)}
                      {!isLoading && resultFooter && (<ResultFooter>{resultFooter}</ResultFooter>)}
                    </DropdownBox>)}
                </sources_1.default>) : null}
            </SearchWrapper>);
            }}
      </autoComplete_1.default>);
    }
}
Search.defaultProps = defaultProps;
exports.default = (0, react_router_1.withRouter)(Search);
const DropdownBox = (0, styled_1.default)('div') `
  background: ${p => p.theme.background};
  border: 1px solid ${p => p.theme.border};
  box-shadow: ${p => p.theme.dropShadowHeavy};
  position: absolute;
  top: 36px;
  right: 0;
  width: 400px;
  border-radius: 5px;
  overflow: auto;
  max-height: 60vh;
`;
const SearchWrapper = (0, styled_1.default)('div') `
  position: relative;
`;
const ResultFooter = (0, styled_1.default)('div') `
  position: sticky;
  bottom: 0;
  left: 0;
  right: 0;
`;
const EmptyItem = (0, styled_1.default)(searchResultWrapper_1.default) `
  text-align: center;
  padding: 16px;
  opacity: 0.5;
`;
const LoadingWrapper = (0, styled_1.default)('div') `
  display: flex;
  justify-content: center;
  align-items: center;
  padding: ${(0, space_1.default)(1)};
`;
//# sourceMappingURL=index.jsx.map