Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const circleIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/circleIndicator"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const constants_1 = require("./constants");
const StatusWrapper = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
`;
const IntegrationStatus = (0, styled_1.default)((_a) => {
    var { status } = _a, p = (0, tslib_1.__rest)(_a, ["status"]);
    const theme = (0, react_1.useTheme)();
    return (<StatusWrapper>
      <circleIndicator_1.default size={6} color={theme[constants_1.COLORS[status]]}/>
      <div {...p}>{`${(0, locale_1.t)(status)}`}</div>
    </StatusWrapper>);
}) `
  color: ${p => p.theme[constants_1.COLORS[p.status]]};
  margin-left: ${(0, space_1.default)(0.5)};
  font-weight: light;
  margin-right: ${(0, space_1.default)(0.75)};
`;
exports.default = IntegrationStatus;
//# sourceMappingURL=integrationStatus.jsx.map