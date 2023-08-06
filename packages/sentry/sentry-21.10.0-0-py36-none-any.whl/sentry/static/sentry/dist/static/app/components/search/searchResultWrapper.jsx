Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const SearchResultWrapper = (0, styled_1.default)((_a) => {
    var { highlighted } = _a, props = (0, tslib_1.__rest)(_a, ["highlighted"]);
    return (<div {...props} ref={element => { var _a; return highlighted && ((_a = element === null || element === void 0 ? void 0 : element.scrollIntoView) === null || _a === void 0 ? void 0 : _a.call(element, { block: 'nearest' })); }}/>);
}) `
  cursor: pointer;
  display: block;
  color: ${p => p.theme.textColor};
  padding: 10px;
  scroll-margin: 120px;

  ${p => p.highlighted &&
    (0, react_1.css) `
      color: ${p.theme.purple300};
      background: ${p.theme.backgroundSecondary};
    `};

  &:not(:first-child) {
    border-top: 1px solid ${p => p.theme.innerBorder};
  }
`;
exports.default = SearchResultWrapper;
//# sourceMappingURL=searchResultWrapper.jsx.map