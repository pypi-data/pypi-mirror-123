Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const classnames_1 = (0, tslib_1.__importDefault)(require("classnames"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const icons_1 = require("app/icons");
const iconClose_1 = require("app/icons/iconClose");
const locale_1 = require("app/locale");
const callIfFunction_1 = require("app/utils/callIfFunction");
const input_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/input"));
class SearchBar extends React.PureComponent {
    constructor() {
        super(...arguments);
        this.state = {
            query: this.props.query || this.props.defaultQuery,
            dropdownVisible: false,
        };
        this.searchInputRef = React.createRef();
        this.blur = () => {
            if (this.searchInputRef.current) {
                this.searchInputRef.current.blur();
            }
        };
        this.onSubmit = (evt) => {
            evt.preventDefault();
            this.blur();
            this.props.onSearch(this.state.query);
        };
        this.clearSearch = () => {
            this.setState({ query: this.props.defaultQuery }, () => {
                this.props.onSearch(this.state.query);
                (0, callIfFunction_1.callIfFunction)(this.props.onChange, this.state.query);
            });
        };
        this.onQueryFocus = () => {
            this.setState({
                dropdownVisible: true,
            });
        };
        this.onQueryBlur = () => {
            this.setState({ dropdownVisible: false });
        };
        this.onQueryChange = (evt) => {
            const { value } = evt.target;
            this.setState({ query: value });
            (0, callIfFunction_1.callIfFunction)(this.props.onChange, value);
        };
    }
    UNSAFE_componentWillReceiveProps(nextProps) {
        if (nextProps.query !== this.props.query) {
            this.setState({
                query: nextProps.query,
            });
        }
    }
    render() {
        const { className, width } = this.props;
        return (<div className={(0, classnames_1.default)('search', className)}>
        <form className="form-horizontal" onSubmit={this.onSubmit}>
          <div>
            <StyledInput type="text" className="search-input" placeholder={this.props.placeholder} name="query" ref={this.searchInputRef} autoComplete="off" value={this.state.query} onBlur={this.onQueryBlur} onChange={this.onQueryChange} width={width}/>
            <StyledIconSearch className="search-input-icon" size="sm" color="gray300"/>
            {this.state.query !== this.props.defaultQuery && (<SearchClearButton type="button" className="search-clear-form" priority="link" onClick={this.clearSearch} size="xsmall" icon={<iconClose_1.IconClose />} label={(0, locale_1.t)('Clear')}/>)}
          </div>
        </form>
      </div>);
    }
}
SearchBar.defaultProps = {
    query: '',
    defaultQuery: '',
    onSearch: function () { },
};
const StyledInput = (0, styled_1.default)(input_1.default) `
  width: ${p => (p.width ? p.width : undefined)};
  &.focus-visible {
    box-shadow: inset 0 2px 0 rgba(0, 0, 0, 0.04), 0 0 6px rgba(177, 171, 225, 0.3);
    border-color: #a598b2;
    outline: none;
  }
`;
const StyledIconSearch = (0, styled_1.default)(icons_1.IconSearch) `
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  left: 14px;
`;
const SearchClearButton = (0, styled_1.default)(button_1.default) `
  position: absolute;
  top: 50%;
  height: 16px;
  transform: translateY(-50%);
  right: 10px;
  font-size: ${p => p.theme.fontSizeLarge};
  color: ${p => p.theme.gray200};

  &:hover {
    color: ${p => p.theme.gray300};
  }
`;
exports.default = SearchBar;
//# sourceMappingURL=searchBar.jsx.map