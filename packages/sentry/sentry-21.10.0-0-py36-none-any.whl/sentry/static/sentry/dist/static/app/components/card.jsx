Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const hoverStyle = (0, react_1.css) `
  &:focus,
  &:hover {
    box-shadow: 0px 0px 0px 6px rgba(209, 202, 216, 0.2);
    position: relative;
    outline: none;
  }

  &:active {
    box-shadow: 0px 0px 0px 6px rgba(209, 202, 216, 0.5);
  }

  /* This is to ensure the graph is visually clickable */
  * {
    cursor: pointer;
  }
`;
const Card = (0, styled_1.default)('div') `
  background: ${p => p.theme.background};
  border: 1px solid ${p => p.theme.border};
  border-radius: ${p => p.theme.borderRadius};
  display: flex;
  align-items: stretch;
  flex-direction: column;
  transition: box-shadow 0.2s ease;
  text-align: left;
  padding: 0;

  ${p => p.interactive && 'cursor: pointer'};
  ${p => p.interactive && hoverStyle};
`;
exports.default = Card;
//# sourceMappingURL=card.jsx.map