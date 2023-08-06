Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const errorBoundary_1 = (0, tslib_1.__importDefault)(require("app/components/errorBoundary"));
const getBadge_1 = (0, tslib_1.__importDefault)(require("./getBadge"));
/**
 * Public interface for all "id badges":
 * Organization, project, team, user
 */
const IdBadge = (props) => {
    const componentBadge = (0, getBadge_1.default)(props);
    if (!componentBadge) {
        throw new Error('IdBadge: required property missing (organization, project, team, member, user) or misconfigured');
    }
    return <InlineErrorBoundary mini>{componentBadge}</InlineErrorBoundary>;
};
exports.default = IdBadge;
const InlineErrorBoundary = (0, styled_1.default)(errorBoundary_1.default) `
  background-color: transparent;
  border-color: transparent;
  display: flex;
  align-items: center;
  margin-bottom: 0;
  box-shadow: none;
  padding: 0; /* Because badges don't have any padding, so this should make the boundary fit well */
`;
//# sourceMappingURL=index.jsx.map