Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const Badge = (0, styled_1.default)((_a) => {
    var { children, text } = _a, props = (0, tslib_1.__rest)(_a, ["children", "text"]);
    return (<span {...props}>{children !== null && children !== void 0 ? children : text}</span>);
}) `
  display: inline-block;
  height: 20px;
  min-width: 20px;
  line-height: 20px;
  border-radius: 20px;
  padding: 0 5px;
  margin-left: ${(0, space_1.default)(0.5)};
  font-size: 75%;
  font-weight: 600;
  text-align: center;
  color: ${p => { var _a; return p.theme.badge[(_a = p.type) !== null && _a !== void 0 ? _a : 'default'].color; }};
  background: ${p => { var _a; return p.theme.badge[(_a = p.type) !== null && _a !== void 0 ? _a : 'default'].background; }};
  transition: background 100ms linear;

  position: relative;
  top: -1px;
`;
exports.default = Badge;
//# sourceMappingURL=badge.jsx.map