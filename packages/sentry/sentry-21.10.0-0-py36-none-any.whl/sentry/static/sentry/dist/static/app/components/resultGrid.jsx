Object.defineProperty(exports, "__esModule", { value: true });
exports.ResultGrid = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const dropdownLink_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownLink"));
const menuItem_1 = (0, tslib_1.__importDefault)(require("app/components/menuItem"));
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const icons_1 = require("app/icons");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
class Filter extends React.Component {
    constructor() {
        super(...arguments);
        this.getSelector = () => (<dropdownLink_1.default title={this.getCurrentLabel()}>
      {this.getDefaultItem()}
      {this.props.options.map(([value, label]) => {
                const filterQuery = {
                    [this.props.queryKey]: value,
                    cursor: '',
                };
                const query = Object.assign(Object.assign({}, this.props.location.query), filterQuery);
                return (<menuItem_1.default key={value} isActive={this.props.value === value} to={{ pathname: this.props.path, query }}>
            {label}
          </menuItem_1.default>);
            })}
    </dropdownLink_1.default>);
    }
    getCurrentLabel() {
        const selected = this.props.options.find(item => { var _a; return item[0] === ((_a = this.props.value) !== null && _a !== void 0 ? _a : ''); });
        if (selected) {
            return this.props.name + ': ' + selected[1];
        }
        return this.props.name + ': ' + 'Any';
    }
    getDefaultItem() {
        const query = Object.assign(Object.assign({}, this.props.location.query), { cursor: '' });
        delete query[this.props.queryKey];
        return (<menuItem_1.default key="" isActive={this.props.value === '' || !this.props.value} to={{ pathname: this.props.path, query }}>
        Any
      </menuItem_1.default>);
    }
    render() {
        return (<div className="filter-options">
        {this.props.options.length === 1 ? (<strong>{this.getCurrentLabel()}</strong>) : (this.getSelector())}
      </div>);
    }
}
class SortBy extends React.Component {
    getCurrentSortLabel() {
        var _a;
        return (_a = this.props.options.find(([value]) => value === this.props.value)) === null || _a === void 0 ? void 0 : _a[1];
    }
    getSortBySelector() {
        return (<dropdownLink_1.default title={this.getCurrentSortLabel()} className="sorted-by">
        {this.props.options.map(([value, label]) => {
                const query = Object.assign(Object.assign({}, this.props.location.query), { sortBy: value, cursor: '' });
                return (<menuItem_1.default isActive={this.props.value === value} key={value} to={{ pathname: this.props.path, query }}>
              {label}
            </menuItem_1.default>);
            })}
      </dropdownLink_1.default>);
    }
    render() {
        if (this.props.options.length === 0) {
            return null;
        }
        return (<div className="sort-options">
        Showing results sorted by
        {this.props.options.length === 1 ? (<strong className="sorted-by">{this.getCurrentSortLabel()}</strong>) : (this.getSortBySelector())}
      </div>);
    }
}
class ResultGrid extends React.Component {
    constructor() {
        super(...arguments);
        this.state = this.defaultState;
        this.onSearch = (e) => {
            var _a, _b;
            const location = (_a = this.props.location) !== null && _a !== void 0 ? _a : {};
            const { query } = this.state;
            const targetQueryParams = Object.assign(Object.assign({}, ((_b = location.query) !== null && _b !== void 0 ? _b : {})), { query, cursor: '' });
            e.preventDefault();
            react_router_1.browserHistory.push({
                pathname: this.props.path,
                query: targetQueryParams,
            });
        };
        this.onQueryChange = (evt) => {
            this.setState({ query: evt.target.value });
        };
    }
    componentWillMount() {
        this.fetchData();
    }
    componentWillReceiveProps() {
        var _a, _b;
        const queryParams = this.query;
        this.setState({
            query: (_a = queryParams.query) !== null && _a !== void 0 ? _a : '',
            sortBy: (_b = queryParams.sortBy) !== null && _b !== void 0 ? _b : this.props.defaultSort,
            filters: Object.assign({}, queryParams),
            pageLinks: null,
            loading: true,
            error: false,
        }, this.fetchData);
    }
    get defaultState() {
        var _a, _b;
        const queryParams = this.query;
        return {
            rows: [],
            loading: true,
            error: false,
            pageLinks: null,
            query: (_a = queryParams.query) !== null && _a !== void 0 ? _a : '',
            sortBy: (_b = queryParams.sortBy) !== null && _b !== void 0 ? _b : this.props.defaultSort,
            filters: Object.assign({}, queryParams),
        };
    }
    get query() {
        var _a, _b;
        return ((_b = ((_a = this.props.location) !== null && _a !== void 0 ? _a : {}).query) !== null && _b !== void 0 ? _b : {});
    }
    remountComponent() {
        this.setState(this.defaultState, this.fetchData);
    }
    refresh() {
        this.setState({ loading: true }, this.fetchData);
    }
    fetchData() {
        // TODO(dcramer): this should explicitly allow filters/sortBy/cursor/perPage
        const queryParams = Object.assign(Object.assign(Object.assign({}, this.props.defaultParams), { sortBy: this.state.sortBy }), this.query);
        this.props.api.request(this.props.endpoint, {
            method: this.props.method,
            data: queryParams,
            success: (data, _, resp) => {
                var _a;
                this.setState({
                    loading: false,
                    error: false,
                    rows: data,
                    pageLinks: (_a = resp === null || resp === void 0 ? void 0 : resp.getResponseHeader('Link')) !== null && _a !== void 0 ? _a : null,
                });
            },
            error: () => {
                this.setState({
                    loading: false,
                    error: true,
                });
            },
        });
    }
    renderLoading() {
        return (<tr>
        <td colSpan={this.props.columns.length}>
          <div className="loading">
            <div className="loading-indicator"/>
            <div className="loading-message">Hold on to your butts!</div>
          </div>
        </td>
      </tr>);
    }
    renderError() {
        return (<tr>
        <td colSpan={this.props.columns.length}>
          <div className="alert-block alert-error">Something bad happened :(</div>
        </td>
      </tr>);
    }
    renderNoResults() {
        return (<tr>
        <td colSpan={this.props.columns.length}>No results found.</td>
      </tr>);
    }
    renderResults() {
        return this.state.rows.map(row => {
            var _a, _b, _c, _d;
            return (<tr key={(_b = (_a = this.props).keyForRow) === null || _b === void 0 ? void 0 : _b.call(_a, row)}>{(_d = (_c = this.props).columnsForRow) === null || _d === void 0 ? void 0 : _d.call(_c, row)}</tr>);
        });
    }
    render() {
        const { filters, sortOptions, path, location } = this.props;
        return (<div className="result-grid">
        <div className="table-options">
          {this.props.hasSearch && (<div className="result-grid-search">
              <form onSubmit={this.onSearch}>
                <div className="form-group">
                  <input type="text" className="form-control input-search" placeholder="search" style={{ width: 300 }} name="query" autoComplete="off" value={this.state.query} onChange={this.onQueryChange}/>
                  <button type="submit" className="btn btn-sm btn-primary">
                    <icons_1.IconSearch size="xs"/>
                  </button>
                </div>
              </form>
            </div>)}
          <SortBy options={sortOptions !== null && sortOptions !== void 0 ? sortOptions : []} value={this.state.sortBy} path={path !== null && path !== void 0 ? path : ''} location={location}/>
          {Object.keys(filters !== null && filters !== void 0 ? filters : {}).map(filterKey => (<Filter key={filterKey} queryKey={filterKey} value={this.state.filters[filterKey]} path={path !== null && path !== void 0 ? path : ''} location={location} {...filters === null || filters === void 0 ? void 0 : filters[filterKey]}/>))}
        </div>

        <table className="table table-grid">
          <thead>
            <tr>{this.props.columns}</tr>
          </thead>
          <tbody>
            {this.state.loading
                ? this.renderLoading()
                : this.state.error
                    ? this.renderError()
                    : this.state.rows.length === 0
                        ? this.renderNoResults()
                        : this.renderResults()}
          </tbody>
        </table>
        {this.props.hasPagination && this.state.pageLinks && (<pagination_1.default pageLinks={this.state.pageLinks}/>)}
      </div>);
    }
}
exports.ResultGrid = ResultGrid;
ResultGrid.defaultProps = {
    path: '',
    endpoint: '',
    method: 'GET',
    columns: [],
    sortOptions: [],
    filters: {},
    defaultSort: '',
    keyForRow: row => row.id,
    columnsForRow: () => [],
    defaultParams: {
        per_page: 50,
    },
    hasPagination: true,
    hasSearch: false,
};
exports.default = (0, withApi_1.default)(ResultGrid);
//# sourceMappingURL=resultGrid.jsx.map