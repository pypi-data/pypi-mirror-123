Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const checkboxFancy_1 = (0, tslib_1.__importDefault)(require("app/components/checkboxFancy/checkboxFancy"));
const dropdownAutoComplete_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownAutoComplete"));
const highlight_1 = (0, tslib_1.__importDefault)(require("app/components/highlight"));
const textOverflow_1 = (0, tslib_1.__importDefault)(require("app/components/textOverflow"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const input_1 = require("app/styles/input");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
function GroupByField({ metricTags, groupBy = [], onChange }) {
    const hasSelected = !!groupBy.length;
    function handleClick(tag) {
        if (groupBy.includes(tag)) {
            const filteredGroupBy = groupBy.filter(groupByOption => groupByOption !== tag);
            onChange(filteredGroupBy);
            return;
        }
        onChange([...new Set([...groupBy, tag])]);
    }
    function handleUnselectAll(event) {
        event.stopPropagation();
        onChange([]);
    }
    return (<dropdownAutoComplete_1.default searchPlaceholder={(0, locale_1.t)('Search tag')} items={metricTags.map(metricTag => ({
            value: metricTag,
            searchKey: metricTag,
            label: ({ inputValue }) => (<Item onClick={() => handleClick(metricTag)}>
            <div>
              <highlight_1.default text={inputValue}>{metricTag}</highlight_1.default>
            </div>
            <checkboxFancy_1.default isChecked={groupBy.includes(metricTag)}/>
          </Item>),
        }))} style={{
            width: '100%',
            borderRadius: 0,
        }} maxHeight={110}>
      {({ isOpen, getActorProps }) => (<Field {...getActorProps()} hasSelected={hasSelected} isOpen={isOpen}>
          {!hasSelected ? (<Placeholder>{(0, locale_1.t)('Group by')}</Placeholder>) : (<React.Fragment>
              <StyledTextOverflow>
                {groupBy.map(groupByOption => groupByOption).join(',')}
              </StyledTextOverflow>
              <StyledClose color={hasSelected ? 'textColor' : 'gray300'} onClick={handleUnselectAll}/>
            </React.Fragment>)}
          <ChevronWrapper>
            <icons_1.IconChevron direction={isOpen ? 'up' : 'down'} size="sm" color={isOpen ? 'textColor' : 'gray300'}/>
          </ChevronWrapper>
        </Field>)}
    </dropdownAutoComplete_1.default>);
}
exports.default = GroupByField;
const Field = (0, styled_1.default)('div') `
  ${p => (0, input_1.inputStyles)(p)};
  padding: 0 10px;
  min-width: 250px;
  display: grid;
  grid-template-columns: ${p => p.hasSelected ? '1fr max-content max-content' : '1fr  max-content'};
  resize: none;
  overflow: hidden;
  align-items: center;
  ${p => p.isOpen &&
    `
      border-bottom-left-radius: 0;
      border-bottom-right-radius: 0;
    `}
`;
const Item = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: 1fr max-content;
  grid-gap: ${(0, space_1.default)(1.5)};
  word-break: break-all;
`;
const ChevronWrapper = (0, styled_1.default)('div') `
  width: 14px;
  height: 14px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-left: ${(0, space_1.default)(1)};
`;
const StyledClose = (0, styled_1.default)(icons_1.IconClose) `
  height: 100%;
  width: 10px;
  padding: ${(0, space_1.default)(1)} 0;
  stroke-width: 1.5;
  margin-left: ${(0, space_1.default)(1)};
  box-sizing: content-box;
`;
const Placeholder = (0, styled_1.default)('div') `
  flex: 1;
  color: ${p => p.theme.gray200};
  padding: 0 ${(0, space_1.default)(0.25)};
`;
const StyledTextOverflow = (0, styled_1.default)(textOverflow_1.default) `
  flex: 1;
`;
//# sourceMappingURL=groupByField.jsx.map