Object.defineProperty(exports, "__esModule", { value: true });
exports.filterToLocationQuery = exports.decodeFilterFromLocation = exports.stringToFilter = exports.filterToColor = exports.filterToSearchConditions = exports.filterToField = exports.spanOperationBreakdownSingleColumns = exports.SpanOperationBreakdownFilter = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const guideAnchor_1 = require("app/components/assistant/guideAnchor");
const dropdownButton_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownButton"));
const dropdownControl_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownControl"));
const utils_1 = require("app/components/performance/waterfall/utils");
const radio_1 = (0, tslib_1.__importDefault)(require("app/components/radio"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const queryString_1 = require("app/utils/queryString");
const latencyChart_1 = require("./transactionOverview/latencyChart");
// Make sure to update other instances like trends column fields, discover field types.
var SpanOperationBreakdownFilter;
(function (SpanOperationBreakdownFilter) {
    SpanOperationBreakdownFilter["None"] = "none";
    SpanOperationBreakdownFilter["Http"] = "http";
    SpanOperationBreakdownFilter["Db"] = "db";
    SpanOperationBreakdownFilter["Browser"] = "browser";
    SpanOperationBreakdownFilter["Resource"] = "resource";
})(SpanOperationBreakdownFilter = exports.SpanOperationBreakdownFilter || (exports.SpanOperationBreakdownFilter = {}));
const OPTIONS = [
    SpanOperationBreakdownFilter.Http,
    SpanOperationBreakdownFilter.Db,
    SpanOperationBreakdownFilter.Browser,
    SpanOperationBreakdownFilter.Resource,
];
exports.spanOperationBreakdownSingleColumns = OPTIONS.map(o => `spans.${o}`);
function Filter(props) {
    const { currentFilter, onChangeFilter, organization } = props;
    if (!organization.features.includes('performance-ops-breakdown')) {
        return null;
    }
    const dropDownButtonProps = {
        children: (<React.Fragment>
        <icons_1.IconFilter size="xs"/>
        <FilterLabel>
          {currentFilter === SpanOperationBreakdownFilter.None
                ? (0, locale_1.t)('Filter')
                : (0, locale_1.tct)('Filter - [operationName]', {
                    operationName: currentFilter,
                })}
        </FilterLabel>
      </React.Fragment>),
        priority: 'default',
        hasDarkBorderBottomColor: false,
    };
    return (<guideAnchor_1.GuideAnchor target="span_op_breakdowns_filter" position="top">
      <Wrapper>
        <dropdownControl_1.default menuWidth="240px" blendWithActor button={({ isOpen, getActorProps }) => (<StyledDropdownButton {...getActorProps()} showChevron={false} isOpen={isOpen} hasDarkBorderBottomColor={dropDownButtonProps.hasDarkBorderBottomColor} priority={dropDownButtonProps.priority} data-test-id="filter-button">
              {dropDownButtonProps.children}
            </StyledDropdownButton>)}>
          <MenuContent onClick={event => {
            // propagated clicks will dismiss the menu; we stop this here
            event.stopPropagation();
        }}>
            <Header onClick={event => {
            event.stopPropagation();
            onChangeFilter(SpanOperationBreakdownFilter.None);
        }}>
              <HeaderTitle>{(0, locale_1.t)('Operation')}</HeaderTitle>
              <radio_1.default radioSize="small" checked={SpanOperationBreakdownFilter.None === currentFilter}/>
            </Header>
            <List>
              {Array.from([...OPTIONS], (filterOption, index) => {
            const operationName = filterOption;
            return (<ListItem key={String(index)} isChecked={false} onClick={event => {
                    event.stopPropagation();
                    onChangeFilter(filterOption);
                }}>
                    <OperationDot backgroundColor={(0, utils_1.pickBarColor)(operationName)}/>
                    <OperationName>{operationName}</OperationName>
                    <radio_1.default radioSize="small" checked={filterOption === currentFilter}/>
                  </ListItem>);
        })}
            </List>
          </MenuContent>
        </dropdownControl_1.default>
      </Wrapper>
    </guideAnchor_1.GuideAnchor>);
}
const FilterLabel = (0, styled_1.default)('span') `
  margin-left: ${(0, space_1.default)(1)};
`;
const Wrapper = (0, styled_1.default)('div') `
  position: relative;
  display: flex;

  margin-right: ${(0, space_1.default)(1)};
`;
const StyledDropdownButton = (0, styled_1.default)(dropdownButton_1.default) `
  white-space: nowrap;
  max-width: 200px;

  z-index: ${p => p.theme.zIndex.dropdown};

  &:hover,
  &:active {
    ${p => !p.isOpen &&
    p.hasDarkBorderBottomColor &&
    `
          border-bottom-color: ${p.theme.button.primary.border};
        `}
  }

  ${p => !p.isOpen &&
    p.hasDarkBorderBottomColor &&
    `
      border-bottom-color: ${p.theme.button.primary.border};
    `}
`;
const MenuContent = (0, styled_1.default)('div') `
  max-height: 250px;
  overflow-y: auto;
  border-top: 1px solid ${p => p.theme.gray200};
`;
const Header = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: auto min-content;
  grid-column-gap: ${(0, space_1.default)(1)};
  align-items: center;

  margin: 0;
  background-color: ${p => p.theme.backgroundSecondary};
  color: ${p => p.theme.gray300};
  font-weight: normal;
  font-size: ${p => p.theme.fontSizeMedium};
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};
  border-bottom: 1px solid ${p => p.theme.border};
`;
const HeaderTitle = (0, styled_1.default)('span') `
  font-size: ${p => p.theme.fontSizeMedium};
`;
const List = (0, styled_1.default)('ul') `
  list-style: none;
  margin: 0;
  padding: 0;
`;
const ListItem = (0, styled_1.default)('li') `
  display: grid;
  grid-template-columns: max-content 1fr max-content;
  grid-column-gap: ${(0, space_1.default)(1)};
  align-items: center;
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};
  border-bottom: 1px solid ${p => p.theme.border};
  :hover {
    background-color: ${p => p.theme.backgroundSecondary};
  }

  &:hover span {
    color: ${p => p.theme.blue300};
    text-decoration: underline;
  }
