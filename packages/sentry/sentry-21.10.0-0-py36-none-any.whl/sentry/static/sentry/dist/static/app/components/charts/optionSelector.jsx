Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const styles_1 = require("app/components/charts/styles");
const dropdownBubble_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownBubble"));
const dropdownButton_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownButton"));
const dropdownControl_1 = require("app/components/dropdownControl");
const dropdownMenu_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownMenu"));
const featureBadge_1 = (0, tslib_1.__importDefault)(require("app/components/featureBadge"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const truncate_1 = (0, tslib_1.__importDefault)(require("app/components/truncate"));
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const defaultProps = {
    menuWidth: 'auto',
};
class OptionSelector extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {};
        this.menuContainerRef = (0, react_1.createRef)();
    }
    componentDidMount() {
        this.setMenuContainerWidth();
    }
    shouldComponentUpdate(nextProps, nextState) {
        return !(0, isEqual_1.default)(nextProps, this.props) || !(0, isEqual_1.default)(nextState, this.state);
    }
    componentDidUpdate(prevProps) {
        if (prevProps.selected !== this.props.selected) {
            this.setMenuContainerWidth();
        }
    }
    setMenuContainerWidth() {
        var _a, _b;
        const menuContainerWidth = (_b = (_a = this.menuContainerRef) === null || _a === void 0 ? void 0 : _a.current) === null || _b === void 0 ? void 0 : _b.offsetWidth;
        if (menuContainerWidth) {
            this.setState({ menuContainerWidth });
        }
    }
    render() {
        const { menuContainerWidth } = this.state;
        const { options, onChange, selected, title, menuWidth, featureType } = this.props;
        const selectedOption = options.find(opt => selected === opt.value) || options[0];
        return (<styles_1.InlineContainer>
        <styles_1.SectionHeading>
          {title}
          {(0, utils_1.defined)(featureType) ? <StyledFeatureBadge type={featureType}/> : null}
        </styles_1.SectionHeading>
        <MenuContainer ref={this.menuContainerRef}>
          <dropdownMenu_1.default alwaysRenderMenu={false}>
            {({ isOpen, getMenuProps, getActorProps }) => (<react_1.Fragment>
                <StyledDropdownButton {...getActorProps()} size="zero" isOpen={isOpen}>
                  <TruncatedLabel>{String(selectedOption.label)}</TruncatedLabel>
                </StyledDropdownButton>
                <StyledDropdownBubble {...getMenuProps()} alignMenu="right" width={menuWidth} minWidth={menuContainerWidth} isOpen={isOpen} blendWithActor={false} blendCorner>
                  {options.map(opt => (<StyledDropdownItem key={opt.value} onSelect={onChange} eventKey={opt.value} disabled={opt.disabled} isActive={selected === opt.value} data-test-id={`option-${opt.value}`}>
                      <tooltip_1.default title={opt.tooltip} containerDisplayMode="inline">
                        <StyledTruncate isActive={selected === opt.value} value={String(opt.label)} maxLength={60} expandDirection="left"/>
                      </tooltip_1.default>
                    </StyledDropdownItem>))}
                </StyledDropdownBubble>
              </react_1.Fragment>)}
          </dropdownMenu_1.default>
        </MenuContainer>
      </styles_1.InlineContainer>);
    }
}
OptionSelector.defaultProps = defaultProps;
const TruncatedLabel = (0, styled_1.default)('span') `
  ${overflowEllipsis_1.default};
  max-width: 400px;
`;
const StyledTruncate = (0, styled_1.default)(truncate_1.default) `
  & span {
    ${p => p.isActive &&
    `
      color: ${p.theme.white};
      background: ${p.theme.active};
      border: none;
    `}
  }
`;
const MenuContainer = (0, styled_1.default)('div') `
  display: inline-block;
  position: relative;
`;
const StyledDropdownButton = (0, styled_1.default)(dropdownButton_1.default) `
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};
  font-weight: normal;
  z-index: ${p => (p.isOpen ? p.theme.zIndex.dropdownAutocomplete.actor : 'auto')};
`;
const StyledDropdownBubble = (0, styled_1.default)(dropdownBubble_1.default) `
  display: ${p => (p.isOpen ? 'block' : 'none')};
  overflow: visible;
  ${p => p.minWidth && p.width === 'auto' && `min-width: calc(${p.minWidth}px + ${(0, space_1.default)(3)})`};
`;
const StyledDropdownItem = (0, styled_1.default)(dropdownControl_1.DropdownItem) `
  line-height: ${p => p.theme.text.lineHeightBody};
  white-space: nowrap;
`;
const StyledFeatureBadge = (0, styled_1.default)(featureBadge_1.default) `
  margin-left: 0px;
`;
exports.default = OptionSelector;
//# sourceMappingURL=optionSelector.jsx.map