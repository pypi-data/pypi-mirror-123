Object.defineProperty(exports, "__esModule", { value: true });
exports.imageStyle = void 0;
const react_1 = require("@emotion/react");
const imageStyle = (props) => (0, react_1.css) `
  position: absolute;
  top: 0px;
  left: 0px;
  border-radius: ${props.round ? '50%' : '3px'};
  ${props.grayscale &&
    (0, react_1.css) `
    padding: 1px;
    filter: grayscale(100%);
  `}
  ${props.suggested &&
    (0, react_1.css) `
    opacity: 50%;
  `}
`;
exports.imageStyle = imageStyle;
//# sourceMappingURL=styles.jsx.map