`;
const OperationDot = (0, styled_1.default)('div') `
  content: '';
  display: block;
  width: 8px;
  min-width: 8px;
  height: 8px;
  margin-right: ${(0, space_1.default)(1)};
  border-radius: 100%;

  background-color: ${p => p.backgroundColor};
`;
const OperationName = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeMedium};
  ${overflowEllipsis_1.default};
`;
function filterToField(option) {
    switch (option) {
        case SpanOperationBreakdownFilter.None:
            return undefined;
        default: {
            return `spans.${option}`;
        }
    }
}
exports.filterToField = filterToField;
function filterToSearchConditions(option, location) {
    let field = filterToField(option);
    if (!field) {
        field = 'transaction.duration';
    }
    // Add duration search conditions implicitly
    const { min, max } = (0, latencyChart_1.decodeHistogramZoom)(location);
    let query = '';
    if (typeof min === 'number') {
        query = `${query} ${field}:>${min}ms`;
    }
    if (typeof max === 'number') {
        query = `${query} ${field}:<${max}ms`;
    }
    switch (option) {
        case SpanOperationBreakdownFilter.None:
            return query ? query.trim() : undefined;
        default: {
            return `${query} has:${filterToField(option)}`.trim();
        }
    }
}
exports.filterToSearchConditions = filterToSearchConditions;
function filterToColor(option) {
    switch (option) {
        case SpanOperationBreakdownFilter.None:
            return (0, utils_1.pickBarColor)('');
        default: {
            return (0, utils_1.pickBarColor)(option);
        }
    }
}
exports.filterToColor = filterToColor;
function stringToFilter(option) {
    if (Object.values(SpanOperationBreakdownFilter).includes(option)) {
        return option;
    }
    return SpanOperationBreakdownFilter.None;
}
exports.stringToFilter = stringToFilter;
function decodeFilterFromLocation(location) {
    return stringToFilter((0, queryString_1.decodeScalar)(location.query.breakdown, SpanOperationBreakdownFilter.None));
}
exports.decodeFilterFromLocation = decodeFilterFromLocation;
function filterToLocationQuery(option) {
    return {
        breakdown: option,
    };
}
exports.filterToLocationQuery = filterToLocationQuery;
exports.default = Filter;
//# sourceMappingURL=filter.jsx.map