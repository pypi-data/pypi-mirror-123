Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const dropdownControl_1 = (0, tslib_1.__importStar)(require("app/components/dropdownControl"));
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
class RepositorySwitcher extends react_1.PureComponent {
    constructor() {
        super(...arguments);
        this.state = {};
        this.dropdownButton = (0, react_1.createRef)();
        this.handleRepoFilterChange = (activeRepo) => {
            const { router, location } = this.props;
            router.push(Object.assign(Object.assign({}, location), { query: Object.assign(Object.assign({}, location.query), { cursor: undefined, activeRepo }) }));
        };
    }
    componentDidMount() {
        this.setButtonDropDownWidth();
    }
    setButtonDropDownWidth() {
        var _a, _b;
        const dropdownButtonWidth = (_b = (_a = this.dropdownButton) === null || _a === void 0 ? void 0 : _a.current) === null || _b === void 0 ? void 0 : _b.offsetWidth;
        if (dropdownButtonWidth) {
            this.setState({ dropdownButtonWidth });
        }
    }
    render() {
        const { activeRepository, repositories } = this.props;
        const { dropdownButtonWidth } = this.state;
        const activeRepo = activeRepository === null || activeRepository === void 0 ? void 0 : activeRepository.name;
        return (<StyledDropdownControl minMenuWidth={dropdownButtonWidth} label={<react_1.Fragment>
            <FilterText>{`${(0, locale_1.t)('Filter')}:`}</FilterText>
            {activeRepo}
          </react_1.Fragment>} buttonProps={{ forwardRef: this.dropdownButton }}>
        {repositories
                .map(repo => repo.name)
                .map(repoName => (<dropdownControl_1.DropdownItem key={repoName} onSelect={this.handleRepoFilterChange} eventKey={repoName} isActive={repoName === activeRepo}>
              <RepoLabel>{repoName}</RepoLabel>
            </dropdownControl_1.DropdownItem>))}
      </StyledDropdownControl>);
    }
}
exports.default = RepositorySwitcher;
const StyledDropdownControl = (0, styled_1.default)(dropdownControl_1.default) `
  margin-bottom: ${(0, space_1.default)(1)};
  > *:nth-child(2) {
    right: auto;
    width: auto;
    ${p => p.minMenuWidth && `min-width: calc(${p.minMenuWidth}px + 10px);`}
    border-radius: ${p => p.theme.borderRadius};
    border-top-left-radius: 0px;
    border: 1px solid ${p => p.theme.button.default.border};
    top: calc(100% - 1px);
  }
`;
const FilterText = (0, styled_1.default)('em') `
  font-style: normal;
  color: ${p => p.theme.gray300};
  margin-right: ${(0, space_1.default)(0.5)};
`;
const RepoLabel = (0, styled_1.default)('div') `
  ${overflowEllipsis_1.default}
`;
//# sourceMappingURL=repositorySwitcher.jsx.map