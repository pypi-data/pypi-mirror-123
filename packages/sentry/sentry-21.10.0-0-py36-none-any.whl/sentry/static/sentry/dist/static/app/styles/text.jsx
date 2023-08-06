Object.defineProperty(exports, "__esModule", { value: true });
const react_1 = require("@emotion/react");
const textStyles = () => (0, react_1.css) `
  /* stylelint-disable no-descending-specificity */
  h1,
  h2,
  h3,
  h4,
  h5,
  h6,
  p,
  ul,
  ol,
  table,
  dl,
  blockquote,
  form,
  pre,
  .auto-select-text,
  .section,
  [class^='highlight-'] {
    margin-bottom: 20px;

    &:last-child {
      margin-bottom: 0;
    }
  }
  /* stylelint-enable */
`;
exports.default = textStyles;
//# sourceMappingURL=text.jsx.map