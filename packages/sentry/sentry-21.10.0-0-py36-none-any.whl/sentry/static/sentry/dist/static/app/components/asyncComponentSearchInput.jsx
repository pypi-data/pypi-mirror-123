Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const debounce_1 = (0, tslib_1.__importDefault)(require("lodash/debounce"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const locale_1 = require("app/locale");
const input_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/input"));
/**
 * This is a search input that can be easily used in AsyncComponent/Views.
 *
 * It probably doesn't make too much sense outside of an AsyncComponent atm.
 */
class AsyncComponentSearchInput extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            query: '',
            busy: false,
        };
        this.immediateQuery = (searchQuery) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { location, api } = this.props;
            this.setState({ busy: true });
            try {
                const [data, , resp] = yield api.requestPromise(`${this.props.url}`, {
                    includeAllArgs: true,
                    method: 'GET',
                    query: Object.assign(Object.assign({}, location.query), { query: searchQuery }),
                });
                // only update data if the request's query matches the current query
                if (this.state.query === searchQuery) {
                    this.props.onSuccess(data, resp);
                }
            }
            catch (_a) {
                this.props.onError();
            }
            this.setState({ busy: false });
        });
        this.query = (0, debounce_1.default)(this.immediateQuery, this.props.debounceWait);
        this.handleChange = (query) => {
            this.query(query);
            this.setState({ query });
        };
        this.handleInputChange = (evt) => this.handleChange(evt.target.value);
        /**
         * This is called when "Enter" (more specifically a form "submit" event) is pressed.
         */
        this.handleSearch = (evt) => {
            const { updateRoute, onSearchSubmit } = this.props;
            evt.preventDefault();
            // Update the URL to reflect search term.
            if (updateRoute) {
                const { router, location } = this.props;
                router.push({
                    pathname: location.pathname,
                    query: {
                        query: this.state.query,
                    },
                });
            }
            if (typeof onSearchSubmit !== 'function') {
                return;
            }
            onSearchSubmit(this.state.query, evt);
        };
    }
    render() {
        const { placeholder, children, className } = this.props;
        const { busy, query } = this.state;
        const defaultSearchBar = (<Form onSubmit={this.handleSearch}>
        <input_1.default value={query} onChange={this.handleInputChange} className={className} placeholder={placeholder}/>
        {busy && <StyledLoadingIndicator size={18} hideMessage mini/>}
      </Form>);
        return children === undefined
            ? defaultSearchBar
            : children({ defaultSearchBar, busy, value: query, handleChange: this.handleChange });
    }
}
AsyncComponentSearchInput.defaultProps = {
    placeholder: (0, locale_1.t)('Search...'),
    debounceWait: 200,
};
const StyledLoadingIndicator = (0, styled_1.default)(loadingIndicator_1.default) `
  position: absolute;
  right: 25px;
  top: 50%;
  transform: translateY(-13px);
`;
const Form = (0, styled_1.default)('form') `
  position: relative;
`;
exports.default = (0, react_router_1.withRouter)(AsyncComponentSearchInput);
//# sourceMappingURL=asyncComponentSearchInput.jsx.map