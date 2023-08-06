Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const panels_1 = require("app/components/panels");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const StyledPanel = (0, styled_1.default)(panels_1.Panel) `
  padding-top: ${(0, space_1.default)(2)};
  margin-bottom: 0;
`;
const Div = (0, styled_1.default)('div') ``;
const getPerformanceWidgetContainer = ({ containerType, }) => {
    if (containerType === 'panel') {
        return StyledPanel;
    }
    else if (containerType === 'inline') {
        return Div;
    }
    else {
        return Div;
    }
};
exports.default = getPerformanceWidgetContainer;
//# sourceMappingURL=performanceWidgetContainer.jsx.map