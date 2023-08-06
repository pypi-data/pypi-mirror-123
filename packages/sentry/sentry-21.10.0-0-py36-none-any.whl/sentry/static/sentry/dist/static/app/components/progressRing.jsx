Object.defineProperty(exports, "__esModule", { value: true });
exports.RingText = exports.RingBar = exports.RingBackground = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const framer_motion_1 = require("framer-motion");
const testableTransition_1 = (0, tslib_1.__importDefault)(require("app/utils/testableTransition"));
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const Text = (0, styled_1.default)('div') `
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  width: 100%;
  color: ${p => p.theme.chartLabel};
  font-size: ${p => p.theme.fontSizeExtraSmall};
  padding-top: 1px;
  transition: color 100ms;
  ${p => p.textCss && p.textCss(p)}
`;
exports.RingText = Text;
const AnimatedText = (0, framer_motion_1.motion)(Text);
AnimatedText.defaultProps = {
    initial: { opacity: 0, y: -10 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0, y: 10 },
    transition: (0, testableTransition_1.default)(),
};
const ProgressRing = (_a) => {
    var { value, minValue = 0, maxValue = 100, size = 20, barWidth = 3, text, textCss, animateText = false, progressColor = theme_1.default.green300, backgroundColor = theme_1.default.gray200, progressEndcaps } = _a, p = (0, tslib_1.__rest)(_a, ["value", "minValue", "maxValue", "size", "barWidth", "text", "textCss", "animateText", "progressColor", "backgroundColor", "progressEndcaps"]);
    const radius = size / 2 - barWidth / 2;
    const circumference = 2 * Math.PI * radius;
    const boundedValue = Math.min(Math.max(value, minValue), maxValue);
    const progress = (boundedValue - minValue) / (maxValue - minValue);
    const percent = progress * 100;
    const progressOffset = (1 - progress) * circumference;
    const TextComponent = animateText ? AnimatedText : Text;
    let textNode = (<TextComponent key={text === null || text === void 0 ? void 0 : text.toString()} {...{ textCss, percent }}>
      {text}
    </TextComponent>);
    textNode = animateText ? (<framer_motion_1.AnimatePresence initial={false}>{textNode}</framer_motion_1.AnimatePresence>) : (textNode);
    return (<RingSvg height={radius * 2 + barWidth} width={radius * 2 + barWidth} {...p}>
      <RingBackground r={radius} barWidth={barWidth} cx={radius + barWidth / 2} cy={radius + barWidth / 2} color={backgroundColor}/>
      <RingBar strokeDashoffset={progressOffset} strokeLinecap={progressEndcaps} circumference={circumference} r={radius} barWidth={barWidth} cx={radius + barWidth / 2} cy={radius + barWidth / 2} color={progressColor}/>
      <foreignObject height="100%" width="100%">
        {text !== undefined && textNode}
      </foreignObject>
    </RingSvg>);
};
const RingSvg = (0, styled_1.default)('svg') `
  position: relative;
`;
const RingBackground = (0, styled_1.default)('circle') `
  fill: none;
  stroke: ${p => p.color};
  stroke-width: ${p => p.barWidth}px;
  transition: stroke 100ms;
`;
exports.RingBackground = RingBackground;
const RingBar = (0, styled_1.default)('circle') `
  fill: none;
  stroke: ${p => p.color};
  stroke-width: ${p => p.barWidth}px;
  stroke-dasharray: ${p => p.circumference} ${p => p.circumference};
  transform: rotate(-90deg);
  transform-origin: 50% 50%;
  transition: stroke-dashoffset 200ms, stroke 100ms;
`;
exports.RingBar = RingBar;
exports.default = ProgressRing;
//# sourceMappingURL=progressRing.jsx.map