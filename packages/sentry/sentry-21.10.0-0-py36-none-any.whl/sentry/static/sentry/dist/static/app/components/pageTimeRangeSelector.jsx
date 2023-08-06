Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const timeRangeSelector_1 = (0, tslib_1.__importDefault)(require("app/components/organizations/timeRangeSelector"));
const panels_1 = require("app/components/panels");
const constants_1 = require("app/constants");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
function PageTimeRangeSelector(_a) {
    var { className } = _a, props = (0, tslib_1.__rest)(_a, ["className"]);
    const [isCalendarOpen, setIsCalendarOpen] = (0, react_1.useState)(false);
    return (<DropdownDate className={className} isCalendarOpen={isCalendarOpen}>
      <timeRangeSelector_1.default key={`period:${props.relative}-start:${props.start}-end:${props.end}-utc:${props.utc}-defaultPeriod:${props.defaultPeriod}`} label={<DropdownLabel>{(0, locale_1.t)('Date Range:')}</DropdownLabel>} onToggleSelector={isOpen => setIsCalendarOpen(isOpen)} relativeOptions={constants_1.DEFAULT_RELATIVE_PERIODS} {...props}/>
    </DropdownDate>);
}
const DropdownDate = (0, styled_1.default)(panels_1.Panel) `
  display: flex;
  justify-content: center;
  align-items: center;
  height: 42px;

  background: ${p => p.theme.background};
  border: 1px solid ${p => p.theme.border};
  border-radius: ${p => p.isCalendarOpen
    ? `${p.theme.borderRadius} ${p.theme.borderRadius} 0 0`
    : p.theme.borderRadius};
  padding: 0;
  margin: 0;
  font-size: ${p => p.theme.fontSizeMedium};
  color: ${p => p.theme.textColor};

  /* TimeRangeRoot in TimeRangeSelector */
  > div {
    width: 100%;
    align-self: stretch;
  }

  /* StyledItemHeader used to show selected value of TimeRangeSelector */
  > div > div:first-child {
    padding: 0 ${(0, space_1.default)(2)};
  }

  /* Menu that dropdowns from TimeRangeSelector */
  > div > div:last-child {
    /* Remove awkward 1px width difference on dropdown due to border */
    box-sizing: content-box;
    font-size: 1em;
  }
`;
const DropdownLabel = (0, styled_1.default)('span') `
  text-align: left;
  font-weight: 600;
  color: ${p => p.theme.textColor};

  > span:last-child {
    font-weight: 400;
  }
`;
exports.default = PageTimeRangeSelector;
//# sourceMappingURL=pageTimeRangeSelector.jsx.map