Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const timeSince_1 = (0, tslib_1.__importDefault)(require("app/components/timeSince"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const TimesTag = ({ lastSeen, firstSeen }) => {
    return (<Wrapper>
      <StyledIconClock size="xs" color="gray300"/>
      {lastSeen &&
            (0, getDynamicText_1.default)({
                value: (<timeSince_1.default tooltipTitle={(0, locale_1.t)('Last Seen')} date={lastSeen} suffix={(0, locale_1.t)('ago')} shorten/>),
                fixed: '10s ago',
            })}
      {firstSeen && lastSeen && (<Separator className="hidden-xs hidden-sm">&nbsp;|&nbsp;</Separator>)}
      {firstSeen &&
            (0, getDynamicText_1.default)({
                value: (<timeSince_1.default tooltipTitle={(0, locale_1.t)('First Seen')} date={firstSeen} suffix={(0, locale_1.t)('old')} className="hidden-xs hidden-sm" shorten/>),
                fixed: '10s old',
            })}
    </Wrapper>);
};
const Wrapper = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  font-size: ${p => p.theme.fontSizeSmall};
`;
const Separator = (0, styled_1.default)('span') `
  color: ${p => p.theme.subText};
`;
const StyledIconClock = (0, styled_1.default)(icons_1.IconClock) `
  margin-right: 2px;
`;
exports.default = TimesTag;
//# sourceMappingURL=timesTag.jsx.map