Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const notAvailable_1 = (0, tslib_1.__importDefault)(require("app/components/notAvailable"));
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const radio_1 = (0, tslib_1.__importDefault)(require("app/components/radio"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const utils_2 = require("../../utils");
function ReleaseComparisonChartRow({ type, role, drilldown, thisRelease, allReleases, diff, showPlaceholders, activeChart, chartDiff, onChartChange, onExpanderToggle, expanded, withExpanders, }) {
    return (<ChartTableRow htmlFor={type} isActive={type === activeChart} isLoading={showPlaceholders} role={role} expanded={expanded}>
      <DescriptionCell>
        <TitleWrapper>
          <radio_1.default id={type} disabled={false} checked={type === activeChart} onChange={() => onChartChange(type)}/>
          {utils_2.releaseComparisonChartLabels[type]}&nbsp;{drilldown}
        </TitleWrapper>
      </DescriptionCell>
      <NumericCell>
        {showPlaceholders ? (<placeholder_1.default height="20px"/>) : (0, utils_1.defined)(allReleases) ? (allReleases) : (<notAvailable_1.default />)}
      </NumericCell>
      <NumericCell>
        {showPlaceholders ? (<placeholder_1.default height="20px"/>) : (0, utils_1.defined)(thisRelease) ? (thisRelease) : (<notAvailable_1.default />)}
      </NumericCell>
      <NumericCell>
        {showPlaceholders ? (<placeholder_1.default height="20px"/>) : (0, utils_1.defined)(diff) ? (chartDiff) : (<notAvailable_1.default />)}
      </NumericCell>
      {withExpanders && (<ExpanderCell>
          {role === 'parent' && (<ToggleButton onClick={() => onExpanderToggle(type)} borderless size="zero" icon={<icons_1.IconChevron direction={expanded ? 'up' : 'down'}/>} label={(0, locale_1.t)('Toggle chart group')}/>)}
        </ExpanderCell>)}
    </ChartTableRow>);
}
const Cell = (0, styled_1.default)('div') `
  text-align: right;
  color: ${p => p.theme.subText};
  ${overflowEllipsis_1.default}
`;
const NumericCell = (0, styled_1.default)(Cell) `
  font-variant-numeric: tabular-nums;
`;
const DescriptionCell = (0, styled_1.default)(Cell) `
  text-align: left;
  overflow: visible;
  color: ${p => p.theme.textColor};
`;
const ExpanderCell = (0, styled_1.default)(Cell) `
  display: flex;
  align-items: center;
  justify-content: flex-end;
`;
const TitleWrapper = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  position: relative;
  z-index: 1;
  background: ${p => p.theme.background};

  input {
    width: ${(0, space_1.default)(2)};
    height: ${(0, space_1.default)(2)};
    flex-shrink: 0;
    background-color: ${p => p.theme.background};
    margin-right: ${(0, space_1.default)(1)} !important;

    &:checked:after {
      width: ${(0, space_1.default)(1)};
      height: ${(0, space_1.default)(1)};
    }

    &:hover {
      cursor: pointer;
    }
  }
`;
const ChartTableRow = (0, styled_1.default)('label') `
  display: contents;
  font-weight: 400;
  margin-bottom: 0;

  > * {
    padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};
  }

  ${p => p.isActive &&
    !p.isLoading &&
    (0, react_1.css) `
      ${Cell}, ${NumericCell}, ${DescriptionCell}, ${TitleWrapper}, ${ExpanderCell} {
        background-color: ${p.theme.bodyBackground};
      }
    `}

  &:hover {
    cursor: pointer;
    ${ /* sc-selector */Cell}, ${ /* sc-selector */NumericCell}, ${
/* sc-selector */ DescriptionCell},${ /* sc-selector */ExpanderCell}, ${ /* sc-selector */TitleWrapper} {
      ${p => !p.isLoading && `background-color: ${p.theme.bodyBackground}`}
    }
  }

  ${p => (p.role === 'default' || (p.role === 'parent' && !p.expanded)) &&
    (0, react_1.css) `
      &:not(:last-child) {
        ${Cell}, ${NumericCell}, ${DescriptionCell}, ${ExpanderCell} {
          border-bottom: 1px solid ${p.theme.border};
        }
      }
    `}

  ${p => p.role === 'children' &&
    (0, react_1.css) `
      ${DescriptionCell} {
        padding-left: 44px;
        position: relative;
        &:before {
          content: '';
          width: 15px;
          height: 36px;
          position: absolute;
          top: -17px;
          left: 24px;
          border-bottom: 1px solid ${p.theme.border};
          border-left: 1px solid ${p.theme.border};
        }
      }
    `}

    ${p => p.role === 'children' &&
    (0, react_1.css) `
      ${Cell}, ${NumericCell}, ${DescriptionCell}, ${ExpanderCell} {
        padding-bottom: ${(0, space_1.default)(0.75)};
        padding-top: ${(0, space_1.default)(0.75)};
        border-bottom: 0;
      }
    `}
`;
const ToggleButton = (0, styled_1.default)(button_1.default) `
  &,
  &:hover,
  &:focus,
  &:active {
    background: transparent;
  }
`;
exports.default = ReleaseComparisonChartRow;
//# sourceMappingURL=releaseComparisonChartRow.jsx.map