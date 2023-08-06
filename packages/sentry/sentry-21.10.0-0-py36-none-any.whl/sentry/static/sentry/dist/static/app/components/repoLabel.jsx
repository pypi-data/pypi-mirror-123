Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const RepoLabel = (0, styled_1.default)('span') `
  /* label mixin from bootstrap */
  font-weight: 700;
  color: ${p => p.theme.white};
  text-align: center;
  white-space: nowrap;
  border-radius: 0.25em;
  /* end of label mixin from bootstrap */

  ${overflowEllipsis_1.default};

  display: inline-block;
  vertical-align: text-bottom;
  line-height: 1;
  background: ${p => p.theme.gray200};
  padding: 3px;
  max-width: 86px;
  font-size: ${p => p.theme.fontSizeSmall};
`;
exports.default = RepoLabel;
//# sourceMappingURL=repoLabel.jsx.map