Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const BaseScoreBar = ({ score, className, vertical, size = 40, thickness = 4, radius = 3, palette = theme_1.default.similarity.colors, }) => {
    const maxScore = palette.length;
    // Make sure score is between 0 and maxScore
    const scoreInBounds = score >= maxScore ? maxScore : score <= 0 ? 0 : score;
    // Make sure paletteIndex is 0 based
    const paletteIndex = scoreInBounds - 1;
    // Size of bar, depends on orientation, although we could just apply a transformation via css
    const barProps = {
        vertical,
        thickness,
        size,
        radius,
    };
    return (<div className={className}>
      {[...Array(scoreInBounds)].map((_j, i) => (<Bar {...barProps} key={i} color={palette[paletteIndex]}/>))}
      {[...Array(maxScore - scoreInBounds)].map((_j, i) => (<Bar key={`empty-${i}`} {...barProps} empty/>))}
    </div>);
};
const ScoreBar = (0, styled_1.default)(BaseScoreBar) `
  display: flex;

  ${p => p.vertical
    ? `flex-direction: column-reverse;
    justify-content: flex-end;`
    : 'min-width: 80px;'};
`;
const Bar = (0, styled_1.default)('div') `
  border-radius: ${p => p.radius}px;
  margin: 2px;
  ${p => p.empty && `background-color: ${p.theme.similarity.empty};`};
  ${p => p.color && `background-color: ${p.color};`};

  width: ${p => (!p.vertical ? p.thickness : p.size)}px;
  height: ${p => (!p.vertical ? p.size : p.thickness)}px;
`;
exports.default = ScoreBar;
//# sourceMappingURL=scoreBar.jsx.map