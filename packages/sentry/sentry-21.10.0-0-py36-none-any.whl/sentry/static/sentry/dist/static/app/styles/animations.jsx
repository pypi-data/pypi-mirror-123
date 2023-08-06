Object.defineProperty(exports, "__esModule", { value: true });
exports.alertHighlight = exports.highlight = exports.slideInUp = exports.slideInLeft = exports.slideInRight = exports.expandOut = exports.pulse = exports.fadeOut = exports.fadeIn = exports.growDown = exports.growIn = void 0;
const react_1 = require("@emotion/react");
exports.growIn = (0, react_1.keyframes) `
  0% {
    opacity: 0;
    transform: scale(0.75);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
`;
const growDown = (height) => (0, react_1.keyframes) `
  0% {
    height: 0;
  }
  100% {
    height: ${height};
  }
`;
exports.growDown = growDown;
exports.fadeIn = (0, react_1.keyframes) `
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
`;
exports.fadeOut = (0, react_1.keyframes) `
  0% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
`;
const pulse = (size) => (0, react_1.keyframes) `
  0% {
    transform: scale(1,1);
  }
  50% {
    transform: scale(${size}, ${size});
  }
  100% {
    transform: scale(1, 1);
  }
`;
exports.pulse = pulse;
exports.expandOut = (0, react_1.keyframes) `
  0% {
    transform: scale(1, 1);
    opacity: 1;
  }

  100% {
    transform: scale(5, 5);
    opacity: 0;
  }
`;
exports.slideInRight = (0, react_1.keyframes) `
  0% {
    transform: translateX(20px);
    opacity: 0;
  }

  100% {
    transform: translateX(0);
    opacity: 1;
  }
`;
exports.slideInLeft = (0, react_1.keyframes) `
  0% {
    transform: translateX(-20px);
    opacity: 0;
  }

  100% {
    transform: translateX(0);
    opacity: 1;
  }
`;
exports.slideInUp = (0, react_1.keyframes) `
  0% {
    transform: translateY(10px);
    opacity: 0;
  }

  100% {
    transform: translateY(0);
    opacity: 1;
  }
`;
const highlight = (color) => (0, react_1.keyframes) `
  0%,
  100% {
    background: rgba(255, 255, 255, 0);
  }

  25% {
    background: ${color};
  }
`;
exports.highlight = highlight;
// TODO(ts): priority should be pulled from `keyof typeof theme.alert`
const alertHighlight = (priority, theme) => (0, react_1.keyframes) `
  0%,
  100% {
    background: rgba(255, 255, 255, 0);
    border-color: transparent;
  }

  25% {
    background: ${theme.alert[priority].backgroundLight};
    border-color: ${theme.alert[priority].border};
  }
`;
exports.alertHighlight = alertHighlight;
//# sourceMappingURL=animations.jsx.map