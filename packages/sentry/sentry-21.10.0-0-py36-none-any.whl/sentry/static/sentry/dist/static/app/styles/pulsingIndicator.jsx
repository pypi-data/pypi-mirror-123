Object.defineProperty(exports, "__esModule", { value: true });
const react_1 = require("@emotion/react");
const pulse = (0, react_1.keyframes) `
  0% {
    transform: scale(0.1);
    opacity: 1
  }

  40%, 100% {
    transform: scale(0.8);
    opacity: 0;
  }
`;
const pulsingIndicatorStyles = (p) => (0, react_1.css) `
  height: 8px;
  width: 8px;
  border-radius: 50%;
  background: ${p.theme.orange400};
  position: relative;

  &:before {
    content: '';
    display: block;
    position: absolute;
    height: 100px;
    width: 100px;
    border-radius: 50%;
    top: -46px;
    left: -46px;
    border: 4px solid ${p.theme.orange300};
    transform-origin: center;
    animation: ${pulse} 3s ease-out infinite;
  }
`;
exports.default = pulsingIndicatorStyles;
//# sourceMappingURL=pulsingIndicator.jsx.map