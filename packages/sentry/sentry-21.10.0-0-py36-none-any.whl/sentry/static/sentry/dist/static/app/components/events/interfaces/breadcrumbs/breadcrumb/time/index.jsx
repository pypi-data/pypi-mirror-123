Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const highlight_1 = (0, tslib_1.__importDefault)(require("app/components/highlight"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const utils_1 = require("app/utils");
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const utils_2 = require("./utils");
const Time = (0, react_1.memo)(function Time({ timestamp, relativeTime, displayRelativeTime, searchTerm, }) {
    if (!((0, utils_1.defined)(timestamp) && (0, utils_1.defined)(relativeTime))) {
        return <div />;
    }
    const { date, time, displayTime } = (0, utils_2.getFormattedTimestamp)(timestamp, relativeTime, displayRelativeTime);
    return (<Wrapper>
      <tooltip_1.default title={<div>
            <div>{date}</div>
            {time !== '\u2014' && <div>{time}</div>}
          </div>} containerDisplayMode="inline-flex" disableForVisualTest>
        {(0, getDynamicText_1.default)({
            value: <highlight_1.default text={searchTerm}>{displayTime}</highlight_1.default>,
            fixed: '00:00:00',
        })}
      </tooltip_1.default>
    </Wrapper>);
});
exports.default = Time;
const Wrapper = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeSmall};
  color: ${p => p.theme.textColor};
`;
//# sourceMappingURL=index.jsx.map