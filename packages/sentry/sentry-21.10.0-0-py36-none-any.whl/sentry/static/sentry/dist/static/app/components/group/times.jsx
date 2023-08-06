Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const timeSince_1 = (0, tslib_1.__importDefault)(require("app/components/timeSince"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const Times = ({ lastSeen, firstSeen }) => (<Container>
    <FlexWrapper>
      {lastSeen && (<react_1.Fragment>
          <StyledIconClock size="11px"/>
          <timeSince_1.default date={lastSeen} suffix={(0, locale_1.t)('ago')}/>
        </react_1.Fragment>)}
      {firstSeen && lastSeen && (<span className="hidden-xs hidden-sm">&nbsp;—&nbsp;</span>)}
      {firstSeen && (<timeSince_1.default date={firstSeen} suffix={(0, locale_1.t)('old')} className="hidden-xs hidden-sm"/>)}
    </FlexWrapper>
  </Container>);
const Container = (0, styled_1.default)('div') `
  flex-shrink: 1;
  min-width: 0; /* flex-hack for overflow-ellipsised children */
`;
const FlexWrapper = (0, styled_1.default)('div') `
  ${overflowEllipsis_1.default}

  /* The following aligns the icon with the text, fixes bug in Firefox */
  display: flex;
  align-items: center;
`;
const StyledIconClock = (0, styled_1.default)(icons_1.IconClock) `
  /* this is solely for optics, since TimeSince always begins
  with a number, and numbers do not have descenders */
  margin-right: ${(0, space_1.default)(0.5)};
`;
exports.default = Times;
//# sourceMappingURL=times.jsx.map