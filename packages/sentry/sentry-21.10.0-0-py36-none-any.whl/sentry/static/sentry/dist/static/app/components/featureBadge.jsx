Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const circleIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/circleIndicator"));
const tagDeprecated_1 = (0, tslib_1.__importDefault)(require("app/components/tagDeprecated"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const defaultTitles = {
    alpha: (0, locale_1.t)('This feature is internal and available for QA purposes'),
    beta: (0, locale_1.t)('This feature is available for early adopters and may change'),
    new: (0, locale_1.t)('This feature is new! Try it out and let us know what you think'),
};
const labels = {
    alpha: (0, locale_1.t)('alpha'),
    beta: (0, locale_1.t)('beta'),
    new: (0, locale_1.t)('new'),
};
function BaseFeatureBadge(_a) {
    var { type, variant = 'badge', title, noTooltip } = _a, p = (0, tslib_1.__rest)(_a, ["type", "variant", "title", "noTooltip"]);
    const theme = (0, react_1.useTheme)();
    return (<div {...p}>
      <tooltip_1.default title={title !== null && title !== void 0 ? title : defaultTitles[type]} disabled={noTooltip} position="right">
        <React.Fragment>
          {variant === 'badge' && <StyledTag priority={type}>{labels[type]}</StyledTag>}
          {variant === 'indicator' && (<circleIndicator_1.default color={theme.badge[type].indicatorColor} size={8}/>)}
        </React.Fragment>
      </tooltip_1.default>
    </div>);
}
const StyledTag = (0, styled_1.default)(tagDeprecated_1.default) `
  padding: 3px ${(0, space_1.default)(0.75)};
`;
const FeatureBadge = (0, styled_1.default)(BaseFeatureBadge) `
  display: inline-flex;
  align-items: center;
  margin-left: ${(0, space_1.default)(0.75)};
  position: relative;
  top: -1px;
`;
exports.default = FeatureBadge;
//# sourceMappingURL=featureBadge.jsx.map