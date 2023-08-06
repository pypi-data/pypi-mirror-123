Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const classnames_1 = (0, tslib_1.__importDefault)(require("classnames"));
const utils_1 = require("app/utils");
const Context = (0, styled_1.default)('div') `
  display: inline;
`;
const ContextLine = function (props) {
    const { line, isActive, className } = props;
    let lineWs = '';
    let lineCode = '';
    if ((0, utils_1.defined)(line[1]) && line[1].match) {
        [, lineWs, lineCode] = line[1].match(/^(\s*)(.*?)$/m);
    }
    const Component = !props.children ? React.Fragment : Context;
    return (<li className={(0, classnames_1.default)(className, 'expandable', { active: isActive })} key={line[0]}>
      <Component>
        <span className="ws">{lineWs}</span>
        <span className="contextline">{lineCode}</span>
      </Component>
      {props.children}
    </li>);
};
exports.default = ContextLine;
//# sourceMappingURL=contextLine.jsx.map