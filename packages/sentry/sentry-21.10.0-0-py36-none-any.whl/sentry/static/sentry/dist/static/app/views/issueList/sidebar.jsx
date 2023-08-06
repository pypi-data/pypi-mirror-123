Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const map_1 = (0, tslib_1.__importDefault)(require("lodash/map"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const iconClose_1 = require("app/icons/iconClose");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const stream_1 = require("app/utils/stream");
const tagFilter_1 = (0, tslib_1.__importDefault)(require("./tagFilter"));
class IssueListSidebar extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            queryObj: (0, stream_1.queryToObj)(this.props.query),
            textFilter: (0, stream_1.queryToObj)(this.props.query).__text,
        };
        this.onSelectTag = (tag, value) => {
            const newQuery = Object.assign({}, this.state.queryObj);
            if (value) {
                newQuery[tag.key] = value;
            }
            else {
                delete newQuery[tag.key];
            }
            this.setState({
                queryObj: newQuery,
            }, this.onQueryChange);
        };
        this.onTextChange = (evt) => {
            this.setState({ textFilter: evt.target.value });
        };
        this.onTextFilterSubmit = (evt) => {
            evt && evt.preventDefault();
            const newQueryObj = Object.assign(Object.assign({}, this.state.queryObj), { __text: this.state.textFilter });
            this.setState({
                queryObj: newQueryObj,
            }, this.onQueryChange);
        };
        this.onQueryChange = () => {
            const query = (0, stream_1.objToQuery)(this.state.queryObj);
            this.props.onQueryChange && this.props.onQueryChange(query);
        };
        this.onClearSearch = () => {
            this.setState({
                textFilter: '',
            }, this.onTextFilterSubmit);
        };
    }
    componentWillReceiveProps(nextProps) {
        // If query was updated by another source (e.g. SearchBar),
        // clobber state of sidebar with new query.
        const query = (0, stream_1.objToQuery)(this.state.queryObj);
        if (!(0, isEqual_1.default)(nextProps.query, query)) {
            const queryObj = (0, stream_1.queryToObj)(nextProps.query);
            this.setState({
                queryObj,
                textFilter: queryObj.__text,
            });
        }
    }
    render() {
        const { loading, tagValueLoader, tags } = this.props;
        return (<StreamSidebar>
        {loading ? (<loadingIndicator_1.default />) : (<React.Fragment>
            <StreamTagFilter>
              <StyledHeader>{(0, locale_1.t)('Text')}</StyledHeader>
              <form onSubmit={this.onTextFilterSubmit}>
                <input className="form-control" placeholder={(0, locale_1.t)('Search title and culprit text body')} onChange={this.onTextChange} value={this.state.textFilter}/>
                {this.state.textFilter && (<StyledIconClose size="xs" onClick={this.onClearSearch}/>)}
              </form>
              <StyledHr />
            </StreamTagFilter>

            {(0, map_1.default)(tags, tag => (<tagFilter_1.default value={this.state.queryObj[tag.key]} key={tag.key} tag={tag} onSelect={this.onSelectTag} tagValueLoader={tagValueLoader}/>))}
          </React.Fragment>)}
      </StreamSidebar>);
    }
}
IssueListSidebar.defaultProps = {
    tags: {},
    query: '',
    onQueryChange: function () { },
};
exports.default = IssueListSidebar;
const StreamSidebar = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: column;
  width: 100%;
`;
const StyledIconClose = (0, styled_1.default)(iconClose_1.IconClose) `
  cursor: pointer;
  position: absolute;
  top: 13px;
  right: 10px;
  color: ${p => p.theme.gray200};

  &:hover {
    color: ${p => p.theme.gray300};
  }
`;
const StyledHeader = (0, styled_1.default)('h6') `
  color: ${p => p.theme.subText};
  margin-bottom: ${(0, space_1.default)(1)};
`;
const StreamTagFilter = (0, styled_1.default)('div') `
  margin-bottom: ${(0, space_1.default)(2)};
`;
const StyledHr = (0, styled_1.default)('hr') `
  margin: ${(0, space_1.default)(2)} 0 0;
`;
//# sourceMappingURL=sidebar.jsx.map