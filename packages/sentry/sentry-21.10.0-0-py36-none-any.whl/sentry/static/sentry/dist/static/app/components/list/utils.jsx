Object.defineProperty(exports, "__esModule", { value: true });
exports.getListSymbolStyle = exports.listSymbol = void 0;
const tslib_1 = require("tslib");
const react_1 = require("@emotion/react");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const bulletStyle = (theme) => (0, react_1.css) `
  padding-left: ${(0, space_1.default)(3)};
  list-style-type: circle;
  & > li::marker {
    color: ${theme.subText};
  }
`;
const numericStyle = (theme, { isSolid = false, initialCounterValue = 0 }) => (0, react_1.css) `
  & > li {
    padding-left: ${(0, space_1.default)(4)};
    :before {
      border-radius: 50%;
      position: absolute;
      counter-increment: numberedList;
      content: counter(numberedList);
      display: flex;
      align-items: center;
      justify-content: center;
      text-align: center;
      left: 0;
      ${isSolid
    ? (0, react_1.css) `
            width: 24px;
            height: 24px;
            font-weight: 500;
            font-size: ${theme.fontSizeSmall};
            background-color: ${theme.yellow300};
          `
    : (0, react_1.css) `
            top: 3px;
            width: 18px;
            height: 18px;
            font-weight: 600;
            font-size: 10px;
            border: 1px solid ${theme.gray500};
          `}
    }
  }
  counter-reset: numberedList ${initialCounterValue};
`;
exports.listSymbol = {
    numeric: 'numeric',
    'colored-numeric': 'colored-numeric',
    bullet: 'bullet',
};
function getListSymbolStyle(theme, symbol, initialCounterValue) {
    switch (symbol) {
        case 'numeric':
            return numericStyle(theme, { initialCounterValue });
        case 'colored-numeric':
            return numericStyle(theme, { isSolid: true, initialCounterValue });
        default:
            return bulletStyle(theme);
    }
}
exports.getListSymbolStyle = getListSymbolStyle;
//# sourceMappingURL=utils.jsx.map