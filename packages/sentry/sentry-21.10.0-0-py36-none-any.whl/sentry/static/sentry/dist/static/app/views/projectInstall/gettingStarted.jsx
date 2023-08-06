Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const organization_1 = require("app/styles/organization");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
function GettingStarted({ className, children }) {
    return <organization_1.PageContent className={className}>{children}</organization_1.PageContent>;
}
exports.default = (0, styled_1.default)(GettingStarted) `
  background: ${p => p.theme.background};
  padding-top: ${(0, space_1.default)(3)};
`;
//# sourceMappingURL=gettingStarted.jsx.map